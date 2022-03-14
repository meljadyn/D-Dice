-- determine the number of movies with an IMDb rating of 10.0
-- output a table with a single column and single row containing the number of movies with 10.0
SELECT COUNT(movies.title) FROM movies JOIN ratings ON movies.id = ratings.movie_id WHERE rating = 10.0;