import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer, CrossEncoder


# =========================
# 1. 加载 schema 数据
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
# 2. 加载问题数据
# =========================
def load_questions(path):
    items = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


# =========================
# 3. 加载已有 FAISS 索引
# =========================
def load_index(save_dir):
    index = faiss.read_index(os.path.join(save_dir, "faiss_index.bin"))
    with open(os.path.join(save_dir, "table_names.json"), "r", encoding="utf-8") as f:
        table_names = json.load(f)
    print(f"索引加载完成，共 {index.ntotal} 条向量")
    return index, table_names


# =========================
# 4. Reranker
# =========================
def rerank(query, candidates, texts, reranker, top_k=25):
    pairs = [(query, texts[i]) for i in candidates]
    scores = reranker.predict(pairs)
    sorted_items = sorted(
        zip(candidates, scores),
        key=lambda x: x[1],
        reverse=True
    )
    return sorted_items[:top_k]


# =========================
# 5. 查询函数：相似度 top40 + rerank top25
# =========================
def search_with_scores(query, model, index, table_names, texts, reranker,
                       sim_top_k=40, rerank_top_k=25):
    # --- 第一步：embedding 相似度召回 top40 ---
    query_vec = model.encode(
        [query],
        normalize_embeddings=True
    ).astype("float32")

    scores, indices = index.search(query_vec, sim_top_k)

    sim_results = []
    for i in range(sim_top_k):
        idx = int(indices[0][i])
        score = float(scores[0][i])
        sim_results.append({
            "index": idx,
            "table_name": table_names[idx],
            "text": texts[idx],
            "similarity_score": score
        })

    # --- 第二步：rerank 精排 top25 ---
    candidate_indices = [int(i) for i in indices[0]]
    reranked = rerank(query, candidate_indices, texts, reranker, rerank_top_k)

    rerank_results = []
    for idx, r_score in reranked:
        sim_score = next(
            (r["similarity_score"] for r in sim_results if r["index"] == idx),
            None
        )
        rerank_results.append({
            "index": idx,
            "table_name": table_names[idx],
            "text": texts[idx],
            "similarity_score": sim_score,
            "rerank_score": float(r_score)
        })

    return sim_results, rerank_results


# =========================
# 6. 主流程
# =========================
if __name__ == "__main__":
    schema_path = "../sql/description/schema_texts.jsonl"
    index_dir = "../embedding/index"
    questions_path = "../question/olympedia_questions.jsonl"
    output_path = "../retrival_result/olympedia_questions_search_results.json"
    model_path = r"D:\models\huggingface_models"

    # ---- 加载模型 ----
    print("加载 embedding 模型...")
    model = SentenceTransformer(
        "BAAI/bge-m3",
        cache_folder=model_path,
        local_files_only=True
    )

    print("加载 reranker 模型...")
    reranker = CrossEncoder(
        "BAAI/bge-reranker-base",
        device="cpu",
        cache_folder=model_path,
        local_files_only=True
    )

    # ---- 加载 schema 数据和已有索引 ----
    print("加载 schema 数据...")
    texts, table_names = load_schema_texts(schema_path)

    print("加载 FAISS 索引...")
    index, _ = load_index(index_dir)

    # ---- 加载问题 ----
    print("加载问题数据...")
    items = load_questions(questions_path)
    print(f"共 {len(items)} 个问题")

    # ---- 逐问题检索表 ----
    all_results = []
    for i, item in enumerate(items):
        query = item["question"]
        print(f"[{i+1}/{len(items)}] 查询: {query}")

        sim_top40, rerank_top25 = search_with_scores(
            query, model, index, table_names, texts, reranker,
            sim_top_k=40,
            rerank_top_k=25
        )

        all_results.append({
            "id": item["id"],
            "question": query,
            "category": item.get("category", ""),
            "answer": item.get("answer", []),
            "similarity_top40": sim_top40,
            "rerank_top25": rerank_top25
        })

    # ---- 保存结果 ----
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存到 {output_path}")
    print(f"共处理 {len(all_results)} 个问题")
