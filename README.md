# D&Dice
### A dice roller website

#### Video Demo: https://youtu.be/DKBCqvLDWKU

#### What is the backend built on?
This website is built using Flask, Python, and Jinja. I wanted to use something I was familiar with for the base so that I could expand into something I was very proud of.

### What is the frontend built on?
I decided to use Tailwind CSS and Daisy UI for this project. I found that out of the box bootstrap didn't look the way I wanted, and it was difficult to modernize it extensively without formatting over their custom CSS. In my research, Tailwind is a new and popular frontend framework and I was intrigued by its differences from Bootstrap. Tailwind encourages writing your styles directly into the HTML file and doesn't have any large components built in. This was a brand new workflow for me and I really enjoyed it, especially with Daisy UI to fill in a few of the component gaps and provide me with pre-styled buttons and forms.

### What files did I make for this?
##### index.html && app.route("/")
I wanted a one-page design for this project, which was a massive challenge for me. When every function is on a separate page, you have a good organization and flow to your code. It's easy to separate out the data between forms without thinking about it, and one error isn't likely to ripple through your entire website.

###### Quick Roller
This homepage has two "base" functions. One is the Quick Roller. This segment has an input box that can optionally be auto-filled for you by pressing buttons. It's designed so that if you don't like typing custom dice commands manually (like 2d4+1d20, standard tabletop dice notation), the buttons can do it for you. (See the video for a demo of that!).

After you submit that form, it parses your dice notation and outputs 1. the raw "rolls", and 2. the added total. This will further be explained in the app.py section.

###### Custom Roller
This function is also on the homepage, but it requires the user to be logged in the index function of app.py, there is a persisting notification for any user who is not logged in that this function is unavailable, and any attempts to submit custom rolls will be bounced back. I wanted users to be able to enjoy the website and understand its purpose without being logged in, and so a user will always have full access to the quick roller.

The custom roller, once you're logged in, allows the user to input a dice roll's name and formula, and allows a one-click roll from there. For example, a user could submit a roll called DEXTERITY, bound to 1d20+4. This way, any time they needed a dexterity check, it's only one click away. This function required me to input information into my SQLite3 database (dndice.db).

###### solve_roll()
This function is the core of the program. I spent a lot of time figuring out how to sort through, error check, and format dice rolls to the point that I could reliably write an algorithm to "solve" them. If the input to the program is "1d20", it's easy. Once it becomes more complicated, like "1d12+4d6-1d4-9", it gets more complicated.

The solve_roll function starts by removing extra spaces, and checking that the only characters are 0-9, +, -, and d. It outputs an error message if this is untrue.

It also references several other functions. format_roll() is designed to, well, format the roll. It takes an input like 1d20+12d4-3 and outputs it in a list of list, where 2d4 would be listed as ['+', '12', 'd', '4']. This allows my following functions to get easy access to every necessary symbol. I also wrote in a lot of format checks here. It rejects any inputs with more than one "d", that has symbols in the wrong order (i.e. "d+12") , and a wide variety of other catches that would make the roll incalculable.

There is also a separate function to format the rolls into something I can show to the user, so that a user can see that their request to roll "4d6+2d4-3" actually outputted, for example, these rolls: "4+1+5+6, 2+3, -3". The raw rolls have a comma separation between dice, and shows modifiers with their respective + or - symbol. 

And of course, the sum function will allow the user to see the final total. No one likes adding dice themselves. Because I'd put so much work into formatting and testing, I was able to replace and use an eval statement on the final string, which made the sum function a lot easier than it would've been otherwise. 

I also utilized try and except in the sum function. format_roll() was able to format any valid string in my testing, and so if anything slipped through that into sum that sum couldn't solve, I felt safe in assuming the formatting was invalid, and so I set an except statement to alert the user to invalid formatting.

##### register.html and login.html
These are fairly non-noteworthy. I used a database to record the user's information, and had a matching database table for the user's custom roll macros. I specifically wanted to ensure that error messages didn't send users to an entirely different page (not that I didn't love the memes in finance), and so I used an alert for the login and register functions as a means to notify the user of any input errors.

##### layout.html
This was the template for the site, built largely off DaisyUI's navbar options. Using DaisyUI, I built a navbar that featured an icon and dropdown for mobile users, ensuring compatibility for small screens, and a full size navbar for desktop users. It is also in layout that I implemented the theme option.

###### Themes
My site is built using Daisy UI's built in theme codes. Rather than picking colors manually, I picked colors based off of the themes' capabilities. For instance, utilizing "primary", "primary-focus", and "primary-content" as the three shades of a color rather than manually picking them. In conjunction with a CSS theme-change script by saadeghi on github (credited and linked in layout.html) this meant that on a whim, I was able to change the entire theme of my website just by changing the "data-theme" option. I offered this ability to the user as well, but offering the user a choice between one light and dark theme.

### Responsiveness
The entire website is built with Tailwind CSS' recommended "mobile first" approach, and is fully responsive. I built the site with the baseline being mobile screens, and added instructions for any screens that were large enough to justify a separate layout. This was done with tailwind's breakpoint system, as I was able to target "lg", "xl" and "2xl" screens with different instructions with ease.

### And ... that's it!
Thank you to CS50 for making this possible. Without that course, I never could've made something so cool! It may be simple, but I'm proud of it.

Thanks all!
@meljadyn