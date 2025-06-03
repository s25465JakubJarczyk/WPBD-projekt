import pandas as pd
import psycopg2
from psycopg2 import sql

# Dane połączenia z PostgreSQL
db_config = {
    'dbname': 'business_db',
    'user': 'admin',
    'password': 'admin',
    'host': 'postgres',
    'port': 5432
}

# Ścieżki do plików CSV
files = {
    'customers': 'customers.csv',
    'orders': 'orders.csv',
    'products': 'products.csv'
}

# Mapowanie typów Pandas → PostgreSQL
type_mapping = {
    'object': 'TEXT',
    'int64': 'INTEGER',
    'float64': 'FLOAT',
    'bool': 'BOOLEAN',
    'datetime64[ns]': 'TIMESTAMP'
}

def create_table_from_df(cursor, table_name, df):
    columns = []
    for col in df.columns:
        dtype = type_mapping.get(str(df[col].dtype), 'TEXT')
        columns.append(sql.SQL("{} {}").format(sql.Identifier(col), sql.SQL(dtype)))
    
    create_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({});").format(
        sql.Identifier(table_name),
        sql.SQL(', ').join(columns)
    )
    cursor.execute(create_query)

def insert_data(cursor, table_name, df):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    row_count = cursor.fetchone()[0]
    if row_count > 0:
        print(f"Tabela '{table_name}' zawiera już dane – pomijam wstawianie.")
        return

    for _, row in df.iterrows():
        columns = [sql.Identifier(col) for col in df.columns]
        values = [sql.Literal(val) for val in row]
        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({});").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(columns),
            sql.SQL(', ').join(values)
        )
        cursor.execute(insert_query)
    print(f"Wstawiono dane do tabeli '{table_name}'")


def main():
    conn = psycopg2.connect(**db_config)
    conn.autocommit = True
    cur = conn.cursor()

    for table_name, filepath in files.items():
        df = pd.read_csv(filepath)
        create_table_from_df(cur, table_name, df)
        insert_data(cur, table_name, df)  # ta funkcja już wypisuje co trzeba

    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
