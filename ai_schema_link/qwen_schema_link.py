"""
奥林匹克二阶段检索规划器 - 表选择模块
使用 qwen-max 模型从 rerank_top25 中选择 top_k 表并生成列值约束
"""

import json
import os
from openai import OpenAI

# 初始化 OpenAI 客户端（使用阿里云 DashScope API）
client = OpenAI(
    api_key=os.getenv("DASH_SCOPE_API_KEY"),  # 设置您的 API Key
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 加载表描述映射
TABLES_DESC_PATH = "d:/Projects/pythonProject/sql/description/tables_description.json"


def load_tables_description() -> dict[str, dict]:
    """
    加载 tables_description.json，返回 {table_name: description_info} 映射
    """
    with open(TABLES_DESC_PATH, 'r', encoding='utf-8') as f:
        tables = json.load(f)
    return {t["table_name"]: t for t in tables}


_TABLES_DESC_CACHE: dict[str, dict] | None = None


def get_tables_description() -> dict[str, dict]:
    """懒加载并缓存表描述"""
    global _TABLES_DESC_CACHE
    if _TABLES_DESC_CACHE is None:
        _TABLES_DESC_CACHE = load_tables_description()
    return _TABLES_DESC_CACHE

# 系统提示词
SYSTEM_PROMPT = """
你是“奥林匹克二阶段检索规划器”。

输入：
- question
- rerank_top25（已按相关性降序排列）

你的任务：
基于 rerank_top25，输出：
1. top_k_tables（默认 k=8）
2. 可靠提取的列值约束 column_value_constraints 

规则：

【候选表约束】
- 只能从 rerank_top25 中选出 k 个最相关的表。
- 禁止生成 rerank_top25 外的表名。
- top_k_tables 长度必须等于 k。

【约束生成规则】
- 仅当问题中的实体、时间、国家、项目等能可靠映射到表描述中的列时，才生成约束。
- 若无法可靠确定列名、值或 operator，则不要生成该约束。
- 禁止臆造列名。
- column_value_constraints.table_name 必须属于 top_k_tables。
- 一个约束格式如下：

{
  "table_name": "...",
  "column": "...",
  "operator": "=",
  "value": "..."
}

【国家规则】
- 国家必须使用 ISO-3166 alpha-3 三位国家代码。
- 示例：
  中国 -> CHN
  美国 -> USA
  英国 -> GBR

【比赛项目规则】
- 涉及 Olympic event / sport / discipline 时，优先使用模糊匹配：
{
  "column": "event",
  "operator": "LIKE",
  "value": "%Jumping%"
}

【输出格式】
只输出合法 JSON。
禁止输出解释、Markdown、注释。

输出格式：

{
  "question": "...",
  "top_k_tables": [
    "table_a",
    "table_b"
  ],
  "column_value_constraints": [
    {
      "table_name": "table_a",
      "column": "noc", 
      "operator": "=",
      "value": "CHN"
    }
  ]
}
"""


def load_search_results(file_path: str) -> list[dict]:
    """
    从 JSON 文件加载搜索结果

    Args:
        file_path: JSON 文件路径

    Returns:
        搜索结果列表
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_rerank_top25(item: dict, top_n: int = 25) -> list[dict]:
    """
    从搜索结果中提取 rerank top 表（包含表名和描述）

    Args:
        item: 搜索结果条目，包含 rerank_top25
        top_n: 取前 top_n 个表，默认 25

    Returns:
        表名和描述列表
    """
    similarity_list = item.get("rerank_top25", [])
    return [
        {
            "table_name": entry["table_name"],
            "description": entry["text"]
        }
        for entry in similarity_list[:top_n]
    ]


def enrich_rerank_top25_with_table_desc(rerank_top25: list[dict]) -> list[dict]:
    """
    根据 rerank_top25 中的表名，从 tables_description.json 中补充详细的表描述和字段信息

    Args:
        rerank_top25: reranker 重排后的 top 25 表列表（包含 table_name 和 description）

    Returns:
        增强后的表列表，每项额外包含 table_description（详细描述）和 fields（字段列表）
    """
    tables_desc = get_tables_description()
    enriched = []
    for entry in rerank_top25:
        table_name = entry["table_name"]
        desc_info = tables_desc.get(table_name, {})
        enriched.append({
            "table_name": table_name,
            "description": entry.get("description", ""),
            "table_description": desc_info.get("description", ""),
            "fields": [
                {"name": f["name"], "desc": f["desc"]}
                for f in desc_info.get("fields", [])
            ] if desc_info else [],
        })
    return enriched


def table_selector(question: str, rerank_top25: list[dict], k: int = 8, model: str = "qwen-max", verbose: bool = False, process_log_dir: str | None = None, question_id: str | int | None = None) -> dict:
    """
    使用 qwen-max 模型进行表选择

    Args:
        question: 用户问题
        rerank_top25: reranker 重排后的 top 25 表列表（包含 table_name 和 description）
        k: 需要选择的表数量，默认 8
        model: 使用的模型，默认 qwen-max
        verbose: 是否输出中间过程，默认 False
        process_log_dir: 中间过程日志保存目录，为 None 则不保存到文件
        question_id: 问题ID，用于日志文件命名

    Returns:
        dict: 包含 question, top_k_tables, column_value_constraints 的字典
    """
    # 用 tables_description.json 丰富 rerank_top25
    enriched_top25 = enrich_rerank_top25_with_table_desc(rerank_top25)

    # 准备中间过程日志
    log_lines: list[str] = []

    def log(msg: str):
        log_lines.append(msg)
        if verbose:
            print(msg)

    log("\n" + "=" * 60)
    log("[中间过程] enriched rerank_top25:")
    for idx, t in enumerate(enriched_top25):
        log(f"  {idx+1}. {t['table_name']} - {t.get('table_description', '')}")
        for f in t.get("fields", []):
            log(f"      {f['name']}: {f['desc']}")
    log("=" * 60)

    # 构建用户提示
    user_prompt = f"""请基于下列输入返回 JSON：
{{
  "question": "{question}",
  "k": {k},
  "rerank_top25": {json.dumps(enriched_top25, ensure_ascii=False, indent=2)}
}}"""

    log(f"\n[中间过程] user_prompt:\n{user_prompt}")
    log(f"[中间过程] 调用模型: {model}")

    # 调用模型
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )

    raw_content = response.choices[0].message.content

    log(f"\n[中间过程] 模型原始输出:\n{raw_content}")

    # 保存中间过程到文件
    if process_log_dir:
        os.makedirs(process_log_dir, exist_ok=True)
        log_name = f"q_{question_id}" if question_id is not None else "q_unknown"
        log_path = os.path.join(process_log_dir, f"{log_name}.txt")
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(log_lines))

    # 解析响应
    result = json.loads(raw_content)

    # 硬性校验
    assert len(result["top_k_tables"]) == k, f"top_k_tables 长度必须等于 k={k}"

    # 校验 top_k_tables 必须在 rerank_top25 中
    candidate_table_names = {t["table_name"] for t in rerank_top25}
    for t_name in result["top_k_tables"]:
        assert t_name in candidate_table_names, \
            f"top_k_tables 中的表名 {t_name} 不在 rerank_top25 候选池中"

    # 校验 column_value_constraints
    top_k_set = set(result["top_k_tables"])
    for constraint in result.get("column_value_constraints", []):
        assert constraint["table_name"] in top_k_set, \
            f"column_value_constraints 中的表名 {constraint['table_name']} 不在 top_k_tables 中"

    return result


def get_completed_ids(output_file: str) -> set:
    """
    从已存在的 JSONL 文件中提取已完成的 question_id 集合

    Args:
        output_file: JSONL 输出文件路径

    Returns:
        已完成的问题 ID 集合
    """
    completed_ids: set = set()
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        record = json.loads(line)
                        if "id" in record:
                            completed_ids.add(record["id"])
                    except json.JSONDecodeError:
                        continue
    return completed_ids


def process_questions(
    input_file: str = "d:/Projects/pythonProject/retrival_result/olympedia_questions_search_results.json",
    output_file: str = "d:/Projects/pythonProject/ai_schema_link/table_selection_results.jsonl",
    k: int = 8,
    model: str = "qwen-plus",
    verbose: bool = False,
    save_process: bool = False,
    process_log_dir: str = "d:/Projects/pythonProject/ai_schema_link/process",
    resume: bool = True
) -> None:
    """
    批量处理所有问题，每处理一个立即保存（JSONL格式）

    Args:
        input_file: 输入文件路径（olympedia_questions_search_results.json）
        output_file: 输出文件路径（JSONL格式，每行一个JSON）
        k: 每个问题选择的表数量
        model: 使用的模型
        verbose: 是否输出中间过程到控制台
        save_process: 是否保存中间过程到文件
        process_log_dir: 中间过程日志保存目录
        resume: 是否启用断点续传（跳过已生成的问题），默认 True
    """
    # 加载搜索结果
    search_results = load_search_results(input_file)

    # 断点续传：获取已完成的问题 ID
    completed_ids = get_completed_ids(output_file) if resume else set()
    if resume and completed_ids:
        print(f"[断点续传] 检测到已完成 {len(completed_ids)} 个问题，将跳过")

    log_dir = process_log_dir if save_process else None

    total = len(search_results)
    new_count = 0
    skip_count = 0
    for i, item in enumerate(search_results):
        question = item["question"]
        rerank_top25 = extract_rerank_top25(item, top_n=25)
        question_id = item.get("id", i)

        # 跳过已完成的问题
        if resume and question_id in completed_ids:
            skip_count += 1
            if verbose:
                print(f"[{i+1}/{total}] 跳过 (已存在): {question[:50]}...")
            continue

        print(f"[{i+1}/{total}] 处理: {question[:50]}...")

        result = {
            "id": item.get("id"),
            "question": question,
        }

        try:
            table_result = table_selector(
                question, rerank_top25, k=k, model=model,
                verbose=verbose, process_log_dir=log_dir, question_id=question_id
            )
            result.update(table_result)
        except Exception as e:
            print(f"  错误: {e}")
            result["error"] = str(e)

        # 每处理一个立即追加保存
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')

        new_count += 1
        print(f"  已保存到 {output_file}")

    print(f"\n完成！共 {total} 个问题，新增处理 {new_count} 个，跳过 {skip_count} 个")
    print(f"结果追加到 {output_file}")


if __name__ == "__main__":
    # 批量处理所有问题
    process_questions(verbose=True, save_process=True)
