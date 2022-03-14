-- list the titles of all movies with a release date on or after 2018 in alphabetical order
-- output a single column for the title of each movie
-- movies released in 2018 and with release dates in the future should be included
SELECT title FROM movies WHERE year >= 2018 ORDER BY title;