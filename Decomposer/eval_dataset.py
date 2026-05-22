# eval_dataset.py
import json
import os
import random

def load_conf():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def load_jsonl(path):
    items = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    items.append(json.loads(line))
    return items

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def load_qs_from_main(main_path):
    all_qs = []
    
    jl_path = os.path.join(main_path, 'question', 'olympic_questions.jsonl')
    for item in load_jsonl(jl_path):
        q_text = item.get('question', '')
        if q_text:
            all_qs.append({
                'id': item.get('id', ''),
                'question': q_text,
                'category': item.get('category', ''),
                'answer': item.get('answer', []),
                'source': item.get('source', '')
            })
    
    al_path = os.path.join(main_path, 'data', 'aligned_olympic_data.2.json')
    aligned = load_json(al_path)
    if isinstance(aligned, list):
        for item in aligned:
            q_text = item.get('question', '')
            if q_text:
                all_qs.append({
                    'id': item.get('id', ''),
                    'question': q_text,
                    'category': item.get('category', ''),
                    'answer': item.get('answer', []),
                    'source': item.get('source', '')
                })
    
    return all_qs

def dedup_qs(qs):
    seen = set()
    uniq = []
    for q in qs:
        key = q['question'].lower().strip()
        if key not in seen:
            seen.add(key)
            uniq.append(q)
    return uniq

def needs_decomp(q_text):
    low = q_text.lower()
    
    strong_signals = [
        'non-consecutive', 'won more than one', 'in the same event',
        'both', 'respectively', 'compare',
        'went on to', 'then', 'after winning',
        'first', 'last', 'only',
        'but in which', 'and 2008', 'and 1976',
        '2000 and 2004', '2004 and 2008',
        'two', 'three', 'both the'
    ]
    
    return any(kw in low for kw in strong_signals)

def build_test_set(main_path, num=15):
    all_qs = load_qs_from_main(main_path)
    all_qs = dedup_qs(all_qs)
    
    complex_qs = [q for q in all_qs if needs_decomp(q['question'])]
    simple_qs = [q for q in all_qs if not needs_decomp(q['question'])]
    
    print(f'Total questions: {len(all_qs)}')
    print(f'Complex (need decomp): {len(complex_qs)}')
    print(f'Simple (no decomp): {len(simple_qs)}')
    
    random.seed(42)
    if len(complex_qs) > num:
        sampled = random.sample(complex_qs, num)
    else:
        sampled = complex_qs
    
    neg_samples = random.sample(simple_qs, min(10, len(simple_qs)))
    
    test_set = []
    for i, q in enumerate(sampled):
        test_set.append({
            'qid': f'Q{i+1:03d}',
            'orig_q': q['question'],
            'orig_answer': q.get('answer', []),
            'need_decomp': True,
            'gold_subs': [],
            'gold_comb': {'type': '', 'deps': []}
        })
    
    for i, q in enumerate(neg_samples):
        test_set.append({
            'qid': f'N{i+1:03d}',
            'orig_q': q['question'],
            'orig_answer': q.get('answer', []),
            'need_decomp': False,
            'gold_subs': [q['question']],
            'gold_comb': {'type': 'parallel', 'deps': []}
        })
    
    with open('test_set.json', 'w', encoding='utf-8') as f:
        json.dump(test_set, f, ensure_ascii=False, indent=2)
    
    print(f'\nTest set saved: test_set.json')
    print(f'  Positive samples (need decomp): {len(sampled)}')
    print(f'  Negative samples (no decomp needed): {len(neg_samples)}')
    return test_set

def main():
    conf = load_conf()
    main_path = conf.get('main_project_path', 'D:/olympediaRAG-main')
    build_test_set(main_path, num=15)

if __name__ == '__main__':
    main()
# run_evaluation.py
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from decomposer import decomposer, load_conf

