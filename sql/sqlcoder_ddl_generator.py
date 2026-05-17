"""
使用 SQLCoder 生成 DDL 的脚本
功能：读取 reranker 后的表信息，使用 SQLCoder 生成对应的 DDL 语句
"""

import json
import os
import re
import time
from typing import Optional
from tqdm import tqdm

# ============= 配置区域 =============
# SQLCoder 本地模型路径
SQLCODER_MODEL_PATH = "d:/path/to/your/sqlcoder-7b"  # 修改为你的本地模型路径

# 输入输出路径
RERANKER_RESULTS_PATH = "d:/Projects/pythonProject/ai_schema_link/table_selection_results.jsonl"
OUTPUT_DDL_PATH = "d:/Projects/pythonProject/sql/generated_ddl.sql"
TABLE_DDL_MAPPING_PATH = "d:/Projects/pythonProject/sql/table_ddl_mapping.jsonl"
EXISTING_DDL_PATH = "d:/Projects/pythonProject/data/initial_ddl.sql"

# 推理配置
MAX_NEW_TOKENS = 1024
TEMPERATURE = 0.1
BATCH_SIZE = 1


# ============= SQLCoder 推理 =============

class SQLCoderInference:
    """SQLCoder 本地推理类"""
    
    def __init__(self, model_path: str, device: str = "cuda"):
        """
        初始化 SQLCoder 模型
        
        Args:
            model_path: 本地模型路径
            device: 推理设备，"cuda" 或 "cpu"
        """
        self.model_path = model_path
        self.device = device
        self.pipeline = None
        
    def load_model(self):
        """加载模型"""
        from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
        
        print(f"正在加载模型: {self.model_path}")
        print(f"使用设备: {self.device}")
        
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            trust_remote_code=True
        )
        
        # 根据显存情况调整量化方式
        model_kwargs = {
            "device_map": "auto",
            "trust_remote_code": True,
        }
        
        # 尝试使用量化加载以节省显存
        try:
            from transformers import BitsAndBytesConfig
            quantization_config = BitsAndBytesConfig(
                load_in_8bit=True,
                llm_int8_threshold=6.0,
            )
            model_kwargs["quantization_config"] = quantization_config
            print("使用 8-bit 量化加载")
        except ImportError:
            print("bitsandbytes 不可用，使用默认加载方式")
        
        model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            **model_kwargs
        )
        
        self.pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=MAX_NEW_TOKENS,
            temperature=TEMPERATURE,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )
        
        print("模型加载完成!")
    
    def generate_ddl(self, table_name: str, table_description: str,
                    sample_data: Optional[str] = None,
                    context_tables: Optional[list] = None) -> str:
        """
        使用 SQLCoder 生成表的 DDL 语句
        
        Args:
            table_name: 表名
            table_description: 表的描述信息
            sample_data: 示例数据（可选）
            context_tables: 相关的上下文表信息（可选）
        
        Returns:
            生成的 DDL 语句
        """
        if self.pipeline is None:
            self.load_model()
        
        # 构建 prompt
        prompt = self._build_ddl_prompt(table_name, table_description, sample_data, context_tables)
        
        # 推理
        try:
            result = self.pipeline(
                prompt,
                return_full_text=False,
                clean_up_tokenization_spaces=True,
            )
            
            if result and len(result) > 0:
                generated_text = result[0].get("generated_text", "")
                # 提取 SQL 语句
                return self._extract_sql(generated_text)
            return ""
        except Exception as e:
            return f"ERROR: {str(e)}"
    
    def _build_ddl_prompt(self, table_name: str, description: str,
                         sample_data: Optional[str] = None,
                         context_tables: Optional[list] = None) -> str:
        """构建生成 DDL 的 prompt"""
        
        prompt = f"""<human>: You are an expert SQL developer. Based on the following table information, generate the MySQL CREATE TABLE DDL statement.

Table Name: {table_name}
Description: {description}
"""
        
        if sample_data:
            prompt += f"\nSample Data (first 5 rows):\n{sample_data}\n"
        
        if context_tables:
            prompt += "\nRelated Tables (for reference):\n"
            for ctx in context_tables[:5]:
                prompt += f"  - {ctx.get('table_name', 'unknown')}: {ctx.get('description', '')}\n"
        
        prompt += """
Generate the complete MySQL CREATE TABLE statement with:
1. Appropriate column names in snake_case
2. Correct data types (VARCHAR, INT, TEXT, DATETIME, etc.)
3. Primary key constraint
4. Indexes for foreign keys and frequently queried columns
5. Table comment describing the table's purpose

Output ONLY the SQL DDL statement without any explanation.
<bot>:"""
        return prompt
    
    def _extract_sql(self, text: str) -> str:
        """从生成的文本中提取 SQL 语句"""
        # 尝试提取 ```sql ... ``` 或 ``` ... ``` 块
        sql_patterns = [
            r'```sql\n(.*?)```',
            r'```\n(.*?)```',
            r'(CREATE TABLE.*)',
        ]
        
        for pattern in sql_patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # 如果没有匹配到代码块，返回原文
        return text.strip()


