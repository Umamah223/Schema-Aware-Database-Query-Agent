import streamlit as st
import os
import tempfile
from schema_reader import get_schema
from sql_generator import generate_sql
from executor import execute_with_retry

st.set_page_config(page_title="AI Database Query Agent", page_icon="🤖", layout="wide")

st.markdown(
    "<h1 style='color:#003366;'>Schema-Aware Database Query Agent</h1>",
    unsafe_allow_html=True
)
st.write("Upload a SQLite database and ask questions in plain English!")

# File uploader
uploaded_file = st.file_uploader(" Upload your SQLite Database", type=['db', 'sqlite', 'sqlite3'])

if uploaded_file:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        db_path = tmp_file.name
    
    # Show schema
    st.subheader(" Database Schema")
    with st.expander("Click to view schema", expanded=False):
        schema = get_schema(db_path)
        st.text(schema)
    
    # Question input
    st.subheader(" Ask a Question")
    user_question = st.text_input(
        "What would you like to know about your data?",
        placeholder="e.g., How many customers are there? or Show top 5 products by sales"
    )
    
    if user_question:
        col1, col2 = st.columns(2)
        
        with col1:
            # Generate SQL
            with st.spinner("🤔 Generating SQL..."):
                sql = generate_sql(user_question, schema)
            st.subheader(" Generated SQL")
            st.code(sql, language="sql")
        
        with col2:
            # Execute query
            with st.spinner("⚡ Executing query..."):
                df, final_sql, error = execute_with_retry(db_path, sql, schema, user_question)
            
            if df is not None:
                st.subheader("Results:")
                st.dataframe(df, use_container_width=True)
                st.success(f" Found {len(df)} result(s)")
                
                # Download button
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download as CSV",
                    csv,
                    "query_results.csv",
                    "text/csv"
                )
            else:
                st.error(f"❌ Query failed: {error}")
    
    # Clean up
    os.unlink(db_path)

# Sidebar
with st.sidebar:
    st.header("📝 How to Use")
    st.write("""
    1. **Upload** a SQLite database (.db or .sqlite file)
    2. **View** the schema to understand your data
    3. **Ask** questions in plain English
    4. **Get** results instantly!
    """)
    
    st.header("💡 Example Questions")
    st.write("""
    Try questions like:
    - How many customers are there?
    - What is the average payment value?
    - Show top 5 product categories
    - Which sellers have the most orders?
    - What's the average review score?
    """)
    
    st.header("ℹ️ About")
    st.write("""
    Powered by **Groq** (free LLM API).
    Your data never leaves your machine - 
    only the schema structure is sent to the AI.
    """)