"""
Configuration file for SPLADE retrieval paths.
Update these paths according to your actual file locations.
"""

# ============================================================================
# PATH CONFIGURATION
# ============================================================================

# Base directory for the project
PROJECT_ROOT = "D:/Projects/pythonProject"

# SPLADE Model Path
SPLADE_MODEL_PATH = "D:/Projects/pythonProject/model/splade-cocondenser-ensembledistil"

# SPLADE Index Base Path (contains text, infobox, table subdirectories)
SPLADE_INDEX_BASE = "D:/Projects/pythonProject/splade/indices"

# Olympedia Questions File
QUESTIONS_FILE = "D:/Projects/pythonProject/question/olympedia_questions.jsonl"

# Output Directory for Retrieval Results
OUTPUT_DIR = "D:/Projects/pythonProject/retrival_result"

# ============================================================================
# CORPUS FILE PATHS
# ============================================================================

# ⚠️ IMPORTANT: Update these paths to your actual corpus file locations!
# These files are required for SPLADE retrieval.
# If you don't have these files, you may need to:
# 1. Download them from the original server
# 2. Generate them using process_raw_data_olympedia.py
# 3. Contact your team to get the files

# Option 1: If you have the corpus files in a separate directory
# CORPUS_BASE_DIR = "D:/Projects/olympedia/data/olympedia_corpus_results"

# Option 2: If you have the corpus files in the project directory ✓ (当前使用)
CORPUS_BASE_DIR = "D:/Projects/pythonProject/olympedia/olympedia_corpus_results"

# Option 3: If you have the corpus files in the original server path format
# CORPUS_BASE_DIR = "/2013006894/JZ/WIKIQA/WikiQA/data/alignment/olympedia/olympedia_corpus_results"

# Individual corpus file paths (auto-generated from CORPUS_BASE_DIR)
CORPUS_FILES = {
    "text": f"{CORPUS_BASE_DIR}_text.jsonl",
    "infobox": f"{CORPUS_BASE_DIR}_infobox.jsonl",
    "table": f"{CORPUS_BASE_DIR}_table.jsonl"
}

# ============================================================================
# RETRIEVAL PARAMETERS
# ============================================================================

# Default number of top results to retrieve per content type
DEFAULT_TOP_K = 10

# Minimum score threshold for retrieval (0.0 = no threshold)
DEFAULT_THRESHOLD = 0.0

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_corpus_path(content_type: str) -> str:
    """
    Get corpus file path for a specific content type.
    
    Args:
        content_type: One of 'text', 'infobox', 'table'
    
    Returns:
        Full path to the corpus file
    """
    if content_type not in CORPUS_FILES:
        raise ValueError(f"Invalid content_type: {content_type}. Must be one of {list(CORPUS_FILES.keys())}")
    return CORPUS_FILES[content_type]

def get_index_path(content_type: str) -> str:
    """
    Get index directory path for a specific content type.
    
    Args:
        content_type: One of 'text', 'infobox', 'table'
    
    Returns:
        Full path to the index directory
    """
    if content_type not in ["text", "infobox", "table"]:
        raise ValueError(f"Invalid content_type: {content_type}. Must be one of ['text', 'infobox', 'table']")
    return f"{SPLADE_INDEX_BASE}/results_{content_type}_index"

def validate_paths() -> dict:
    """
    Validate that all required paths exist.
    
    Returns:
        Dictionary with validation results for each path
    """
    import os
    
    results = {
        "model": {"path": SPLADE_MODEL_PATH, "exists": os.path.exists(SPLADE_MODEL_PATH)},
        "questions": {"path": QUESTIONS_FILE, "exists": os.path.exists(QUESTIONS_FILE)},
        "indices": {},
        "corpus": {}
    }
    
    # Check indices
    for content_type in ["text", "infobox", "table"]:
        index_path = get_index_path(content_type)
        results["indices"][content_type] = {
            "path": index_path,
            "exists": os.path.exists(index_path)
        }
    
    # Check corpus files
    for content_type, corpus_path in CORPUS_FILES.items():
        results["corpus"][content_type] = {
            "path": corpus_path,
            "exists": os.path.exists(corpus_path)
        }
    
    return results

def print_validation_results():
    """Print validation results in a readable format."""
    results = validate_paths()
    
    print("=" * 80)
    print("PATH VALIDATION RESULTS")
    print("=" * 80)
    
    # Model
    print(f"\nSPLADE Model:")
    print(f"  Path: {results['model']['path']}")
    print(f"  Status: {'✓ EXISTS' if results['model']['exists'] else '✗ NOT FOUND'}")
    
    # Questions
    print(f"\nQuestions File:")
    print(f"  Path: {results['questions']['path']}")
    print(f"  Status: {'✓ EXISTS' if results['questions']['exists'] else '✗ NOT FOUND'}")
    
    # Indices
    print(f"\nSPLADE Indices:")
    for content_type, info in results["indices"].items():
        print(f"  {content_type.upper()}:")
        print(f"    Path: {info['path']}")
        print(f"    Status: {'✓ EXISTS' if info['exists'] else '✗ NOT FOUND'}")
    
    # Corpus files
    print(f"\nCorpus Files:")
    for content_type, info in results["corpus"].items():
        print(f"  {content_type.upper()}:")
        print(f"    Path: {info['path']}")
        print(f"    Status: {'✓ EXISTS' if info['exists'] else '✗ NOT FOUND'}")
    
    print("\n" + "=" * 80)
    
    # Check if all required files exist
    model_exists = results['model']['exists']
    questions_exist = results['questions']['exists']
    indices_exist = all(info['exists'] for info in results['indices'].values())
    corpus_exist = all(info['exists'] for info in results['corpus'].values())
    
    all_exist = model_exists and questions_exist and indices_exist and corpus_exist
    
    if all_exist:
        print("✓ All paths are valid!")
    else:
        print("✗ Some paths are missing. Please update the configuration.")
        print("\nMissing files:")
        if not results['model']['exists']:
            print(f"  - SPLADE Model: {results['model']['path']}")
        if not results['questions']['exists']:
            print(f"  - Questions File: {results['questions']['path']}")
        for content_type, info in results["indices"].items():
            if not info['exists']:
                print(f"  - {content_type.upper()} Index: {info['path']}")
        for content_type, info in results["corpus"].items():
            if not info['exists']:
                print(f"  - {content_type.upper()} Corpus: {info['path']}")
    
    print("=" * 80)

if __name__ == "__main__":
    """Run validation when script is executed directly."""
    print_validation_results()