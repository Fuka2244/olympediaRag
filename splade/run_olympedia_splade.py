#!/usr/bin/env python3
"""
Unified script for building and using SPLADE index for Olympedia.
"""
import argparse
from calendar import c
import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.."))

from olympedia_index_construction import OlympediaIndexConstructor
from olympedia_retrieval import OlympediaSpladeRetrieval


def main():
    parser = argparse.ArgumentParser(description="Olympedia SPLADE Index and Retrieval")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Build index command
    build_parser = subparsers.add_parser("build", help="Build SPLADE index")
    build_parser.add_argument("--category", type=str, required=True,
                              help="Category of the Olympedia corpus")
    build_parser.add_argument("--data_type", type=str, required=True,
                              help="Data type of the Olympedia corpus")
    build_parser.add_argument("--corpus_path", type=str, required=True,
                              help="Path to the Olympedia corpus JSONL file")
    build_parser.add_argument("--index_path", type=str, required=True,
                              help="Path to save the SPLADE index")
    build_parser.add_argument("--model_path", type=str, required=True,
                              help="Path to the SPLADE model")
    build_parser.add_argument("--batch_size", type=int, default=32,
                              help="Batch size for encoding (default: 32)")
    build_parser.add_argument("--max_length", type=int, default=512,
                              help="Maximum sequence length (default: 512)")
    
    # Retrieve command
    retrieve_parser = subparsers.add_parser("retrieve", help="Retrieve from index")
    retrieve_parser.add_argument("--category", type=str, required=True,
                                 help="Category of the Olympedia corpus")
    retrieve_parser.add_argument("--data_type", type=str, required=True,
                                 help="Data type of the Olympedia corpus")
    retrieve_parser.add_argument("--corpus_path", type=str, required=True,
                                 help="Path to the Olympedia corpus JSONL file")
    retrieve_parser.add_argument("--index_path", type=str, required=True,
                                 help="Path to the SPLADE index")
    retrieve_parser.add_argument("--model_path", type=str, required=True,
                                 help="Path to the SPLADE model")
    retrieve_parser.add_argument("--query", type=str, required=True,
                                 help="Search query")
    retrieve_parser.add_argument("--top_k", type=int, default=10,
                                 help="Number of top results to return (default: 10)")
    
    args = parser.parse_args()
    
    if args.command == "build":
        constructor = OlympediaIndexConstructor()
        constructor.run(
            category=args.category,
            data_type=args.data_type,
            corpus_path=args.corpus_path,
            splade_index_path=args.index_path,
            model_path=args.model_path,
            batch_size=args.batch_size,
            max_length=args.max_length
        )
    elif args.command == "retrieve":
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
            print(f"   Text: {r['linearized'][:150]}...")
            print()
    else:
        parser.print_help()


if __name__ == "__main__":
    """
    Usage Examples:
    
    1. Build index:
       python run_olympedia_splade.py build \
           --category results \
           --data_type text \
           --corpus_path /path/to/olympedia_corpus.jsonl \
           --index_path /path/to/output_index \
           --model_path /path/to/splade-model \
           --batch_size 32 \
           --max_length 512
    
    2. Retrieve from index:
       python run_olympedia_splade.py retrieve \
           --category results \
           --data_type text \
           --corpus_path /path/to/olympedia_corpus.jsonl \
           --index_path /path/to/splade_index \
           --model_path /path/to/splade-model \
           --query "Sweden Giant Slalom 1952" \
           --top_k 10
    
    3. Quick test:
       # First build the index
       python run_olympedia_splade.py build \
           --category results \
           --data_type text \
           --corpus_path /path/to/corpus.jsonl \
           --index_path /path/to/index \
           --model_path /path/to/model
       
       # Then retrieve
       python run_olympedia_splade.py retrieve \
           --category results \
           --data_type text \
           --corpus_path /path/to/corpus.jsonl \
           --index_path /path/to/index \
           --model_path /path/to/model \
           --query "your query"
    """
    main()
