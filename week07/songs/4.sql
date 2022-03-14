-- lists the names of any songs that have danceability, energy, and valence greater than 0.75.
-- output a table with a single column for the name of each song.
SELECT name FROM songs WHERE danceability > 0.75 AND energy > 0.75 AND valence > 0.75;