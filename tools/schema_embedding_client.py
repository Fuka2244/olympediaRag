import json
import numpy as np
import faiss
from huggingface_hub import InferenceClient

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
# 2. 使用 HuggingFace InferenceClient 生成 Embedding
# =========================
class HFInferenceEmbedding:
    def __init__(self, model_name, api_token=None):
        self.model_name = model_name
        self.client = InferenceClient(
            model=model_name,
            token=api_token  # 如果没有 token，可以使用免费服务（有限制）
        )

    def encode(self, texts, normalize_embeddings=True, show_progress_bar=False):
        """
        批量生成 embedding
        """
        embeddings = []

        # 批量处理
        batch_size = 50
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            try:
                # 使用 feature-extraction 任务
                result = self.client.feature_extraction(
                    text=batch
                )

                # 转换为 numpy 数组
                if isinstance(result, list):
                    batch_embeddings = np.array(result)
                else:
                    batch_embeddings = np.array(result.tolist())

                embeddings.append(batch_embeddings)

                if show_progress_bar:
                    print(f"Processed {min(i + batch_size, len(texts))}/{len(texts)} texts")

            except Exception as e:
                print(f"Error processing batch {i}: {e}")
                # 使用零向量作为后备
                dim = 384  # 根据模型调整
                batch_embeddings = np.zeros((len(batch), dim), dtype=np.float32)
                embeddings.append(batch_embeddings)

        # 合并所有批次
        embeddings = np.vstack(embeddings).astype("float32")

        # 归一化
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
    # 获取免费 token: https://huggingface.co/settings/tokens
    HF_TOKEN = None  # 填入你的 token，例如 "hf_xxxxxxxxxxxx"

    # 可选的模型
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # 轻量级 (384维)
    # MODEL_NAME = "BAAI/bge-small-en-v1.5"  # 更好的性能 (384维)
    # MODEL_NAME = "BAAI/bge-base-en-v1.5"  # 更高精度 (768维)
    # MODEL_NAME = "BAAI/bge-m3"  # 最强性能 (1024维)

    # 1. 加载数据
    texts, table_names = load_schema_texts(schema_path)
    print(f"加载了 {len(texts)} 条文本")

    # 2. 初始化 InferenceClient
    model = HFInferenceEmbedding(MODEL_NAME, HF_TOKEN)

    # 3. 生成 embedding（从远程 API）
    print(f"\n使用模型: {MODEL_NAME}")
    print("开始生成 embedding（调用 HuggingFace Serverless API）...")
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
