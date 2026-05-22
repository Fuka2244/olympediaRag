"""
SQL执行结果评估脚本
评估SQL执行结果是否覆盖了正确答案，并统计不同k值的覆盖率
"""
import os
import sys
import json
import re
from collections import defaultdict
from loguru import logger
from typing import Dict, List, Set, Tuple

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# ============================================================================
# 文件路径配置
# ============================================================================

QUESTIONS_FILE = "D:/Projects/pythonProject/question/olympedia_questions.jsonl"
SQL_EXECUTION_RESULTS = "D:/Projects/pythonProject/mysql_retrival/results/sql_execution_results.jsonl"
OUTPUT_DIR = "D:/Projects/pythonProject/mysql_retrival/evaluate"

# ============================================================================
# 评估参数配置
# ============================================================================

# 输出文件名
EVALUATION_RESULT_FILE = "evaluation_results.json"
COVERAGE_REPORT_FILE = "coverage_report.txt"
DETAILED_REPORT_FILE = "detailed_report.jsonl"
COVERED_QUESTIONS_FILE = "covered_questions.jsonl"

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


def extract_names_from_results(results: List[Dict]) -> Set[str]:
    """
    从SQL执行结果中提取姓名
    
    Args:
        results: SQL执行结果列表
    
    Returns:
        提取的姓名集合
    """
    names = set()
    
    for result in results:
        # 遍历结果中的所有字段
        for key, value in result.items():
            if value and isinstance(value, str):
                # 尝试提取姓名（假设姓名字段包含name, athlete, competitor等关键词）
                if any(keyword in key.lower() for keyword in ['name', 'athlete', 'competitor', 'gold', 'silver', 'bronze']):
                    # 清理姓名
                    cleaned_name = value.strip()
                    if cleaned_name and cleaned_name.lower() not in ['null', 'none', 'n/a']:
                        names.add(cleaned_name)
            elif value and isinstance(value, (int, float)):
                # 数字可能是ID，不是姓名，跳过
                continue
    
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


def load_sql_execution_results(file_path: str) -> Dict[int, Dict[int, Dict]]:
    """
    加载SQL执行结果
    
    Args:
        file_path: SQL执行结果文件路径
    
    Returns:
        执行结果字典 {question_id: {k: execution_result}}
    """
    logger.info(f"从 {file_path} 加载SQL执行结果")
    
    results = defaultdict(dict)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data = json.loads(line.strip())
                question_id = data['input'].get('id')
                k_value = data['input'].get('k')
                
                if question_id and k_value is not None:
                    results[question_id][k_value] = data
    
    logger.info(f"✓ 加载了 {len(results)} 个问题的执行结果")
    return results


# ============================================================================
# 评估函数
# ============================================================================

def evaluate_single_result(question_data: Dict, execution_result: Dict) -> Dict:
    """
    评估单个SQL执行结果
    
    Args:
        question_data: 问题数据（包含正确答案）
        execution_result: SQL执行结果
    
    Returns:
        评估结果
    """
    question_id = question_data.get('id')
    correct_answers = question_data.get('answer', [])
    
    # 获取SQL执行结果
    output = execution_result.get('output', {})
    success = output.get('success', False)
    sql_results = output.get('results', [])
    
    # 如果SQL执行失败，直接返回未覆盖
    if not success or not sql_results:
        return {
            'question_id': question_id,
            'covered': False,
            'covered_answers': [],
            'missing_answers': correct_answers,
            'extracted_names': [],
            'execution_success': False,
            'row_count': 0
        }
    
    # 从执行结果中提取姓名
    extracted_names = extract_names_from_results(sql_results)
    
    # 检查每个正确答案是否被覆盖
    covered_answers = []
    missing_answers = []
    
    for correct_answer in correct_answers:
        is_covered = False
        
        for extracted_name in extracted_names:
            if fuzzy_match(correct_answer, extracted_name):
                is_covered = True
                covered_answers.append({
                    'correct_answer': correct_answer,
                    'matched_with': extracted_name
                })
                break
        
        if not is_covered:
            missing_answers.append(correct_answer)
    
    # 判断是否完全覆盖
    covered = len(missing_answers) == 0
    
    return {
        'question_id': question_id,
        'covered': covered,
        'covered_answers': covered_answers,
        'missing_answers': missing_answers,
        'extracted_names': list(extracted_names),
        'execution_success': success,
        'row_count': len(sql_results)
    }


