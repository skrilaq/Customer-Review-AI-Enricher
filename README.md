# Customer-Review-AI-Enricher

An automated data-enrichment pipeline built with **Python**, **SQLite**, and **Google Gemini API**. 

This project simulates a real-world enterprise analytics workflow: it extracts raw, unstructured customer reviews stored in a relational database, leverages Large Language Models (LLMs) to perform structured sentiment analysis and department classification, and automatically updates the database with deterministic JSON outputs for downstream business intelligence.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Database:** SQLite3
* **AI Provider:** Google Gemini API (`google-genai` SDK)
* **Model:** `gemini-2.5-flash`
* **Data Format:** Structured JSON (`application/json` schema enforcing)

---

## 📂 Project Architecture & File Logic (`main.py`)

The pipeline operates in 5 sequential stages within `main.py`:

### Step-by-Step Execution Flow:

1. **Database Initialization & Schema Setup:**  
   Establishes a connection to `data.db` and safely creates the `customer_reviews` table if it doesn't exist. If the database is empty, it populates initial mock data (raw customer text with unassigned/`NULL` sentiment and department fields).

2. **Targeted Data Extraction (`SELECT`):**  
   Queries only the records where `sentiment IS NULL` using `cursor.fetchall()`. This ensures the pipeline is efficient and only processes unprocessed feedback.

3. **Deterministic LLM Structuring (`google-genai`):**  
   Sends each review text to `gemini-2.5-flash`. By configuring `response_mime_type="application/json"`, the LLM is constrained to output strict JSON containing only two keys: `sentiment` and `departament`.

4. **Database Mutation (`UPDATE`):**  
   Parses the returned JSON using `json.loads()` and updates the database record using parameterized queries (`WHERE id = ?`). Parameterization prevents SQL injection and syntax errors caused by special characters in LLM responses.

5. **Analytics Verification:**  
   Executes a final `SELECT` query to display the fully enriched dataset in the console, confirming zero missing values.

---

## 🚀 How to Run Locally

### 1. Prerequisites
Install the required dependencies:
```bash
pip install google-genai

$env:GEMINI_API_KEY="your_api_key_here"

python main.py

