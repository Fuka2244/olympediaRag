# Qwen SQL生成器使用说明

## 功能介绍

这个脚本使用阿里云通义千问(Qwen)的API来读取数据库DDL结构，并根据自然语言问题生成相应的SQL查询语句。

## 安装依赖

首先安装必要的Python包：

```bash
pip install -r requirements.txt
```

或者单独安装dashscope：

```bash
pip install dashscope>=1.14.0
```

## 获取API Key

1. 访问 [阿里云百炼平台](https://bailian.console.aliyun.com/)
2. 注册/登录账号
3. 创建API Key（选择DashScope类型）
4. 复制API Key

## 配置API Key

有两种方式配置API Key：

### 方式1：环境变量（推荐）

在Windows上设置环境变量：
```cmd
set DASHSCOPE_API_KEY=你的API_KEY
```

在Linux/Mac上：
```bash
export DASHSCOPE_API_KEY=你的API_KEY
```

### 方式2：修改代码

直接在 `qwen_sql_generator.py` 文件中修改：
```python
API_KEY = "你的真实API_KEY"
```

## 使用方法

### 1. 准备输入文件

确保以下文件存在：

- **data/initial_ddl.sql** - 数据库表结构定义
- **data/questions.txt** - 自然语言问题（每行一个问题）

当前 `questions.txt` 中的问题：
```
Which Ethiopian men have won the Olympic marathon?
```

### 2. 运行脚本

```bash
python qwen_sql_generator.py
```

### 3. 查看结果

脚本会：
1. 读取DDL文件
2. 读取问题文件
3. 调用Qwen API生成SQL
4. 输出生成的SQL
5. 将SQL保存到 `generated_sql.sql`

## 示例输出

```
================================================================================
Qwen SQL生成器
================================================================================

正在读取DDL文件: d:/Projects/pythonProject/data/initial_ddl.sql
✓ DDL文件读取成功

正在读取问题文件: d:/Projects/pythonProject/data/questions.txt
✓ 问题读取成功: Which Ethiopian men have won the Olympic marathon?

================================================================================
正在调用Qwen API生成SQL...
================================================================================
问题: Which Ethiopian men have won the Olympic marathon?

生成的SQL:
SELECT a.full_name, a.noc, ar.event, ar.medal
FROM athlete_infobox a
JOIN athlete_results ar ON a.athlete_id = ar.athlete_id
WHERE a.noc = 'ETH'
  AND a.sex = 'Men'
  AND ar.event LIKE '%marathon%'
  AND ar.medal = 'Gold'
================================================================================

✓ SQL已保存到: d:/Projects/pythonProject/generated_sql.sql
```

## 自定义问题

编辑 `data/questions.txt` 文件，可以添加多个问题（每行一个）：

```
Which Ethiopian men have won the Olympic marathon?
How many gold medals did China win in 2008?
List all athletes who participated in swimming events
```

## 支持的模型

脚本默认使用 `qwen-plus` 模型。你也可以修改 `MODEL_NAME` 变量使用其他模型：

- `qwen-plus` - 通义千问Plus（推荐）
- `qwen-turbo` - 通义千问Turbo（速度更快）
- `qwen-max` - 通义千问Max（能力更强）

## 注意事项

1. **API调用限制**: 阿里云API有调用次数和并发限制，请注意使用量
2. **网络连接**: 需要稳定的网络连接来调用API
3. **DDL大小**: 如果DDL文件很大，可能会影响生成质量和响应时间
4. **SQL验证**: 生成的SQL建议在使用前进行验证

## 故障排除

### API Key未设置
```
⚠️  警告: 请先设置DASHSCOPE_API_KEY环境变量!
```
解决：按上述配置方法设置API Key

### 文件读取失败
```
❌ 无法读取DDL文件
```
解决：检查文件路径是否正确，文件是否存在

### API调用失败
```
API调用失败: 401 - InvalidApiKey
```
解决：检查API Key是否正确、是否已激活

## 相关文件

- `qwen_sql_generator.py` - 主程序
- `data/initial_ddl.sql` - 数据库表结构
- `data/questions.txt` - 自然语言问题
- `generated_sql.sql` - 生成的SQL查询（输出文件）
