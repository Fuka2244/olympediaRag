# Schema Linking 使用指南

## 概述

本项目的Schema Linking模块采用**全自动**方式，可以自动识别自然语言问题中涉及的表和列，适合大规模Schema（50+表）。

## 工作原理

### 1. 自动匹配机制

系统会自动执行以下步骤：

1. **关键词提取**：使用jieba分词从问题中提取关键词
2. **模糊匹配**：将关键词与所有表名、列名、描述进行相似度匹配
3. **相似度计算**：使用SequenceMatcher算法计算相似度分数（0-1）
4. **阈值过滤**：只保留相似度≥0.3的匹配结果（可调）
5. **Top-K选择**：每张表最多返回5个最相关的列（可调）

### 2. 关键匹配源

系统会自动搜索以下内容进行匹配：
- 表名（如：employees, departments）
- 表描述（如：员工信息表）
- 列名（如：name, join_date）
- 列描述（如：入职日期）

## 使用方法

### 1. 定义Schema（重要！）

在`ddl_schema.py`中定义你的Schema时，**一定要为每个表和列提供清晰的描述**：

```python
TABLE_METADATA = {
    "your_table_name": {
        "columns": {
            "column1": {
                "type": "VARCHAR(100)", 
                "description": "这里写清晰的中文描述"  # 重要！
            },
            "column2": {
                "type": "INT",
                "description": "这里写清晰的中文描述"  # 重要！
            }
        },
        "description": "表的描述"  # 重要！
    }
}
```

### 2. 调用Schema Linker

```python
from schema_linking import SchemaLinker

# 初始化（自动模式）
schema_linker = SchemaLinker()

# 执行schema linking
result = schema_linker.link_schema(
    question="查询薪资最高的员工",
    threshold=0.3,  # 可选：相似度阈值
    top_k=5        # 可选：每表最多列数
)

# 查看结果
print(f"相关表: {result['relevant_tables']}")
print(f"相关列: {result['relevant_columns']}")
print(f"匹配详情: {result['match_details']}")  # 调试用
```

### 3. 参数说明

- **threshold**：相似度阈值（默认0.3）
  - 降低阈值：匹配更多结果，但可能包含不相关的
  - 提高阈值：匹配更精准，但可能遗漏相关结果

- **top_k**：每张表最多返回的列数（默认5）
  - 用于控制prompt长度，避免token超限

## 配置优化建议

### 对于50+表的大型Schema

1. **优化描述质量**
   - 描述应该包含业务术语
   - 尽量使用问题中可能出现的词汇
   - 示例：
     ```python
     "description": "用户基本信息，包含注册时间、登录次数"  # 好
     "description": "user info"  # 不好，对于中文问题
     ```

2. **调整匹配参数**
   ```python
   # 如果匹配太宽泛
   result = schema_linker.link_schema(question, threshold=0.4)
   
   # 如果匹配太少
   result = schema_linker.link_schema(question, threshold=0.2)
   
   # 如果单表列太多导致prompt过长
   result = schema_linker.link_schema(question, top_k=3)
   ```

3. **使用匹配详情调试**
   ```python
   result = schema_linker.link_schema(question)
   for detail in result['match_details']:
       print(detail)
   ```
   输出示例：
   ```
   关键词 '薪资' -> 列 'salary' (表: employees, 相似度: 0.50)
   关键词 '员工' -> 表 'employees' (相似度: 0.75)
   ```

## 示例

### 输入问题
```
"查询2023年入职的员工姓名和薪资"
```

### Schema Linking自动识别结果
```python
{
    "relevant_tables": ["employees"],
    "relevant_columns": {
        "employees": ["name", "join_date", "salary"]
    },
    "match_details": [
        "关键词 '2023' -> 列 'join_date' (表: employees, 相似度: 0.30)",
        "关键词 '入职' -> 列 'join_date' (表: employees, 相似度: 0.75)",
        "关键词 '员工' -> 表 'employees' (相似度: 0.75)",
        "关键词 '姓名' -> 列 'name' (表: employees, 相似度: 0.67)",
        "关键词 '薪资' -> 列 'salary' (表: employees, 相似度: 0.50)"
    ]
}
```

## 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖：
- jieba：中文分词
- 其他依赖见requirements.txt

## 性能说明

- 支持数百张表的大规模Schema
- 使用搜索索引，性能与表数量成线性关系
- 单次匹配耗时：50张表约10-50ms

## 常见问题

**Q: 为什么匹配不到某些表？**
A: 检查表和列的description是否清晰，尝试降低threshold。

**Q: 匹配了太多不相关的表？**
A: 提高threshold值，或优化description使其更具体。

**Q: Prompt太长超过模型限制？**
A: 降低top_k值，减少每表返回的列数。

**Q: 英文表名/列名能匹配吗？**
A: 可以，系统会同时匹配中英文。建议在description中包含中文说明。
