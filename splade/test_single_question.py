"""SPLADE retrieval test script for Olympedia questions.
Reads questions from olympedia_questions.jsonl and saves results every 10 questions.
"""
import os
import sys
import json
from loguru import logger

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from olympedia_retrieval import OlympediaSpladeRetrieval
from config import (
    CORPUS_FILES,
    SPLADE_INDEX_BASE,
    SPLADE_MODEL_PATH,
    OUTPUT_DIR,
    validate_paths,
    QUESTIONS_FILE
)


def load_questions(questions_file):
    """Load questions from JSONL file."""
    logger.info(f"Loading questions from {questions_file}")
    questions = []
    with open(questions_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                questions.append(json.loads(line.strip()))
    logger.info(f"✓ Loaded {len(questions)} questions")
    return questions


def retrieve_for_question(question_data, retrievers, top_k=25):
    """Perform retrieval for a single question using pre-initialized retrievers."""
    question_id = question_data.get("id")
    question_text = question_data.get("question", "")
    category = question_data.get("category", "Unknown")
    
    logger.info(f"Processing question {question_id}: {question_text[:60]}...")
    
    result = {
        "id": question_id,
        "question": question_text,
        "category": category,
        "retrieval_results": {}
    }
    
    # Retrieve from each content type
    for content_type, retriever in retrievers.items():
        try:
            candidates = retriever.retrieve(question_text, top_k=top_k)
            
            result["retrieval_results"][content_type] = {
                "status": "success",
                "count": len(candidates),
                "results": []
            }
            
            # Format results with full content
            for j, cand in enumerate(candidates[:top_k], 1):
                result_info = {
                    "rank": j,
                    "id": cand["id"],
                    "score": float(cand["score"]),
                    "page_title": cand["data"].get("page_title", "N/A"),
                    "content_type": cand["data"].get("content_type", "N/A"),
                    "category": cand["data"].get("category", []),
                    "content": cand["data"].get("content", {}),
                    "page_hierarchy": cand["data"].get("page_hierarchy", []),
                    "linearized": retriever._linearize_record(cand["data"])
                }
                result["retrieval_results"][content_type]["results"].append(result_info)
            
            logger.info(f"  {content_type}: ✓ {len(candidates)} results")
            
        except Exception as e:
            logger.error(f"  {content_type}: ✗ {e}")
            result["retrieval_results"][content_type] = {
                "status": "error",
                "message": str(e)
            }
    
    return result


def initialize_retrievers(top_k=25):
    """Initialize retrievers for all content types."""
    logger.info("Initializing retrievers...")
    
    retrievers = {}
    
    for content_type, corpus_path in CORPUS_FILES.items():
        logger.info(f"  Initializing {content_type.upper()} retriever...")
        index_path = os.path.join(SPLADE_INDEX_BASE, f"olympedia_results_{content_type}_index")
        
        try:
            retriever = OlympediaSpladeRetrieval(
                corpus_path=corpus_path,
                index_path=index_path,
                model_path=SPLADE_MODEL_PATH,
                top_k=top_k,
                category="results",
                data_type=content_type
            )
            retrievers[content_type] = retriever
            logger.info(f"  ✓ {content_type.upper()} retriever initialized")
        except Exception as e:
            logger.error(f"  ✗ Failed to initialize {content_type.upper()} retriever: {e}")
            raise
    
    logger.info("✓ All retrievers initialized")
    return retrievers


def save_batch_results(results, output_file, batch_num, total_batches):
    """Save batch results to JSONL file."""
    logger.info(f"Saving batch {batch_num}/{total_batches} to {output_file}")
    
    with open(output_file, 'a', encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')
    
    logger.info(f"✓ Saved {len(results)} results to {output_file}")


def process_questions_batch(questions, retrievers, output_file, batch_size=10, top_k=25):
    """Process questions in batches and save results periodically."""
    total_questions = len(questions)
    total_batches = (total_questions + batch_size - 1) // batch_size
    
    logger.info("=" * 80)
    logger.info("SPLADE Retrieval - Batch Processing")
    logger.info("=" * 80)
    logger.info(f"Total questions: {total_questions}")
    logger.info(f"Batch size: {batch_size}")
    logger.info(f"Top K results: {top_k}")
    logger.info(f"Total batches: {total_batches}")
    logger.info(f"Output file: {output_file}")
    logger.info("")
    
    # Clear output file if it exists
    if os.path.exists(output_file):
        logger.info(f"Clearing existing output file: {output_file}")
        open(output_file, 'w').close()
    
    # Process questions in batches
    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, total_questions)
        batch_questions = questions[start_idx:end_idx]
        
        logger.info(f"Processing batch {batch_num + 1}/{total_batches} (questions {start_idx + 1}-{end_idx})")
        logger.info("-" * 80)
        
        batch_results = []
        
        for i, question_data in enumerate(batch_questions):
            question_idx = start_idx + i + 1
            logger.info(f"[{question_idx}/{total_questions}] ", end="")
            
            result = retrieve_for_question(question_data, retrievers, top_k=top_k)
            batch_results.append(result)
        
        # Save batch results
        save_batch_results(batch_results, output_file, batch_num + 1, total_batches)
        logger.info("")
    
    logger.info("=" * 80)
    logger.info("✓ All questions processed successfully")
    logger.info("=" * 80)
    logger.info(f"Total results saved to: {output_file}")


def test_all_questions(top_k=25):
    """Test retrieval for all questions in the questions file."""
    
    # Validate paths first
    logger.info("Validating paths...")
    validation = validate_paths()
    
    # Check if corpus files exist
    missing_corpus = [ct for ct, info in validation["corpus"].items() if not info["exists"]]
    if missing_corpus:
        logger.error("✗ Corpus files not found!")
        logger.error("Please update CORPUS_BASE_DIR in config.py")
        logger.error("\nMissing corpus files:")
        for ct in missing_corpus:
            logger.error(f"  - {ct}: {validation['corpus'][ct]['path']}")
        logger.error("\nYou need to:")
        logger.error("1. Download/copy the corpus files to the correct location")
        logger.error("2. Or update the CORPUS_BASE_DIR in config.py to point to your files")
        return None
    
    # Load questions
    questions = load_questions(QUESTIONS_FILE)
    
    if not questions:
        logger.error("✗ No questions loaded!")
        return None
    
    # Initialize retrievers
    retrievers = initialize_retrievers(top_k=top_k)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "olympedia_questions_splade_results.jsonl")
    
    # Process questions in batches
    process_questions_batch(questions, retrievers, output_file, batch_size=10, top_k=top_k)
    
    return output_file


