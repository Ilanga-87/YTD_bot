FROM python:3.10.8-alpine
WORKDIR /app
ENV BOT_APP = bot.py

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "./bot.py"]