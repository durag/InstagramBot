# This is a free Instagram bot web service

## Description
This is a feww webservice which is used to automate your Instagram account.
Contrary to the average user assumption, this service does NOT give you bot followers.

The purpose of this service is to login to your account using the set of logins credentials you provide 
and while logged in to YOUR account, automatically follow and like Instagram pages and posts. In doing so, the hope is that the 
users who are followed by your page will notice your Instagram page and follow you back.

After 2 days, the bot will automatically UNFOLLOW the pages it has followed so the list of pages YOU are following, will never be 
greater than 2 days worth of bot following.

This up side to this service compared to a service which just gives you bot followers is, the followers your receive from the bot 
controlling your account and following other users, are most likely all real interative users. You don't have to worry about bots following you back because most Instagram botting services don't have a "follow back" feature because...what's the point of that?

## Instructions
Using your web browser, navigate to http://185.14.184.125
You will be given the following screen
![GitHub Logo](main.jpg)
Format: ![Alt Text](url)

# Starting a bot
Click on `start new bot`
You will given the following screen
![GitHub Logo](create_empty.jpg)
Format: ![Alt Text](url)

Fill in your instagram login information using the `username` and `password` boxes.

Using the radio buttons, adjust the amount of posts and pages to like and follow per day.

In the first scrollable text box, provide a list of comma separated comments you would like
the bot to post for you. If you do not want the bot to post comments for you, you can leave this box empty.

In the second scrollable text box, provide a list of comma separated hash tags. These tags will 
be used to load lists of posts and pages for the bot to like and follow for you.
YOU MUST PROVIDE A LIST OF HASH TAGS

The last `Yes` or `No` radio buttons at the bottom indicate to the bot whether or not you want the bot 
to post comments for you.

Once you have filled out your requirements, your screen should look similar to this.
![GitHub Logo](create_filled.jpg)
Format: ![Alt Text](url)

Click `submit` and you should be taken to a "Thank You" screen like this
![GitHub Logo](thankyou.jpg)
Format: ![Alt Text](url)

# Check your bot status
From the main screen, click the button that says `view bot progress`
From this screen, you can enter your username and the bot will show you the most current progress report.

If you have just started your bot within the last 5 minutes, there will not be a progress report available 
and the server will tell you there is not a bot running under that username. If you wait 5 minutes, there should be a progress report for your bot for you to see.

# Stopping your bot
From the main screen, click the button  that says `stop existing bot`
From this screen, you can enter your Instagram username and password and if there is a bot running under those credentials, 
the server will stop it. If there is no bot running under those credentials or the credentials you provided were incorrect, 
the server will respond by saying there is no bot running under that username.

# Possible issues
Yes...this bot server is most likely not in your area. Because of this, Instagram will notice a login attempt from a different part 
of the world relative to where you normally login. Sometimes this can keep the bot from properly logging in to your account. If this happens when you try to start a bot for your account, the server will respond saying `The credentials you provided were incorrect`
If this happens and you know your username and password was correct, check your profile on Instagram and make sure there isn't a "Suspicious login notification". If there is, say it was you who tried to login, then go back to the bot server and try to start the bot again.