def evaluate_all_results(questions: Dict[int, Dict], 
                        execution_results: Dict[int, Dict[int, Dict]]) -> Dict:
    """
    评估所有SQL执行结果
    
    Args:
        questions: 问题字典
        execution_results: SQL执行结果字典
    
    Returns:
        评估结果
    """
    logger.info("开始评估所有SQL执行结果")
    
    # 按k值分组统计
    k_statistics = defaultdict(lambda: {
        'total_questions': 0,
        'covered_questions': 0,
        'failed_questions': 0,
        'question_details': []
    })
    
    # 详细评估结果
    detailed_results = []
    
    # 遍历每个问题
    for question_id, question_data in questions.items():
        if question_id not in execution_results:
            logger.warning(f"问题 {question_id} 没有执行结果")
            continue
        
        question_results = execution_results[question_id]
        
        # 遍历每个k值
        for k_value, execution_result in question_results.items():
            # 评估单个结果
            evaluation = evaluate_single_result(question_data, execution_result)
            
            # 更新统计
            k_statistics[k_value]['total_questions'] += 1
            
            if evaluation['execution_success']:
                if evaluation['covered']:
                    k_statistics[k_value]['covered_questions'] += 1
            else:
                k_statistics[k_value]['failed_questions'] += 1
            
            # 保存详细信息
            k_statistics[k_value]['question_details'].append({
                'question_id': question_id,
                'question': question_data.get('question', ''),
                'k': k_value,
                'evaluation': evaluation
            })
            
            # 保存详细结果
            detailed_results.append({
                'question_id': question_id,
                'question': question_data.get('question', ''),
                'correct_answers': question_data.get('answer', []),
                'k': k_value,
                'evaluation': evaluation,
                'sql': execution_result['input'].get('generated_sql', ''),
                'used_tables': execution_result['input'].get('used_tables', [])
            })
    
    # 计算覆盖率
    for k_value, stats in k_statistics.items():
        if stats['total_questions'] > 0:
            stats['coverage_rate'] = stats['covered_questions'] / stats['total_questions']
            stats['success_rate'] = (stats['total_questions'] - stats['failed_questions']) / stats['total_questions']
        else:
            stats['coverage_rate'] = 0.0
            stats['success_rate'] = 0.0
    
    logger.info("✓ 评估完成")
    
    return {
        'k_statistics': dict(k_statistics),
        'detailed_results': detailed_results
    }


# ============================================================================
# 结果保存函数
# ============================================================================

