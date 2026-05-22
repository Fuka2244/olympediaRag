"""
向量检索结果HIT@k评估脚本
评估SPLADE向量检索结果与标准答案的HIT@k指标
"""
import os
import sys
import json
import re
from collections import defaultdict
from loguru import logger
from typing import Dict, List, Set, Tuple

# ============================================================================
# 文件路径配置
# ============================================================================

QUESTIONS_FILE = "D:/Projects/pythonProject/question/olympedia_questions.jsonl"
RETRIEVAL_RESULTS_FILE = "D:/Projects/pythonProject/retrival_result/olympedia_questions_splade_results.jsonl"
OUTPUT_DIR = "D:/Projects/pythonProject/retrival_result/evaluate"

# ============================================================================
# 评估参数配置
# ============================================================================

# 输出文件名
HIT_AT_K_RESULTS_FILE = "hit_at_k_results.json"
HIT_QUESTIONS_FILE = "hit_questions.jsonl"
HIT_REPORT_FILE = "hit_at_k_report.txt"

# HIT@k的k值列表
K_VALUES = [1, 5, 10, 25]

# 内容类型
CONTENT_TYPES = ["text", "infobox", "table"]

# ============================================================================
# 答案匹配配置
# ============================================================================

# 是否进行模糊匹配
FUZZY_MATCH = True

# 模糊匹配的相似度阈值（0-1）
SIMILARITY_THRESHOLD = 0.8

# ============================================================================
# 辅助函数
# ============================================================================

def normalize_name(name: str) -> str:
    """
    标准化姓名，用于匹配
    
    Args:
        name: 原始姓名
    
    Returns:
        标准化后的姓名
    """
    if not name:
        return ""
    
    # 转换为小写
    name = name.lower().strip()
    
    # 移除特殊字符和多余空格
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', ' ', name)
    
    return name


def fuzzy_match(name1: str, name2: str, threshold: float = SIMILARITY_THRESHOLD) -> bool:
    """
    模糊匹配两个姓名
    
    Args:
        name1: 第一个姓名
        name2: 第二个姓名
        threshold: 相似度阈值
    
    Returns:
        是否匹配
    """
    name1_norm = normalize_name(name1)
    name2_norm = normalize_name(name2)
    
    # 完全匹配
    if name1_norm == name2_norm:
        return True
    
    # 包含匹配
    if name1_norm in name2_norm or name2_norm in name1_norm:
        return True
    
    # 简单的相似度计算（基于共同字符）
    if FUZZY_MATCH:
        chars1 = set(name1_norm.replace(' ', ''))
        chars2 = set(name2_norm.replace(' ', ''))
        
        if not chars1 or not chars2:
            return False
        
        intersection = chars1 & chars2
        union = chars1 | chars2
        
        similarity = len(intersection) / len(union)
        
        return similarity >= threshold
    
    return False


def extract_names_from_content(content: dict, content_type: str) -> Set[str]:
    """
    从检索结果的content中提取姓名
    
    Args:
        content: 检索结果的content字段
        content_type: 内容类型（text/infobox/table）
    
    Returns:
        提取的姓名集合
    """
    names = set()
    
    if content_type == "text":
        # 从文本中提取姓名
        text = content.get("text", "")
        if text:
            # 使用正则表达式提取可能的姓名
            # 假设姓名首字母大写，由2-3个单词组成
            name_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2}\b'
            potential_names = re.findall(name_pattern, text)
            
            for name in potential_names:
                cleaned_name = name.strip()
                if cleaned_name and len(cleaned_name.split()) >= 2:
                    names.add(cleaned_name)
    
    elif content_type == "infobox":
        # 从infobox的键值对中提取姓名
        for key, value in content.items():
            if isinstance(value, str):
                # 检查键名是否包含姓名相关关键词
                if any(keyword in key.lower() for keyword in ['name', 'athlete', 'competitor', 'gold', 'silver', 'bronze', 'winner']):
                    cleaned_name = value.strip()
                    if cleaned_name and cleaned_name.lower() not in ['null', 'none', 'n/a', '-']:
                        names.add(cleaned_name)
    
    elif content_type == "table":
        # 从表格数据中提取姓名
        for key, value in content.items():
            if isinstance(value, str):
                # 检查键名或值是否包含姓名相关关键词
                if any(keyword in key.lower() for keyword in ['name', 'athlete', 'competitor', 'gold', 'silver', 'bronze', 'winner']):
                    cleaned_name = value.strip()
                    if cleaned_name and cleaned_name.lower() not in ['null', 'none', 'n/a', '-']:
                        names.add(cleaned_name)
    
    return names


