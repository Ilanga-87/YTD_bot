from yt_dlp import YoutubeDL
from yt_dlp.utils import YoutubeDLError
import yt_dlp


def get_info(url):
    ytdl_opts = {
            "quiet": True,
            'cachedir': False,
        }
    try:
        with YoutubeDL(ytdl_opts) as ydl:
            video_info = ydl.extract_info(url, download=False)
            title = video_info['title']
            duration = video_info['duration']
            output_duration = get_output_duration(duration)
            return f"You want to download audio \n{title}: {output_duration}"

    except YoutubeDLError as e:
        error_text = str(e).split(": ")[-1].strip()
        return f"{error_text} Please check copied URL."


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
                'preferredcodec': ext,
                'preferredquality': 'bestaudio',
            # TODO: add logger and progress_hook
            }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
        }
    try:
        with YoutubeDL(ytdl_opts) as ydl:
            video_info = ydl.extract_info(url, download=False)
            title = video_info['title']
            ydl.download([url])
            return f'uploads/audio/{title}.{ext}'
    except YoutubeDLError:
        pass


class MyLogger(object):
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


def my_hook(file):
    if file['status'] == 'finished':
        print(f"Done {file['filename']} downloading, now post-processing ...")
    if file['status'] == 'downloading':
        print(f'Downloading: {file["filename"]}. '
              f'Downloaded {file["downloaded_bytes"]}. '
              f'Total {file["total_bytes_estimate"]}'
              f'Speed {file["speed"]}. '
              f'Elapsed {file["elapsed"]}. '
              f'ETA: {file["eta"]}. '
              )
        pass


if __name__ == '__main__':
    get_info("https://www.youtube.com/watch?v=ktvTqknDobU")

    help(yt_dlp.YoutubeDL)
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