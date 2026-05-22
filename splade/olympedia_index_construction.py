"""
Class to create a sparse index of the Olympedia corpus.
Adapted for JSONL format with text and table content types.
"""
import os
import sys
import json
import pickle
import torch
import numpy as np
import pandas as pd
from torch.utils.data import Dataset
from torch.utils.data.dataloader import DataLoader
from tqdm.auto import tqdm
from transformers import AutoTokenizer
from loguru import logger

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.."))

from inverted_index import IndexDictOfArray
from models import Splade


def move_model(model, device):
    """
    Function to move the model to the given device.
    """
    if device == torch.device("cuda"):
        model.eval()
        if torch.cuda.device_count() > 1:
            model = torch.nn.DataParallel(model)
        model.to(device)
    else:
        model.to(device)


class OlympediaCollectionDataset(Dataset):
    """
    Dataset to iterate over Olympedia corpus in JSONL format.
    Format per line: JSON object with id, page_title, content_type, content fields.
    """

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.id_dict = {}      # dict storing the doc id
        self.text_dict = {}    # dict storing the linearized text for indexing
        self.data_dict = {}    # dict storing the full data
        
        logger.info(f"Preloading Olympedia dataset at {data_path}")

        # loading dataset from JSONL
        with open(data_path, "r", encoding="utf-8") as fp:
            for i, line in enumerate(fp):
                record = json.loads(line.strip())
                doc_id = record["id"]
                self.id_dict[i] = doc_id
                self.text_dict[i] = self._linearize_record(record)
                self.data_dict[i] = record
                
        self.collection_size = len(self.id_dict)
        logger.info(f"Loaded {self.collection_size} documents")

    def __len__(self):
        return self.collection_size

    def __getitem__(self, idx):
        return {
            "id": self.id_dict[idx],
            "text": self.text_dict[idx],
            "data": self.data_dict[idx]
        }
    
    @staticmethod
    def _join_meta_parts(parts) -> str:
        """Join list-like metadata with '; '; skip empty; coerce items to str."""
        if not parts:
            return ""
        return "; ".join(str(p) for p in parts if p is not None and str(p).strip() != "")

    @staticmethod
    def _content_dict_to_index_text(content: dict) -> str:
        """
        Table / infobox ``content`` is often a flat dict of column -> string.
        Skip ``links`` (list of dicts) — serializing it adds noise and unstable repr for SPLADE.
        """
        skip = {"links"}
        pieces = []
        for k, v in content.items():
            if k in skip:
                continue
            if isinstance(v, (dict, list)):
                continue
            pieces.append(f"{k}: {v}")
        return " ".join(pieces)

    def _linearize_record(self, record: dict) -> str:
        """Convert record to text for SPLADE indexing."""
        page_title = record.get("page_title", "") or ""
        content_type = record.get("content_type", "")
        category = record.get("category", [])
        page_hierarchy = record.get("page_hierarchy", [])
        content = record.get("content", {})

        # ``page_hierarchy`` is the same path as extractor ``content_path`` (section chain; no separate section_title).
        header = "\n".join(
            x
            for x in (
                page_title,
                self._join_meta_parts(category),
                self._join_meta_parts(page_hierarchy),
            )
            if x
        )

        if content_type == "text":
            text_content = content.get("text", "") if isinstance(content, dict) else ""
            return f"{header}\n{text_content}".strip()
        if content_type in ("table", "infobox"):
            if not isinstance(content, dict):
                content = {}
            table_text = self._content_dict_to_index_text(content)
            return f"{header}\n{table_text}".strip()
        return page_title
    
    def to_df(self):
        """Converts the dataset into a Pandas DataFrame."""
        df = pd.DataFrame.from_dict(self.data_dict, orient="index")
        return df


class OlympediaCollectionDataLoader(DataLoader):
    """
    Dataloader for the Olympedia collection.
    Based on https://github.com/naver/splade.
    """
    def __init__(self, tokenizer_type, max_length, **kwargs):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_type, clean_up_tokenization_spaces=True)
        self.max_length = max_length
        super().__init__(collate_fn=self.collate_fn, **kwargs, pin_memory=True)

    def collate_fn(self, batch):
        """
        batch is a list of dicts with keys: id, text, data
        """
        ids = [item["id"] for item in batch]
        texts = [item["text"] for item in batch]
        data = [item["data"] for item in batch]
        
        processed = self.tokenizer(
            texts,
            add_special_tokens=True,
            padding="longest",  # pad to max sequence length in batch
            truncation="longest_first",  # truncates to self.max_length
            max_length=self.max_length,
            return_attention_mask=True
        )
        return {
            **{k: torch.tensor(v) for k, v in processed.items()},
            "id": ids,
            "data": data
        }


