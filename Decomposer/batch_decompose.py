import json
import os
import time
from decomposer import decomposer

def load_olympedia_questions(file_path):
    questions = []
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    questions.append(json.loads(line))
    return questions

def process_question(item, index, total):
    question_id = item.get('id', index)
    question_text = item.get('question', '')
    
    print(f"[{index + 1}/{total}] Processing ID {question_id}: {question_text[:50]}...")
    
    try:
        result = decomposer(question_text)
        return {
            "id": question_id,
            "original_question": result.get('original_question', question_text),
            "category": item.get('category', ''),
            "answer": item.get('answer', []),
            "source": item.get('source', ''),
            "sub_questions": result.get('sub_questions', []),
            "combination": result.get('combination', {})
        }
    except Exception as e:
        print(f"  Error: {e}")
        return {
            "id": question_id,
            "original_question": question_text,
            "category": item.get('category', ''),
            "answer": item.get('answer', []),
            "source": item.get('source', ''),
            "sub_questions": [],
            "combination": {"type": "parallel", "description": f"Error: {str(e)}", "dependencies": []}
        }

def batch_decompose(input_file, output_file, isTest=False):
    print("=" * 60)
    print("批量问题分解器 (Olympedia Questions)")
    print("=" * 60)
    
    questions = load_olympedia_questions(input_file)
    total_questions = len(questions)
    
    if isTest:
        end_index = min(5, total_questions)
        print(f"测试模式: 处理前 {end_index} 个问题")
    else:
        end_index = total_questions
        print(f"完整模式: 处理所有 {total_questions} 个问题")
    
    print("-" * 60)
    
    results = []
    success_count = 0
    failed_count = 0
    
    start_time = time.time()
    
    for i in range(end_index):
        result = process_question(questions[i], i, end_index)
        
        if result['sub_questions'] and 'Error' not in result.get('combination', {}).get('description', ''):
            success_count += 1
        else:
            failed_count += 1
        
        results.append(result)
        time.sleep(0.5)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')
    
    print("-" * 60)
    print(f"处理完成!")
    print(f"成功: {success_count}, 失败: {failed_count}")
    print(f"总耗时: {elapsed_time:.2f} 秒")
    print(f"平均每个问题: {elapsed_time/len(results):.2f} 秒")
    print(f"结果已保存到: {output_file}")
    print("=" * 60)
    
    return results

def main():
    input_file = 'D:/Projects/pythonProject/question/olympedia_questions.jsonl'
    output_file = 'D:/Projects/pythonProject/Decomposer/olympedia_decomposition_results.jsonl'
    
    isTest = False
    
    import sys
    if len(sys.argv) > 1:
        isTest = sys.argv[1].lower() == 'true'
    
    mode = "测试模式" if isTest else "完整模式"
    print(f"运行模式: {mode}")
    print(f"使用方法: python batch_decompose.py [isTest]")
    print(f"示例: python batch_decompose.py true  # 测试模式")
    print(f"      python batch_decompose.py false # 完整模式")
    print()
    
    batch_decompose(input_file, output_file, isTest=isTest)

if __name__ == "__main__":
    main()