# Schema-Aware Database Query Agent

An AI-powered database assistant that enables users to interact with SQLite databases using natural language. Instead of writing SQL queries manually, users can simply ask questions in plain English, and the application automatically generates, executes, and displays the results.

Built with **Python**, **Streamlit**, **SQLite**, and **Groq LLMs**, the system dynamically analyzes the uploaded database schema to generate accurate SQL queries tailored to the user's database.


## Overview

Working with databases typically requires an understanding of database schemas. This project removes that barrier by allowing users to query databases conversationally.

The application automatically extracts the schema of an uploaded SQLite database, generates schema-aware SQL queries from natural-language questions, executes those queries, and presents the results in an intuitive interface.

## Features

* Upload SQLite databases (`.db`, `.sqlite`, `.sqlite3`)
* Automatic database schema extraction
* AI-powered SQL generation using Groq API
* Natural language querying
* Automatic SQL execution
* CSV export functionality
* Streamlit-based user interface

---

## How It Works

### 1. Launch the Application

Start the Streamlit application and open the web interface.

### 2. Upload a SQLite Database

Upload any SQLite database file (`.db`, `.sqlite`, or `.sqlite3`).

### 3. View the Database Schema

The application automatically analyzes the uploaded database and displays its schema, allowing users to understand:

* Available tables
* Column names
* Database structure
* Relationships between tables

This helps users explore unfamiliar databases before querying them.

### 4. Ask Questions in Plain English

Examples:

* How many customers are there?
* Which product has the highest sales?
* Show the top 5 sellers by revenue.
* What is the average review score?

### 5. Generate SQL Automatically

The Groq-powered LLM analyzes both the user's question and the uploaded database schema to generate a valid SQL query.

### 6. Execute the Query

The generated SQL query is automatically executed against the uploaded database.

### 7. View and Download Results

Query results are displayed directly within the application and can be downloaded as a CSV file for further analysis.

---

## Example Workflow

### User Question

```text
Which product has the highest sales?
```

### Generated SQL

```sql
SELECT product_name, SUM(sales) AS total_sales
FROM products
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 1;
```

### Output

| Product Name | Total Sales |
| ------------ | ----------- |
| Product A    | 125000      |

The results can then be downloaded as a CSV file.

---

## Technology Stack

* Python
* Streamlit
* SQLite
* Groq API
* Pandas

---

## Prerequisites

* Python 3.8 or higher
* Groq API Key

Get a free API key from:

https://console.groq.com/keys

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/Umamah223/Schema-Aware-Database-Query-Agent.git
cd Schema-Aware-Database-Query-Agent
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

### Run the Application

```bash
streamlit run app.py
```

---

## Future Improvements

* PostgreSQL & MySQL support
* Data visualization and chart generation
* Multi-database support
* Conversational follow-up questions

---

