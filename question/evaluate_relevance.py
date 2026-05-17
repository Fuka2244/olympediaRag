import json
from collections import Counter, defaultdict

with open('question/olympic_search_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# ============================================================
# 表的详细描述映射（用于相关性判断）
# ============================================================
TABLE_SEMANTICS = {
    "affiliations_athletes": "组织与运动员的关联关系",
    "affiliations_infobox": "体育组织/俱乐部的基本信息",
    "athlete_biography": "运动员传记文本",
    "athlete_infobox": "运动员核心结构化信息(姓名、国籍等)",
    "athlete_olympic_records": "运动员保持的奥运纪录",
    "athlete_organization_roles": "运动员在体育组织中担任的职务",
    "athlete_other_participations": "运动员非竞赛角色的奥运参与",
    "athlete_results": "运动员的比赛成绩和奖牌",
    "ceremonies_coach_oath": "开幕式教练宣誓",
    "ceremonies_official_oath": "开幕式官员宣誓",
    "ceremonies_torch_bearers": "火炬手信息",
    "country_description": "国家描述文本",
    "country_edition": "国家每届奥运参赛统计",
    "country_edition_result": "国家每届奥运成绩",
    "country_infobox": "国家基本信息(NOC等)",
    "country_medal_by_game": "国家每届奖牌统计",
    "country_medal_by_sport": "国家各项目奖牌统计",
    "country_most_successful_competitors": "各国最成功运动员",
    "country_participants": "国家参赛人数统计",
    "country_sport": "国家各项目参赛统计",
    "country_sport_result": "国家各项目成绩",
    "definitions": "奥运相关定义和解释",
    "edition_countries": "每届奥运参赛国家",
    "edition_result": "每届奥运成绩和赛事信息",
    "edition_sport_events": "每届奥运赛事项目",
    "edition_sport_info": "每届奥运项目信息(场馆等)",
    "edition_sport_medal": "每届奥运项目奖牌获得者",
    "edition_sport_medal_table": "每届奥运项目奖牌榜",
    "edition_sport_overview": "每届奥运历史概述",
    "editions_basic_info": "每届奥运基本信息(年份、城市等)",
    "editions_bid_process": "申奥过程信息",
    "editions_medal_details": "每届奥运奖牌明细",
    "editions_medal_table": "每届奥运奖牌榜",
    "editions_overview": "每届奥运概述描述",
    "editions_top_competitors": "每届奥运顶尖运动员",
    "event_names_basic_info": "具体赛事项目的基本信息",
    "event_names_best_performance_bycountry": "各项目各国最佳表现",
    "event_names_countries": "各项目参赛国家",
    "event_names_medal_winners": "各项目奖牌获得者",
    "event_names_medals_by_country": "各项目各国奖牌数",
    "event_names_participants": "各项目参赛者信息",
    "event_names_top_medallists": "各项目顶尖奖牌获得者",
    "event_names_total_participants": "各项目总参赛人数",
    "event_total_participants": "奥运赛事总参赛人数",
    "events_non_starters": "报名但未参赛的运动员",
    "events_participants": "赛事参赛者信息",
    "flagbearers": "开幕式旗手",
    "horse_biography": "马术马匹传记",
    "horse_event_record": "马术赛事纪录",
    "horse_info": "马匹基本信息",
    "ioc_meetings": "IOC会议信息",
    "olympic_athlete_results": "奥运运动员比赛结果",
    "olympics_athlete_biographies": "奥运运动员传记",
    "olympics_athletes_infobox": "奥运运动员基本信息",
    "organizations": "体育组织信息",
    "organizations_presidents": "体育组织主席",
    "place_names": "奥运相关地名",
    "place_people_relations": "地点与人物关系(出生/死亡地)",
    "records_archery": "射箭奥运/世界纪录",
    "records_athletics": "田径奥运/世界纪录",
    "records_cycling": "自行车奥运/世界纪录",
    "records_short_track_speed_skating": "短道速滑纪录",
    "records_speed_skating": "速滑纪录",
    "records_swimming": "游泳奥运/世界纪录",
    "records_weightlifting": "举重奥运/世界纪录",
    "sport_group_events": "运动大项的赛事",
    "sport_group_medals": "运动大项奖牌信息",
    "sport_groups": "运动大项分类",
    "sports": "奥运运动项目信息",
    "venue_events_relations": "场馆与赛事关系",
    "venues": "奥运比赛场馆",
}

# ============================================================
# 基于规则的相关性评估函数
# 根据问题中的关键词和表的功能来判断
# ============================================================
def evaluate_relevance(question, answer, table_name):
    """
    返回: 3=高度相关, 2=相关, 1=部分相关, 0=不相关
    """
    q = question.lower()
    a = [x.lower() for x in answer] if answer else []
    
    # ---- 规则匹配 ----
    
    # 年份/哪届 -> editions_basic_info
    if any(w in q for w in ["which year", "what year", "when were", "when was", "when did", "first modern", "first olympic"]):
        if table_name == "editions_basic_info":
            return 3
    
    # 主办城市 -> editions_basic_info, editions_bid_process, place_names
    if any(w in q for w in ["host city", "hosted the", "where were", "where was", "which city"]):
        if table_name in ["editions_basic_info", "editions_bid_process", "place_names"]:
            return 3
        if table_name in ["venues", "edition_sport_info"]:
            return 2
    
    # 奖牌/奖牌榜
    if any(w in q for w in ["medal table", "medal tally", "medal count", "most medals", "total medals", "medal standings"]):
        if table_name in ["editions_medal_table", "edition_sport_medal_table", "country_medal_by_game", "country_medal_by_sport"]:
            return 3
        if table_name in ["editions_medal_details", "edition_sport_medal", "event_names_medals_by_country", "country_edition_result"]:
            return 2
    
    # 金/银/铜牌获得者
    if any(w in q for w in ["gold medal", "silver medal", "bronze medal", "medal winner", "won gold", "won silver", "won bronze", "medallist", "medalist"]):
        if table_name in ["edition_sport_medal", "event_names_medal_winners", "editions_medal_details", "editions_top_competitors", "event_names_top_medallists"]:
            return 3
        if table_name in ["country_most_successful_competitors", "country_medal_by_game", "olympic_athlete_results", "athlete_results"]:
            return 2
        if table_name in ["country_edition_result", "edition_result", "country_sport_result"]:
            return 1
    
    # 运动员/人物
    if any(w in q for w in ["who ", "who won", "who is", "who was", "athlete", "competitor", "champion"]):
        if table_name in ["olympics_athletes_infobox", "athlete_infobox", "olympics_athlete_biographies", "athlete_biography"]:
            return 3
        if table_name in ["editions_top_competitors", "country_most_successful_competitors", "event_names_top_medallists", "flagbearers"]:
            return 2
        if table_name in ["athlete_results", "olympic_athlete_results", "edition_sport_medal", "event_names_medal_winners"]:
            return 2
    
    # 旗手
    if "flag bearer" in q or "flagbearer" in q or "carried the flag" in q:
        if table_name == "flagbearers":
            return 3
    
    # 火炬手
    if "torch" in q or "flame" in q or "relay" in q:
        if table_name == "ceremonies_torch_bearers":
            return 3
    
    # 宣誓
    if "oath" in q:
        if table_name in ["ceremonies_coach_oath", "ceremonies_official_oath"]:
            return 3
    
    # 纪录
    if any(w in q for w in ["record", "world record", "olympic record"]):
        if table_name.startswith("records_"):
            return 3
        if table_name == "athlete_olympic_records":
            return 2
    
    # 国家参赛
    if any(w in q for w in ["how many countries", "which countries", "country partici", "nations competed", "countries competed"]):
        if table_name in ["edition_countries", "country_edition", "country_participants", "country_infobox"]:
            return 3
    
    # 场馆
    if any(w in q for w in ["venue", "stadium", "arena"]):
        if table_name in ["venues", "venue_events_relations", "edition_sport_info"]:
            return 3
    
    # 项目/运动
    if any(w in q for w in ["how many sports", "which sport", "what sport", "discipline", "new sport"]):
        if table_name in ["sports", "sport_groups", "edition_sport_events"]:
            return 3
    
    # 开幕/闭幕
    if any(w in q for w in ["opening ceremony", "closing ceremony", "ceremony"]):
        if table_name in ["ceremonies_torch_bearers", "ceremonies_coach_oath", "ceremonies_official_oath", "flagbearers"]:
            return 3
    
    # 马术
    if any(w in q for w in ["horse", "equestrian"]):
        if table_name in ["horse_info", "horse_biography", "horse_event_record"]:
            return 3
    
    # 参赛人数
    if any(w in q for w in ["how many athletes", "how many participants", "how many competitor", "total participant"]):
        if table_name in ["event_names_total_participants", "event_total_participants", "country_participants", "country_edition"]:
            return 3
    
    # 申奥
    if any(w in q for w in ["bid", "bidding", "candidate city"]):
        if table_name == "editions_bid_process":
            return 3
    
    # 未参赛
    if "did not start" in q or "non-starter" in q or "did not compete" in q:
        if table_name == "events_non_starters":
            return 3
    
    # IOC
    if "ioc" in q:
        if table_name in ["ioc_meetings", "organizations", "organizations_presidents"]:
            return 3
    
    # 通用：如果问题明确提到某项目名，event_names_* 系列相关
    specific_sports = ["swimming", "athletics", "gymnastics", "fencing", "rowing", "boxing", "wrestling", 
                       "cycling", "tennis", "diving", "sailing", "shooting", "archery", "judo", "volleyball",
                       "basketball", "football", "hockey", "handball", "table tennis", "badminton", "weightlifting",
                       "canoe", "kayak", "modern pentathlon", "triathlon", "rugby", "golf", "taekwondo", "karate",
                       "skating", "skiing", "bobsleigh", "luge", "curling", "ice hockey", "biathlon",
                       "steeplechase", "marathon", "sprint", "relay", "freestyle", "backstroke", "breaststroke",
                       "butterfly", "medley", "decathlon", "heptathlon", "pole vault", "high jump", "long jump",
                       "triple jump", "hurdle", "discus", "javelin", "hammer", "shot put", "walk", "road race"]
    
    has_sport_keyword = any(sport in q for sport in specific_sports)
    if has_sport_keyword:
        if table_name in ["event_names_basic_info", "event_names_medal_winners", "event_names_participants",
                          "edition_sport_medal", "edition_sport_events", "sports", "sport_groups"]:
            return 2
    
    # 如果问题提到具体国家
    country_keywords = ["britain", "british", "usa", "america", "american", "german", "germany", "france", "french",
                        "italy", "italian", "australia", "australian", "china", "chinese", "japan", "japanese",
                        "russia", "russian", "soviet", "canada", "canadian", "netherlands", "dutch",
                        "hungary", "hungarian", "sweden", "swedish", "finland", "finnish", "norway", "norwegian",
                        "denmark", "danish", "poland", "polish", "belgium", "belgian", "brazil", "brazilian",
                        "south korea", "korean", "india", "indian", "kenya", "kenyan", "jamaica", "jamaican",
                        "ethiopia", "ethiopian", "new zealand", "spain", "spanish", "portugal", "portuguese",
                        "cuba", "cuban", "romania", "romanian", "yugoslavia", "czech", "switzerland", "swiss",
                        "austria", "austrian", "argentina", "mexico", "mexican", "greece", "greek", "egypt",
                        "ireland", "irish", "scotland", "scottish", "wales", "welsh", "ukraine", "ukrainian",
                        "turkey", "turkish", "south africa", "thailand", "thai", "indonesia", "malaysia",
                        "philippines", "colombia", "chile", "peru", "nigeria", "nigerian", "ghana", "cameroon",
                        "morocco", "tunisia", "algeria", "pakistan", "iran", "iraqi", "israel", "saudi",
                        "palestin"]
    has_country = any(c in q for c in country_keywords)
    if has_country:
        if table_name in ["country_medal_by_game", "country_edition_result", "country_most_successful_competitors",
                          "country_sport_result", "country_infobox", "country_description", "country_edition",
                          "country_participants", "event_names_medals_by_country", "event_names_countries"]:
            return 2
    
    # 默认：基于表类型的弱相关
    # 问题问人 -> athlete相关表部分相关
    # 问题问国家 -> country相关表部分相关
    # 其他 -> 不相关
    return 0

def evaluate_relevance_fallback(question, answer, table_name):
    """
    更宽松的评估：检查表的关键词是否与问题有重叠
    """
    q_words = set(question.lower().replace("?", "").replace(",", "").replace(".", "").split())
    
    # 表的关键词
    table_kw = {
        "editions_basic_info": {"edition", "olympics", "games", "year", "city", "basic"},
        "editions_top_competitors": {"edition", "competitor", "top", "athlete", "medal"},
        "edition_sport_medal": {"edition", "medal", "winner", "sport"},
        "athlete_olympic_records": {"athlete", "record", "olympic", "performance"},
        "country_most_successful_competitors": {"country", "competitor", "successful", "medal"},
        "flagbearers": {"flag", "bearer", "ceremony", "parade", "country"},
        "editions_bid_process": {"edition", "bid", "host", "city"},
        "country_medal_by_game": {"country", "medal", "edition", "games"},
        "event_names_medal_winners": {"event", "medal", "winner"},
        "ceremonies_coach_oath": {"ceremony", "oath", "coach"},
        "country_sport_result": {"country", "sport", "result", "medal"},
        "olympics_athletes_infobox": {"athlete", "basic", "info", "olympics"},
        "events_non_starters": {"event", "non", "starter", "athlete"},
        "edition_sport_events": {"edition", "event", "sport", "competition"},
        "event_names_top_medallists": {"event", "medallist", "top", "champion"},
        "sports": {"sport", "discipline", "competition", "olympics"},
        "event_names_basic_info": {"event", "basic", "info", "competition"},
        "athlete_other_participations": {"athlete", "participation", "role"},
        "place_names": {"place", "location", "city", "geography"},
        "country_description": {"country", "description", "nation"},
        "editions_medal_details": {"edition", "medal", "detail", "winner"},
        "country_infobox": {"country", "noc", "organization", "basic"},
        "ceremonies_torch_bearers": {"ceremony", "torch", "bearer", "flame"},
        "athlete_infobox": {"athlete", "personal", "info", "bio"},
        "editions_medal_table": {"edition", "medal", "table", "ranking"},
        "country_edition_result": {"country", "result", "edition", "medal"},
        "country_edition": {"country", "participation", "edition", "games"},
        "edition_sport_medal_table": {"edition", "medal", "table", "sport"},
        "edition_sport_info": {"edition", "sport", "info", "venue"},
        "edition_sport_overview": {"edition", "overview", "history"},
        "editions_overview": {"edition", "overview", "history", "description"},
        "event_names_participants": {"event", "participant", "competition"},
        "event_names_total_participants": {"event", "participant", "total"},
        "event_total_participants": {"event", "participant", "athlete"},
        "olympics_athlete_biographies": {"athlete", "biography", "bio"},
        "olympic_athlete_results": {"athlete", "result", "competition", "medal"},
        "athlete_results": {"athlete", "result", "competition", "medal"},
        "athlete_biography": {"athlete", "biography", "bio", "personal"},
        "horse_info": {"horse", "info", "equestrian"},
        "horse_biography": {"horse", "biography"},
        "horse_event_record": {"horse", "event", "record"},
        "venues": {"venue", "stadium", "arena", "facility"},
        "records_swimming": {"record", "swimming", "world", "olympic"},
        "records_athletics": {"record", "athletics", "world", "olympic"},
        "records_archery": {"record", "archery", "world", "olympic"},
        "records_cycling": {"record", "cycling", "world", "olympic"},
        "records_weightlifting": {"record", "weightlifting", "world", "olympic"},
        "records_speed_skating": {"record", "speed", "skating"},
        "records_short_track_speed_skating": {"record", "short", "track", "skating"},
    }
    
    kws = table_kw.get(table_name, set())
    if not kws:
        return 0
    overlap = len(q_words & kws)
    if overlap >= 3:
        return 2
    if overlap >= 2:
        return 1
    return 0


# ============================================================
# 对每个问题评估 Top1, Top3, Top5, Top25 的相关性
# ============================================================
results = {
    "sim_top1": [], "sim_top3": [], "sim_top5": [], "sim_top40": [],
    "rerank_top1": [], "rerank_top3": [], "rerank_top5": [], "rerank_top25": []
}

eval_details = []

for item in data:
    question = item['question']
    answer = item.get('answer', [])
    
    # Similarity 评估
    for k, topk_list, top_n in [
        ("sim_top1", item['similarity_top40'], 1),
        ("sim_top3", item['similarity_top40'], 3),
        ("sim_top5", item['similarity_top40'], 5),
        ("sim_top40", item['similarity_top40'], 40),
    ]:
        tables = [x['table_name'] for x in topk_list[:top_n]]
        # 取最高相关性
        best_rel = max(evaluate_relevance(question, answer, t) for t in tables)
        fallback_rels = [max(evaluate_relevance(question, answer, t), evaluate_relevance_fallback(question, answer, t)) for t in tables]
        best_rel_fb = max(fallback_rels)
        results[k].append(best_rel_fb)
    
    # Rerank 评估
    for k, topk_list, top_n in [
        ("rerank_top1", item['rerank_top25'], 1),
        ("rerank_top3", item['rerank_top25'], 3),
        ("rerank_top5", item['rerank_top25'], 5),
        ("rerank_top25", item['rerank_top25'], 25),
    ]:
        tables = [x['table_name'] for x in topk_list[:top_n]]
        fallback_rels = [max(evaluate_relevance(question, answer, t), evaluate_relevance_fallback(question, answer, t)) for t in tables]
        best_rel_fb = max(fallback_rels)
        results[k].append(best_rel_fb)
    
    # 记录详细：rerank_top1的具体评估
    r1_table = item['rerank_top25'][0]['table_name'] if item['rerank_top25'] else 'N/A'
    r1_rel = max(evaluate_relevance(question, answer, r1_table), evaluate_relevance_fallback(question, answer, r1_table))
    s1_table = item['similarity_top40'][0]['table_name'] if item['similarity_top40'] else 'N/A'
    s1_rel = max(evaluate_relevance(question, answer, s1_table), evaluate_relevance_fallback(question, answer, s1_table))
    
    eval_details.append({
        "id": item['id'],
        "question": question,
        "answer": answer,
        "sim_top1_table": s1_table,
        "sim_top1_relevance": s1_rel,
        "rerank_top1_table": r1_table,
        "rerank_top1_relevance": r1_rel,
    })

# ============================================================
# 输出统计
# ============================================================
lines = []
def p(s=""):
    lines.append(s)

p("=" * 70)
p("Top-K 相关性评估报告")
p("=" * 70)
p(f"\n总问题数: {len(data)}")
p(f"评分标准: 3=高度相关, 2=相关, 1=部分相关, 0=不相关")
p(f"注意: 对每个TopK范围取【最高相关性】，即只要TopK中有相关表就算命中")

for method, label in [("sim", "Similarity"), ("rerank", "Rerank")]:
    p(f"\n{'='*70}")
    p(f"{label} 检索相关性")
    p(f"{'='*70}")
    for k in ["top1", "top3", "top5", "top40" if method == "sim" else "top25"]:
        scores = results[f"{method}_{k}"]
        total = len(scores)
        high = sum(1 for s in scores if s >= 3)
        rel = sum(1 for s in scores if s >= 2)
        partial = sum(1 for s in scores if s >= 1)
        none = sum(1 for s in scores if s == 0)
        p(f"\n  {label} {k.upper():>5}: 高度相关={high}({high/total*100:.1f}%) | 相关={rel}({rel/total*100:.1f}%) | 部分相关={partial}({partial/total*100:.1f}%) | 不相关={none}({none/total*100:.1f}%)")

# ---- Rerank vs Similarity Top1 对比 ----
p(f"\n{'='*70}")
p("Rerank Top1 vs Similarity Top1 对比")
p(f"{'='*70}")

both_high = sum(1 for d in eval_details if d['sim_top1_relevance'] >= 3 and d['rerank_top1_relevance'] >= 3)
sim_high_rerank_low = sum(1 for d in eval_details if d['sim_top1_relevance'] >= 2 and d['rerank_top1_relevance'] <= 1)
rerank_high_sim_low = sum(1 for d in eval_details if d['rerank_top1_relevance'] >= 2 and d['sim_top1_relevance'] <= 1)
both_low = sum(1 for d in eval_details if d['sim_top1_relevance'] <= 1 and d['rerank_top1_relevance'] <= 1)

p(f"  两者都高度相关(≥2): {both_high} ({both_high/len(eval_details)*100:.1f}%)")
p(f"  Similarity好但Rerank差: {sim_high_rerank_low} ({sim_high_rerank_low/len(eval_details)*100:.1f}%)")
p(f"  Rerank好但Similarity差: {rerank_high_sim_low} ({rerank_high_sim_low/len(eval_details)*100:.1f}%)")
p(f"  两者都不好(≤1): {both_low} ({both_low/len(eval_details)*100:.1f}%)")

# Rerank提升的问题
p(f"\n--- Rerank Top1 比 Similarity Top1 更好的问题 (采样) ---")
improved = [d for d in eval_details if d['rerank_top1_relevance'] > d['sim_top1_relevance']]
for d in improved[:10]:
    p(f"  [{d['sim_top1_relevance']}->{d['rerank_top1_relevance']}] Q: {d['question'][:70]}")
    p(f"      Sim: {d['sim_top1_table']} | Rerank: {d['rerank_top1_table']}")

# Rerank下降的问题
p(f"\n--- Rerank Top1 比 Similarity Top1 更差的问题 (采样) ---")
degraded = [d for d in eval_details if d['rerank_top1_relevance'] < d['sim_top1_relevance']]
for d in degraded[:10]:
    p(f"  [{d['sim_top1_relevance']}->{d['rerank_top1_relevance']}] Q: {d['question'][:70]}")
    p(f"      Sim: {d['sim_top1_table']} | Rerank: {d['rerank_top1_table']}")

# ---- 不相关问题分析 ----
p(f"\n{'='*70}")
p("Rerank Top1 不相关问题 (score=0) - 采样20个")
p(f"{'='*70}")

irrelevant = [d for d in eval_details if d['rerank_top1_relevance'] == 0]
p(f"  总计: {len(irrelevant)} ({len(irrelevant)/len(eval_details)*100:.1f}%)")
for d in irrelevant[:20]:
    p(f"  Q: {d['question'][:80]}")
    p(f"     Rerank Top1: {d['rerank_top1_table']} | Sim Top1: {d['sim_top1_table']}")

# ---- 各Rerank Top1得分区间下的相关性 ----
p(f"\n{'='*70}")
p("Rerank Top1 得分区间 vs 相关性")
p(f"{'='*70}")

# 低分(<=0.001), 中低(0.001-0.005), 中(0.005-0.01), 高(>0.01)
score_ranges = [(0, 0.001, "≤0.001"), (0.001, 0.005, "0.001-0.005"), (0.005, 0.01, "0.005-0.01"), (0.01, 1.0, ">0.01")]

for low, high, label in score_ranges:
    subset = [(d, item) for d, item in zip(eval_details, data) 
              if item['rerank_top25'] and low <= item['rerank_top25'][0]['rerank_score'] < high]
    if subset:
        rel_count = sum(1 for d, _ in subset if d['rerank_top1_relevance'] >= 2)
        total = len(subset)
        p(f"  Rerank得分 {label:>12}: 问题数={total}, 相关(≥2)={rel_count} ({rel_count/total*100:.1f}%)")

p(f"\n{'='*70}")
p("评估完成")
p(f"{'='*70}")

# 写入报告
with open('question/relevance_evaluation.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

# 同时将详细评估结果写入JSON
with open('question/relevance_details.json', 'w', encoding='utf-8') as f:
    json.dump(eval_details, f, ensure_ascii=False, indent=2)

print("Reports saved.")
