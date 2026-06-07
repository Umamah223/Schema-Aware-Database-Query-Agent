import sqlite3

def get_schema(db_path):
    """Getting database structure with relationships and table count"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # TABLE COUNT
    schema_text = f"DATABASE SCHEMA\n"
    schema_text += f"Total Tables: {len(tables)}\n"
    schema_text += "=" * 50 + "\n\n"
    
    # Storing foreign key info for later
    foreign_keys = {}
    
    for (table_name,) in tables:
        schema_text += f"Table: {table_name}\n"
        
        # Column details
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        schema_text += "   Columns:\n"
        for col in columns:
            col_id = col[0]
            col_name = col[1]
            col_type = col[2]
            is_pk = "PRIMARY KEY" if col[5] else ""
            schema_text += f"     - {col_name} ({col_type}) {is_pk}\n"
        
        # Foreign keys
        cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        fks = cursor.fetchall()
        if fks:
            schema_text += "   Relationships:\n"
            for fk in fks:
                fk_col = fk[3]
                ref_table = fk[2]
                ref_col = fk[4]
                schema_text += f"     → {fk_col} references {ref_table}({ref_col})\n"
                foreign_keys[f"{table_name}.{fk_col}"] = f"{ref_table}.{ref_col}"
        
        # Row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        row_count = cursor.fetchone()[0]
        schema_text += f"   Total rows: {row_count:,}\n"
        
        # Get sample data (first 2 rows)
        try:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 2;")
            samples = cursor.fetchall()
            if samples:
                schema_text += "   Sample rows:\n"
                for row in samples:
                    schema_text += f"     {row}\n"
        except:
            pass
        
        schema_text += "\n"
    
    # Summary of relationships found
    if foreign_keys:
        schema_text += "Important Relationships Summary:\n"
        for source, target in foreign_keys.items():
            schema_text += f"   {source} → {target}\n"
    
    conn.close()
    return schema_text

if __name__ == "__main__":
    schema = get_schema("olist.sqlite")
    print(schema)