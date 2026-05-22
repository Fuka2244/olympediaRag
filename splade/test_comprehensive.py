"""
Comprehensive test script for SPLADE retrieval on Olympedia questions.
Tests retrieval from text, infobox, and table indices with detailed output.
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
    validate_paths
)


def test_single_detailed():
    """Test retrieval with detailed output and analysis."""
    
    # Validate paths first
    logger.info("Validating paths...")
    validation = validate_paths()
    
    # Check if corpus files exist
    missing_corpus = [ct for ct, info in validation["corpus"].items() if not info["exists"]]
    if missing_corpus:
        logger.error("✗ Corpus files not found!")
        logger.error("Please update CORPUS_BASE_DIR in config.py")
        return None
    
    # Test questions
    test_questions = [
        {
            "id": 277,
            "question": "Olympians Who Set a World Record in Speed Skating",
            "category": "Winter Sports",
            "expected_keywords": ["speed skating", "world record", "olympian"]
        },
        {
            "id": 231,
            "question": "Olympic Equestrian Riders - Winning Medals in Dressage and Jumping",
            "category": "Equestrian",
            "expected_keywords": ["equestrian", "dressage", "jumping", "medal"]
        },
        {
            "id": 236,
            "question": "Olympic Divers - Individual Double Champions, Different Years",
            "category": "Aquatics",
            "expected_keywords": ["diving", "champion", "individual"]
        }
    ]
    
    logger.info("=" * 80)
    logger.info("SPLADE Retrieval Comprehensive Test")
    logger.info("=" * 80)
    logger.info(f"Testing {len(test_questions)} questions")
    logger.info("")
    
    all_results = {}
    
    for i, test_q in enumerate(test_questions, 1):
        question = test_q["question"]
        question_id = test_q["id"]
        category = test_q["category"]
        expected_keywords = test_q["expected_keywords"]
        
        logger.info(f"[{i}/{len(test_questions)}] Testing question {question_id}")
        logger.info(f"  Question: {question}")
        logger.info(f"  Category: {category}")
        logger.info(f"  Expected keywords: {', '.join(expected_keywords)}")
        logger.info("")
        
        results = {}
        
        # Test each content type
        for content_type, corpus_path in CORPUS_FILES.items():
            logger.info(f"  Testing {content_type.upper()} retrieval...")
            logger.info(f"    Corpus: {corpus_path}")
            
            index_path = os.path.join(SPLADE_INDEX_BASE, f"olympedia_results_{content_type}_index")
            
            try:
                # Initialize retriever
                retriever = OlympediaSpladeRetrieval(
                    corpus_path=corpus_path,
                    index_path=index_path,
                    model_path=SPLADE_MODEL_PATH,
                    top_k=10,
                    category="results",
                    data_type=content_type
                )
                
                # Perform retrieval
                candidates = retriever.retrieve(question, top_k=10)
                
                # Store results
                results[content_type] = {
                    "status": "success",
                    "count": len(candidates),
                    "results": []
                }
                
                # Format results
                for j, cand in enumerate(candidates[:10], 1):
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
                    results[content_type]["results"].append(result_info)
                
                logger.info(f"    ✓ Retrieved {len(candidates)} results")
                
                # Show top 3 results
                logger.info(f"    Top 3 results:")
                for j, res in enumerate(results[content_type]["results"][:3], 1):
                    logger.info(f"      {j}. Score: {res['score']:.4f} | {res['page_title']}")
                
            except Exception as e:
                logger.error(f"    ✗ Error: {e}")
                results[content_type] = {
                    "status": "error",
                    "message": str(e)
                }
            
            logger.info("")
        
        all_results[question_id] = {
            "question": question,
            "category": category,
            "expected_keywords": expected_keywords,
            "retrieval_results": results
        }
        
        logger.info("-" * 80)
        logger.info("")
    
    # Save comprehensive results
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "comprehensive_test_results.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    logger.info("=" * 80)
    logger.info("COMPREHENSIVE TEST SUMMARY")
    logger.info("=" * 80)
    
    for qid, result in all_results.items():
        logger.info(f"\nQuestion {qid}: {result['question'][:50]}...")
        for content_type, retrieval_result in result["retrieval_results"].items():
            status = retrieval_result["status"]
            if status == "success":
                count = retrieval_result["count"]
                logger.info(f"  {content_type.upper():10s}: ✓ {count} results")
            else:
                logger.info(f"  {content_type.upper():10s}: ✗ {retrieval_result['message']}")
    
    logger.info(f"\n✓ Comprehensive results saved to: {output_file}")
    
    return all_results


def test_batch_sample():
    """Test batch retrieval with a small sample of questions."""
    
    logger.info("=" * 80)
    logger.info("SPLADE Retrieval Batch Test (Sample)")
    logger.info("=" * 80)
    
    # Load questions
    questions_file = "D:/Projects/pythonProject/question/olympedia_questions.jsonl"
    
    logger.info(f"Loading questions from {questions_file}")
    questions = []
    with open(questions_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                questions.append(json.loads(line.strip()))
    
    # Test with first 3 questions
    sample_size = 3
    sample_questions = questions[:sample_size]
    
    logger.info(f"Testing with first {sample_size} questions")
    logger.info("")
    
    results = []
    
    for i, q in enumerate(sample_questions, 1):
        question_id = q.get("id")
        question_text = q.get("question", "")
        category = q.get("category", "Unknown")
        
        logger.info(f"[{i}/{sample_size}] Question {question_id}: {question_text[:60]}...")
        
        result = {
            "id": question_id,
            "question": question_text,
            "category": category,
            "retrieval_results": {}
        }
        
        # Retrieve from each content type
        for content_type, corpus_path in CORPUS_FILES.items():
            index_path = os.path.join(SPLADE_INDEX_BASE, f"olympedia_results_{content_type}_index")
            
            try:
                retriever = OlympediaSpladeRetrieval(
                    corpus_path=corpus_path,
                    index_path=index_path,
                    model_path=SPLADE_MODEL_PATH,
                    top_k=5,
                    category="results",
                    data_type=content_type
                )
                
                candidates = retriever.retrieve(question_text, top_k=5)
                
                result["retrieval_results"][content_type] = {
                    "status": "success",
                    "count": len(candidates),
                    "top_result": {
                        "id": candidates[0]["id"],
                        "score": float(candidates[0]["score"]),
                        "title": candidates[0]["data"].get("page_title", "N/A")
                    } if candidates else None
                }
                
                logger.info(f"  {content_type}: ✓ {len(candidates)} results")
                
            except Exception as e:
                logger.error(f"  {content_type}: ✗ {e}")
                result["retrieval_results"][content_type] = {
                    "status": "error",
                    "message": str(e)
                }
        
        results.append(result)
        logger.info("")
    
    # Save batch results
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "batch_test_sample_results.jsonl")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')
    
    logger.info(f"✓ Batch results saved to: {output_file}")
    
    return results


if __name__ == "__main__":
    """
    Usage:
        # Run comprehensive test
        python test_comprehensive.py
        
        # Run batch sample test
        python test_comprehensive.py --batch
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Comprehensive SPLADE retrieval tests")
    parser.add_argument("--batch", action="store_true", help="Run batch sample test instead of comprehensive test")
    args = parser.parse_args()
    
    if args.batch:
        test_batch_sample()
    else:
        test_single_detailed()