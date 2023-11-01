FROM python:3.10.8-alpine
WORKDIR /app

ENV PATH "$PATH:/mnt/d/PyCharm/Bots/YTD_bot"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BOT_APP = bot.py

# create directory for the botop user
RUN mkdir -p /home/botop

# create the botop user
RUN addgroup -S botop && adduser -S botop -G botop

# create the appropriate directories
ENV HOME=/home/botop
ENV APP_HOME=/home/botop/ytd_bot
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/uploads && mkdir $APP_HOME/uploads/audio
WORKDIR $APP_HOME

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apk update && apk upgrade && apk add ffmpeg

# copy project
COPY . $APP_HOME

# chown all the files to the botop user
RUN chown -R botop:botop $APP_HOME

# change to the botop user
USER botop
CMD ["python", "./bot.py"]