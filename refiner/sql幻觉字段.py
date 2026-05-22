import pymysql
import re
import difflib
import dashscope
from dashscope import Generation

# ================= 配置区 =================
DB_CONFIG = {
    "host": "localhost",
    "user": "refiner",
    "password": "123456",
    "database": "aolinpike",
    "charset": "utf8mb4"
}

# 填入你的 API Key
dashscope.api_key = "sk-c05e07d094484bcd97c40c234d85923c"


# ==========================================

class HardcoreRefiner:
    def __init__(self):
        self.schema = {}
        self.all_tables = []
        self.all_columns = []
        self.fetch_metadata()

    def fetch_metadata(self):
        """同步数据库真实的表名、列名以及字段注释"""
        try:
            conn = pymysql.connect(**DB_CONFIG)
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = [t[0] for t in cursor.fetchall()]
                self.all_tables = tables
                self.schema = {}
                self.all_columns = []
                for table in tables:
                    cursor.execute(f"SHOW FULL COLUMNS FROM `{table}`")
                    columns_info = cursor.fetchall()
                    cols_with_comments = {}
                    for col in columns_info:
                        col_name = col[0]
                        col_comment = col[8]
                        cols_with_comments[col_name] = col_comment if col_comment else "无注释"
                        self.all_columns.append(col_name)
                    self.schema[table] = cols_with_comments
            conn.close()
            self.all_columns = list(set(self.all_columns))
            print("✅ [元数据] 同步成功（已包含字段注释）")
        except Exception as e:
            print(f"❌ [元数据] 同步失败: {e}")

    def call_qwen_fix(self, bad_sql, question, target_tables):
        """调用 qwen-turbo 进行精准范围的语义级修复"""
        print(f"🧠 正在针对表 {target_tables} 进行精准语义对齐...")

        # 【核心优化】：只构造当前 SQL 涉及到的表的 Schema，缩小 AI 搜索空间
        schema_context = "你【必须】且【只能】从以下指定的表及其字段中选择：\n"
        for tbl in target_tables:
            tbl_lower = tbl.lower()
            if tbl_lower in self.schema:
                schema_context += f"- 表 {tbl_lower}:\n"
                for col_name, col_comment in self.schema[tbl_lower].items():
                    schema_context += f"  * {col_name} (含义: {col_comment})\n"

        messages = [
            {
                "role": "system",
                "content": "你是一个严格的 SQL 字段修复专家。你的任务是修复列名幻觉。你必须保留原始 SQL 的查询逻辑和表名，严禁切换到其他表。"
            },
            {
                "role": "user",
                "content": f"""
【选定的数据库 Schema】：
{schema_context}

【用户原始意图】：{question}
【待修复的 SQL】：{bad_sql}

【修正规则】：
1. 必须使用提供的 Schema 修复幻觉字段。
2. 严禁修改 FROM 和 JOIN 后面的表名。
3. 检查每个别名（如 t1, t2）对应的表，确保该别名下的字段在对应的表中真实存在。
4. 检查 JOIN 条件。如果表中有 'athlete_id' 字段，请优先使用它进行关联，而不是简单的 'id'。确保 t1 和 t2 关联的是同一个运动员。
5. 直接返回 SQL 文本，不要任何解释。
6.如果你检查到字段名不存在，请你在 Schema 中找到最相似的字段名，并使用它替换原始字段名。
"""
            }
        ]

        try:
            response = Generation.call(
                model='qwen-turbo',
                messages=messages,
                result_format='message'
            )
            if response.status_code == 200:
                fixed_sql = response.output.choices[0].message.content
                fixed_sql = re.sub(r'```sql\s*|\s*```', '', fixed_sql).strip()
                return fixed_sql
            else:
                print(f"❌ LLM 调用失败: {response.code} - {response.message}")
                return bad_sql
        except Exception as e:
            print(f"❌ LLM 请求异常: {e}")
            return bad_sql

    def align_and_fix(self, sql, user_question=""):
        # 1. 【保护常量】
        literals = re.findall(r"'(.*?)'|\"(.*?)\"", sql)
        placeholder_sql = re.sub(r"'(.*?)'|\"(.*?)\"", "'__LITERAL__'", sql)

        logs = []

        # 2. 【本地初步对齐表名】
        # 先提取表名，确保我们知道要去哪几个表找列
        tables_in_sql = re.findall(r'FROM\s+([a-zA-Z_0-9]+)|JOIN\s+([a-zA-Z_0-9]+)', placeholder_sql, re.I)
        target_tables = [t[0] or t[1] for t in tables_in_sql]
        fixed_sql = placeholder_sql

        for tbl in target_tables:
            if tbl.lower() not in self.all_tables:
                match = difflib.get_close_matches(tbl.lower(), self.all_tables, n=1, cutoff=0.6)
                if match:
                    fixed_sql = re.sub(r'\b' + re.escape(tbl) + r'\b', match[0], fixed_sql)
                    logs.append(f"本地修正表名: {tbl} -> {match[0]}")
                    # 更新 target_tables 列表，供后续 LLM 使用
                    target_tables[target_tables.index(tbl)] = match[0]

        # 3. 【判定是否需要 LLM】
        valid_columns = []
        for tbl in target_tables:
            if tbl.lower() in self.schema:
                valid_columns.extend(self.schema[tbl.lower()].keys())

        all_words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', fixed_sql)
        keywords = {'SELECT', 'FROM', 'WHERE', 'JOIN', 'ON', 'AND', 'OR', 'LIKE', 'AS', 'SUM', 'COUNT', 'AVG', 'GROUP',
                    'BY', 'HAVING'}

        need_llm = False
        for word in all_words:
            # 跳过表别名 (t1, t2) 和关键字
            if len(word) <= 2 or (word.startswith('t') and word[1:].isdigit()):
                continue
            if word.upper() not in keywords and word != "__LITERAL__" and word.lower() not in self.all_tables:
                if word.lower() not in valid_columns:
                    need_llm = True
                    logs.append(f"检测到潜在幻觉字段: {word}，请求 AI 进行定向修复")

        # 4. 【执行 LLM 修复】
        if need_llm:
            # 【重要】：传入当前涉及的 target_tables
            fixed_sql = self.call_qwen_fix(fixed_sql, user_question, target_tables)
            logs.append("✨ LLM 语义修复完成")

        # 5. 【恢复常量】
        final_sql = fixed_sql
        for lit in literals:
            val = lit[0] or lit[1]
            final_sql = final_sql.replace("'__LITERAL__'", f"'{val}'", 1)

        return final_sql, logs

    def verify_in_db(self, sql):
        print(f"\n🚀 正在执行物理验证...")
        try:
            conn = pymysql.connect(**DB_CONFIG)
            with conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                print("✨ [验证成功] SQL 语义对齐且可执行！")
                print(f"📊 查询结果示例: {result[:3]}")
                return True
        except pymysql.Error as e:
            print(f"❌ [执行报错] 错误码 {e.args[0]}: {e.args[1]}")
            return False


if __name__ == "__main__":
    refiner = HardcoreRefiner()

    # 使用你刚才失败的测试用例 1
    question = "查询所有男性运动员的名字及其生平传记"
    test_sql = """
        SELECT t1.athlete_name, t2.role_name FROM affiliations_athletes t1 JOIN athlete_organization_roles t2 ON t1.uid = t2.uid;
    """

    print(f"1. 初始 SQL: {test_sql.strip()}")
    refined_sql, logs = refiner.align_and_fix(test_sql, user_question=question)

    print("\n2. 纠偏日志:")
    for log in logs: print(f"   - {log}")

    print(f"\n3. 最终修复后的 SQL:\n{refined_sql}")
    refiner.verify_in_db(refined_sql)