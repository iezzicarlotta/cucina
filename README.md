# La Cucina Italiana – Acquisto di ricette complete

## Descrizione
Web application che permette di consultare ricette italiane complete, visualizzare il costo per persona, autenticarsi, gestire un carrello e completare l'acquisto di ricette con ingredienti inclusi.

## Tecnologie utilizzate
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Backend**: Python, Flask
- **Database**: MySQL
- **Sicurezza**: bcrypt per hashing password, sessioni Flask

## Architettura
```
/backend   -> API Flask (autenticazione, ricette, carrello, ordini)
/frontend  -> pagine HTML/CSS/JS
/database  -> schema e seed del database
```

## Avvio del progetto
1. **Database**
   - Creare il database eseguendo `database/schema.sql`.
   - Popolare i dati con `database/seed.sql`.
2. **Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```
3. **Frontend**
   - Aprire `frontend/index.html` in un browser.
   - Configurare un proxy o servire i file tramite un server statico per garantire le richieste alla API.

## Cosa funziona
- Autenticazione login/logout con sessione.
- Elenco ricette con filtro per genere e costo per persona.
- Dettaglio ricetta con ingredienti e vini consigliati.
- Gestione carrello e checkout con calcolo totale.

## Cosa resta da fare
- Gestione errori avanzata e validazioni UI.
- Pagamenti reali e stato ordini più dettagliato.
- Upload immagini e gestione admin.

## Note sull'architettura
Il backend espone endpoint REST per autenticazione, ricette, carrello e checkout. Il frontend usa fetch API per interagire con i dati e gestisce la UI in modo dinamico.
