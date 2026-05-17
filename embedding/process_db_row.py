import json
"""
    将表schema_summary描述转换为embedding用文本
"""

def build_table_text(table):
    """
    将单个表schema转换为embedding用文本
    """
    table_name = table.get("table_name", "")
    category = table.get("category", "")
    description = table.get("description", "")
    keywords = table.get("keywords", [])

    # keywords拼接
    keywords_str = ", ".join(keywords)

    # 构造最终文本（推荐格式）
    text = f"""

Description: {description}
Table name: {table_name}
Category: {category}
Keywords: {keywords_str}
"""
    return text.strip()


def process_json_to_texts(json_path):
    """
    读取JSON并转换为文本列表
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = []

    for table in data:
        table_text = build_table_text(table)
        results.append({
            "table_name": table["table_name"],
            "text": table_text
        })

    return results


def save_texts_to_file(results, output_path):
    """
    保存为jsonl（推荐，方便向量化）
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in results:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    input_path = "../sql/description/tables_summary.json"  # 你的原始JSON
    output_path = "../sql/description/schema_texts.jsonl"

    results = process_json_to_texts(input_path)
    save_texts_to_file(results, output_path)

    print(f"处理完成，共 {len(results)} 张表")