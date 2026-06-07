import sqlite3
import pandas as pd

def execute_sql(db_path, sql_query):
    """Execute SQL and return results as DataFrame"""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(sql_query, conn)
    conn.close()
    return df

def execute_with_retry(db_path, initial_sql, schema_text, user_question):
    """Execute SQL, if fails, ask LLM to fix it"""
    from sql_generator import client
    
    current_sql = initial_sql
    
    for attempt in range(3):
        try:
            conn = sqlite3.connect(db_path)
            df = pd.read_sql_query(current_sql, conn)
            conn.close()
            return df, current_sql, None  # Success!
            
        except Exception as e:
            error_msg = str(e)
            print(f" Attempt {attempt + 1} failed: {error_msg}")
            
            if attempt == 2:  # Last attempt
                conn.close()
                return None, current_sql, error_msg
            
            # Prompting the LLM to fix the error
            fix_prompt = f"""
The following SQL query failed with this error: {error_msg}

Database Schema:
{schema_text}

Original question: {user_question}

Failed SQL:
{current_sql}

Please fix the SQL query.. Return ONLY the corrected SQL.
"""
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": fix_prompt}]
            )
            current_sql = response.choices[0].message.content.strip()
            current_sql = current_sql.replace("```sql", "").replace("```", "").strip()

if __name__ == "__main__":
    from schema_reader import get_schema
    from sql_generator import generate_sql
    
    schema = get_schema("olist.sqlite")
    
    # Testing a question
    question = "How many customers are there?"
    sql = generate_sql(question, schema)
    print(f" Generated SQL:\n{sql}\n")
    
    df, final_sql, error = execute_with_retry("olist.sqlite", sql, schema, question)
    
    if df is not None:
        print(" Results:")
        print(df)
    else:
        print(f" Failed: {error}")