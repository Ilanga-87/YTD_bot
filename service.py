from yt_dlp import YoutubeDL
from yt_dlp.utils import YoutubeDLError


def get_info(url):
    ytdl_opts = {
            "quiet": True,
            'cachedir': False,
        }
    try:
        with YoutubeDL(ytdl_opts) as ydl:
            video_info = ydl.extract_info(url, download=False)
            print(video_info)
            video_id = video_info['id']
            title = video_info['title']
            duration = video_info['duration']
            output_duration = get_output_duration(duration)
            return f"You want to download audio \n\t {title}: {output_duration}"

    except YoutubeDLError:
        return f"URL {url} looks truncated. Please try to copy it again."


def get_output_duration(seconds: int):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return f'{hours}:{minutes}:{seconds}s' if hours > 0 else f'{minutes}:{seconds}'


def download(url, ext):
    ytdl_opts = {
            "quiet": True,
            'cachedir': False,
            'outtmpl': f'uploads/audio/%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': ext, # wav, flac, mp3, aac, m4a, ogg, webm
                'preferredquality': 'bestaudio', # 128, 192, 256, 320 // higher for flac etc
            # TODO: add logger and progress_hook
            }],
        }
    try:
        with YoutubeDL(ytdl_opts) as ydl:
            ydl.download([url])
            return {"status": True}
    except YoutubeDLError:
        pass


if __name__ == '__main__':
    get_info("https://www.youtube.com/watch?v=ktvTqknDobU")
