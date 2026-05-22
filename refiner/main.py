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

dashscope.api_key = ""
# ==========================================


# ================= 语法修正模块 =================
def ask_llm_to_fix_syntax(bad_sql, error_msg, question, warning_msg=""):
    """调用大模型修正 SQL 语法错误"""
    prompt = f"""
        你是一个 SQL 语法修复专家。
        {warning_msg}

        【纠错原则】
        1. 必须保留原查询的所有意图（主查询、关联表、过滤条件均不能丢失）。
        2. 严格遵守子句顺序：SELECT -> FROM -> JOIN -> WHERE -> GROUP BY -> HAVING -> ORDER BY -> LIMIT。
        3. 修复括号嵌套错误，确保每个 ( 都有对应的 )。
        4. 仅输出修复后的纯文本 SQL。

        用户意图：{question}
        错误 SQL：{bad_sql}
        报错信息：{error_msg}
    """
    try:
        response = Generation.call(
            model='qwen-turbo',
            prompt=prompt,
            api_key=dashscope.api_key,
            result_format='message'
        )

        if response.status_code == 200:
            content = response.output.choices[0].message.content.strip()
            sql_pattern = re.compile(r'SELECT.*?;', re.DOTALL | re.IGNORECASE)
            match = sql_pattern.search(content)

            if match:
                clean_sql = match.group().strip()
            else:
                clean_sql = content.replace('```sql', '').replace('```', '').strip()

            return clean_sql
        else:
            print(f"AI 接口报错: {response.message}")
            return bad_sql

    except Exception as e:
        print(f"语法修复异常: {e}")
        return bad_sql


def fix_syntax(original_question, sql_to_fix, max_retry=3):
    """修正 SQL 语法错误"""
    print("\n" + "="*50)
    print("📌 第一步：语法修正")
    print("="*50)
    
    retry_count = 0
    current_sql = sql_to_fix
    last_sql = None
    warning_msg = ""

    while retry_count < max_retry:
        print(f"\n--- 语法修正 第 {retry_count + 1} 次尝试 ---")
        print(f"SQL: {current_sql}")

        try:
            connection = pymysql.connect(**DB_CONFIG)
            with connection.cursor() as cursor:
                cursor.execute(current_sql)
                result = cursor.fetchall()
                print("✅ [语法修正成功] SQL 语法正确！")
                return current_sql, None
        except pymysql.Error as e:
            error_code = e.args[0]
            error_msg = str(e)

            if error_code != 1064:
                print(f"✅ [语法正确] (错误码 {error_code}): {error_msg}")
                return current_sql, None

            if current_sql == last_sql:
                warning_msg = "🚨【严重警告】：你刚刚提供的 SQL 依然报同样的语法错误！请不要重复输出。请重新检查 HAVING、ORDER BY、GROUP BY 的先后顺序，并确保所有关键字拼写正确。"
                print(f"⚠️ 检测到重复输出，激活破局警告模式。")
            else:
                warning_msg = ""
            
            last_sql = current_sql
            print(f"❌ 语法错误 (错误码 {error_code}): {error_msg}")

            current_sql = ask_llm_to_fix_syntax(current_sql, error_msg, original_question, warning_msg)
            retry_count += 1

    print("⚠️ 语法修正达到最大重试次数。")
    return None, None


