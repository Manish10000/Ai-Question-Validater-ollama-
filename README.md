# AI Question Validator (Ollama)

A Streamlit-based application that validates multiple-choice questions using AI and web search capabilities.

## Features

- Upload CSV files containing multiple-choice questions
- Validate questions using Llama 3.2 model via Ollama
- Web search integration using DuckDuckGo
- Progress tracking for question validation
- Downloadable validation reports
- Sample CSV template provided

## Setup

1. Ensure you have Python 3.8+ installed
2. Install Ollama and run the Llama 3.2 model
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   streamlit run questionvalidations.py
   ```

## CSV Format

The input CSV should contain the following columns:
- id: Question identifier
- sub_category: Subject subcategory
- category: Main category
- question_name: Brief question title
- question_description: Detailed question
- A, B, C, D: Multiple choice options
- Answer: Correct answer (A, B, C, or D)
- Level: Question difficulty level

## Usage

1. Download the sample CSV to understand the required format
2. Prepare your questions in the same format
3. Upload your CSV file
4. Wait for the validation process to complete
5. Download the validation report