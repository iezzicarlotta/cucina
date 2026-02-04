import sqlite3
import os
from pathlib import Path

here = Path(__file__).parent
db_path = here / "dev.db"

# Remove existing DB for a clean start (comment out if you want persistence)
if db_path.exists():
    db_path.unlink()

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Create minimal tables compatible with the backend usage
cur.executescript('''
CREATE TABLE GENERI (ID INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT UNIQUE);
CREATE TABLE RICETTE (ID INTEGER PRIMARY KEY AUTOINCREMENT, titolo TEXT NOT NULL, descrizione TEXT NOT NULL, porzioni_default INTEGER DEFAULT 4, tempo_preparazione_min INTEGER, difficolta TEXT DEFAULT 'media');
CREATE TABLE MEDIA (ID INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT NOT NULL, tipo TEXT NOT NULL, ID_RICETTA INTEGER NOT NULL);
CREATE TABLE INGREDIENTI (ID INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, unita_base TEXT NOT NULL, prezzo_per_unita REAL NOT NULL);
CREATE TABLE RICETTA_INGREDIENTE (ID_RICETTA INTEGER NOT NULL, ID_INGREDIENTE INTEGER NOT NULL, quantita_per_persona REAL NOT NULL, unita_misura TEXT NOT NULL, PRIMARY KEY (ID_RICETTA, ID_INGREDIENTE));
CREATE TABLE VINI (ID INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, descrizione TEXT, tipo TEXT, nazione TEXT, regione TEXT, prezzo REAL);
CREATE TABLE UTENTI (ID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, email TEXT UNIQUE, password_hash TEXT, nome TEXT, cognome TEXT);
CREATE TABLE GENERE_RICETTA (ID_GENERE INTEGER NOT NULL, ID_RICETTA INTEGER NOT NULL, PRIMARY KEY (ID_GENERE, ID_RICETTA));
CREATE TABLE CARRELLI (ID INTEGER PRIMARY KEY AUTOINCREMENT, ID_UTENTE INTEGER NOT NULL, creato DATETIME DEFAULT CURRENT_TIMESTAMP, aggiornato DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE CARRELLO_ITEM (ID INTEGER PRIMARY KEY AUTOINCREMENT, ID_CARRELLO INTEGER NOT NULL, ID_RICETTA INTEGER NOT NULL, ID_VINO INTEGER, persone INTEGER NOT NULL DEFAULT 1, prezzo_item REAL);
CREATE TABLE ORDINI (ID INTEGER PRIMARY KEY AUTOINCREMENT, ID_UTENTE INTEGER NOT NULL, totale REAL NOT NULL, data_ordine DATETIME DEFAULT CURRENT_TIMESTAMP, stato TEXT DEFAULT 'creato', indirizzo_consegna TEXT);
CREATE TABLE ORDINE_RICETTA (ID_ORDINE INTEGER NOT NULL, ID_RICETTA INTEGER NOT NULL, ID_VINO INTEGER, persone INTEGER NOT NULL, prezzo_item REAL NOT NULL, PRIMARY KEY (ID_ORDINE, ID_RICETTA));
''')

# Insert sample data
cur.executescript('''
INSERT INTO UTENTI (username, email, password_hash, nome, cognome) VALUES
('mario','mario@example.com','$2b$12$mxVp9KR0tCeAoAnANyV7r.PWuyggl659SALTCZXQ6JfRicqusYZ/6','Mario','Rossi');

INSERT INTO RICETTE (titolo, descrizione, porzioni_default, tempo_preparazione_min, difficolta) VALUES
('Spaghetti alla Carbonara','Pasta cremosa con guanciale e pecorino.',4,25,'media');

INSERT INTO INGREDIENTI (nome, unita_base, prezzo_per_unita) VALUES
('Spaghetti','g',0.02),('Guanciale','g',0.04),('Pecorino Romano','g',0.05),('Uova','pz',0.30);

INSERT INTO RICETTA_INGREDIENTE (ID_RICETTA, ID_INGREDIENTE, quantita_per_persona, unita_misura) VALUES
(1,1,100,'g'),(1,2,40,'g'),(1,3,25,'g'),(1,4,1,'pz');

INSERT INTO VINI (nome, descrizione, tipo, nazione, regione, prezzo) VALUES
('Chianti Classico','Vino toscano','Rosso','Italia','Toscana',12.50);

INSERT INTO MEDIA (url, tipo, ID_RICETTA) VALUES
('https://images.unsplash.com/photo-1521389508051-d7ffb5dc8fb1','image',1);

INSERT INTO GENERI (nome) VALUES ('Primo');
INSERT INTO GENERE_RICETTA (ID_GENERE, ID_RICETTA) VALUES (1,1);
''')

conn.commit()
conn.close()
print('SQLite DB created at', db_path)
