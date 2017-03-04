# Project 2  Handin 2 Daniel Wilson
I tried to use a simple theme for this project that I could manipulate using CSS.
I used a simple white theme with subtle background pattern.
In the interaction with my chatbot I added a 'What should I wear?' command, which leverages the DarkSky API and gives a response informing the user of the forcasted weather.

## Known Problems
This was a very challenging project. Although I was not able to finish all the assigned milestones on the first handin, it was completed in the end.
As of now there are no problems that I know of. If I had more time I would add another API call to add to the chatbot personality.
I would also look into speeding up the socketio intervals so that when a user disconnects, they are removed from the database faster.
This would prevent duplicate entries of the user appearing in the userlist if they try to log back into the app to quickly.
I would really liked to have been able to get the login authentication to trigger a history load. Instead the user is prompted to click get history button.

#### Improvements from handin 1
1. Built ChatBot
  * Name ends with bot, profile picture clearly identifiable as a bot.
  * Responds to !! about, !! help, !! say <something>, unrecognized command, and an additional 'What time is it?' command.
  * Added 'What should I wear?' command for handin 2 which uses Dark Sky API.
2. Google authentication
  * I added Google authentication functionality but removed the functionality at the last minute. The authentication works but I could not figure out how to impliment logging out. I felt the app worked better with only FaceBook login functionality.
3. User list
  * Added sidebar to chat window that displays functioning user list. The users are added to a database table and removed by their flask SID upon disconnect.
  * Chatbot is always logged in.