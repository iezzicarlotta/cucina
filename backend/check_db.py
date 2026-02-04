import sqlite3

# Connessione al database SQLite
def check_database():
    try:
        conn = sqlite3.connect('dev.db')
        cursor = conn.cursor()

        # Elenco delle tabelle
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tabelle nel database:", tables)

        # Contenuto di ogni tabella
        for table in tables:
            table_name = table[0]
            print(f"\nContenuto della tabella {table_name}:")
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            for row in rows:
                print(row)

        cursor.close()
        conn.close()
    except Exception as e:
        print("Errore durante la verifica del database:", e)

if __name__ == "__main__":
    check_database()