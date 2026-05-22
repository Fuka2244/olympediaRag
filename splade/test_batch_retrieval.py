"""
Batch test script for SPLADE retrieval on Olympedia questions.
Processes all questions from olympedia_questions.jsonl and retrieves from 
text, infobox, and table indices separately.
"""
import os
import sys
import json
from loguru import logger

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from olympedia_retrieval import OlympediaSpladeRetrieval


def batch_retrieve_questions(questions_file: str, 
                            corpus_base_path: str,
                            index_base_path: str,
                            model_path: str,
                            output_file: str,
                            top_k: int = 10,
                            max_questions: int = None):
    """
    Batch retrieve results for all questions.
    
    Args:
        questions_file: Path to questions JSONL file
        corpus_base_path: Base path for corpus files
        index_base_path: Base path for index directories
        model_path: Path to SPLADE model
        output_file: Output file for results
        top_k: Number of top results per content type
        max_questions: Maximum number of questions to process
    """
    
    logger.info("=" * 80)
    logger.info("SPLADE Retrieval Batch Test")
    logger.info("=" * 80)
    logger.info(f"Questions file: {questions_file}")
    logger.info(f"Corpus base path: {corpus_base_path}")
    logger.info(f"Index base path: {index_base_path}")
    logger.info(f"Model path: {model_path}")
    logger.info(f"Output file: {output_file}")
    logger.info(f"Top-K: {top_k}")
    logger.info("")
    
    # Load questions
    logger.info("Loading questions...")
    questions = []
    with open(questions_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                questions.append(json.loads(line.strip()))
    
    if max_questions:
        questions = questions[:max_questions]
        logger.info(f"Processing first {max_questions} questions")
    else:
        logger.info(f"Processing all {len(questions)} questions")
    
    logger.info("")
    
    # Initialize retrievers for each content type
    content_types = ["text", "infobox", "table"]
    retrievers = {}
    
    for content_type in content_types:
        corpus_path = f"{corpus_base_path}_{content_type}.jsonl"
        index_path = os.path.join(index_base_path, f"olympedia_results_{content_type}_index")
        
        logger.info(f"Initializing {content_type} retriever...")
        logger.info(f"  Corpus: {corpus_path}")
        logger.info(f"  Index: {index_path}")
        
        try:
            retriever = OlympediaSpladeRetrieval(
                corpus_path=corpus_path,
                index_path=index_path,
                model_path=model_path,
                top_k=top_k,
                category="results",
                data_type=content_type
            )
            retrievers[content_type] = retriever
            logger.info(f"  ✓ {content_type} retriever initialized")
        except Exception as e:
            logger.error(f"  ✗ Failed to initialize {content_type} retriever: {e}")
            retrievers[content_type] = None
        
        logger.info("")
    
    # Check if any retrievers were initialized
    active_retrievers = [ct for ct, r in retrievers.items() if r is not None]
    if not active_retrievers:
        logger.error("No retrievers were initialized successfully!")
        return
    
    logger.info(f"Active retrievers: {', '.join(active_retrievers)}")
    logger.info("")
    
    # Process each question
    logger.info("Starting batch retrieval...")
    logger.info("")
    
    # Clear output file if exists
    if os.path.exists(output_file):
        os.remove(output_file)
    
    results_summary = {
        "total_questions": len(questions),
        "processed": 0,
        "errors": 0,
        "by_content_type": {ct: {"success": 0, "errors": 0, "total_results": 0} 
                           for ct in content_types}
    }
    
    for i, q in enumerate(questions, 1):
        question_id = q.get("id")
        question_text = q.get("question", "")
        category = q.get("category", "Unknown")
        
        logger.info(f"[{i}/{len(questions)}] Question {question_id}: {question_text[:60]}...")
        logger.info(f"  Category: {category}")
        
        result = {
            "id": question_id,
            "question": question_text,
            "category": category,
            "answer": q.get("answer", []),
            "source": q.get("source", ""),
            "retrieval_results": {}
        }
        
        # Retrieve from each content type
        for content_type in active_retrievers:
            retriever = retrievers[content_type]
            
            try:
                candidates = retriever.retrieve(question_text, top_k=top_k)
                
                # Format results
                formatted_results = []
                for j, cand in enumerate(candidates[:top_k], 1):
                    formatted_results.append({
                        "rank": j,
                        "id": cand["id"],
                        "score": float(cand["score"]),
                        "page_title": cand["data"].get("page_title", "N/A"),
                        "content_type": cand["data"].get("content_type", "N/A"),
                        "category": cand["data"].get("category", []),
                        "content": cand["data"].get("content", {}),
                        "page_hierarchy": cand["data"].get("page_hierarchy", []),
                        "linearized": retriever._linearize_record(cand["data"])
                    })
                
                result["retrieval_results"][content_type] = {
                    "status": "success",
                    "count": len(formatted_results),
                    "results": formatted_results
                }
                
                # Update summary
                results_summary["by_content_type"][content_type]["success"] += 1
                results_summary["by_content_type"][content_type]["total_results"] += len(formatted_results)
                
                logger.info(f"  {content_type}: ✓ {len(formatted_results)} results")
                
            except Exception as e:
                logger.error(f"  {content_type}: ✗ Error: {e}")
                result["retrieval_results"][content_type] = {
                    "status": "error",
                    "message": str(e)
                }
                results_summary["by_content_type"][content_type]["errors"] += 1
        
        # Save result to output file
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')
        
        results_summary["processed"] += 1
        logger.info("")
    
    # Print summary
    logger.info("=" * 80)
    logger.info("BATCH RETRIEVAL SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Total questions: {results_summary['total_questions']}")
    logger.info(f"Successfully processed: {results_summary['processed']}")
    logger.info(f"Errors: {results_summary['errors']}")
    logger.info("")
    
    for content_type in content_types:
        summary = results_summary["by_content_type"][content_type]
        logger.info(f"{content_type.upper()}:")
        logger.info(f"  Successful retrievals: {summary['success']}")
        logger.info(f"  Errors: {summary['errors']}")
        logger.info(f"  Total results: {summary['total_results']}")
        logger.info("")
    
    logger.info(f"✓ Results saved to: {output_file}")
    
    return results_summary


if __name__ == "__main__":
    """
    Usage:
        # Process all questions with default settings
        python test_batch_retrieval.py
        
        # Process first 5 questions
        python test_batch_retrieval.py --max_questions 5
        
        # Process with custom top_k
        python test_batch_retrieval.py --top_k 20 --max_questions 3
    """
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch SPLADE retrieval on Olympedia questions")
    parser.add_argument("--questions", type=str, 
                       default="D:/Projects/pythonProject/question/olympedia_questions.jsonl",
                       help="Path to questions JSONL file")
    parser.add_argument("--corpus_base", type=str, 
                       default="D:/Projects/olympedia/data/olympedia_corpus_results",
                       help="Base path for corpus files")
    parser.add_argument("--index_base", type=str, 
                       default="D:/Projects/pythonProject/splade/indices",
                       help="Base path for index directories")
    parser.add_argument("--model", type=str, 
                       default="D:/Projects/pythonProject/model/splade-cocondenser-ensembledistil",
                       help="Path to SPLADE model")
    parser.add_argument("--output", type=str, 
                       default="D:/Projects/pythonProject/retrival_result/olympedia_questions_splade_batch.jsonl",
                       help="Output file for retrieval results")
    parser.add_argument("--top_k", type=int, default=10,
                       help="Number of top results to retrieve per content type")
    parser.add_argument("--max_questions", type=int, default=None,
                       help="Maximum number of questions to process")
    
    args = parser.parse_args()
    
    # Run batch retrieval
    summary = batch_retrieve_questions(
        questions_file=args.questions,
        corpus_base_path=args.corpus_base,
        index_base_path=args.index_base,
        model_path=args.model,
        output_file=args.output,
        top_k=args.top_k,
        max_questions=args.max_questions
    )