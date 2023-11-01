# YouTube_to_AudioBot

Telegram bot for downloading audio files from YouTube. Supporting formats: mp3, flac, wav, m4a.
To use bot without installation: https://t.me/YouTube_to_AudioBot or @YouTube_to_AudioBot

## Description

Bot is written on Python-Telegram-Bot module.
The downloading and conversion process is based on the "youtube-dlp" library.

## Getting started

### Dependencies

- OS Linux or Windows with WSL2 support
- Docker

## Preparation

First, you need to obtain a token for your Telegram bot using BotFather.

## Installation

To install via Docker, follow these steps:

1. Clone this git repository by running the following command in your Linux/WSL terminal:
```commandline
git clone https://github.com/Ilanga-87/YTD_bot
```
2. Navigate to the project directory using the "cd" command:

```commandline
cd YTD_bot/
```

3. Create an ".env" file in the project directory and fill in the TELEGRAM_TOKEN variable:
```commandline
nano .env
```

```commandline
TELEGRAM_TOKEN=token_you_get_from_botfather
```

6. To build production image and run container, use the following command:
```
docker compose up --build -d
```

## Usage

Once the installation is complete, open your bot in Telegram.

Please note that this service allows to download MP3 files from YouTube videos for personal use only,
and you should comply with YouTube's terms of service and any applicable copyright laws.



## Features

- Download audio files from YouTube videos in 4 formats: mp3, flac, wav, m4a.
- Very simple and straightforward interface: just send YouTube link and select audio format.
- Two languages support: English and Russian.

If you encounter any issues or have questions, feel free to reach out for support.
