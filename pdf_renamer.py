import os
import PyPDF2
import argparse
import requests
import json
import time

def extract_text_from_pdf(pdf_path, max_pages=10):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for i, page in enumerate(reader.pages):
            if i >= max_pages:
                break
            text += page.extract_text()
    return text

def get_filename_from_openrouter(text, current_filename):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "anthropic/claude-3-haiku",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that suggests appropriate filenames based on PDF content. Respond with ONLY the filename, without any explanations or additional text."},
            {"role": "user", "content": f"Based on the following text extracted from a PDF, suggest an appropriate filename (without extension): {text[:1000]}"}
        ]
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            new_filename = result['choices'][0]['message']['content'].strip()
            return new_filename if new_filename else os.path.splitext(current_filename)[0]
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                print(f"Error calling OPENROUTER API: {e}")
                return os.path.splitext(current_filename)[0]
            time.sleep(2 ** attempt)  # Exponential backoff

def main():
    parser = argparse.ArgumentParser(description='Rename PDF files based on their content using OPENROUTER LLM.')
    parser.add_argument('directory', nargs='?', help='Path to the directory containing PDF files')
    parser.add_argument('--dry-run', action='store_true', help='Show new filenames without renaming')
    parser.add_argument('--max-pages', type=int, default=10, help='Maximum number of pages to analyze (default: 10)')
    args = parser.parse_args()

    if args.directory is None:
        parser.print_help()
        return

    if 'OPENROUTER_API_KEY' not in os.environ:
        print("Error: OPENROUTER_API_KEY environment variable is not set.")
        return

    directory = args.directory

    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory, filename)
            text = extract_text_from_pdf(file_path, args.max_pages)
            
            new_filename = get_filename_from_openrouter(text, filename)
            new_filename = new_filename.replace(" ", "_") + ".pdf"
            
            if args.dry_run:
                print(f"Would rename '{filename}' to '{new_filename}'")
            else:
                new_file_path = os.path.join(directory, new_filename)
                os.rename(file_path, new_file_path)
                print(f"Renamed '{filename}' to '{new_filename}'")

if __name__ == "__main__":
    main()
