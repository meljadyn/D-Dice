-- list the names of all people who starred in a movie in which Kevin Bacon also starred.
-- output a table with a single column for the name of each person.
-- There may be multiple people named Kevin Bacon in the database. Be sure to only select the Kevin Bacon born in 1958.
-- Kevin Bacon himself should not be included in the resulting list.
SELECT name FROM people
JOIN stars ON people.id = person_id
WHERE stars.movie_id IN (SELECT stars.movie_id FROM stars
JOIN people ON people.id = person_id
WHERE name = "Kevin Bacon" AND birth = 1958)
AND NOT name = "Kevin Bacon";