USE la_cucina_italiana;

-- UTENTI
INSERT INTO UTENTI (username, email, password_hash, nome, cognome) VALUES
('mario', 'mario@example.com', '$2b$12$mxVp9KR0tCeAoAnANyV7r.PWuyggl659SALTCZXQ6JfRicqusYZ/6', 'Mario', 'Rossi'),
('lucia', 'lucia@example.com', '$2b$12$SZDIv1y4Xx2nz6vqMefmtugAvTiIgn1WmlRWluUe5lL385SOEUCx2', 'Lucia', 'Bianchi'),
('paolo', 'paolo@example.com', '$2b$12$PvwwDtUiqPOTStrXofQUguseSyVzjV37Q/im.hTL9AYpysnLaUy8.', 'Paolo', 'Verdi');


-- GENERI sample
INSERT INTO GENERI (nome) VALUES
('Primo'), ('Secondo'), ('Antipasto'), ('Dolce');


-- RICETTE
INSERT INTO RICETTE (titolo, descrizione, porzioni_default, tempo_preparazione_min, difficolta) VALUES
('Spaghetti alla Carbonara', 'Pasta cremosa con guanciale e pecorino.', 4, 25, 'media'),
('Risotto ai Funghi', 'Risotto mantecato con funghi porcini.', 4, 40, 'media'),
('Pollo alla Cacciatora', 'Pollo stufato con pomodoro e olive.', 4, 60, 'media'),
('Bruschetta al Pomodoro', 'Pane tostato con pomodoro e basilico.', 2, 10, 'facile'),
('Tiramisù Classico', 'Dolce al cucchiaio con mascarpone e caffè.', 6, 30, 'media');


-- Associazioni ricetta - genere
INSERT INTO GENERE_RICETTA (ID_GENERE, ID_RICETTA) VALUES
(1,1),(1,2),(2,3),(3,4),(4,5);


-- INGREDIENTI
INSERT INTO INGREDIENTI (nome, unita_base, prezzo_per_unita) VALUES
('Spaghetti', 'g', 0.02),
('Guanciale', 'g', 0.04),
('Pecorino Romano', 'g', 0.05),
('Uova', 'pz', 0.30),
('Riso Carnaroli', 'g', 0.03),
('Funghi Porcini', 'g', 0.06),
('Burro', 'g', 0.02),
('Pollo', 'g', 0.01),
('Pomodori pelati', 'g', 0.01),
('Olive nere', 'g', 0.05),
('Pane casereccio', 'g', 0.01),
('Basilico', 'g', 0.08),
('Mascarpone', 'g', 0.04),
('Savoiardi', 'g', 0.03),
('Caffè', 'ml', 0.01);


-- RICETTA_INGREDIENTE
INSERT INTO RICETTA_INGREDIENTE (ID_RICETTA, ID_INGREDIENTE, quantita_per_persona, unita_misura) VALUES
(1, 1, 100, 'g'),
(1, 2, 40, 'g'),
(1, 3, 25, 'g'),
(1, 4, 1, 'pz'),
(2, 5, 90, 'g'),
(2, 6, 50, 'g'),
(2, 7, 20, 'g'),
(3, 8, 200, 'g'),
(3, 9, 80, 'g'),
(3, 10, 20, 'g'),
(4, 11, 80, 'g'),
(4, 9, 60, 'g'),
(4, 12, 5, 'g'),
(5, 13, 80, 'g'),
(5, 14, 60, 'g'),
(5, 15, 40, 'ml'),
(5, 4, 1, 'pz');


-- VINI
INSERT INTO VINI (nome, descrizione, tipo, nazione, regione, prezzo) VALUES
('Chianti Classico', 'Vino toscano classico', 'Rosso', 'Italia', 'Toscana', 12.50),
('Pinot Grigio', 'Bianco fresco', 'Bianco', 'Italia', 'Veneto', 10.00),
('Barbera d\'Asti', 'Rosso piemontese', 'Rosso', 'Italia', 'Piemonte', 11.00),
('Prosecco', 'Spumante leggero', 'Spumante', 'Italia', 'Veneto', 9.00),
('Marsala', 'Vino liquoroso', 'Liquoroso', 'Italia', 'Sicilia', 8.50);


-- RICETTA_VINO
INSERT INTO RICETTA_VINO (ID_RICETTA, ID_VINO, annata) VALUES
(1,1,2018),(2,2,2020),(3,3,2019),(4,4,2021),(5,5,2016);
