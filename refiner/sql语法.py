import pymysql
import dashscope  # 假设你使用通义千问的SDK
from dashscope import Generation

# 1. 配置数据库连接信息
DB_CONFIG = {
    "host": "localhost",
    "user": "refiner",  # 建议用低权限账号
    "password": "123456",
    "database": "aolinpike",
    "charset": "utf8mb4"
}


# 2. 调用大模型进行修复的函数
import re


def ask_llm_to_fix(bad_sql, error_msg, question,warning_msg=""):
    # 强化 Prompt：通过指令约束 AI 的行为
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
            model='qwen-turbo',  # 使用 turbo 即可胜任语法修复
            prompt=prompt,
            api_key='',
            result_format='message'
        )

        if response.status_code == 200:
            content = response.output.choices[0].message.content.strip()

            # --- 增强版清洗逻辑：使用正则表达式提取真正的 SQL ---
            # 即使 AI 不听话加了代码块，也能把里面的内容抠出来
            sql_pattern = re.compile(r'SELECT.*?;', re.DOTALL | re.IGNORECASE)
            match = sql_pattern.search(content)

            if match:
                clean_sql = match.group().strip()
            else:
                # 如果没搜到标准的 SELECT...; 格式，则尝试清理常见的 Markdown 标记
                clean_sql = content.replace('```sql', '').replace('```', '').strip()

            return clean_sql
        else:
            print(f"AI 接口报错: {response.message}")
            return bad_sql

    except Exception as e:
        print(f"修复函数异常: {e}")
        return bad_sql


# 3. 核心：Refiner 执行与纠错逻辑
def run_and_refine_sql(original_question, sql_to_test, max_retry=10):
    retry_count = 0
    current_sql = sql_to_test
    last_sql = None  # 用于记录上一次的 SQL，检测是否陷入循环
    warning_msg = ""  # 用于存放给 AI 的额外警告
    last_error_code = None

    while retry_count < max_retry:
        print(f"\n--- 第 {retry_count + 1} 次尝试 ---")
        print(f"尝试 SQL: {current_sql}")

        try:
            connection = pymysql.connect(**DB_CONFIG)
            with connection.cursor() as cursor:
                cursor.execute(current_sql)
                result = cursor.fetchall()
                print("✨ [完全成功] SQL 语法正确且已查询到数据！")
                return current_sql, result


        except pymysql.Error as e:

            error_code = e.args[0]

            error_msg = str(e)

            # 改进逻辑：如果是 1064（语法错）或者 报错里包含连在一起的关键字嫌疑

            # 我们就继续让 AI 修复

            is_likely_spacing_issue = "FROM" in error_msg.upper() and error_code == 1054

            if error_code != 1064 and not is_likely_spacing_issue:
                print(f"🎯 [语法修复成功] SQL 语法已修正！")

                return current_sql, None
                # --- 破局逻辑开始 ---
            if current_sql == last_sql:
                # 如果这次的 SQL 和上次一模一样，说明 AI 卡住了
                warning_msg = "🚨【严重警告】：你刚刚提供的 SQL 依然报同样的语法错误！请不要重复输出。请重新检查 HAVING、ORDER BY、GROUP BY 的先后顺序，并确保所有关键字拼写正确。"
                print(f"⚠️ 检测到 AI 输出重复，已激活“破局”警告模式。")
            else:
                warning_msg = ""  # 如果有变化，则清空警告
            last_sql = current_sql  # 更新记录
            print(f"❌ 触发纠错机制 (错误码 {error_code}): {error_msg}")

            current_sql = ask_llm_to_fix(current_sql, error_msg, original_question, warning_msg)

            retry_count += 1

    print("⚠️ 达到最大重试次数，仍存在语法问题。")
    return None, None


# 4. 测试运行
if __name__ == "__main__":
    test_question = "谁获得了2024年金牌？"
    wrong_sql = """SELECT t1.athlete_name, t2.role_name FROM affiliations_athletes t1 JOIN athlete_organization_roles t2 ON t1.uid = t2.uid"""

    final_sql, data = run_and_refine_sql(test_question, wrong_sql)
