import os
from yt_dlp import YoutubeDL
from yt_dlp.utils import YoutubeDLError

from manage_data import yt_url


def get_info(url):
    ytdl_opts = {
        "quiet": True,
        'cachedir': False,
    }
    try:
        with YoutubeDL(ytdl_opts) as ydl:
            track_url = extract_single_from_playlist(url)
            video_info = ydl.extract_info(track_url, download=False)
            title = video_info['title']
            new_title = title.replace("/", "")
            yt_url.append(new_title)
            duration = video_info['duration']
            output_duration = get_output_duration(duration)
            return f"You want to download audio \n{title} ({output_duration})"

    except YoutubeDLError as e:
        error_text = str(e).split(": ")[-1].strip()
        return f"{error_text} Please check copied URL."


def extract_single_from_playlist(video_url):
    """Get URL to single track from playlist, channel or another instance."""
    splitted_url = video_url.split('&')
    return splitted_url[0]


def get_output_duration(seconds: int):
    """Get output duration from seconds."""
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return f'{hours}:{minutes}:{seconds}s' if hours > 0 else f'{minutes}:{seconds}'


def download(url, title, ext):
    ytdl_opts = {
        "quiet": True,
        'cachedir': False,
        'outtmpl': f'uploads/audio/{title}.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': ext,
            'preferredquality': 'bestaudio',
        }],
        'logger': YTDLogger(),
        'progress_hooks': [progress_hook],
    }
    try:
        with YoutubeDL(ytdl_opts) as ydl:
            track_url = extract_single_from_playlist(url)
            video_info = ydl.extract_info(track_url, download=False)
            title = video_info['title']
            new_title = title.replace("/", "")
            ydl.download([track_url])
            file = f'D:/PyCharm/Bots/YTD_bot/uploads/audio/{title}.{ext}'
            # new_file = f'D:/PyCharm/Bots/YTD_bot/uploads/audio/{new_title}.{ext}'
            # old_path = file[:]
            # new_path = new_file[:]
            # os.rename(old_path, new_path)
            return f"uploads/audio/{new_title}.{ext}"
    except YoutubeDLError as e:
        error_text = str(e).split(": ")[-1].strip()
        return f"{error_text}"


class YTDLogger(object):
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def progress_hook(file):
    if file['status'] == 'finished':
        print(f"Done {file['filename']} downloading, now post-processing ...")
    if file['status'] == 'downloading':
        progress = file['downloaded_bytes'] * 100 / file['total_bytes_estimate']
        print(f"Downloading: {file['filename']}. "
              f"Progress: {progress}%. "
              # f"Speed {file['speed']}. "
              # f"Elapsed {file['elapsed']}. "
              # f"ETA: {file['eta']}. "
              )
        pass


if __name__ == '__main__':
    get_info("https://www.youtube.com/watch?v=ktvTqknDobU")

    progress_hooks_info = """
    progress_hooks:    A list of functions that get called on download
 |                     progress, with a dictionary with the entries
 |                     * status: One of "downloading", "error", or "finished".
 |                               Check this first and ignore unknown values.
 |                     * info_dict: The extracted info_dict
 |  
 |                     If status is one of "downloading", or "finished", the
 |                     following properties may also be present:
 |                     * filename: The final filename (always present)
 |                     * tmpfilename: The filename we're currently writing to
 |                     * downloaded_bytes: Bytes on disk
 |                     * total_bytes: Size of the whole file, None if unknown
 |                     * total_bytes_estimate: Guess of the eventual file size,
 |                                             None if unavailable.
 |                     * elapsed: The number of seconds since download started.
 |                     * eta: The estimated time in seconds, None if unknown
 |                     * speed: The download speed in bytes/second, None if
 |                              unknown
 |                     * fragment_index: The counter of the currently
 |                                       downloaded video fragment.
 |                     * fragment_count: The number of fragments (= individual
 |                                       files that will be merged)
 |  
 |                     Progress hooks are guaranteed to be called at least once
 |                     (with status "finished") if the download is successful."""

    postprocessor_hooks_info = """
     postprocessor_hooks:  A list of functions that get called on postprocessing
 |                     progress, with a dictionary with the entries
 |                     * status: One of "started", "processing", or "finished".
 |                               Check this first and ignore unknown values.
 |                     * postprocessor: Name of the postprocessor
 |                     * info_dict: The extracted info_dict
 |  
 |                     Progress hooks are guaranteed to be called at least twice
 |                     (with status "started" and "finished") if the processing is successful."""
