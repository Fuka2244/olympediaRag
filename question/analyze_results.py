import json
import sys
from collections import Counter

# 加载数据
with open('question/olympic_search_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def mean(lst):
    return sum(lst) / len(lst) if lst else 0

def median(lst):
    s = sorted(lst)
    n = len(s)
    if n == 0: return 0
    if n % 2 == 1: return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2

lines = []
def p(s=""):
    lines.append(s)

p("=" * 70)
p("Olympic 检索结果分析报告")
p("=" * 70)
p(f"\n总问题数: {len(data)}")

# ---- 1. 基础统计 ----
p(f"\n{'='*70}")
p("1. 基础统计")
p(f"{'='*70}")

sim_top1_scores = []
sim_top40_scores = []
sim_avg_scores = []
for item in data:
    top40 = item['similarity_top40']
    if top40:
        scores = [x['similarity_score'] for x in top40]
        sim_top1_scores.append(scores[0])
        sim_top40_scores.append(scores[-1])
        sim_avg_scores.append(mean(scores))

p(f"\n--- Similarity Top40 得分 ---")
p(f"  Top1 得分:  均值={mean(sim_top1_scores):.4f}, 中位数={median(sim_top1_scores):.4f}, 最小={min(sim_top1_scores):.4f}, 最大={max(sim_top1_scores):.4f}")
p(f"  Top40 得分: 均值={mean(sim_top40_scores):.4f}, 中位数={median(sim_top40_scores):.4f}, 最小={min(sim_top40_scores):.4f}, 最大={max(sim_top40_scores):.4f}")
p(f"  平均得分:   均值={mean(sim_avg_scores):.4f}, 中位数={median(sim_avg_scores):.4f}")

rerank_top1_scores = []
rerank_top25_scores = []
rerank_avg_scores = []
for item in data:
    top25 = item['rerank_top25']
    if top25:
        scores = [x['rerank_score'] for x in top25]
        rerank_top1_scores.append(scores[0])
        rerank_top25_scores.append(scores[-1])
        rerank_avg_scores.append(mean(scores))

p(f"\n--- Rerank Top25 得分 ---")
p(f"  Top1 得分:  均值={mean(rerank_top1_scores):.6f}, 中位数={median(rerank_top1_scores):.6f}, 最小={min(rerank_top1_scores):.6f}, 最大={max(rerank_top1_scores):.6f}")
p(f"  Top25 得分: 均值={mean(rerank_top25_scores):.6f}, 中位数={median(rerank_top25_scores):.6f}, 最小={min(rerank_top25_scores):.6f}, 最大={max(rerank_top25_scores):.6f}")
p(f"  平均得分:   均值={mean(rerank_avg_scores):.6f}, 中位数={median(rerank_avg_scores):.6f}")

# ---- 2. 表频次分析 ----
p(f"\n{'='*70}")
p("2. 表频次分析")
p(f"{'='*70}")

sim_top1_tables = Counter()
for item in data:
    if item['similarity_top40']:
        sim_top1_tables[item['similarity_top40'][0]['table_name']] += 1

p(f"\n--- Similarity Top1 最常命中的表 (Top15) ---")
for table, count in sim_top1_tables.most_common(15):
    p(f"  {table}: {count} ({count/len(data)*100:.1f}%)")

rerank_top1_tables = Counter()
for item in data:
    if item['rerank_top25']:
        rerank_top1_tables[item['rerank_top25'][0]['table_name']] += 1

p(f"\n--- Rerank Top1 最常命中的表 (Top15) ---")
for table, count in rerank_top1_tables.most_common(15):
    p(f"  {table}: {count} ({count/len(data)*100:.1f}%)")

sim_table_freq = Counter()
for item in data:
    for x in item['similarity_top40']:
        sim_table_freq[x['table_name']] += 1

p(f"\n--- Similarity Top40 中出现频次最高的表 (Top15) ---")
for table, count in sim_table_freq.most_common(15):
    p(f"  {table}: {count} (出现在 {count/len(data)*100:.1f}% 的问题中)")

rerank_table_freq = Counter()
for item in data:
    for x in item['rerank_top25']:
        rerank_table_freq[x['table_name']] += 1

p(f"\n--- Rerank Top25 中出现频次最高的表 (Top15) ---")
for table, count in rerank_table_freq.most_common(15):
    p(f"  {table}: {count} (出现在 {count/len(data)*100:.1f}% 的问题中)")

# ---- 3. Similarity vs Rerank 排序变化 ----
p(f"\n{'='*70}")
p("3. Similarity vs Rerank 排序变化分析")
p(f"{'='*70}")

top1_change_count = 0
top1_same_count = 0
rank_changes = []

for item in data:
    sim_top1_table = item['similarity_top40'][0]['table_name'] if item['similarity_top40'] else None
    rerank_top1_table = item['rerank_top25'][0]['table_name'] if item['rerank_top25'] else None
    
    if sim_top1_table != rerank_top1_table:
        top1_change_count += 1
    else:
        top1_same_count += 1
    
    sim_top1_idx = item['similarity_top40'][0]['index'] if item['similarity_top40'] else None
    if sim_top1_idx is not None and item['rerank_top25']:
        rerank_indices = [x['index'] for x in item['rerank_top25']]
        if sim_top1_idx in rerank_indices:
            rerank_pos = rerank_indices.index(sim_top1_idx)
            rank_changes.append(rerank_pos)

p(f"  Top1 一致: {top1_same_count} ({top1_same_count/len(data)*100:.1f}%)")
p(f"  Top1 变化: {top1_change_count} ({top1_change_count/len(data)*100:.1f}%)")

if rank_changes:
    p(f"\n  Similarity Top1 在 Rerank 中的排名位置:")
    p(f"    仍在Top1: {rank_changes.count(0)} ({rank_changes.count(0)/len(rank_changes)*100:.1f}%)")
    p(f"    降至Top5: {sum(1 for c in rank_changes if c < 5)} ({sum(1 for c in rank_changes if c < 5)/len(rank_changes)*100:.1f}%)")
    p(f"    降至Top10: {sum(1 for c in rank_changes if c < 10)} ({sum(1 for c in rank_changes if c < 10)/len(rank_changes)*100:.1f}%)")
    p(f"    掉出Top25: {len(data) - len(rank_changes)} ({(len(data) - len(rank_changes))/len(data)*100:.1f}%)")

# ---- 4. Rerank 提升/下降分析 ----
p(f"\n{'='*70}")
p("4. Rerank 提升最大和下降最大的表")
p(f"{'='*70}")

rank_shifts = []
for item in data:
    sim_ranks = {x['index']: i for i, x in enumerate(item['similarity_top40'])}
    rerank_ranks = {x['index']: i for i, x in enumerate(item['rerank_top25'])}
    
    for idx in rerank_ranks:
        if idx in sim_ranks:
            shift = sim_ranks[idx] - rerank_ranks[idx]
            table_name = item['rerank_top25'][rerank_ranks[idx]]['table_name']
            rank_shifts.append((table_name, sim_ranks[idx], rerank_ranks[idx], shift))

promoted = [s for s in rank_shifts if s[3] > 0]
demoted = [s for s in rank_shifts if s[3] < 0]

promoted_tables = Counter([s[0] for s in promoted])
demoted_tables = Counter([s[0] for s in demoted])

p(f"\n--- Rerank 提升最频繁的表 (Top10) ---")
for table, count in promoted_tables.most_common(10):
    avg_shift = mean([s[3] for s in promoted if s[0] == table])
    p(f"  {table}: 提升{count}次, 平均提升{avg_shift:.1f}位")

p(f"\n--- Rerank 下降最频繁的表 (Top10) ---")
for table, count in demoted_tables.most_common(10):
    avg_shift = mean([s[3] for s in demoted if s[0] == table])
    p(f"  {table}: 下降{count}次, 平均下降{abs(avg_shift):.1f}位")

# ---- 5. 得分分布区间 ----
p(f"\n{'='*70}")
p("5. Similarity Top1 得分分布")
p(f"{'='*70}")

bins = [0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0]
for i in range(len(bins)-1):
    count = sum(1 for s in sim_top1_scores if bins[i] <= s < bins[i+1])
    p(f"  [{bins[i]:.1f}, {bins[i+1]:.1f}): {count} ({count/len(sim_top1_scores)*100:.1f}%)")

p(f"\n{'='*70}")
p("6. Rerank Top1 得分分布")
p(f"{'='*70}")

rerank_bins = [0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
for i in range(len(rerank_bins)-1):
    count = sum(1 for s in rerank_top1_scores if rerank_bins[i] <= s < rerank_bins[i+1])
    p(f"  [{rerank_bins[i]}, {rerank_bins[i+1]}): {count} ({count/len(rerank_top1_scores)*100:.1f}%)")

# ---- 7. 低分问题 ----
p(f"\n{'='*70}")
p("7. Similarity Top1 得分最低的10个问题")
p(f"{'='*70}")

scored_items = [(item, item['similarity_top40'][0]['similarity_score']) for item in data if item['similarity_top40']]
scored_items.sort(key=lambda x: x[1])

for item, score in scored_items[:10]:
    rerank_t1 = item['rerank_top25'][0]['table_name'] if item['rerank_top25'] else 'N/A'
    q = item['question'][:80]
    p(f"  [{score:.4f}] Q: {q}")
    p(f"         SimTop1: {item['similarity_top40'][0]['table_name']} | RerankTop1: {rerank_t1}")

# ---- 8. 高分问题 ----
p(f"\n{'='*70}")
p("8. Similarity Top1 得分最高的10个问题")
p(f"{'='*70}")

scored_items_desc = sorted(scored_items, key=lambda x: x[1], reverse=True)

for item, score in scored_items_desc[:10]:
    q = item['question'][:80]
    p(f"  [{score:.4f}] Q: {q}")
    p(f"         Top1表: {item['similarity_top40'][0]['table_name']}")

# ---- 9. 覆盖率 ----
p(f"\n{'='*70}")
p("9. 表覆盖率")
p(f"{'='*70}")

all_tables = set()
sim_t1_tables = set()
rerank_t1_tables = set()
sim_t40_tables = set()
rerank_t25_tables = set()

for item in data:
    for x in item['similarity_top40']:
        all_tables.add(x['table_name'])
        sim_t40_tables.add(x['table_name'])
    for x in item['rerank_top25']:
        rerank_t25_tables.add(x['table_name'])
    if item['similarity_top40']:
        sim_t1_tables.add(item['similarity_top40'][0]['table_name'])
    if item['rerank_top25']:
        rerank_t1_tables.add(item['rerank_top25'][0]['table_name'])

p(f"  总共涉及的表: {len(all_tables)}")
p(f"  作为 Similarity Top1 的表: {len(sim_t1_tables)}")
p(f"  作为 Rerank Top1 的表: {len(rerank_t1_tables)}")
p(f"  出现在 Similarity Top40 的表: {len(sim_t40_tables)}")
p(f"  出现在 Rerank Top25 的表: {len(rerank_t25_tables)}")

never_top1 = sim_t40_tables - sim_t1_tables
p(f"\n  从未被Similarity Top1命中的表 ({len(never_top1)}):")
for t in sorted(never_top1):
    freq = sim_table_freq.get(t, 0)
    p(f"    {t}: 在top40中出现{freq}次")

# ---- 10. Category维度分析 ----
p(f"\n{'='*70}")
p("10. 按 Category 分组的检索得分")
p(f"{'='*70}")

category_scores = {}
for item in data:
    cat = item.get('category', 'unknown')
    if item['similarity_top40']:
        score = item['similarity_top40'][0]['similarity_score']
        category_scores.setdefault(cat, []).append(score)

for cat in sorted(category_scores.keys(), key=lambda c: mean(category_scores[c]), reverse=True):
    scores = category_scores[cat]
    p(f"  {cat}: 平均Top1={mean(scores):.4f}, 问题数={len(scores)}")

p(f"\n{'='*70}")
p("分析完成")
p(f"{'='*70}")

# 写入文件
with open('question/analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("Report saved to question/analysis_report.txt")
