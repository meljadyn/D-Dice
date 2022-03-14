-- Keep a log of any SQL queries you execute as you solve the mystery.

/*
Currently Known:
Theft took place on July 28, 2021 on Humphrey Street
*/

-- to see the tables options
.schema

-- to find the crime reports
SELECT id, description
  FROM [crime_scene_reports]
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND street LIKE "%Humphrey%";

/*
New Info:
Crime Report ID is 295
Theft took place in the bakery at 10:15am. All three interviews mention the bakery.
*/

.tables
.schema interviews

-- Try to find info on the interviews of the three witnesses
SELECT *
  FROM interviews
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND transcript LIKE "%bakery%";

/*
New Info:
Ruth (ID 161) - saw the thief get in a car within 10 minutes of the theft and leave the parking lot
Eugene (ID 162) - recognized the thief; they had withdrawn money from the ATM on Leggett Street "earlier [that] morning"
Raymond (ID 163) - the thief called someone for less than a minute; the thief said they were planning on taking the
                   earliest flight out of fiftyville tomorrow, and asked the person on the phone to purchase the ticket
Emma (ID 193) - bakery owner. Someone came in, whispered into the phone for half an hour, and left. Never bought anything.
*/

.tables
.schema bakery_security_logs

-- look for the thief's car - minute is set to be within a 10 minute range of the crime at 10:15
SELECT id, hour, minute, activity, license_plate
  FROM [bakery_security_logs]
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND hour = 10
   AND minute BETWEEN 15 AND 25;

.tables
.schema atm_transactions

-- look for the atm transaction on leggett st
SELECT id, account_number, transaction_type, amount
  FROM [atm_transactions]
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND transaction_type LIKE "withdraw"
   AND atm_location LIKE "Leggett%";

.tables
.schema phone_calls

-- check for the short call from the thief to the plane ticket-purchaser
SELECT id, duration, caller, receiver
  FROM phone_calls
 WHERE year = 2021
   AND month = 07
   AND day = 28
   AND duration <= 60; -- I think this is in seconds?

.tables
.schema airports
.schema flights

-- find the flight out of fiftyville
  SELECT id, hour, minute -- should help me determine the first flight out
    FROM flights
   WHERE year = 2021
     AND month = 7
     AND day = 29 -- day after the crime
     AND origin_airport_id =
         (SELECT id
            FROM airports
           WHERE city LIKE "Fiftyville")
ORDER BY hour, minute;

/*
NEW INFO:
First flight out was ID 36 at 8:20am
*/

.tables
.schema passengers
.schema people

-- find a passenger on the plane whose license plate matches from the bakery
SELECT name
  FROM people
       JOIN passengers
       ON passengers.passport_number = people.passport_number
       WHERE flight_id = 36   -- the flight id of the first flight out
INTERSECT   -- list only names that appear on both lists
SELECT name
  FROM people
       JOIN bakery_security_logs AS bakery
       ON bakery.license_plate = people.license_plate
       WHERE year = 2021   -- use the same bakery specifications as I did earlier to find license plate
       AND month = 7
       AND day = 28
       AND hour = 10
       AND minute BETWEEN 15 AND 25;

/*
Answers: Bruce, Kelsey, Luca, Sofia
*/

-- to find the names of those who used an ATM in the morning
SELECT DISTINCT name
  FROM people
       JOIN bank_accounts AS bank
         ON bank.person_id = people.id
               JOIN atm_transactions AS atm
                 ON atm.account_number = bank.account_number
              WHERE bank.account_number IN
                    (SELECT account_number
                       FROM [atm_transactions]
                      WHERE year = 2021
                        AND month = 7
                        AND day = 28
                        AND transaction_type LIKE "withdraw"
                        AND atm_location LIKE "Leggett%");


-- CROSS REFERENCE THE SEARCH RESULTS TO FIND COMMONALITIES
SELECT DISTINCT name -- check the names of those who made suspicious ATM transactions
  FROM people
       JOIN bank_accounts AS bank
         ON bank.person_id = people.id
               JOIN atm_transactions AS atm
                 ON atm.account_number = bank.account_number
              WHERE bank.account_number IN
                    (SELECT account_number
                       FROM [atm_transactions]
                      WHERE year = 2021
                        AND month = 7
                        AND day = 28
                        AND transaction_type LIKE "withdraw"
                        AND atm_location LIKE "Leggett%")
INTERSECT
SELECT name -- people on the first flight out of Fiftyville
  FROM people
       JOIN passengers
       ON passengers.passport_number = people.passport_number
       WHERE flight_id = 36   -- the flight id of the first flight out
INTERSECT
SELECT name -- people who pulled out of the bakery parking lot within 10 min of crime
  FROM people
       JOIN bakery_security_logs AS bakery
       ON bakery.license_plate = people.license_plate
       WHERE year = 2021   -- use the same bakery specifications as I did earlier to find license plate
       AND month = 7
       AND day = 28
       AND hour = 10
       AND minute BETWEEN 15 AND 25;

/*
ANSWERS: Bruce and Luca
*/

-- oops, forgot to check their phone number. Let's cross reference that too
SELECT name
  FROM people
       JOIN phone_calls
         ON phone_number = caller
      WHERE year = 2021
        AND month = 07
        AND day = 28
        AND duration <= 60 -- I think this is in seconds?
INTERSECT
SELECT DISTINCT name -- check the names of those who made suspicious ATM transactions
  FROM people
       JOIN bank_accounts AS bank
         ON bank.person_id = people.id
               JOIN atm_transactions AS atm
                 ON atm.account_number = bank.account_number
              WHERE bank.account_number IN
                    (SELECT account_number
                       FROM [atm_transactions]
                      WHERE year = 2021
                        AND month = 7
                        AND day = 28
                        AND transaction_type LIKE "withdraw"
                        AND atm_location LIKE "Leggett%")
INTERSECT
SELECT name -- people on the first flight out of Fiftyville
  FROM people
       JOIN passengers
       ON passengers.passport_number = people.passport_number
       WHERE flight_id = 36   -- the flight id of the first flight out
INTERSECT
SELECT name -- people who pulled out of the bakery parking lot within 10 min of crime
  FROM people
       JOIN bakery_security_logs AS bakery
       ON bakery.license_plate = people.license_plate
       WHERE year = 2021   -- use the same bakery specifications as I did earlier to find license plate
       AND month = 7
       AND day = 28
       AND hour = 10
       AND minute BETWEEN 15 AND 25;

/* Answer: BRUCE is our unlucky criminal - not quite tough enough to survive SQL database lookups. */

-- If I can find who Bruce called, I should be able to find his accomplice
SELECT name
  FROM people
        JOIN phone_calls
          ON receiver = phone_number -- joining on receiver should give the name of the person Bruce was calling
       WHERE year = 2021
         AND month = 07
         AND day = 28
         AND duration <= 60 -- I think this is in seconds?
         AND caller =
             (SELECT phone_number -- I don't have his phone number written down, oops
                FROM people
               WHERE name = "Bruce");

/* ROBIN is the accomplice! */

-- and I forgot to find the destination of the flight, but I still have the flight number so it shouldn't be too bad

.schema flights
.schema airports

SELECT city
  FROM airports
       JOIN flights
         ON destination_airport_id = airports.id
      WHERE flights.id = 36;

-- and there we have it! Bruce was helped by Robin and he flew off to New York City, only to be arrested not long after.
-- LESSONS: Never mess with SQL and absolutely NEVER mess with CS50's Rubber Duck.