if __name__ == "__main__":
    """
    Usage:
        # Process all questions with top 25 results (saves every 10 questions)
        python test_single_question.py
        
        # Process with custom batch size and top K
        python test_single_question.py --batch_size 5 --top_k 10
        
        # Process limited number of questions
        python test_single_question.py --max_questions 20 --top_k 25
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="SPLADE retrieval for Olympedia questions")
    parser.add_argument("--batch_size", type=int, default=10, help="Number of questions to process before saving (default: 10)")
    parser.add_argument("--top_k", type=int, default=25, help="Number of top results to retrieve per content type (default: 25)")
    parser.add_argument("--max_questions", type=int, default=None, help="Maximum number of questions to process (default: all)")
    args = parser.parse_args()
    
    # Load questions
    questions = load_questions(QUESTIONS_FILE)
    
    # Limit questions if specified
    if args.max_questions:
        questions = questions[:args.max_questions]
        logger.info(f"Processing first {args.max_questions} questions only")
    
    # Validate paths
    validation = validate_paths()
    missing_corpus = [ct for ct, info in validation["corpus"].items() if not info["exists"]]
    if missing_corpus:
        logger.error("✗ Corpus files not found!")
        logger.error("Please update CORPUS_BASE_DIR in config.py")
        sys.exit(1)
    
    # Initialize retrievers with top_k
    retrievers = initialize_retrievers(top_k=args.top_k)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "olympedia_questions_splade_results.jsonl")
    
    # Process questions in batches
    process_questions_batch(questions, retrievers, output_file, batch_size=args.batch_size, top_k=args.top_k)