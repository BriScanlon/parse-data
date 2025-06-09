from pathlib import Path
from datetime import datetime
from keybert import KeyBERT

# Initialize KeyBERT model once
kw_model = KeyBERT()

def extract_keywords(text, top_n=10):
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),
        stop_words='english',
        top_n=top_n
    )
    return [kw for kw, score in keywords]

# Define the root directory
root_dir = Path('./temp')

# Find all files recursively
all_files = [f for f in root_dir.rglob('*') if f.is_file()]

for file in all_files:
    print(f"\n--- {file.name} ---")

    # Creation time
    created_datetime = datetime.fromtimestamp(file.stat().st_ctime)
    print("Created: ", created_datetime)

    # Modified time
    modified_datetime = datetime.fromtimestamp(file.stat().st_mtime)
    print("Last modified: ", modified_datetime)

    try:
        # Read file content
        text = file.read_text(encoding='utf-8', errors='ignore')

        # Extract keywords
        keywords = extract_keywords(text)
        print("Keywords:", keywords)

    except Exception as e:
        print("Error reading or processing file:", e)
