"""
MySQL SQL执行脚本
从sql_generation_results.jsonl读取SQL语句并在MySQL数据库中执行
每10条结果保存一次到JSONL文件
"""
import os
import sys
import json
import time
from datetime import datetime
from loguru import logger

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from config import (
    MYSQL_CONFIG,
    SQL_RESULTS_FILE,
    OUTPUT_DIR,
    OUTPUT_FILE,
    BATCH_SIZE,
    QUERY_TIMEOUT,
    MAX_RETRIES,
    LOG_FILE,
    validate_config,
    print_config
)


class MySQLExecutor:
    """MySQL SQL执行器"""
    
    def __init__(self):
        """初始化MySQL连接"""
        self.connection = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """连接到MySQL数据库"""
        try:
            import pymysql
            self.connection = pymysql.connect(**MYSQL_CONFIG)
            self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            logger.info("✓ 成功连接到MySQL数据库")
        except ImportError:
            logger.error("✗ 未安装pymysql库，请运行: pip install pymysql")
            sys.exit(1)
        except Exception as e:
            logger.error(f"✗ 连接MySQL失败: {e}")
            sys.exit(1)
    
    def execute_query(self, sql, max_retries=MAX_RETRIES):
        """执行SQL查询"""
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                self.cursor.execute(sql)
                results = self.cursor.fetchall()
                execution_time = time.time() - start_time
                
                return {
                    "success": True,
                    "results": results,
                    "row_count": len(results),
                    "execution_time": round(execution_time, 4),
                    "error": None
                }
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"查询失败，重试 {attempt + 1}/{max_retries}: {e}")
                    time.sleep(1)
                else:
                    return {
                        "success": False,
                        "results": [],
                        "row_count": 0,
                        "execution_time": 0,
                        "error": str(e)
                    }
    
    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("✓ 数据库连接已关闭")


def load_sql_results(file_path):
    """加载SQL生成结果"""
    logger.info(f"从 {file_path} 加载SQL结果")
    sql_results = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                sql_results.append(json.loads(line.strip()))
    
    logger.info(f"✓ 加载了 {len(sql_results)} 条SQL记录")
    return sql_results


