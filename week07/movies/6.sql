-- determine the average rating of all movies released in 2012.
-- output a table with a single column and a single row (not including the header) containing the average rating.
SELECT AVG(rating) FROM ratings JOIN movies ON movie_id = id WHERE year = 2012;