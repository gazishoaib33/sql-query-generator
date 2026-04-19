# backend/prompt.py

FEW_SHOT_EXAMPLES = """
-- Example 1
-- Schema: CREATE TABLE employees (id INT, name TEXT, department TEXT, salary DECIMAL, hire_date DATE);
-- Question: Show all employees in the Engineering department earning more than 50000
SELECT * FROM employees
WHERE department = 'Engineering' AND salary > 50000;

-- Example 2
-- Schema: CREATE TABLE orders (id INT, customer_id INT, product TEXT, amount DECIMAL, order_date DATE);
-- Question: Total revenue by product for last month
SELECT product, SUM(amount) AS total_revenue
FROM orders
WHERE order_date >= DATE('now', 'start of month', '-1 month')
  AND order_date < DATE('now', 'start of month')
GROUP BY product
ORDER BY total_revenue DESC;

-- Example 3
-- Schema: CREATE TABLE customers (id INT, name TEXT, email TEXT, country TEXT, joined_date DATE);
-- Question: How many customers joined from each country?
SELECT country, COUNT(*) AS customer_count
FROM customers
GROUP BY country
ORDER BY customer_count DESC;
"""

SYSTEM_PROMPT = """You are an expert SQL developer. Your job is to convert natural language questions into accurate SQL queries.

Rules you must follow:
1. Return ONLY the SQL query — no explanation, no markdown, no backticks
2. Use standard SQL syntax compatible with SQLite
3. Always use proper aliases (AS) for calculated columns
4. Use JOIN instead of subqueries where possible for readability
5. If the question is ambiguous, make the most reasonable assumption
6. Never use DROP, DELETE, UPDATE or INSERT — read-only SELECT only

Here are examples of correct input/output:
""" + FEW_SHOT_EXAMPLES


def build_prompt(schema: str, question: str) -> str:
    """
    Constructs the user message that gets sent to Claude.
    Injects the actual database schema and the user's question.
    """
    return f"""Database Schema:
{schema}

Natural Language Question:
{question}

SQL Query:"""