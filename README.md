# Egg_Hatcher

**Description**

Egg Hatcher is an online game and social experiment based off [The Button](https://en.wikipedia.org/wiki/The_Button_(Reddit)).

The website displays a chicken and two buttons. One button has the chicken lay an egg, while the other button hatches all the eggs. The goal is to see who can hatch the most eggs at once, but the current number of eggs is unknown. Each player can only hatch one egg every 60 seconds, so there is tension as the player decides if they should lay another egg or hatch all the eggs for themselves. A user can login with a username to keep track of the most eggs they've peronsally hatched. When a player hatches the eggs they will see their scores and the high score.

**Instructions**
Download project code and install required packages (flask and flask-sqlalchemy)
Run egg_hatcher.py in terminal to start a local host of the website.

**Code Structure**
The website is built using flask as a web framework and a database model using flask-sqlalchemy to keep track of user info and scores. There is are classes for the timer function and keeping track of the egg count. 
