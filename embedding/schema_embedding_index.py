import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer, CrossEncoder

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
# 2. 生成 Embedding
# =========================
def build_embeddings(model, texts):
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )
    return np.array(embeddings).astype("float32")


# =========================
# 3. 构建 FAISS 索引
# =========================
def build_faiss_index(embeddings):
    dim = embeddings.shape[1]

    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    print(f"✅ 索引构建完成，共 {index.ntotal} 条向量")
    return index


# =========================
# 4. 保存索引
# =========================
def save_index(index, table_names, save_dir="index"):
    os.makedirs(save_dir, exist_ok=True)

    faiss.write_index(index, os.path.join(save_dir, "faiss_index.bin"))

    with open(os.path.join(save_dir, "table_names.json"), "w", encoding="utf-8") as f:
        json.dump(table_names, f, ensure_ascii=False, indent=2)

    print("💾 索引已保存！")


# =========================
# 5. 加载索引
# =========================
def load_index(save_dir="index"):
    index = faiss.read_index(os.path.join(save_dir, "faiss_index.bin"))

    with open(os.path.join(save_dir, "table_names.json"), "r", encoding="utf-8") as f:
        table_names = json.load(f)

    print("📦 索引加载完成！")
    return index, table_names


# =========================
# 6. Reranker（核心新增）
# =========================
def rerank(query, candidates, texts, reranker, top_k=5):
    pairs = [(query, texts[i]) for i in candidates]

    scores = reranker.predict(pairs)

    sorted_items = sorted(
        zip(candidates, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_items[:top_k]


# =========================
# 7. 查询函数（升级版）
# =========================
def search(query, model, index, table_names, texts, reranker,
           top_k=5, rerank_k=20):

    print(f"\n🔍 查询: {query}")

    # 1️⃣ embedding召回（扩大范围）
    query_vec = model.encode(
        [query],
        normalize_embeddings=True
    ).astype("float32")

    scores, indices = index.search(query_vec, rerank_k)

    # 2️⃣ rerank（精排）
    reranked = rerank(query, indices[0], texts, reranker, top_k)

    results = []
    for idx, score in reranked:
        results.append({
            "table_name": table_names[idx],
            "score": float(score)
        })

    return results


# =========================
# 8. 主流程
# =========================
if __name__ == "__main__":
    schema_path = "../sql/description/schema_texts.jsonl"
    index_dir = "index"

    model_path = r"D:\models\huggingface_models"

    # =========================
    # 1. 加载模型（统一路径）
    # =========================
    print("🤖 加载 embedding 模型...")
    model = SentenceTransformer(
        "BAAI/bge-m3",
        cache_folder=model_path,
        local_files_only=True
    )

    print("🤖 加载 reranker 模型...")
    reranker = CrossEncoder(
        "BAAI/bge-reranker-base",   # ⭐ 推荐先用 base（更轻）
        device="cpu",
        cache_folder=model_path     # ⭐ 同样路径！
    )

    # =========================
    # 2. 加载或构建索引
    # =========================
    if os.path.exists(os.path.join(index_dir, "faiss_index.bin")):
        print("📂 检测到已有索引，直接加载...")
        index, table_names = load_index(index_dir)

        # ⚠️ 注意：texts 仍需加载（rerank需要）
        texts, _ = load_schema_texts(schema_path)

    else:
        print("🚀 首次运行，构建索引...")

        texts, table_names = load_schema_texts(schema_path)

        embeddings = build_embeddings(model, texts)

        index = build_faiss_index(embeddings)

        save_index(index, table_names, index_dir)

    # =========================
    # 3. 测试查询
    # =========================
    query = "Which athletes won gold medals in swimming?"

    results = search(
        query,
        model,
        index,
        table_names,
        texts,
        reranker,
        top_k=73,
        rerank_k=73
    )

    print("\n📊 查询结果（rerank后）：")
    for r in results:
        print(r)