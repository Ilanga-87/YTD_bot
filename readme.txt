YouTube_to_AudioBot

TO START BOT

1. First of all you should get TOKEN for your bot. Go to BotFather in Telegam and create your bot.
Now you should create .env file and place your TOKEN in variable TELEGRAM_TOKEN.
Of course, you can choose another name or even another approach to keep you TOKEN. In this case you should edit 15th stroke in bot.py.

2. You need Docker. If you don't have it, install according instructions for your OS.
When you have Docker, you can put in CLI

docker compose build
docker compose up

or any another command to build and start container. Choose your favorite one.

Then just follow your bot link and Telegram and enjoy!

TO CLEAN UP FOLDER FROM OLD FILES

It isn't a good idea to keep old files. So we should delete them after some time. Here is example to clean up files after 7 days.

First, this command will find and delete all files older than 7 days in any subdirectory in /home/uploads/audio:

find /home/uploads/audio -mtime +6 -type f -delete

We need -mtime +6 and not +7 because -mtime counts 24h periods. As explained in the -atime section of man find (-mtime works in the same way):

   -atime n
          File  was  last  accessed n*24 hours ago.  When find figures out
          how many 24-hour periods ago the file  was  last  accessed,  any
          fractional part is ignored, so to match -atime +1, a file has to
          have been accessed at least two days ago.

So, to find a file that was modified 7 or more days ago, we need to find files that were modified more than 6 days ago, hence -mtime +6.

The next step is to have this command run once a day. Here is example for root, but it is not best practice. In real prod we should change username to actual user. So, edit /etc/crontab:

sudo nano /etc/crontab

And add this line:

@daily root find /home/uploads/audio -mtime +6 -type f -delete

That will run the find command once a day and delete the files.