def extract_names_from_linearized(linearized: str) -> Set[str]:
    """
    从线性化文本中提取姓名
    
    Args:
        linearized: 线性化文本
    
    Returns:
        提取的姓名集合
    """
    names = set()
    
    if not linearized:
        return names
    
    # 使用正则表达式提取可能的姓名
    name_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2}\b'
    potential_names = re.findall(name_pattern, linearized)
    
    for name in potential_names:
        cleaned_name = name.strip()
        if cleaned_name and len(cleaned_name.split()) >= 2:
            names.add(cleaned_name)
    
    return names


# ============================================================================
# 数据加载函数
# ============================================================================

def load_questions(file_path: str) -> Dict[int, Dict]:
    """
    加载问题文件
    
    Args:
        file_path: 问题文件路径
    
    Returns:
        问题字典 {id: question_data}
    """
    logger.info(f"从 {file_path} 加载问题")
    
    questions = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data = json.loads(line.strip())
                question_id = data.get('id')
                if question_id:
                    questions[question_id] = data
    
    logger.info(f"✓ 加载了 {len(questions)} 个问题")
    return questions


def load_retrieval_results(file_path: str) -> Dict[int, Dict]:
    """
    加载向量检索结果
    
    Args:
        file_path: 检索结果文件路径
    
    Returns:
        检索结果字典 {question_id: retrieval_data}
    """
    logger.info(f"从 {file_path} 加载检索结果")
    
    results = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data = json.loads(line.strip())
                question_id = data.get('id')
                if question_id:
                    results[question_id] = data
    
    logger.info(f"✓ 加载了 {len(results)} 个问题的检索结果")
    return results


# ============================================================================
# HIT@k评估函数
# ============================================================================

def evaluate_hit_at_k_for_question(question_data: Dict, 
                                  retrieval_data: Dict,
                                  k_values: List[int],
                                  content_types: List[str]) -> Dict:
    """
    评估单个问题的HIT@k
    
    Args:
        question_data: 问题数据（包含正确答案）
        retrieval_data: 检索结果数据
        k_values: 要评估的k值列表
        content_types: 要评估的内容类型列表
    
    Returns:
        HIT@k评估结果
    """
    question_id = question_data.get('id')
    correct_answers = question_data.get('answer', [])
    
    if not correct_answers:
        return {
            'question_id': question_id,
            'has_answers': False,
            'hit_at_k': {k: False for k in k_values},
            'hit_at_k_by_type': {ct: {k: False for k in k_values} for ct in content_types}
        }
    
    retrieval_results = retrieval_data.get('retrieval_results', {})
    
    # 存储每个内容类型在每个k值下的命中情况
    hit_at_k_by_type = {ct: {k: False for k in k_values} for ct in content_types}
    
    # 存储每个内容类型在每个k值下提取的姓名
    extracted_names_by_type = {ct: {k: [] for k in k_values} for ct in content_types}
    
    # 存储每个内容类型在每个k值下匹配的答案
    matched_answers_by_type = {ct: {k: [] for k in k_values} for ct in content_types}
    
    # 遍历每个内容类型
    for content_type in content_types:
        type_results = retrieval_results.get(content_type, {})
        
        if type_results.get('status') != 'success':
            continue
        
        results_list = type_results.get('results', [])
        
        # 遍历每个k值
        for k in k_values:
            top_k_results = results_list[:k]
            
            # 从top k结果中提取所有姓名
            all_names = set()
            
            for result in top_k_results:
                # 从content中提取姓名
                content = result.get('content', {})
                names_from_content = extract_names_from_content(content, content_type)
                all_names.update(names_from_content)
                
                # 从linearized中提取姓名
                linearized = result.get('linearized', '')
                names_from_linearized = extract_names_from_linearized(linearized)
                all_names.update(names_from_linearized)
            
            # 将set转换为list以便JSON序列化
            extracted_names_by_type[content_type][k] = list(all_names)
            
            # 检查每个正确答案是否被匹配
            matched_answers = []
            
            for correct_answer in correct_answers:
                is_matched = False
                
                for extracted_name in all_names:
                    if fuzzy_match(correct_answer, extracted_name):
                        is_matched = True
                        matched_answers.append({
                            'correct_answer': correct_answer,
                            'matched_with': extracted_name
                        })
                        break
            
            matched_answers_by_type[content_type][k] = matched_answers
            
            # 如果所有正确答案都被匹配，则命中
            if len(matched_answers) == len(correct_answers):
                hit_at_k_by_type[content_type][k] = True
    
    # 计算总体HIT@k（任一内容类型命中即算命中）
    hit_at_k = {k: False for k in k_values}
    
    for k in k_values:
        # 任一内容类型命中即算命中
        for content_type in content_types:
            if hit_at_k_by_type[content_type][k]:
                hit_at_k[k] = True
                break
    
    return {
        'question_id': question_id,
        'question': question_data.get('question', ''),
        'correct_answers': correct_answers,
        'has_answers': len(correct_answers) > 0,
        'hit_at_k': hit_at_k,
        'hit_at_k_by_type': hit_at_k_by_type,
        'extracted_names_by_type': extracted_names_by_type,
        'matched_answers_by_type': matched_answers_by_type
    }


