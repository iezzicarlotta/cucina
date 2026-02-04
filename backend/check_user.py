import sqlite3

# Connessione al database SQLite
def check_user_credentials():
    try:
        conn = sqlite3.connect('dev.db')
        cursor = conn.cursor()

        # Recupera le credenziali dell'utente
        cursor.execute("SELECT username, email, password_hash FROM UTENTI WHERE username='mario'")
        user = cursor.fetchone()
        if user:
            print("Credenziali utente:", user)
        else:
            print("Utente 'mario' non trovato.")

        cursor.close()
        conn.close()
    except Exception as e:
        print("Errore durante la verifica delle credenziali:", e)

if __name__ == "__main__":
    check_user_credentials()