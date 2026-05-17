# HuggingFace Embedding 使用说明

本文件夹提供了三种使用 HuggingFace 模型生成 Embedding 的方法：

## 方法对比

| 方法 | 文件 | 优点 | 缺点 | 适用场景 |
|------|------|------|------|----------|
| **本地下载** | `schema_embedding_index.py` | 速度快，无网络依赖 | 需要下载模型（几百MB到几GB） | 频繁使用，有存储空间 |
| **Requests API** | `schema_embedding_api.py` | 不下载模型，灵活 | 需要处理请求细节 | 简单调用，批量处理 |
| **InferenceClient** | `schema_embedding_client.py` | 官方支持，易用 | 依赖网络 | **推荐**，大多数场景 |

---

## 方法1: 本地下载（原始方案）

**文件**: `schema_embedding_index.py`

```python
from sentence_transformers import SentenceTransformer

# 自动下载模型到本地缓存
model = SentenceTransformer("BAAI/bge-m3")
embeddings = model.encode(texts)
```

**优点**:
- ✅ 推理速度快（本地计算）
- ✅ 不受网络限制
- ✅ 无调用次数限制

**缺点**:
- ❌ 首次需要下载模型（BGE-M3 约 2.3GB）
- ❌ 占用磁盘空间

---

## 方法2: HuggingFace API（Requests）

**文件**: `schema_embedding_api.py`

```python
import requests

model = HuggingFaceEmbedding(
    "sentence-transformers/all-MiniLM-L6-v2",
    api_token=None  # 可选
)
embeddings = model.encode(texts)
```

**优点**:
- ✅ 不下载模型
- ✅ 灵活控制请求

**缺点**:
- ❌ 需要处理 HTTP 请求细节
- ❌ 免费版有速率限制

---

## 方法3: HuggingFace InferenceClient（推荐）⭐

**文件**: `schema_embedding_client.py`

```python
from huggingface_hub import InferenceClient

client = InferenceClient(
    model="sentence-transformers/all-MiniLM-L6-v2",
    token=None  # 可选
)
embeddings = client.feature_extraction(text=texts)
```

**优点**:
- ✅ 官方库，代码简洁
- ✅ 不下载模型
- ✅ 支持多种模型类型
- ✅ 自动处理批量请求

**缺点**:
- ❌ 依赖网络
- ❌ 免费版有速率限制

---

## 安装依赖

### 方法1（本地）:
```bash
pip install sentence-transformers faiss-cpu numpy
```

### 方法2 & 方法3（API）:
```bash
pip install huggingface_hub faiss-cpu numpy requests
```

---

## 获取 HuggingFace Token（可选）

1. 访问: https://huggingface.co/settings/tokens
2. 点击 "New token"
3. 创建 token（选择 "Read" 权限即可）
4. 复制 token（格式: `hf_xxxxxxxxxxxxxxxx`）

**注意**:
- ✅ 有 token: 更高的速率限制
- ❌ 无 token: 免费版，有限制但可以使用

---

## 使用方法

### 快速开始

```python
from schema_embedding_client import HFInferenceEmbedding, build_faiss_index, search

# 1. 初始化模型（不下载到本地）
model = HFInferenceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    api_token=None  # 可选
)

# 2. 生成 embedding
embeddings = model.encode(texts, normalize_embeddings=True)

# 3. 构建 FAISS 索引
index = build_faiss_index(embeddings)

# 4. 查询
results = search(query, model, index, table_names, top_k=5)
```

### 运行完整示例

```bash
# 确保先创建 schema_texts.jsonl
cd tools
python schema_embedding_client.py
```

---

## 推荐模型

| 模型 | 维度 | 速度 | 精度 | 大小 |
|------|------|------|------|------|
| `sentence-transformers/all-MiniLM-L6-v2` | 384 | ⚡⚡⚡ | ⭐⭐⭐ | 80MB |
| `BAAI/bge-small-en-v1.5` | 384 | ⚡⚡ | ⭐⭐⭐⭐ | 133MB |
| `BAAI/bge-base-en-v1.5` | 768 | ⚡⚡ | ⭐⭐⭐⭐⭐ | 420MB |
| `BAAI/bge-m3` | 1024 | ⚡ | ⭐⭐⭐⭐⭐ | 2.3GB |

**推荐**:
- 速度快: `all-MiniLM-L6-v2`
- 平衡: `bge-small-en-v1.5`
- 高精度: `bge-m3`

---

## 费用说明

### 免费版（无 token）
- ❌ 速率限制较低
- ❌ 可能排队
- ✅ 完全免费

### 免费版（有 token）
- ✅ 更高的速率限制
- ✅ 优先处理
- ✅ 完全免费

### 付费版（Inference Endpoints）
- ✅ 无速率限制
- ✅ 更快响应
- ❌ 按使用量计费

详情: https://huggingface.co/pricing

---

## 常见问题

### Q1: API 请求失败怎么办？
A: 检查网络连接，或添加 token 提高限制。

### Q2: 速度太慢？
A: 减小 `batch_size`，或改用本地下载方法。

### Q3: 如何离线使用？
A: 必须使用方法1，先下载模型到本地。

### Q4: 支持其他 API（OpenAI）吗？
A: 可以，代码类似，只需替换 API 端点。

---

## 相关链接

- HuggingFace Models: https://huggingface.co/models
- Sentence Transformers: https://www.sbert.net/
- FAISS: https://github.com/facebookresearch/faiss