def evaluate_all_hit_at_k(questions: Dict[int, Dict],
                         retrieval_results: Dict[int, Dict],
                         k_values: List[int],
                         content_types: List[str]) -> Dict:
    """
    评估所有问题的HIT@k
    
    Args:
        questions: 问题字典
        retrieval_results: 检索结果字典
        k_values: 要评估的k值列表
        content_types: 要评估的内容类型列表
    
    Returns:
        HIT@k评估结果
    """
    logger.info("开始评估HIT@k")
    
    # 统计结果
    hit_statistics = {
        'total_questions': len(questions),
        'questions_with_answers': 0,
        'hit_at_k': {k: {'hit_count': 0, 'total_count': 0, 'hit_rate': 0.0} for k in k_values},
        'hit_at_k_by_type': {
            ct: {k: {'hit_count': 0, 'total_count': 0, 'hit_rate': 0.0} for k in k_values}
            for ct in content_types
        },
        'question_details': []
    }
    
    # 详细评估结果
    detailed_results = []
    
    # 遍历每个问题
    for question_id, question_data in questions.items():
        if question_id not in retrieval_results:
            logger.warning(f"问题 {question_id} 没有检索结果")
            continue
        
        retrieval_data = retrieval_results[question_id]
        
        # 评估单个问题
        evaluation = evaluate_hit_at_k_for_question(
            question_data, retrieval_data, k_values, content_types
        )
        
        # 更新统计
        if evaluation['has_answers']:
            hit_statistics['questions_with_answers'] += 1
            
            # 更新总体HIT@k统计
            for k in k_values:
                hit_statistics['hit_at_k'][k]['total_count'] += 1
                if evaluation['hit_at_k'][k]:
                    hit_statistics['hit_at_k'][k]['hit_count'] += 1
            
            # 更新按内容类型的HIT@k统计
            for content_type in content_types:
                for k in k_values:
                    hit_statistics['hit_at_k_by_type'][content_type][k]['total_count'] += 1
                    if evaluation['hit_at_k_by_type'][content_type][k]:
                        hit_statistics['hit_at_k_by_type'][content_type][k]['hit_count'] += 1
        
        # 保存详细信息
        hit_statistics['question_details'].append(evaluation)
        detailed_results.append(evaluation)
    
    # 计算命中率
    for k in k_values:
        total = hit_statistics['hit_at_k'][k]['total_count']
        hit_count = hit_statistics['hit_at_k'][k]['hit_count']
        hit_statistics['hit_at_k'][k]['hit_rate'] = hit_count / total if total > 0 else 0.0
    
    for content_type in content_types:
        for k in k_values:
            total = hit_statistics['hit_at_k_by_type'][content_type][k]['total_count']
            hit_count = hit_statistics['hit_at_k_by_type'][content_type][k]['hit_count']
            hit_statistics['hit_at_k_by_type'][content_type][k]['hit_rate'] = hit_count / total if total > 0 else 0.0
    
    logger.info("✓ HIT@k评估完成")
    
    return {
        'hit_statistics': hit_statistics,
        'detailed_results': detailed_results
    }


# ============================================================================
# 结果保存函数
# ============================================================================

