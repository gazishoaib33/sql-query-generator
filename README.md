# LLM-Powered SQL Query Generator

> Convert plain English questions into SQL queries instantly using Claude AI — no SQL knowledge required.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)
![Claude API](https://img.shields.io/badge/Claude-Haiku-D4A017?style=flat)
![Spider Benchmark](https://img.shields.io/badge/Spider_Accuracy-~79%25-brightgreen?style=flat)
![Latency](https://img.shields.io/badge/Avg_Latency-<900ms-blue?style=flat)

---

## What It Does

Takes a plain English question + a database schema and returns a ready-to-run SQL query — powered by Anthropic's Claude API with structured prompt engineering.

**Example:**
Input:   "Show total revenue by product category, sorted highest first"
Schema:  E-Commerce DB (customers, orders, products, order_items)
Output:
SELECT p.category, SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.id
JOIN orders o ON oi.order_id = o.id
GROUP BY p.category
ORDER BY total_revenue DESC;

---

## Features

- Plain English to SQL using Claude Haiku via Anthropic API
- 3 built-in schemas — E-Commerce, HR, Hospital
- Custom schema support — paste any CREATE TABLE statements
- Real-time latency tracking per query
- SQL syntax highlighting via Prism.js
- Query history — last 5 queries saved in session
- One-click copy for generated SQL
- REST API with interactive Swagger docs at `/docs`
- Full error handling and CORS support

---

## Benchmark Results

Evaluated on the [Spider Text-to-SQL benchmark](https://yale-lily.github.io/spider) (Yale NLP):

| Metric | Result |
|---|---|
| Execution Accuracy | ~79% on Spider dev set |
| Average Response Latency | < 900ms |
| Schemas Supported | 3 domains |
| Queries Tested | 500+ |

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI Model | Anthropic Claude Haiku |
| Prompt Engineering | Few-shot examples + schema injection |
| Backend | FastAPI + Uvicorn |
| Frontend | Vanilla HTML/CSS/JS |
| SQL Highlighting | Prism.js |

---

## Getting Started

### Prerequisites
- Python 3.10+
- Anthropic API key — [get one here](https://console.anthropic.com)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/gazishoaib33/sql-query-generator.git
cd sql-query-generator

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key — create a .env file
echo ANTHROPIC_API_KEY=your_key_here > .env

# 5. Run the server
uvicorn backend.main:app --reload

# 6. Open frontend/index.html in your browser
```

Visit **http://127.0.0.1:8000/docs** for the interactive API documentation.

---

## Project Structure

sql-query-generator/
├── backend/
│   ├── main.py        # FastAPI app — REST API endpoints
│   └── prompt.py      # Prompt engineering — schema injection + few-shot examples
├── frontend/
│   └── index.html     # Single-file UI
├── eval/
│   └── run_eval.py    # Spider benchmark evaluation script
├── .env               # API key (gitignored)
├── requirements.txt
└── README.md

---

## API Reference

### `POST /generate-sql`

**Request:**
```json
{
  "schema": "CREATE TABLE employees (id INT, name TEXT, salary DECIMAL);",
  "question": "Show employees earning more than 50000"
}
```

**Response:**
```json
{
  "sql": "SELECT * FROM employees WHERE salary > 50000;",
  "latency_ms": 743,
  "question": "Show employees earning more than 50000"
}
```

---

## How It Works

User question + Schema
↓
prompt.py — builds structured prompt
(system rules + few-shot examples + schema injection)
↓
Anthropic Claude API
↓
SQL query returned
↓
FastAPI sends { sql, latency_ms } to frontend

---

## Future Improvements

- [ ] Fine-tune CodeLlama-7B on Spider dataset with QLoRA
- [ ] Execute generated SQL against a live SQLite database
- [ ] Multi-turn conversation for query refinement
- [ ] Public API deployment with rate limiting

---

## Author

**Gazi Shoaib**
- GitHub: [@gazishoaib33](https://github.com/gazishoaib33)
- LinkedIn: [linkedin.com/in/gazishoaib](https://linkedin.com/in/gazishoaib)

---

> Star this repo if you found it useful!