class SparseIndexing:
    """
    Class that processes the entire collection and constructs the corresponding inverted index.
    Based on https://github.com/naver/splade.
    """
    def __init__(self, splade_index_path, model, splade_config, dim_voc=None, force_new=True, **kwargs):
        self.model = model
        self.model_path = splade_config["splade_model_type_or_path"]
        self.splade_config = splade_config
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        move_model(self.model, self.device)
        self.index_dir = splade_index_path
        
        self.sparse_index = IndexDictOfArray(self.index_dir, dim_voc=dim_voc, force_new=force_new)

    def run(self, collection_loader, id_dict=None):
        # encode documents
        doc_ids = []
        count = 0
        with torch.no_grad():
            for t, batch in enumerate(tqdm(collection_loader)):
                inputs = {k: v.to(self.device) for k, v in batch.items() if k not in {"id", "data"}}
                batch_documents = self.model(d_kwargs=inputs)["d_rep"]
                row, col = torch.nonzero(batch_documents, as_tuple=True)
                data = batch_documents[row, col]
                row = row + count
                batch_ids = batch["id"]
                if id_dict:
                    batch_ids = [id_dict[x] for x in batch_ids]
                count += len(batch_ids)
                doc_ids.extend(batch_ids)
                self.sparse_index.add_batch_document(row.cpu().numpy(), col.cpu().numpy(), data.cpu().numpy(), n_docs=len(batch_ids))
        
        # store index or return to caller function
        if self.index_dir is not None:
            self.sparse_index.save()
            pickle.dump(doc_ids, open(os.path.join(self.index_dir, "doc_ids.pkl"), "wb"))
            logger.info("Done indexing over the corpus...")
            logger.info("Index contains {} posting lists".format(len(self.sparse_index)))
            logger.info("Index contains {} documents".format(len(doc_ids)))
        else:
            # if no index_dir, we do not write the index to disk but return it
            for key in list(self.sparse_index.index_doc_id.keys()):
                # convert to numpy
                self.sparse_index.index_doc_id[key] = np.array(self.sparse_index.index_doc_id[key], dtype=np.int32)
                self.sparse_index.index_doc_value[key] = np.array(self.sparse_index.index_doc_value[key], dtype=np.float32)
            out = {"index": self.sparse_index, "ids_mapping": doc_ids}
            return out


class OlympediaIndexConstructor:
    """
    Build SPLADE index for Olympedia corpus.
    """
    def run(
        self,
        corpus_path: str,
        splade_index_path: str,
        model_path: str,
        max_length: int = 512,
        batch_size: int = 32,
        category: str = "",
        data_type: str = "",
    ):
        if category or data_type:
            logger.info(
                "Building SPLADE index (category={!r}, data_type={!r}) from {}",
                category,
                data_type,
                corpus_path,
            )

        # Initialize model
        model = Splade(model_path, agg="max")

        # Create dataset
        dataset = OlympediaCollectionDataset(data_path=corpus_path)

        # Create dataloader - use model_path for tokenizer to avoid downloading from HuggingFace
        d_loader = OlympediaCollectionDataLoader(
            dataset=dataset,
            tokenizer_type=model_path,
            max_length=max_length,
            batch_size=batch_size,
            shuffle=False,
            num_workers=0,
        )

        # Build index
        indexing = SparseIndexing(
            splade_index_path=splade_index_path,
            model=model,
            splade_config={
                "splade_model_type_or_path": model_path,
                "splade_tokenizer_type": model_path
            }
        )
        indexing.run(d_loader)
        logger.info(f"Index built successfully at {splade_index_path}")


def build_olympedia_index():
    """CLI entry point for building Olympedia index."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", type=str, required=True,
                        help="Category of the Olympedia corpus")
    parser.add_argument("--data_type", type=str, required=True,
                        help="Data type of the Olympedia corpus")
    parser.add_argument("--corpus_path", type=str, required=True,
                        help="Path to the Olympedia corpus JSONL file")
    parser.add_argument("--index_path", type=str, required=True,
                        help="Path to save the SPLADE index")
    parser.add_argument("--model_path", type=str, required=True,
                        help="Path to the SPLADE model")
    parser.add_argument("--batch_size", type=int, default=32,
                        help="Batch size for encoding (default: 32)")
    parser.add_argument("--max_length", type=int, default=512,
                        help="Maximum sequence length (default: 512)")
    args = parser.parse_args()
    
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


if __name__ == "__main__":
    """
    Usage Examples:
    
    1. Build index:
       python olympedia_index_construction.py \
           --category results \
           --data_type text \
           --corpus_path /path/to/olympedia_corpus_{category}_{data_type}.jsonl \
           --index_path /path/to/output_index \
           --model_path /path/to/splade-model \
           --batch_size 32 \
           --max_length 512
    
    2. Build index with larger batch size:
       python olympedia_index_construction.py \
           --category results \
           --data_type text \
           --corpus_path /path/to/olympedia_corpus_{category}_{data_type}.jsonl \
           --index_path /path/to/output_index \
           --model_path /path/to/splade-model \
           --batch_size 64 \
           --max_length 512
    """
    build_olympedia_index()