# ================= 幻觉字段修正模块 =================
class HallucinationRefiner:
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
            print("✅ [元数据] 同步成功")
        except Exception as e:
            print(f"❌ [元数据] 同步失败: {e}")

    def call_qwen_fix(self, bad_sql, question, target_tables):
        """调用大模型进行幻觉字段修复"""
        print(f"🧠 正在针对表 {target_tables} 进行字段对齐...")

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
4. 检查 JOIN 条件。如果表中有 'athlete_id' 字段，请优先使用它进行关联。
5. 直接返回 SQL 文本，不要任何解释。
6. 如果检查到字段名不存在，请在 Schema 中找到最相似的字段名，并使用它替换。
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

    def fix_hallucination(self, sql, user_question=""):
        """修正幻觉字段错误"""
        print("\n" + "="*50)
        print("📌 第二步：幻觉字段修正")
        print("="*50)

        logs = []

        # 保护常量
        literals = re.findall(r"'(.*?)'|\"(.*?)\"", sql)
        placeholder_sql = re.sub(r"'(.*?)'|\"(.*?)\"", "'__LITERAL__'", sql)

        # 初步对齐表名
        tables_in_sql = re.findall(r'FROM\s+([a-zA-Z_0-9]+)|JOIN\s+([a-zA-Z_0-9]+)', placeholder_sql, re.I)
        target_tables = [t[0] or t[1] for t in tables_in_sql]
        fixed_sql = placeholder_sql

        for tbl in target_tables:
            if tbl.lower() not in self.all_tables:
                match = difflib.get_close_matches(tbl.lower(), self.all_tables, n=1, cutoff=0.6)
                if match:
                    fixed_sql = re.sub(r'\b' + re.escape(tbl) + r'\b', match[0], fixed_sql)
                    logs.append(f"本地修正表名: {tbl} -> {match[0]}")
                    target_tables[target_tables.index(tbl)] = match[0]

        # 判定是否需要 LLM
        valid_columns = []
        for tbl in target_tables:
            if tbl.lower() in self.schema:
                valid_columns.extend(self.schema[tbl.lower()].keys())

        all_words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', fixed_sql)
        keywords = {'SELECT', 'FROM', 'WHERE', 'JOIN', 'ON', 'AND', 'OR', 'LIKE', 'AS', 'SUM', 'COUNT', 'AVG', 'GROUP',
                    'BY', 'HAVING', 'LIMIT', 'ORDER', 'ASC', 'DESC', 'INNER', 'LEFT', 'RIGHT', 'OUTER', 'NULL'}

        need_llm = False
        for word in all_words:
            if len(word) <= 2 or (word.startswith('t') and word[1:].isdigit()):
                continue
            if word.upper() not in keywords and word != "__LITERAL__" and word.lower() not in self.all_tables:
                if word.lower() not in valid_columns:
                    need_llm = True
                    logs.append(f"检测到潜在幻觉字段: {word}，请求 AI 修复")

        # 执行 LLM 修复
        if need_llm:
            fixed_sql = self.call_qwen_fix(fixed_sql, user_question, target_tables)
            logs.append("✨ LLM 幻觉字段修复完成")
        else:
            logs.append("✅ 未检测到幻觉字段")

        # 恢复常量
        final_sql = fixed_sql
        for lit in literals:
            val = lit[0] or lit[1]
            final_sql = final_sql.replace("'__LITERAL__'", f"'{val}'", 1)

        for log in logs:
            print(f"   - {log}")

        return final_sql

    def verify_in_db(self, sql):
        """在数据库中验证 SQL"""
        print(f"\n🚀 正在执行验证...")
        try:
            conn = pymysql.connect(**DB_CONFIG)
            with conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                print("✅ [验证成功] SQL 可正常执行！")
                print(f"📊 查询结果 ({len(result)} 条): {result[:5]}")
                return True, result
        except pymysql.Error as e:
            print(f"❌ [执行报错] 错误码 {e.args[0]}: {e.args[1]}")
            return False, None


# ================= 主程序 =================
def main():
    print("="*50)
    print("🔧 SQL 语句修正工具")
    print("   流程：语法修正 → 幻觉字段修正")
    print("="*50)

    # 初始化幻觉字段修正器
    refiner = HallucinationRefiner()

    # 用户输入
    print("\n请输入用户问题（或直接回车使用默认示例）：")
    user_question = input("用户问题: ").strip()
    if not user_question:
        user_question = "查询所有男性运动员的名字"
        print(f"  -> 使用默认问题: {user_question}")

    print("\n请输入需要修正的 SQL（或直接回车使用默认示例）：")
    print("SQL: ", end="")
    user_sql = input().strip()
    if not user_sql:
        user_sql = """SELECT t1.athlete_name, t2.biography FROM athletes t1 JOIN athlete_details t2 ON t1.id = t2.athlete_id WHERE t1.gender = '男'"""
        print(f"  -> 使用默认 SQL: {user_sql}")

    print("\n" + "="*60)
    print(f"📝 原始 SQL: {user_sql}")
    print("="*60)

    # 第一步：语法修正
    fixed_sql, _ = fix_syntax(user_question, user_sql)
    
    if fixed_sql is None:
        print("❌ 语法修正失败，尝试进行幻觉字段修正...")
        fixed_sql = user_sql

    # 第二步：幻觉字段修正
    final_sql = refiner.fix_hallucination(fixed_sql, user_question)

    # 最终验证
    print("\n" + "="*50)
    print("📌 第三步：最终验证")
    print("="*50)
    success, result = refiner.verify_in_db(final_sql)

    # 输出结果
    print("\n" + "="*50)
    print("📊 最终结果")
    print("="*50)
    print(f"✅ 最终 SQL:\n{final_sql}")
    
    # 保存结果到文档
    output_file = "sql_query_result.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("SQL 查询结果\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"【用户问题】\n{user_question}\n\n")
        f.write(f"【修正后 SQL】\n{final_sql}\n\n")
        f.write(f"【查询结果】\n")
        if success and result:
            f.write(f"共 {len(result)} 条记录\n\n")
            for i, row in enumerate(result, 1):
                f.write(f"{i}. {row}\n")
            print(f"\n✅ 结果已保存到: {output_file}")
        else:
            f.write("⚠️ SQL 执行失败，未能获取结果\n")
            print(f"\n⚠️ 结果已保存到: {output_file}（但 SQL 执行失败）")


if __name__ == "__main__":
    main()
