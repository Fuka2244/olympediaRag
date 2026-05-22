import glob, json
from typing import Dict, List, Optional

"""
This code is to process the orignal corpus: Wikidata, Wikipedia, Olympedia and Olympics, and convert the corpus into the uniform frame format. 
Since each corpus has different data format, we write separate processing functions for each corpus. The processed corpus will be used for the subsequent alignment and retrieval steps, etc.

"""

def process_olympics(category:Optional[str]="athletes", data_type:Optional[str]=None):
    olympics_file = "./data/olympics/extracted_data/olympics.jsonl"
    frames = list()
    frame_count = 0
    frames.extend(_process_olympics_corpus_file(olympics_file, frame_count, category, data_type))
    print(f"Total length of olympics corpus: {len(frames)}")
    output_path = f"./data/alignment/olympics/olympics_corpus_{category}_{data_type}.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for frame in frames:
            f.write(json.dumps(frame, ensure_ascii=False) + "\n")

def _process_olympics_corpus_file(file: str, frame_count: int, category:Optional[str]=None, data_type:Optional[str]=None) -> List[Dict]:
    frames = list()
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row_data = json.loads(line)
                new_frames = process_olympics_raw_data(row_data, frame_count, category, data_type)

                if new_frames:
                    frames.extend(new_frames)
                    frame_count += len(new_frames)
            except json.JSONDecodeError:
                print (f"Error in line: {line}")
                continue
    return frames

def process_olympics_raw_data(row_data: Dict, frame_count: int, category:Optional[str]=None, data_type:Optional[str]=None) -> List[Dict]:
    new_frames = list()
    page_title = row_data["page_title"]
    source = row_data["source"]
    categories = [row_data.get("category", "")]
    if category and category not in categories:
        return new_frames
    for unit in row_data.get("data_units", []):
        unit_type = unit["data_type"].lower()
        if data_type and unit_type != data_type.lower():
            continue
        if unit_type == "text":
            for p in unit.get("content", []):
                frame = {
                    'id': frame_count,
                    'source': source,
                    'page_title': page_title,
                    'category': categories,
                    'page_hierarchy': unit.get("content_path", []),
                    'content_type': unit_type,
                    'passage_id': p.get("pid"),
                    'links': unit.get("links", []),
                    'content': {"text": p.get("text", "")}
                }
                new_frames.append(frame)
                frame_count += 1
        elif unit_type == "infobox":
            frame = {       
                'id': frame_count,
                'source': source,
                'page_title': page_title,
                'category': categories,
                'page_hierarchy': unit.get("content_path", []),
                'content_type': unit_type,
                'links': unit.get("links", []),
                'content': unit.get("content", {})
            }
            new_frames.append(frame)
            frame_count += 1
            
        elif unit_type == "table":
            rows = unit.get("rows", [])
            for row in rows:
                frame = {
                    'id': frame_count,
                    'source': source,
                    'page_title': page_title,
                    'category': categories,
                    'page_hierarchy': unit.get("content_path", []),
                    'content_type': unit_type,
                    'content': row,
                    'links': unit.get("links", [])
                }
                new_frames.append(frame)
                frame_count += 1
    
        return new_frames


def process_olympedia(category:Optional[str]=None, data_type:Optional[str]=None):
    olympedia_file = "./data/olympedia/extracted_data/olympedia.jsonl"
    frames = list()
    frame_count = 0
    frames.extend(_process_olympedia_corpus_file(olympedia_file, frame_count, category, data_type))
    print(f"Total length of olympedia corpus: {len(frames)} for category: {category} and data_type: {data_type}")
    output_path = f"./data/alignment/olympedia/olympedia_corpus_{category}_{data_type}.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for frame in frames:
            f.write(json.dumps(frame, ensure_ascii=False) + "\n")


def _process_olympedia_corpus_file(file: str, frame_count: int, category:Optional[str]=None, data_type:Optional[str]=None) -> List[Dict]:
    frames = list()
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row_data = json.loads(line)
            new_frames = process_olympedia_raw_data(row_data, frame_count, category, data_type)

            if new_frames:
                frames.extend(new_frames)
                frame_count += len(new_frames)
    return frames


def process_olympedia_raw_data(row_data: Dict, frame_count: int, category:Optional[str]=None, data_type:Optional[str]=None) -> List[Dict]:
    new_frames = list()
    page_title = row_data["page_title"]
    source = row_data["source"]
    categories = [row_data.get("category", "")]
    
    if category and category not in categories:
        return new_frames
    
    for unit in row_data.get("data_units", []):
        unit_type = unit["data_type"].lower()
        if data_type and unit_type != data_type.lower():
            continue
        unit_links = unit.get("links", [])
        #link_texts = [link.get("url", "") for link in unit_links if link.get("url")]
        page_hierarchy = row_data.get("content_path", [])

        if unit_type == "text":
            for p in unit.get("content", []):
                frame = {
                    'id': frame_count,
                    'source': source,
                    'page_title': page_title,
                    'category': categories,
                    'page_hierarchy': page_hierarchy,
                    'content_type': unit_type,
                    'passage_id': p.get("pid"),
                    'content': {"text": p.get("text", "")},
                    'links': unit_links
                }
                new_frames.append(frame)
                frame_count += 1

        elif unit_type == "table":
            rows = unit.get("rows", [])
            for row in rows:
                row_index = rows.index(row)
                row_links = []
                for link in unit_links:
                    if link.get("row") == row_index:
                        if "url" in link:
                            row_links.append({"text": link["text"], "url": link["url"], "field": link["field"]})
                        elif "href" in link:
                            if "https://www.olympedia.org" not in link["href"]:
                                link["href"] = f"https://www.olympedia.org{link['href']}"
                            row_links.append({"text": link["text"], "url": link["href"], "field": link["field"]})
                        else:
                            print (f"Error in link: {link}")
                frame = {
                    'id': frame_count,
                    'source': source,
                    'page_title': page_title,
                    'category': category,
                    'page_hierarchy': page_hierarchy,
                    'content_type': unit_type,
                    'content': row,
                    'links': row_links
                }
                new_frames.append(frame)
                frame_count += 1

        elif unit_type == "infobox":
            frame = {
                'id': frame_count,
                'source': source,
                'page_title': page_title,
                'category': category,
                'page_hierarchy': page_hierarchy,
                'content_type': unit_type,
                'links': unit_links,
                'content': unit.get("content", {})
            }
            new_frames.append(frame)
            frame_count += 1

    return new_frames



def main():

    # process_olympedia(data_type="text")
    # process_olympedia(data_type="infobox")
    # process_olympedia(data_type="table")

    process_olympics(category="athletes", data_type="text")
    process_olympics(category="athletes", data_type="infobox")
    process_olympics(category="athletes", data_type="table")

if __name__ == "__main__":
    main()