def execute_sql_batch(sql_results, executor, batch_size=BATCH_SIZE):
    """批量执行SQL并保存结果"""
    total_sql = len(sql_results)
    total_batches = (total_sql + batch_size - 1) // batch_size
    
    logger.info("=" * 80)
    logger.info("MySQL SQL执行 - 批量处理")
    logger.info("=" * 80)
    logger.info(f"总SQL数量: {total_sql}")
    logger.info(f"批量大小: {batch_size}")
    logger.info(f"总批次数: {total_batches}")
    logger.info("")
    
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    
    # 清空输出文件
    if os.path.exists(output_file):
        logger.info(f"清空现有输出文件: {output_file}")
        open(output_file, 'w').close()
    
    # 统计信息
    success_count = 0
    error_count = 0
    total_execution_time = 0
    
    # 批量处理
    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, total_sql)
        batch_sqls = sql_results[start_idx:end_idx]
        
        logger.info(f"处理批次 {batch_num + 1}/{total_batches} (SQL {start_idx + 1}-{end_idx})")
        logger.info("-" * 80)
        
        batch_results = []
        
        for i, sql_data in enumerate(batch_sqls):
            sql_idx = start_idx + i + 1
            question_id = sql_data.get("id")
            question = sql_data.get("question", "")
            k_value = sql_data.get("k")
            sql = sql_data.get("generated_sql", "")
            used_tables = sql_data.get("used_tables", [])
            
            logger.info(f"[{sql_idx}/{total_sql}] 问题ID {question_id}, k={k_value}")
            logger.info(f"  问题: {question[:60]}...")
            logger.info(f"  使用表: {', '.join(used_tables)}")
            
            # 执行SQL
            execution_result = executor.execute_query(sql)
            
            # 构建结果
            result = {
                "input": {
                    "id": question_id,
                    "question": question,
                    "k": k_value,
                    "used_tables": used_tables,
                    "generated_sql": sql
                },
                "output": {
                    "success": execution_result["success"],
                    "results": execution_result["results"],
                    "row_count": execution_result["row_count"],
                    "execution_time": execution_result["execution_time"],
                    "error": execution_result["error"],
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            batch_results.append(result)
            
            # 更新统计
            if execution_result["success"]:
                success_count += 1
                total_execution_time += execution_result["execution_time"]
                logger.info(f"  ✓ 成功: {execution_result['row_count']} 行, 耗时 {execution_result['execution_time']:.4f}秒")
            else:
                error_count += 1
                logger.error(f"  ✗ 失败: {execution_result['error']}")
            
            logger.info("")
        
        # 保存批次结果
        save_batch_results(batch_results, output_file, batch_num + 1, total_batches)
    
    # 打印总结
    logger.info("=" * 80)
    logger.info("执行总结")
    logger.info("=" * 80)
    logger.info(f"总SQL数量: {total_sql}")
    logger.info(f"成功执行: {success_count}")
    logger.info(f"执行失败: {error_count}")
    logger.info(f"成功率: {success_count/total_sql*100:.2f}%")
    logger.info(f"总执行时间: {total_execution_time:.4f}秒")
    logger.info(f"平均执行时间: {total_execution_time/success_count if success_count > 0 else 0:.4f}秒")
    logger.info(f"结果保存到: {output_file}")
    logger.info("=" * 80)


def save_batch_results(results, output_file, batch_num, total_batches):
    """保存批次结果到JSONL文件"""
    logger.info(f"保存批次 {batch_num}/{total_batches} 到 {output_file}")
    
    with open(output_file, 'a', encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')
    
    logger.info(f"✓ 保存了 {len(results)} 条结果")


def main():
    """主函数"""
    # 配置日志
    logger.remove()
    logger.add(sys.stdout, level="INFO")
    logger.add(LOG_FILE, level="INFO", rotation="10 MB")
    
    # 打印配置
    print_config()
    
    # 验证配置
    errors = validate_config()
    if errors:
        logger.error("✗ 配置错误:")
        for error in errors:
            logger.error(f"  - {error}")
        sys.exit(1)
    
    # 加载SQL结果
    sql_results = load_sql_results(SQL_RESULTS_FILE)
    
    if not sql_results:
        logger.error("✗ 没有加载到SQL结果")
        sys.exit(1)
    
    # 创建执行器
    executor = MySQLExecutor()
    
    try:
        # 批量执行SQL
        execute_sql_batch(sql_results, executor, batch_size=BATCH_SIZE)
    finally:
        # 关闭连接
        executor.close()


if __name__ == "__main__":
    """
    使用方法:
        # 使用默认配置执行
        python execute_sql.py
        
        # 自定义批量大小
        python execute_sql.py --batch_size 5
        
        # 限制执行数量
        python execute_sql.py --max_sql 50
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="MySQL SQL执行脚本")
    parser.add_argument("--batch_size", type=int, default=BATCH_SIZE, help="批量保存大小")
    parser.add_argument("--max_sql", type=int, default=None, help="最大执行SQL数量")
    args = parser.parse_args()
    
    # 修改全局配置
    if args.batch_size:
        BATCH_SIZE = args.batch_size
    
    # 加载SQL结果
    sql_results = load_sql_results(SQL_RESULTS_FILE)
    
    # 限制执行数量
    if args.max_sql:
        sql_results = sql_results[:args.max_sql]
        logger.info(f"只执行前 {args.max_sql} 条SQL")
    
    # 创建执行器
    executor = MySQLExecutor()
    
    try:
        # 批量执行SQL
        execute_sql_batch(sql_results, executor, batch_size=BATCH_SIZE)
    finally:
        # 关闭连接
        executor.close()