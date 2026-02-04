USE la_cucina_italiana;

INSERT INTO users (username, email, password_hash) VALUES
('mario', 'mario@example.com', '$2b$12$mxVp9KR0tCeAoAnANyV7r.PWuyggl659SALTCZXQ6JfRicqusYZ/6'),
('lucia', 'lucia@example.com', '$2b$12$SZDIv1y4Xx2nz6vqMefmtugAvTiIgn1WmlRWluUe5lL385SOEUCx2'),
('paolo', 'paolo@example.com', '$2b$12$PvwwDtUiqPOTStrXofQUguseSyVzjV37Q/im.hTL9AYpysnLaUy8.');

INSERT INTO recipes (title, description, image_url, genre) VALUES
('Spaghetti alla Carbonara', 'Pasta cremosa con guanciale e pecorino.', 'https://images.unsplash.com/photo-1521389508051-d7ffb5dc8fb1', 'Primo'),
('Risotto ai Funghi', 'Risotto mantecato con funghi porcini.', 'https://images.unsplash.com/photo-1506354666786-959d6d497f1a', 'Primo'),
('Pollo alla Cacciatora', 'Pollo stufato con pomodoro e olive.', 'https://images.unsplash.com/photo-1604908176997-125f25cc6f3d', 'Secondo'),
('Bruschetta al Pomodoro', 'Pane tostato con pomodoro e basilico.', 'https://images.unsplash.com/photo-1523987355523-c7b5b84e4c1a', 'Antipasto'),
('Tiramisù Classico', 'Dolce al cucchiaio con mascarpone e caffè.', 'https://images.unsplash.com/photo-1505253716362-afaea1d3d1af', 'Dolce');

INSERT INTO ingredients (name, unit, price_per_unit) VALUES
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

INSERT INTO recipe_ingredients (recipe_id, ingredient_id, qty_per_person) VALUES
(1, 1, 100),
(1, 2, 40),
(1, 3, 25),
(1, 4, 1),
(2, 5, 90),
(2, 6, 50),
(2, 7, 20),
(3, 8, 200),
(3, 9, 80),
(3, 10, 20),
(4, 11, 80),
(4, 9, 60),
(4, 12, 5),
(5, 13, 80),
(5, 14, 60),
(5, 15, 40),
(5, 4, 1);

INSERT INTO wines (name, price) VALUES
('Chianti Classico', 12.50),
('Pinot Grigio', 10.00),
('Barbera d\'Asti', 11.00),
('Prosecco', 9.00),
('Marsala', 8.50);

INSERT INTO recipe_wines (recipe_id, wine_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);