def load_test_set():
    with open('test_set.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_test_set(test_set):
    with open('test_set.json', 'w', encoding='utf-8') as f:
        json.dump(test_set, f, ensure_ascii=False, indent=2)

def calc_sim(model, a, b):
    emb_a = model.encode([a], convert_to_tensor=True)
    emb_b = model.encode([b], convert_to_tensor=True)
    return float(np.dot(emb_a, emb_b.T)[0][0])

def match_subs(gold, pred, model, thresh=0.85):
    matched = 0
    for g in gold:
        for p in pred:
            if calc_sim(model, g, p) >= thresh:
                matched += 1
                break
    return matched

def eval_sqc(gold_subs, pred_subs, model, thresh=0.85):
    if not gold_subs:
        return 1.0
    matched = match_subs(gold_subs, pred_subs, model, thresh)
    return matched / len(gold_subs)

def eval_sqr(pred_subs, model, thresh=0.85):
    n = len(pred_subs)
    if n <= 1:
        return 0.0
    uniq = n
    for i in range(n):
        for j in range(i + 1, n):
            if calc_sim(model, pred_subs[i], pred_subs[j]) >= thresh:
                uniq -= 1
                break
    return 1.0 - (uniq / n)

def eval_dsi(all_preds, model, thresh=0.85):
    if len(all_preds) < 2:
        return 1.0
    scores = []
    for i in range(len(all_preds)):
        for j in range(i + 1, len(all_preds)):
            a_set = set()
            b_set = set()
            for sub in all_preds[i]:
                best = (sub, 0)
                for ref in all_preds[j]:
                    sim = calc_sim(model, sub, ref)
                    if sim > best[1]:
                        best = (ref, sim)
                if best[1] >= thresh:
                    a_set.add(sub)
                    b_set.add(best[0])
            union = len(set(all_preds[i]) | set(all_preds[j]))
            inter = len(a_set)
            scores.append(inter / union if union > 0 else 0)
    return float(np.mean(scores)) if scores else 0.0

def eval_comb_match(gold_comb, pred_comb):
    if not gold_comb or not gold_comb.get('type'):
        return 1.0
    return 1.0 if gold_comb.get('type') == pred_comb.get('type') else 0.0

def run_eval():
    conf = load_conf()
    test_set = load_test_set()
    n_runs = conf.get('eval_runs', 5)
    thresh = conf.get('sim_threshold', 0.85)
    
    print('Loading embedding model...')
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    sqc_list, sqr_list, dsi_list, comb_list, cnt_list = [], [], [], [], []
    
    for idx, item in enumerate(test_set):
        q_text = item['orig_q']
        gold_subs = item.get('gold_subs', [])
        gold_comb = item.get('gold_comb', {})
        
        all_preds = []
        for run in range(n_runs):
            try:
                res = decomposer(q_text)
                pred_subs = res.get('sub_qs', [])
                pred_comb = res.get('comb', {})
                all_preds.append(pred_subs)
                if run == 0:
                    item['pred_subs'] = pred_subs
                    item['pred_comb'] = pred_comb
            except Exception as e:
                print(f'Error Q{item["qid"]}: {e}')
                all_preds.append([])
        
        sqc = eval_sqc(gold_subs, all_preds[0] if all_preds else [], model, thresh)
        sqr = eval_sqr(all_preds[0] if all_preds else [], model, thresh)
        dsi = eval_dsi(all_preds, model, thresh)
        cm = eval_comb_match(gold_comb, item.get('pred_comb', {}))
        
        sqc_list.append(sqc)
        sqr_list.append(sqr)
        dsi_list.append(dsi)
        comb_list.append(cm)
        cnt_list.append(len(all_preds[0]) if all_preds else 0)
        
        item['metrics'] = {'sqc': round(sqc, 4), 'sqr': round(sqr, 4),
                           'dsi': round(dsi, 4), 'comb_acc': cm}
        
        if (idx + 1) % 10 == 0:
            print(f'Progress: {idx + 1}/{len(test_set)}')
    
    save_test_set(test_set)
    
    sqc_mean = float(np.mean(sqc_list))
    sqr_mean = float(np.mean(sqr_list))
    dsi_mean = float(np.mean(dsi_list))
    comb_mean = float(np.mean(comb_list))
    cnt_mean = float(np.mean(cnt_list))
    
    print('\n' + '=' * 55)
    print('Decomposer Evaluation Results')
    print('=' * 55)
    print(f'  Total questions:      {len(test_set)}')
    print(f'  Runs per question:    {n_runs}')
    print(f'  Similarity threshold: {thresh}')
    print('-' * 55)
    print(f'  SQC  (Sub-Q Coverage):       {sqc_mean:.4f}')
    print(f'  SQR  (Sub-Q Redundancy):     {sqr_mean:.4f}')
    print(f'  DSI  (Decomposition Stability): {dsi_mean:.4f}')
    print(f'  Comb (Combination Accuracy):  {comb_mean:.4f}')
    print(f'  Avg Sub-Qs per question:      {cnt_mean:.2f}')
    print('=' * 55)
    
    summary = {
        'n_questions': len(test_set),
        'n_runs': n_runs,
        'threshold': thresh,
        'sqc_mean': round(sqc_mean, 4),
        'sqr_mean': round(sqr_mean, 4),
        'dsi_mean': round(dsi_mean, 4),
        'comb_acc_mean': round(comb_mean, 4),
        'avg_subq_cnt': round(cnt_mean, 2)
    }
    
    with open('eval_results.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print('\nDetailed results saved: eval_results.json')
    return summary

def main():
    run_eval()

if __name__ == '__main__':
    main()