"""
SPLADE retrieval for Olympedia corpus.
"""
import os
import sys
import pandas as pd
import torch
from typing import List, Dict, Optional
from loguru import logger

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.."))

from sparse_retrieval import SparseRetrieval
from models import Splade
from olympedia_index_construction import OlympediaCollectionDataset


class OlympediaSpladeRetrieval:
    """
    SPLADE retrieval for Olympedia corpus.
    """
    def __init__(self,
                 corpus_path: str,
                 index_path: str,
                 model_path: str,
                 threshold: float = 0.0,
                 top_k: int = 100,
                 category: str = "",
                 data_type: str = ""):

        self.corpus_path = corpus_path
        self.index_path = index_path
        self.model_path = model_path
        self.threshold = threshold
        self.top_k = top_k
        self.category = category
        self.data_type = data_type
        # Load model
        self.model = Splade(model_path, agg="max")
        self.dim_voc = self.model.output_dim

        # Load collection
        self.collection = OlympediaCollectionDataset(data_path=corpus_path)
        self.corpus_df = self.collection.to_df()

        # Initialize retrieval - use model_path for tokenizer to avoid downloading from HuggingFace
        self.sparse_retrieval = SparseRetrieval(
            splade_config={
                "splade_tokenizer_type": model_path,
                "splade_model_type_or_path": model_path
            },
            model=self.model,
            collection=self.collection,
            dim_voc=self.dim_voc,
            splade_index_path=index_path
        )

        logger.info(f"OlympediaSpladeRetrieval initialized with index at {index_path}")
        logger.info(f"Collection size: {len(self.collection)}")

    def retrieve(self, query: str, top_k: Optional[int] = None, threshold: Optional[float] = None) -> List[Dict]:
        """
        Retrieve documents for a query.
        
        Args:
            query: Search query string
            top_k: Number of top results to return (default: self.top_k)
            threshold: Minimum score threshold (default: self.threshold)
            
        Returns:
            List of retrieved documents with scores
        """
        top_k = top_k if top_k is not None else self.top_k
        threshold = threshold if threshold is not None else self.threshold
        
        candidates, bow_rep = self.sparse_retrieval.retrieve(
            query=query,
            involve_model=True,
            top_k=top_k if top_k > 0 else 0,
            threshold=threshold
        )
        
        logger.debug(f"Retrieved {len(candidates)} candidates for query: {query[:50]}...")
        
        return candidates
    
    def retrieve_with_linearization(self, query: str, **kwargs) -> List[Dict]:
        """
        Retrieve and return documents with linearized text for display.
        """
        candidates = self.retrieve(query, **kwargs)
        
        # Add linearized text to results
        for cand in candidates:
            record = cand["data"]
            cand["linearized"] = self._linearize_record(record)
            
        return candidates
    
    def _linearize_record(self, record: dict) -> str:
        """Convert record to text (same logic as dataset)."""
        page_title = record.get("page_title", "")
        content_type = record.get("content_type", "")
        page_hierarchy = record.get("page_hierarchy", [])
        category = record.get("category", [])
        #inks = record.get("links", [])
        #etadata = record.get("metadata", {})
        content = record.get("content", {})
        passage_id = record.get("passage_id", None)
        
        if content_type == "text":
            text_content = content.get("text", "")
            return f"{page_title} | {category} | {page_hierarchy} | {passage_id} | {text_content}".strip()
        elif content_type == "table" or content_type == "infobox":
            table_text = " ".join([f"{k}: {v}" for k, v in content.items()])
            return f"{page_title} | {category} | {page_hierarchy} | {table_text}".strip()
        else:
            return f"{page_title} | {category} | {page_hierarchy}".strip()
    
    def batch_retrieve(self, queries: List[str], **kwargs) -> List[List[Dict]]:
        """
        Retrieve documents for multiple queries.
        """
        results = []
        for query in queries:
            results.append(self.retrieve(query, **kwargs))
        return results


def main():
    """CLI for testing retrieval."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", type=str, required=True,
                        help="Category of the Olympedia corpus")
    parser.add_argument("--data_type", type=str, required=True,
                        help="Data type of the Olympedia corpus")
    parser.add_argument("--corpus_path", type=str, required=True,
                        help="Path to the Olympedia corpus JSONL file")
    parser.add_argument("--index_path", type=str, required=True,
                        help="Path to the SPLADE index")
    parser.add_argument("--model_path", type=str, required=True,
                        help="Path to the SPLADE model")
    parser.add_argument("--query", type=str, required=True,
                        help="Search query")
    parser.add_argument("--top_k", type=int, default=10,
                        help="Number of top results to return (default: 10)")
    args = parser.parse_args()
    
    retrieval = OlympediaSpladeRetrieval(
        category=args.category,
        data_type=args.data_type,
        corpus_path=args.corpus_path,
        index_path=args.index_path,
        model_path=args.model_path,
        top_k=args.top_k
    )
    
    results = retrieval.retrieve_with_linearization(args.query)
    
    print(f"\nQuery: {args.query}")
    print(f"Top {len(results)} results:")
    print("-" * 80)
    for i, r in enumerate(results[:args.top_k], 1):
        print(f"{i}. ID: {r['id']}, Score: {r['score']:.4f}")
        print(f"   Title: {r['data'].get('page_title', 'N/A')}")
        print(f"   Date: {r['data'].get('data', 'N/A')}")
        print(f"   Text: {r['linearized'][:150]}...")
        print()


if __name__ == "__main__":
    """
    Usage Examples:
    
    1. Retrieve with query:
       python olympedia_retrieval.py \
           --category results \
           --data_type text \
           --corpus_path /path/to/olympedia_corpus_{category}_{data_type}.jsonl \
           --index_path /path/to/splade_index \
           --model_path /path/to/splade-model \
           --query "Germany table tennis Olympic" \
           --top_k 10
    
    2. Retrieve with more results:
       python olympedia_retrieval.py \
           --category results \
           --data_type text \
           --corpus_path /path/to/olympedia_corpus_{category}_{data_type}.jsonl \
           --index_path /path/to/splade_index \
           --model_path /path/to/splade-model \
           --query "Swimming world record" \
           --top_k 20
    """
    main()