def save_evaluation_results(evaluation_results: Dict, output_dir: str):
    """
    保存评估结果
    
    Args:
        evaluation_results: 评估结果
        output_dir: 输出目录
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存JSON格式结果
    json_file = os.path.join(output_dir, EVALUATION_RESULT_FILE)
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(evaluation_results, f, indent=2, ensure_ascii=False)
    logger.info(f"✓ 评估结果保存到: {json_file}")
    
    # 保存详细报告
    detailed_file = os.path.join(output_dir, DETAILED_REPORT_FILE)
    with open(detailed_file, 'w', encoding='utf-8') as f:
        for result in evaluation_results['detailed_results']:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')
    logger.info(f"✓ 详细报告保存到: {detailed_file}")
    
    # 保存覆盖的问题
    covered_file = os.path.join(output_dir, COVERED_QUESTIONS_FILE)
    save_covered_questions(evaluation_results, covered_file)
    
    # 生成覆盖率报告
    report_file = os.path.join(output_dir, COVERAGE_REPORT_FILE)
    generate_coverage_report(evaluation_results, report_file)
    logger.info(f"✓ 覆盖率报告保存到: {report_file}")


def save_covered_questions(evaluation_results: Dict, output_file: str):
    """
    保存覆盖的问题到单独的文件
    
    Args:
        evaluation_results: 评估结果
        output_file: 输出文件路径
    """
    covered_questions = []
    
    # 从详细结果中提取覆盖的问题
    for result in evaluation_results['detailed_results']:
        evaluation = result['evaluation']
        
        # 只保存执行成功且覆盖了答案的问题
        if evaluation['execution_success'] and evaluation['covered']:
            covered_questions.append({
                'question_id': result['question_id'],
                'question': result['question'],
                'correct_answers': result['correct_answers'],
                'k': result['k'],
                'covered_answers': evaluation['covered_answers'],
                'extracted_names': evaluation['extracted_names'],
                'row_count': evaluation['row_count'],
                'sql': result['sql'],
                'used_tables': result['used_tables']
            })
    
    # 保存到JSONL文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for question in covered_questions:
            f.write(json.dumps(question, ensure_ascii=False) + '\n')
    
    logger.info(f"✓ 覆盖问题保存到: {output_file} (共 {len(covered_questions)} 条)")


def generate_coverage_report(evaluation_results: Dict, output_file: str):
    """
    生成覆盖率报告
    
    Args:
        evaluation_results: 评估结果
        output_file: 输出文件路径
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("SQL执行结果覆盖率评估报告\n")
        f.write("=" * 80 + "\n\n")
        
        k_statistics = evaluation_results['k_statistics']
        
        # 按k值排序
        sorted_k_values = sorted(k_statistics.keys())
        
        f.write("总体统计\n")
        f.write("-" * 80 + "\n\n")
        
        for k_value in sorted_k_values:
            stats = k_statistics[k_value]
            f.write(f"K = {k_value}:\n")
            f.write(f"  总问题数: {stats['total_questions']}\n")
            f.write(f"  覆盖问题数: {stats['covered_questions']}\n")
            f.write(f"  执行失败数: {stats['failed_questions']}\n")
            f.write(f"  覆盖率: {stats['coverage_rate']:.2%}\n")
            f.write(f"  执行成功率: {stats['success_rate']:.2%}\n")
            f.write("\n")
        
        f.write("=" * 80 + "\n")
        f.write("详细问题分析\n")
        f.write("=" * 80 + "\n\n")
        
        for k_value in sorted_k_values:
            stats = k_statistics[k_value]
            f.write(f"K = {k_value} 详细分析:\n")
            f.write("-" * 80 + "\n")
            
            for detail in stats['question_details']:
                question_id = detail['question_id']
                question = detail['question']
                evaluation = detail['evaluation']
                
                f.write(f"问题ID: {question_id}\n")
                f.write(f"问题: {question}\n")
                f.write(f"执行成功: {'是' if evaluation['execution_success'] else '否'}\n")
                
                if evaluation['execution_success']:
                    f.write(f"答案覆盖: {'是' if evaluation['covered'] else '否'}\n")
                    f.write(f"提取的姓名: {', '.join(evaluation['extracted_names'][:5])}...\n")
                    
                    if evaluation['covered_answers']:
                        f.write(f"覆盖的答案: {', '.join([a['correct_answer'] for a in evaluation['covered_answers']])}\n")
                    
                    if evaluation['missing_answers']:
                        f.write(f"未覆盖的答案: {', '.join(evaluation['missing_answers'])}\n")
                else:
                    f.write(f"执行失败\n")
                
                f.write("\n")
            
            f.write("\n")


# ============================================================================
# 主函数
# ============================================================================

def main():
    """主函数"""
    # 配置日志
    logger.remove()
    logger.add(sys.stdout, level="INFO")
    
    logger.info("=" * 80)
    logger.info("SQL执行结果覆盖率评估")
    logger.info("=" * 80)
    
    # 加载数据
    questions = load_questions(QUESTIONS_FILE)
    execution_results = load_sql_execution_results(SQL_EXECUTION_RESULTS)
    
    if not questions:
        logger.error("✗ 没有加载到问题数据")
        return
    
    if not execution_results:
        logger.error("✗ 没有加载到SQL执行结果")
        return
    
    # 评估结果
    evaluation_results = evaluate_all_results(questions, execution_results)
    
    # 保存结果
    save_evaluation_results(evaluation_results, OUTPUT_DIR)
    
    # 打印总结
    logger.info("=" * 80)
    logger.info("评估总结")
    logger.info("=" * 80)
    
    k_statistics = evaluation_results['k_statistics']
    sorted_k_values = sorted(k_statistics.keys())
    
    for k_value in sorted_k_values:
        stats = k_statistics[k_value]
        logger.info(f"K = {k_value}:")
        logger.info(f"  总问题数: {stats['total_questions']}")
        logger.info(f"  覆盖问题数: {stats['covered_questions']}")
        logger.info(f"  覆盖率: {stats['coverage_rate']:.2%}")
        logger.info("")
    
    logger.info("=" * 80)


if __name__ == "__main__":
    """
    使用方法:
        python evaluate_coverage.py
    """
    main()