-- list the names of all people who starred in Toy Story.
-- output a table with a single column for the name of each person.
-- You may assume that there is only one movie in the database with the title Toy Story.
SELECT name FROM people JOIN stars ON people.id = person_id JOIN movies ON movie_id = movies.id WHERE title = "Toy Story";