# ============= 工具函数 =============

def load_reranker_results(file_path: str) -> list:
    """加载 reranker 结果，提取所有唯一的表名"""
    tables_set = set()
    table_info = {}  # 存储表的详细信息
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                if 'top_k_tables' in data:
                    for i, table_name in enumerate(data['top_k_tables']):
                        if table_name not in table_info:
                            table_info[table_name] = {
                                'name': table_name,
                                'description': '',
                                'columns': [],
                                'referenced_by': []
                            }
                        # 记录引用来源
                        table_info[table_name]['referenced_by'].append({
                            'question_id': data.get('id'),
                            'question': data.get('question', '')[:100]
                        })
            except json.JSONDecodeError:
                continue
    
    return list(table_info.keys()), table_info


def extract_table_info_from_sql(ddl_content: str) -> dict:
    """从现有 DDL 中提取表结构信息"""
    tables = {}
    
    # 匹配 CREATE TABLE 语句
    pattern = r'CREATE TABLE.*?`(\w+)`.*?\((.*?)\)\s*ENGINE'
    matches = re.findall(pattern, ddl_content, re.DOTALL | re.IGNORECASE)
    
    for table_name, columns_str in matches:
        columns = []
        # 解析列定义
        col_pattern = r'`(\w+)`\s+([\w()]+(?:\(\d+(?:,\s*\d+)?\))?)\s*(?:CHARACTER SET \w+)?\s*(?:COLLATE \w+)?\s*(?:NULL|NOT NULL)?\s*(?:DEFAULT [^\s,]+)?\s*(?:COMMENT [\'"]([^\'"]*)[\'"])?'
        col_matches = re.findall(col_pattern, columns_str)
        
        for col_name, col_type, col_comment in col_matches:
            columns.append({
                'name': col_name,
                'type': col_type,
                'comment': col_comment
            })
        
        tables[table_name] = {
            'columns': columns,
            'full_ddl': f"CREATE TABLE `{table_name}` ({columns_str})"
        }
    
    return tables


