import json
import requests
import numpy as np
import faiss

# =========================
# 1. 加载数据
# =========================
def load_schema_texts(path):
    texts = []
    table_names = []

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            texts.append(item["text"])
            table_names.append(item["table_name"])

    return texts, table_names


# =========================
# 2. 使用 HuggingFace API 生成 Embedding
# =========================
class HuggingFaceEmbedding:
    def __init__(self, model_name, api_token=None):
        self.model_name = model_name
        self.api_token = api_token
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        self.headers = {}
        if api_token:
            self.headers["Authorization"] = f"Bearer {api_token}"

    def encode(self, texts, normalize_embeddings=True, show_progress_bar=False):
        """
        批量生成 embedding
        """
        embeddings = []

        # 批量处理，每次最多处理 texts 的片段
        batch_size = 50
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            try:
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json={"inputs": batch},
                    timeout=30
                )
                response.raise_for_status()
                result = response.json()

                # 提取 embedding
                if isinstance(result, list):
                    batch_embeddings = result
                elif isinstance(result, dict) and 'embeddings' in result:
                    batch_embeddings = result['embeddings']
                else:
                    batch_embeddings = [[0] * 1024] * len(batch)  # 默认维度

                embeddings.extend(batch_embeddings)

                if show_progress_bar:
                    print(f"Processed {min(i + batch_size, len(texts))}/{len(texts)} texts")

            except Exception as e:
                print(f"Error processing batch {i}: {e}")
                # 失败时返回零向量
                batch_embeddings = [[0] * 1024] * len(batch)
                embeddings.extend(batch_embeddings)

        embeddings = np.array(embeddings).astype("float32")

        # 归一化（用于余弦相似度）
        if normalize_embeddings:
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            embeddings = embeddings / (norms + 1e-8)

        return embeddings


# =========================
# 3. 构建 FAISS 索引
# =========================
def build_faiss_index(embeddings):
    dim = embeddings.shape[1]

    # 使用内积（因为已归一化 → 等价于 cosine）
    index = faiss.IndexFlatIP(dim)

    index.add(embeddings)
    print(f"索引构建完成，共 {index.ntotal} 条向量")

    return index


# =========================
# 4. 查询函数
# =========================
def search(query, model, index, table_names, top_k=5):
    query_vec = model.encode(
        [query],
        normalize_embeddings=True
    ).astype("float32")

    scores, indices = index.search(query_vec, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        results.append({
            "table_name": table_names[idx],
            "score": float(scores[0][i])
        })

    return results


# =========================
# 5. 主流程
# =========================
if __name__ == "__main__":
    # 文件路径
    schema_path = "../sql/description/schema_texts.jsonl"

    # HuggingFace API 配置
    # 如果没有 API token，可以留 None（有限制）
    # 获取免费 token: https://huggingface.co/settings/tokens
    HF_TOKEN = None  # 在这里填入你的 HuggingFace token，例如 "hf_xxxxxxxxxxxx"

    # 可选的模型（支持 embedding 的模型）
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # 轻量级
    # MODEL_NAME = "BAAI/bge-small-en-v1.5"  # 更好的性能
    # MODEL_NAME = "BAAI/bge-m3"  # 最强性能

    # 1. 加载数据
    texts, table_names = load_schema_texts(schema_path)
    print(f"加载了 {len(texts)} 条文本")

    # 2. 初始化 HuggingFace API 客户端
    model = HuggingFaceEmbedding(MODEL_NAME, HF_TOKEN)

    # 3. 生成 embedding（从远程 API）
    print("\n开始生成 embedding（调用 HuggingFace API）...")
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)

    # 4. 构建 FAISS 索引
    index = build_faiss_index(embeddings)

    # =========================
    # 5. 测试查询
    # =========================
    query = "Which athletes won gold medals in swimming?"

    results = search(query, model, index, table_names, top_k=5)

    print("\n查询结果：")
    for r in results:
        print(r)
