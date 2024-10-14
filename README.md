# PDF Renamer

This script renames PDF files based on their content using the OPENROUTER API and Claude 3 Haiku model.

## Setup

1. Ensure you have Python 3.6 or higher installed.

2. Set up a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Set up your OPENROUTER API key as an environment variable:
   - On Windows:
     ```
     set OPENROUTER_API_KEY=your_api_key_here
     ```
   - On macOS and Linux:
     ```
     export OPENROUTER_API_KEY=your_api_key_here
     ```

## Usage

Run the script with the following command:

```
python pdf_renamer.py /path/to/pdf/directory [options]
```

Options:
- `--dry-run`: Show new filenames without renaming
- `--max-pages PAGES`: Maximum number of pages to analyze (default: 10)

## How it works

1. The script extracts text from the first few pages of each PDF file.
2. It sends this text to the OPENROUTER API, which uses the Claude 3 Haiku model to generate an appropriate filename.
3. The PDF is then renamed based on the AI-generated filename.

## Deactivating the virtual environment

When you're done, you can deactivate the virtual environment by running:

```
deactivate
```

## Note

Make sure you have a valid OPENROUTER API key and sufficient credits to use the service. The script includes error handling and retry logic for API calls.