def extract_table_description(file_path: str, table_name: str) -> str:
    """从搜索结果文件中提取表描述"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 查找包含该表名的相似度结果
            pattern = rf'"table_name":\s*"{re.escape(table_name)}".*?"text":\s*"([^"]+)"'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                return match.group(1)
    except Exception:
        pass
    return ""


# ============= 主流程 =============

def generate_ddl_for_tables(
    tables: list, 
    table_info: dict,
    existing_ddl_tables: dict,
    sqlcoder_inference: SQLCoderInference,
    batch_size: int = 1,
    delay: float = 1.0
) -> dict:
    """
    批量为表生成 DDL
    
    Args:
        tables: 表名列表
        table_info: 表的详细信息
        existing_ddl_tables: 已有的 DDL 字典
        sqlcoder_client: SQLCoder 客户端
        batch_size: 每批处理的表数量
        delay: API 调用间隔（秒）
    
    Returns:
        生成的 DDL 字典
    """
    results = {}
    
    print(f"开始为 {len(tables)} 个表生成 DDL...")
    
    for i, table_name in enumerate(tqdm(tables, desc="生成 DDL")):
        # 检查是否已有 DDL
        if table_name in existing_ddl_tables:
            print(f"[{i+1}/{len(tables)}] 表 {table_name} 已有 DDL，跳过")
            results[table_name] = {
                'ddl': existing_ddl_tables[table_name]['full_ddl'],
                'source': 'existing',
                'status': 'success'
            }
            continue
        
        # 获取表信息
        info = table_info.get(table_name, {})
        description = info.get('description', f'Table for {table_name}')
        referenced_by = info.get('referenced_by', [])
        
        # 构建上下文
        context = []
        for ref in referenced_by[:3]:  # 取前3个引用作为上下文
            context.append({
                'table_name': ref.get('question_id'),
                'description': ref.get('question', '')
            })
        
        # 调用 SQLCoder
        try:
            ddl = sqlcoder_inference.generate_ddl(
                table_name=table_name,
                table_description=description,
                context_tables=context
            )
            
            if ddl.startswith("ERROR:"):
                results[table_name] = {
                    'ddl': '',
                    'source': 'sqlcoder',
                    'status': 'error',
                    'error': ddl
                }
                print(f"[{i+1}/{len(tables)}] 表 {table_name} 生成失败: {ddl}")
            else:
                results[table_name] = {
                    'ddl': ddl,
                    'source': 'sqlcoder',
                    'status': 'success'
                }
                print(f"[{i+1}/{len(tables)}] 表 {table_name} 生成成功")
            
            # API 限流处理
            time.sleep(delay)
            
        except Exception as e:
            results[table_name] = {
                'ddl': '',
                'source': 'sqlcoder',
                'status': 'error',
                'error': str(e)
            }
            print(f"[{i+1}/{len(tables)}] 表 {table_name} 生成异常: {str(e)}")
    
    return results


def save_results(results: dict, sql_path: str, mapping_path: str):
    """保存生成结果"""
    # 保存 SQL 文件
    sql_content = "-- Generated DDL Statements\n"
    sql_content += "-- Auto-generated by SQLCoder\n\n"
    sql_content += "SET NAMES utf8mb4;\n"
    sql_content += "SET FOREIGN_KEY_CHECKS = 0;\n\n"
    
    for table_name, result in sorted(results.items()):
        if result['status'] == 'success' and result['ddl']:
            sql_content += f"\n-- Table: {table_name} (Source: {result['source']})\n"
            sql_content += result['ddl'] + ";\n"
    
    sql_content += "\nSET FOREIGN_KEY_CHECKS = 1;\n"
    
    with open(sql_path, 'w', encoding='utf-8') as f:
        f.write(sql_content)
    
    # 保存映射文件 (JSONL)
    with open(mapping_path, 'w', encoding='utf-8') as f:
        for table_name, result in results.items():
            record = {
                'table_name': table_name,
                'status': result['status'],
                'source': result.get('source', ''),
                'ddl': result.get('ddl', ''),
                'error': result.get('error', '')
            }
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    print(f"结果已保存到:\n  - {sql_path}\n  - {mapping_path}")


def main():
    """主函数"""
    print("=" * 60)
    print("SQLCoder DDL 生成工具")
    print("=" * 60)
    
    # 1. 加载 reranker 结果
    print("\n[1/4] 加载 reranker 结果...")
    tables, table_info = load_reranker_results(RERANKER_RESULTS_PATH)
    print(f"   找到 {len(tables)} 个唯一表名")
    
    # 2. 提取现有 DDL
    print("\n[2/4] 提取现有 DDL...")
    existing_ddl_tables = {}
    if os.path.exists(EXISTING_DDL_PATH):
        with open(EXISTING_DDL_PATH, 'r', encoding='utf-8') as f:
            existing_ddl_tables = extract_table_info_from_sql(f.read())
        print(f"   从现有 DDL 中提取了 {len(existing_ddl_tables)} 个表的结构")
    else:
        print("   警告: 现有 DDL 文件不存在，将全部生成")
    
    # 3. 统计需要生成的表
    tables_to_generate = [t for t in tables if t not in existing_ddl_tables]
    print(f"\n[3/4] 生成计划:")
    print(f"   - 已有 DDL: {len(tables) - len(tables_to_generate)} 个表")
    print(f"   - 需要生成: {len(tables_to_generate)} 个表")
    
    if tables_to_generate:
        # 4. 初始化 SQLCoder 推理
        print("\n[4/4] 初始化 SQLCoder 推理...")
        # 自动检测设备
        device = "cuda" if __import__('torch').cuda.is_available() else "cpu"
        inference = SQLCoderInference(SQLCODER_MODEL_PATH, device=device)
        
        # 生成 DDL
        results = generate_ddl_for_tables(
            tables_to_generate,
            table_info,
            existing_ddl_tables,
            inference,
            delay=1.0
        )
        
        # 合并结果
        all_results = {**{t: {'ddl': existing_ddl_tables[t]['full_ddl'], 
                              'source': 'existing', 
                              'status': 'success'} 
                         for t in tables if t in existing_ddl_tables},
                      **results}
    else:
        # 全部使用现有 DDL
        all_results = {t: {'ddl': existing_ddl_tables[t]['full_ddl'], 
                          'source': 'existing', 
                          'status': 'success'} 
                      for t in tables if t in existing_ddl_tables}
    
    # 保存结果
    save_results(all_results, OUTPUT_DDL_PATH, TABLE_DDL_MAPPING_PATH)
    
    # 统计
    success_count = sum(1 for r in all_results.values() if r['status'] == 'success')
    error_count = sum(1 for r in all_results.values() if r['status'] == 'error')
    
    print("\n" + "=" * 60)
    print(f"完成! 成功: {success_count}, 失败: {error_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
