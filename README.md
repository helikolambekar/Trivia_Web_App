# BUMETCS673A1F21P1

Project Description

KnowItAll is an innovative and interactive trivia web application which allows players to test their knowledge across thousands of questions from a variety of topics. Users can participate in single-player or multiplayer games to unlock special player badges. KnowItAll’s global leaderboards reflect the top scores in every category. Prolific players can win lucrative rewards. 
The motivation for the proposed project derives from the desire to create a unique trivia web application with real world utility and impact. Our motivation includes the desire to learn software development skills, agile methodologies, software architecture, design principles. The purpose of the proposed software project is to develop software using secure software development practices while utilizing the latest software development tools and technologies.
Online gaming industry has a very high number of active users. It has an ever increasing market share of advertisement revenue and corporate investment. The potential users for the project include seasoned trivia players, beginners and players motivated by lucrative rewards. 

## HOW TO RUN

1- Clone Repository:
```
$git clone [respository]
```
2- Navigate to the BU... folder
```
cd BUMETCS673A1F21P1/source
```
3- Checkout the right branch
```
$git checkout Gunnar_iter_2
```
4- Navigate to the source folder
```
cd source
```
5- Set up a Virtual Environment - Instructions for this step apply for Mac, PC instructions will be added in a later iteration.
```
MAC
$virtualenv venv
$source venv/bin/activate
PC
$python3 -m venv env
$source env/Scripts/activate
```
You should now see "(env)" before your username in the command line. This keeps all of your dependencies in one location. To check where your python modules of being imported run the command:
```
$which pip
```
to deactivate your vertual environement run the command:
```
(venv)$ deactivate
```
6-Download Dependecies
```bash
pip install -r requirements.txt
```
7-Navigate back to the previous directory
```
cd ..
```
8- Run the flask application
```
$export FLASK_APP=main.py
$export FLASK_ENV=None
$flask run
```
9- Navigate your browser to: http://localhost:5000/
## Features

         

a.	Essential Features


1.	Player Profiles - Users can create an account with username and email ID. Players   can   choose an avatar. 


2.	Categories- Users can choose to answer trivia from topics such as geography, music,     entertainment and sports.


3.	Quiz - For every question, the player must select the correct answer from four different    options within the stipulated time frame. Players score points for every                     correct answer. The difficulty level of the questions increases with the points scored by the player.  Three incorrect answers cause the player to lose the                       match. Final player scores are recorded and compared against top scores on the leaderboard. A player can seek hints during the match depending on their players. 


4.	The Leaderboard- The top 10 players with the best scores in every category are featured on the leaderboard.



b.	Desirable Features


1.	Special Player Badges - Upon achieving a certain high score in the match, the player can unlock special badges which reflect on the player’s profile.


2.	Rewards- The player can win rewards and perks upon completing 1000, 2000 and 5000 questions in a specific trivia category.


3.	Multiplayer Options- Two users are pitted against each other for a trivia showdown. 
                       
c)   Optional Features

1.	Posting to social media platforms- Users can post about player badges and send social media invites to friends to play multiplayer games. 

## Nonfunctional Requirements
Security Requirements 
1.	User Authentication using email
2.	Password Strength Settings
3.	Backup and Recovery Options
•	Scalability
Application is tailored to handle a large number of user requests
•	Reliability
Application should provide reliable results consistently
•	Performance
Application should provide a seamless user experience with high performance even with large traffic volumes
•	Security
Application should be resilient in the face of malicious malware and attacks


## Technology and Frameworks


•	Backend Framework-  Flask
•	Frontend Framework- Javascript
•	Version Control- Git (Github)
•	Project Planning Tool- Pivotal Tracker


