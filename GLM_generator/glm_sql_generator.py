"""
使用 DashScope (千问) API 根据表选择结果生成 SQL 查询
从 k=1 到 k=8 依次生成 SQL
"""
import json
import os
import dashscope
from dashscope import Generation

# DashScope API 配置
DASHSCOPE_API_KEY = os.getenv("DASH_SCOPE_API_KEY")  # 设置您的 API Key
dashscope.api_key = DASHSCOPE_API_KEY

# 文件路径
TABLE_SELECTION_FILE = "d:/Projects/pythonProject/ai_schema_link/table_selection_results.jsonl"
DDL_MAPPING_FILE = "d:/Projects/pythonProject/sql/table_ddl_mapping.jsonl"
OUTPUT_FILE = "d:/Projects/pythonProject/GLM_generator/sql_generation_results.jsonl"

# 最大 k 值
MAX_K = 8


def load_ddl_mapping() -> dict[str, str]:
    """加载表名到 DDL 的映射"""
    mapping = {}
    with open(DDL_MAPPING_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                record = json.loads(line)
                mapping[record["table_name"]] = record["ddl"]
    return mapping


def build_column_constraints_text(column_value_constraints: list[dict], used_tables: list[str]) -> str:
    """将列约束转换为提示文本，只包含使用的表"""
    if not column_value_constraints:
        return "无特定列约束"

    constraints = []
    for c in column_value_constraints:
        if c['table_name'] in used_tables:
            constraint = f"表 {c['table_name']} 的列 {c['column']} {c['operator']} '{c['value']}'"
            constraints.append(constraint)
    return "\n".join(constraints) if constraints else "无特定列约束"


def generate_sql(question: str, ddl_list: list[str], column_constraints: str, k: int, model: str = "qwen-plus", verbose: bool = False) -> str:
    """
    调用 DashScope API 生成 SQL 查询

    Args:
        question: 用户问题
        ddl_list: 按顺序拼接的 DDL 列表
        column_constraints: 列约束文本
        k: 使用的表数量
        model: 使用的模型
        verbose: 是否输出中间过程

    Returns:
        生成的 SQL 查询
    """
    # 构建表元数据字符串
    table_metadata_string = "\n\n".join(ddl_list)

    # 构建提示词 - 要求输出可直接执行的完整SQL
    prompt = f"""### Task
Generate an executable SQL query to answer the question. Output ONLY the SQL query, no explanation.

### Question
{question}

### Available Tables (use first {k} table(s))
Use ONLY the following table(s) for this query:
{table_metadata_string}

### Column Constraints
{column_constraints}

### Output Format
Return ONLY the SQL query that can be executed directly. Example:
```sql
SELECT * FROM table_name WHERE condition;
```
No markdown formatting, no explanations. Just pure SQL."""

    if verbose:
        print(f"\n[提示词]\n{prompt[:500]}...")

    # 调用 DashScope API
    response = Generation.call(
        model=model,
        prompt=prompt,
        result_format='message'
    )

    if response.status_code == 200:
        result = response.output['choices'][0]['message']['content'].strip()
        # 提取纯 SQL（去除可能的 markdown 格式）
        result = result.strip()
        if result.startswith('```sql'):
            result = result[6:]
        elif result.startswith('```'):
            result = result[3:]
        if result.endswith('```'):
            result = result[:-3]
        result = result.strip()
        return result
    else:
        raise Exception(f"API 调用失败: {response.message}")


def get_completed_keys(output_file: str) -> set:
    """获取已完成的 (question_id, k) 组合"""
    completed_keys = set()
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        record = json.loads(line)
                        if "id" in record and "k" in record:
                            completed_keys.add((record["id"], record["k"]))
                    except json.JSONDecodeError:
                        continue
    return completed_keys


def main(input_file: str = TABLE_SELECTION_FILE, output_file: str = OUTPUT_FILE,
         model: str = "qwen-plus", verbose: bool = False, resume: bool = True):
    """
    主函数：处理所有问题并生成 SQL

    Args:
        input_file: 表选择结果文件
        output_file: 输出文件
        model: 使用的模型
        verbose: 是否输出详细日志
        resume: 是否启用断点续传
    """
    # 检查 API Key
    if not DASHSCOPE_API_KEY:
        print("错误: 请设置 DASH_SCOPE_API_KEY 环境变量")
        return

    # 加载 DDL 映射
    print("加载 DDL 映射...")
    ddl_mapping = load_ddl_mapping()
    print(f"已加载 {len(ddl_mapping)} 个表的 DDL")

    # 断点续传
    completed_keys = get_completed_keys(output_file) if resume and os.path.exists(output_file) else set()
    if resume and completed_keys:
        print(f"[断点续传] 检测到已完成 {len(completed_keys)} 个结果，将跳过")

    # 读取表选择结果
    with open(input_file, 'r', encoding='utf-8') as f:
        selections = [json.loads(line.strip()) for line in f if line.strip()]

    total = len(selections)
    total_tasks = total * MAX_K
    new_count = 0
    error_count = 0
    task_num = 0

    for i, selection in enumerate(selections):
        qid = selection.get("id")
        question = selection.get("question", "")
        top_k_tables = selection.get("top_k_tables", [])
        column_constraints_list = selection.get("column_value_constraints", [])

        # 跳过有错误的问题
        if "error" in selection:
            print(f"[{i+1}/{total}] 跳过 (错误): {question[:50]}...")
            continue

        print(f"[{i+1}/{total}] 处理: {question[:50]}...")

        # 从 k=1 到 k=MAX_K 依次生成 SQL
        for k in range(1, MAX_K + 1):
            task_num += 1
            
            # 跳过已完成的任务
            if resume and (qid, k) in completed_keys:
                continue

            print(f"  k={k}/{MAX_K}...", end=" ")

            # 获取前 k 个表的 DDL
            ddl_list = []
            used_tables = top_k_tables[:k]
            for table_name in used_tables:
                if table_name in ddl_mapping:
                    ddl_list.append(ddl_mapping[table_name])

            # 构建列约束文本
            column_constraints_text = build_column_constraints_text(column_constraints_list, used_tables)

            result = {
                "id": qid,
                "question": question,
                "k": k,
                "used_tables": used_tables
            }

            try:
                sql = generate_sql(question, ddl_list, column_constraints_text, k, model=model, verbose=verbose)
                # 清理 SQL 中的换行符，替换为空格
                sql = sql.replace('\n', ' ').replace('\r', ' ')
                # 清理多余空格
                sql = ' '.join(sql.split())
                result["generated_sql"] = sql
                new_count += 1
                print("成功")
                # 保存结果
                with open(output_file, 'a', encoding='utf-8') as f_out:
                    f_out.write(json.dumps(result, ensure_ascii=False) + '\n')
            except Exception as e:
                error_count += 1
                print(f"错误: {e}")

    print(f"\n完成！共 {total} 个问题 x {MAX_K} k值 = {total_tasks} 个任务")
    print(f"新增 {new_count} 个，错误 {error_count} 个")
    print(f"结果保存到: {output_file}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="使用 DashScope (千问) API 生成 SQL 查询")
    parser.add_argument("--model", default="qwen-max", help="使用的模型")
    parser.add_argument("--verbose", action="store_true", help="输出详细日志")
    parser.add_argument("--no-resume", action="store_true", help="禁用断点续传")
    parser.add_argument("--max-k", type=int, default=8, help="最大 k 值")
    args = parser.parse_args()
    
    MAX_K = args.max_k

    main(model=args.model, verbose=args.verbose, resume=not args.no_resume)
