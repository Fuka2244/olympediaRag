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
                best_sim = 0
                best_ref = None
                for ref in all_preds[j]:
                    sim = calc_sim(model, sub, ref)
                    if sim > best_sim:
                        best_sim = sim
                        best_ref = ref
                if best_sim >= thresh:
                    a_set.add(sub)
                    b_set.add(best_ref)
            union = len(set(all_preds[i]) | set(all_preds[j]))
            inter = len(a_set)
            scores.append(inter / union if union > 0 else 0)
    return float(np.mean(scores)) if scores else 0.0

def eval_comb_match(gold_comb, pred_comb):
    if not gold_comb or not gold_comb.get('type'):
        return 1.0
    return 1.0 if gold_comb.get('type') == pred_comb.get('type') else 0.0

def eval_decomp_decision(item, pred_subs):
    need = item.get('need_decomp', True)
    if not need:
        return 1.0 if len(pred_subs) <= 1 else 0.0
    else:
        return 1.0 if len(pred_subs) > 1 else 0.0

def run_eval():
    conf = load_conf()
    test_set = load_test_set()
    n_runs = conf.get('eval_runs', 5)
    thresh = conf.get('sim_threshold', 0.85)
    
    print('Loading embedding model...')
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    pos_items = [it for it in test_set if it.get('need_decomp', True)]
    neg_items = [it for it in test_set if not it.get('need_decomp', True)]
    
    print(f'Positive samples (need decomp): {len(pos_items)}')
    print(f'Negative samples (no decomp needed): {len(neg_items)}')
    
    all_sqc, all_sqr, all_dsi, all_comb, all_cnt = [], [], [], [], []
    all_decomp_acc = []
    
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
                print(f'Error {item["qid"]}: {e}')
                all_preds.append([])
        
        first_preds = all_preds[0] if all_preds else []
        
        sqc = eval_sqc(gold_subs, first_preds, model, thresh) if gold_subs else 1.0
        sqr = eval_sqr(first_preds, model, thresh)
        dsi = eval_dsi(all_preds, model, thresh)
        cm = eval_comb_match(gold_comb, item.get('pred_comb', {})) if gold_comb.get('type') else 1.0
        dc = eval_decomp_decision(item, first_preds)
        
        all_sqc.append(sqc)
        all_sqr.append(sqr)
        all_dsi.append(dsi)
        all_comb.append(cm)
        all_cnt.append(len(first_preds))
        all_decomp_acc.append(dc)
        
        item['metrics'] = {
            'sqc': round(sqc, 4),
            'sqr': round(sqr, 4),
            'dsi': round(dsi, 4),
            'comb_acc': cm,
            'decomp_acc': dc
        }
        
        print(f'[{item["qid"]}] SQC={sqc:.3f} SQR={sqr:.3f} DSI={dsi:.3f} '
              f'Comb={cm} Decomp={dc} SubQs={len(first_preds)}')
    
    save_test_set(test_set)
    
    sqc_mean = float(np.mean(all_sqc))
    sqr_mean = float(np.mean(all_sqr))
    dsi_mean = float(np.mean(all_dsi))
    comb_mean = float(np.mean(all_comb))
    cnt_mean = float(np.mean(all_cnt))
    dc_mean = float(np.mean(all_decomp_acc))
    
    pos_sqc = float(np.mean([all_sqc[i] for i, it in enumerate(test_set) if it.get('need_decomp', True)]))
    pos_dc = float(np.mean([all_decomp_acc[i] for i, it in enumerate(test_set) if it.get('need_decomp', True)]))
    neg_dc = float(np.mean([all_decomp_acc[i] for i, it in enumerate(test_set) if not it.get('need_decomp', True)]))
    
    print('\n' + '=' * 60)
    print('DECOMPOSER EVALUATION RESULTS')
    print('=' * 60)
    print(f'  Total questions:        {len(test_set)}')
    print(f'  Positive (need decomp): {len(pos_items)}')
    print(f'  Negative (no decomp):   {len(neg_items)}')
    print(f'  Runs per question:      {n_runs}')
    print(f'  Similarity threshold:   {thresh}')
    print('-' * 60)
    print(f'  SQC  (Sub-Q Coverage):         {sqc_mean:.4f}')
    print(f'  SQR  (Sub-Q Redundancy):       {sqr_mean:.4f}')
    print(f'  DSI  (Decomp Stability):       {dsi_mean:.4f}')
    print(f'  Comb (Combination Accuracy):   {comb_mean:.4f}')
    print(f'  Dec  (Decomp Decision Acc):    {dc_mean:.4f}')
    print(f'  Avg Sub-Qs per question:       {cnt_mean:.2f}')
    print('-' * 60)
    print(f'  SQC on positive samples only:  {pos_sqc:.4f}')
    print(f'  Decision Acc (positive):        {pos_dc:.4f}')
    print(f'  Decision Acc (negative):        {neg_dc:.4f}')
    print('=' * 60)
    
    summary = {
        'n_total': len(test_set),
        'n_positive': len(pos_items),
        'n_negative': len(neg_items),
        'n_runs': n_runs,
        'threshold': thresh,
        'sqc_mean': round(sqc_mean, 4),
        'sqr_mean': round(sqr_mean, 4),
        'dsi_mean': round(dsi_mean, 4),
        'comb_acc_mean': round(comb_mean, 4),
        'decomp_decision_acc': round(dc_mean, 4),
        'sqc_positive_only': round(pos_sqc, 4),
        'decision_acc_positive': round(pos_dc, 4),
        'decision_acc_negative': round(neg_dc, 4),
        'avg_subq_cnt': round(cnt_mean, 2)
    }
    
    with open('eval_results.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print('\nDetailed results saved to: eval_results.json')
    print('Updated test_set saved to: test_set.json')
    return summary

def main():
    run_eval()

if __name__ == '__main__':
    main()