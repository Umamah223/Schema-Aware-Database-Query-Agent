import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_sql(user_question, schema_text):
    prompt = f"""
You are a SQL expert. Given the database schema below, write a SQLite query to answer the user's question.

{schema_text}

User question: "{user_question}"

RULES:
1. Write ONLY the SQL query, nothing else
2. Only SELECT statements allowed
3. Use proper JOINs when connecting tables
4. Use clear column names
5. Ensure it's valid SQLite syntax

SQL query:
"""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        sql = response.choices[0].message.content.strip()
        sql = sql.replace("```sql", "").replace("```", "").strip()
        return sql
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    from schema_reader import get_schema
    
    schema = get_schema("olist.sqlite")
    
    questions = [
        "How many customers are there?",
        "What is the average payment value?",
        "Show top 5 product categories by number of products",
    ]
    
    for q in questions:
        print(f"\n Question: {q}")
        sql = generate_sql(q, schema)
        print(f" Generated SQL:\n{sql}\n")
        print("-" * 50)