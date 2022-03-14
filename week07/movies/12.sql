-- list the titles of all movies in which both Johnny Depp and Helena Bonham Carter starred.
-- output a table with a single column for the title of each movie.
-- You may assume that there is only one person in the database with the name Johnny Depp.
-- You may assume that there is only one person in the database with the name Helena Bonham Carter.
SELECT title FROM movies
JOIN stars ON movies.id = movie_id
JOIN people ON people.id = person_id
WHERE name = "Helena Bonham Carter"
INTERSECT
SELECT title FROM movies
JOIN stars ON movies.id = movie_id
JOIN people ON people.id = person_id
WHERE name = "Johnny Depp";