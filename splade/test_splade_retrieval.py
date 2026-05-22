"""
Test script for SPLADE retrieval on Olympedia questions.
Retrieves from text, infobox, and table indices separately.
"""
import os
import sys
import json
from typing import List, Dict
from loguru import logger

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from olympedia_retrieval import OlympediaSpladeRetrieval


class OlympediaQuestionsRetriever:
    """
    Retrieve for Olympedia questions using different content type indices.
    """
    
    def __init__(self, 
                 corpus_base_path: str,
                 index_base_path: str,
                 model_path: str,
                 top_k: int = 10):
        """
        Initialize retrievers for different content types.
        
        Args:
            corpus_base_path: Base path for corpus files (e.g., "path/to/olympedia_corpus")
            index_base_path: Base path for index directories (e.g., "path/to/splade/indices")
            model_path: Path to SPLADE model
            top_k: Number of top results to retrieve
        """
        self.corpus_base_path = corpus_base_path
        self.index_base_path = index_base_path
        self.model_path = model_path
        self.top_k = top_k
        
        # Initialize retrievers for different content types
        self.retrievers = {}
        self._initialize_retrievers()
        
    def _initialize_retrievers(self):
        """Initialize retrievers for text, infobox, and table content types."""
        content_types = ["text", "infobox", "table"]
        
        for content_type in content_types:
            corpus_path = f"{self.corpus_base_path}_{content_type}.jsonl"
            index_path = os.path.join(self.index_base_path, f"olympedia_results_{content_type}_index")
            
            logger.info(f"Initializing {content_type} retriever...")
            logger.info(f"  Corpus path: {corpus_path}")
            logger.info(f"  Index path: {index_path}")
            
            try:
                retriever = OlympediaSpladeRetrieval(
                    corpus_path=corpus_path,
                    index_path=index_path,
                    model_path=self.model_path,
                    top_k=self.top_k,
                    category="results",
                    data_type=content_type
                )
                self.retrievers[content_type] = retriever
                logger.info(f"  ✓ {content_type} retriever initialized successfully")
            except Exception as e:
                logger.error(f"  ✗ Failed to initialize {content_type} retriever: {e}")
                self.retrievers[content_type] = None
    
    def retrieve_question(self, question: str, question_id: int = None) -> Dict:
        """
        Retrieve results for a single question across all content types.
        
        Args:
            question: The question text
            question_id: Optional question ID
            
        Returns:
            Dictionary with retrieval results for each content type
        """
        results = {
            "question": question,
            "question_id": question_id,
            "retrieval_results": {}
        }
        
        for content_type, retriever in self.retrievers.items():
            if retriever is None:
                logger.warning(f"Skipping {content_type} retrieval (retriever not initialized)")
                results["retrieval_results"][content_type] = {
                    "status": "error",
                    "message": "Retriever not initialized"
                }
                continue
            
            try:
                logger.info(f"Retrieving for {content_type}...")
                candidates = retriever.retrieve(question, top_k=self.top_k)
                
                # Format results
                formatted_results = []
                for i, cand in enumerate(candidates[:self.top_k], 1):
                    formatted_results.append({
                        "rank": i,
                        "id": cand["id"],
                        "score": float(cand["score"]),
                        "page_title": cand["data"].get("page_title", "N/A"),
                        "content_type": cand["data"].get("content_type", "N/A"),
                        "category": cand["data"].get("category", []),
                        "linearized": retriever._linearize_record(cand["data"])[:200] + "..." if len(retriever._linearize_record(cand["data"])) > 200 else retriever._linearize_record(cand["data"])
                    })
                
                results["retrieval_results"][content_type] = {
                    "status": "success",
                    "count": len(formatted_results),
                    "results": formatted_results
                }
                
                logger.info(f"  ✓ Retrieved {len(formatted_results)} results for {content_type}")
                
            except Exception as e:
                logger.error(f"  ✗ Error retrieving from {content_type}: {e}")
                results["retrieval_results"][content_type] = {
                    "status": "error",
                    "message": str(e)
                }
        
        return results
    
    def retrieve_questions_batch(self, questions_file: str, output_file: str = None, 
                                 max_questions: int = None) -> List[Dict]:
        """
        Retrieve results for multiple questions from a JSONL file.
        
        Args:
            questions_file: Path to questions JSONL file
            output_file: Optional output file to save results
            max_questions: Maximum number of questions to process (None for all)
            
        Returns:
            List of retrieval results
        """
        logger.info(f"Loading questions from {questions_file}")
        
        # Load questions
        questions = []
        with open(questions_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questions.append(json.loads(line.strip()))
        
        if max_questions:
            questions = questions[:max_questions]
        
        logger.info(f"Processing {len(questions)} questions")
        
        # Process each question
        all_results = []
        for i, q in enumerate(questions, 1):
            question_id = q.get("id")
            question_text = q.get("question", "")
            category = q.get("category", "Unknown")
            
            logger.info(f"\n[{i}/{len(questions)}] Processing question {question_id}: {question_text[:60]}...")
            logger.info(f"  Category: {category}")
            
            result = self.retrieve_question(question_text, question_id)
            result["category"] = category
            result["answer"] = q.get("answer", [])
            result["source"] = q.get("source", "")
            
            all_results.append(result)
            
            # Save results incrementally if output file is specified
            if output_file:
                self._save_result(result, output_file)
        
        logger.info(f"\n✓ Completed retrieval for {len(all_results)} questions")
        
        return all_results
    
    def _save_result(self, result: Dict, output_file: str):
        """Append a single result to output file in JSONL format."""
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')


def main():
    """Main function for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test SPLADE retrieval on Olympedia questions")
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
                       default="D:/Projects/pythonProject/retrival_result/olympedia_questions_splade_retrieval.jsonl",
                       help="Output file for retrieval results")
    parser.add_argument("--top_k", type=int, default=10,
                       help="Number of top results to retrieve per content type")
    parser.add_argument("--max_questions", type=int, default=None,
                       help="Maximum number of questions to process")
    parser.add_argument("--single_question", type=str, default=None,
                       help="Test a single question instead of batch processing")
    
    args = parser.parse_args()
    
    # Initialize retriever
    logger.info("=" * 80)
    logger.info("Olympedia Questions SPLADE Retrieval Test")
    logger.info("=" * 80)
    
    retriever = OlympediaQuestionsRetriever(
        corpus_base_path=args.corpus_base,
        index_base_path=args.index_base,
        model_path=args.model,
        top_k=args.top_k
    )
    
    # Check if retrievers were initialized successfully
    active_retrievers = [ct for ct, r in retriever.retrievers.items() if r is not None]
    if not active_retrievers:
        logger.error("No retrievers were initialized successfully. Please check paths and try again.")
        return
    
    logger.info(f"Active retrievers: {', '.join(active_retrievers)}")
    
    # Process single question or batch
    if args.single_question:
        logger.info(f"\nTesting single question: {args.single_question}")
        result = retriever.retrieve_question(args.single_question)
        print("\n" + "=" * 80)
        print("RETRIEVAL RESULTS")
        print("=" * 80)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # Clear output file if it exists
        if os.path.exists(args.output):
            os.remove(args.output)
            logger.info(f"Cleared existing output file: {args.output}")
        
        # Batch process questions
        results = retriever.retrieve_questions_batch(
            questions_file=args.questions,
            output_file=args.output,
            max_questions=args.max_questions
        )
        
        logger.info(f"\n✓ Results saved to: {args.output}")
        logger.info(f"Total questions processed: {len(results)}")
        
        # Print summary statistics
        print("\n" + "=" * 80)
        print("SUMMARY STATISTICS")
        print("=" * 80)
        for content_type in active_retrievers:
            success_count = sum(1 for r in results 
                              if r["retrieval_results"][content_type]["status"] == "success")
            total_results = sum(r["retrieval_results"][content_type].get("count", 0) 
                              for r in results 
                              if r["retrieval_results"][content_type]["status"] == "success")
            print(f"{content_type:10s}: {success_count}/{len(results)} questions, "
                  f"{total_results} total results")


if __name__ == "__main__":
    """
    Usage Examples:
    
    1. Test with default settings:
       python test_splade_retrieval.py
    
    2. Test with specific paths:
       python test_splade_retrieval.py \\
           --questions D:/Projects/pythonProject/question/olympedia_questions.jsonl \\
           --corpus_base D:/Projects/olympedia/data/olympedia_corpus_results \\
           --index_base D:/Projects/pythonProject/splade/indices \\
           --model D:/Projects/pythonProject/model/splade-cocondenser-ensembledistil \\
           --output D:/Projects/pythonProject/retrival_result/test_results.jsonl
    
    3. Test with limited questions:
       python test_splade_retrieval.py --max_questions 5
    
    4. Test a single question:
       python test_splade_retrieval.py \\
           --single_question "Olympians Who Set a World Record in Speed Skating"
    
    5. Test with different top_k:
       python test_splade_retrieval.py --top_k 20 --max_questions 3
    """
    main()