-- list the names of all people who have directed a movie that received a rating of at least 9.0.
-- output a table with a single column for the name of each person.
-- If a person directed more than one movie that received a rating of at least 9.0, they should only appear in your results once.
SELECT DISTINCT name FROM people JOIN directors ON person_id = people.id JOIN ratings ON ratings.movie_id = directors.movie_id WHERE rating >= 9.0;