"""
JSON 和 JSONL 格式互转工具
"""
import json
import os
from typing import Optional


def json_to_jsonl(json_path: str, jsonl_path: Optional[str] = None) -> int:
    """
    将 JSON 数组格式转换为 JSONL 格式。

    Args:
        json_path: JSON 文件路径（数组格式）
        jsonl_path: 输出 JSONL 文件路径，默认为同目录下同名 .jsonl 文件

    Returns:
        转换的记录数
    """
    if jsonl_path is None:
        jsonl_path = json_path.rsplit(".json", 1)[0] + ".jsonl"

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(jsonl_path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"Converted {len(data)} records: {json_path} -> {jsonl_path}")
    return len(data)


def jsonl_to_json(jsonl_path: str, json_path: Optional[str] = None) -> int:
    """
    将 JSONL 格式转换为 JSON 数组格式。

    Args:
        jsonl_path: JSONL 文件路径
        json_path: 输出 JSON 文件路径，默认为同目录下同名 .json 文件

    Returns:
        转换的记录数
    """
    if json_path is None:
        json_path = jsonl_path.rsplit(".jsonl", 1)[0] + ".json"

    data = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Converted {len(data)} records: {jsonl_path} -> {json_path}")
    return len(data)


def batch_json_to_jsonl(input_dir: str, output_dir: Optional[str] = None) -> int:
    """
    批量转换目录下所有 JSON 文件为 JSONL。

    Args:
        input_dir: 输入目录
        output_dir: 输出目录，默认为同输入目录

    Returns:
        转换的文件数
    """
    if output_dir is None:
        output_dir = input_dir
    else:
        os.makedirs(output_dir, exist_ok=True)

    count = 0
    for filename in os.listdir(input_dir):
        if filename.endswith(".json") and not filename.endswith(".jsonl"):
            json_path = os.path.join(input_dir, filename)
            jsonl_path = os.path.join(output_dir, filename[:-5] + ".jsonl")
            json_to_jsonl(json_path, jsonl_path)
            count += 1

    print(f"Batch converted {count} files")
    return count


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="JSON/JSONL 格式互转")
    parser.add_argument("input", help="输入文件路径或目录")
    parser.add_argument("-o", "--output", help="输出文件路径或目录")
    parser.add_argument("-m", "--mode", choices=["json2jsonl", "jsonl2json", "batch"],
                        default="json2jsonl", help="转换模式")

    args = parser.parse_args()

    if args.mode == "batch" or os.path.isdir(args.input):
        batch_json_to_jsonl(args.input, args.output)
    elif args.mode == "json2jsonl":
        json_to_jsonl(args.input, args.output)
    elif args.mode == "jsonl2json":
        jsonl_to_json(args.input, args.output)