def save_hit_at_k_results(hit_results: Dict, output_dir: str):
    """
    保存HIT@k评估结果
    
    Args:
        hit_results: HIT@k评估结果
        output_dir: 输出目录
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存JSON格式结果
    json_file = os.path.join(output_dir, HIT_AT_K_RESULTS_FILE)
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(hit_results, f, indent=2, ensure_ascii=False)
    logger.info(f"✓ HIT@k结果保存到: {json_file}")
    
    # 保存命中了的问题
    hit_file = os.path.join(output_dir, HIT_QUESTIONS_FILE)
    save_hit_questions(hit_results, hit_file)
    
    # 生成HIT@k报告
    report_file = os.path.join(output_dir, HIT_REPORT_FILE)
    generate_hit_at_k_report(hit_results, report_file)
    logger.info(f"✓ HIT@k报告保存到: {report_file}")


def save_hit_questions(hit_results: Dict, output_file: str):
    """
    保存命中了的问题到单独的文件
    
    Args:
        hit_results: HIT@k评估结果
        output_file: 输出文件路径
    """
    hit_questions = []
    
    # 从详细结果中提取命中的问题
    for result in hit_results['detailed_results']:
        if not result['has_answers']:
            continue
        
        # 检查是否在任何k值下命中
        hit_any_k = any(result['hit_at_k'].values())
        
        if hit_any_k:
            hit_questions.append({
                'question_id': result['question_id'],
                'question': result['question'],
                'correct_answers': result['correct_answers'],
                'hit_at_k': result['hit_at_k'],
                'hit_at_k_by_type': result['hit_at_k_by_type'],
                'matched_answers_by_type': result['matched_answers_by_type']
            })
    
    # 保存到JSONL文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for question in hit_questions:
            f.write(json.dumps(question, ensure_ascii=False) + '\n')
    
    logger.info(f"✓ 命中问题保存到: {output_file} (共 {len(hit_questions)} 条)")


def generate_hit_at_k_report(hit_results: Dict, output_file: str):
    """
    生成HIT@k报告
    
    Args:
        hit_results: HIT@k评估结果
        output_file: 输出文件路径
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("向量检索结果HIT@k评估报告\n")
        f.write("=" * 80 + "\n\n")
        
        stats = hit_results['hit_statistics']
        
        f.write("总体统计\n")
        f.write("-" * 80 + "\n")
        f.write(f"总问题数: {stats['total_questions']}\n")
        f.write(f"有答案的问题数: {stats['questions_with_answers']}\n")
        f.write("\n")
        
        f.write("总体HIT@k结果\n")
        f.write("-" * 80 + "\n")
        
        for k in sorted(stats['hit_at_k'].keys()):
            k_stats = stats['hit_at_k'][k]
            f.write(f"HIT@{k}:\n")
            f.write(f"  命中数: {k_stats['hit_count']}\n")
            f.write(f"  总数: {k_stats['total_count']}\n")
            f.write(f"  命中率: {k_stats['hit_rate']:.2%}\n")
            f.write("\n")
        
        f.write("=" * 80 + "\n")
        f.write("按内容类型的HIT@k结果\n")
        f.write("=" * 80 + "\n\n")
        
        for content_type in CONTENT_TYPES:
            f.write(f"{content_type.upper()}:\n")
            f.write("-" * 80 + "\n")
            
            for k in sorted(stats['hit_at_k_by_type'][content_type].keys()):
                k_stats = stats['hit_at_k_by_type'][content_type][k]
                f.write(f"  HIT@{k}: {k_stats['hit_count']}/{k_stats['total_count']} ({k_stats['hit_rate']:.2%})\n")
            
            f.write("\n")
        
        f.write("=" * 80 + "\n")


# ============================================================================
# 主函数
# ============================================================================

def main():
    """主函数"""
    # 配置日志
    logger.remove()
    logger.add(sys.stdout, level="INFO")
    
    logger.info("=" * 80)
    logger.info("向量检索结果HIT@k评估")
    logger.info("=" * 80)
    
    # 加载数据
    questions = load_questions(QUESTIONS_FILE)
    retrieval_results = load_retrieval_results(RETRIEVAL_RESULTS_FILE)
    
    if not questions:
        logger.error("✗ 没有加载到问题数据")
        return
    
    if not retrieval_results:
        logger.error("✗ 没有加载到检索结果")
        return
    
    # 评估HIT@k
    hit_results = evaluate_all_hit_at_k(
        questions, retrieval_results, K_VALUES, CONTENT_TYPES
    )
    
    # 保存结果
    save_hit_at_k_results(hit_results, OUTPUT_DIR)
    
    # 打印总结
    logger.info("=" * 80)
    logger.info("HIT@k评估总结")
    logger.info("=" * 80)
    
    stats = hit_results['hit_statistics']
    
    logger.info(f"总问题数: {stats['total_questions']}")
    logger.info(f"有答案的问题数: {stats['questions_with_answers']}")
    logger.info("")
    
    logger.info("总体HIT@k结果:")
    for k in sorted(stats['hit_at_k'].keys()):
        k_stats = stats['hit_at_k'][k]
        logger.info(f"  HIT@{k}: {k_stats['hit_count']}/{k_stats['total_count']} ({k_stats['hit_rate']:.2%})")
    
    logger.info("")
    logger.info("按内容类型的HIT@k结果:")
    for content_type in CONTENT_TYPES:
        logger.info(f"  {content_type.upper()}:")
        for k in sorted(stats['hit_at_k_by_type'][content_type].keys()):
            k_stats = stats['hit_at_k_by_type'][content_type][k]
            logger.info(f"    HIT@{k}: {k_stats['hit_count']}/{k_stats['total_count']} ({k_stats['hit_rate']:.2%})")
    
    logger.info("=" * 80)


if __name__ == "__main__":
    """
    使用方法:
        python evaluate_hit_at_k.py
    """
    main()