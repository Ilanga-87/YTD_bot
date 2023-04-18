import os
import re
from pydub import AudioSegment

from yt_dlp import YoutubeDL
from yt_dlp.utils import YoutubeDLError

from static_text import messages
from manage_data import id_dict
import manage_data


def get_info(message_id, url):
    ytdl_opts = {
        "quiet": True,
        'cachedir': False,
    }
    try:
        with YoutubeDL(ytdl_opts) as ydl:
            track_url = extract_single_from_playlist(url)
            video_info = ydl.extract_info(track_url, download=False)
            title = video_info['title']
            new_title = clear_title(title)
            id_dict[message_id].append(new_title)
            duration = video_info['duration']
            output_duration = get_output_duration(duration)
            if duration > 4000:
                manage_data.huge_file_flag = True
                message = f"{messages[manage_data.selected_language]['file_too_long_text']}"
                return message.format(title, output_duration)
            if duration > 1200:
                manage_data.long_file_flag = True
                message = f"{messages[manage_data.selected_language]['need_compress_text']}"
                return message.format(title)
                # return f"{messages[manage_data.selected_language]['audio_name_text']} \n{title} ({output_duration})"
            output_duration = get_output_duration(duration)
            return f"{messages[manage_data.selected_language]['audio_name_text']} \n{title} ({output_duration})"

    except YoutubeDLError as e:
        error_text = str(e).split(": ")[-1].strip()
        print(error_text)
        return f"{messages[manage_data.selected_language]['check_url_text']}"


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
    return f'{hours:02}:{minutes:02}:{seconds:02}' if hours > 0 else f'{minutes:02}:{seconds:02}'


def check_file_on_server(filename):
    folder = "uploads/audio/"
    file_path = os.path.join(folder, filename)

    if os.path.isfile(file_path):
        return True
    else:
        return False


def download(url, title, ext):
    ytdl_opts = {
        "quiet": True,
        'cachedir': False,
        'outtmpl': f'uploads/audio/{title}.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': ext,
            'preferredquality': 'bestaudio[filesize<50M]',
        }],
        'logger': YTDLogger(),
        'progress_hooks': [progress_hook],
    }
    try:
        with YoutubeDL(ytdl_opts) as ydl:
            track_url = extract_single_from_playlist(url)
            if not check_file_on_server(title + '.' + ext):
                ydl.download([track_url])

                # Check it size
                file_size = os.path.getsize(f'uploads/audio/{title}.{ext}')
                if file_size > 5000000:
                    print(f"{title} SIZE: {file_size}")
                    return compress_file(title, ext)
                else:
                    return f"uploads/audio/{title}.{ext}"
            return f"uploads/audio/{title}.{ext}"
    except YoutubeDLError as e:
        error_text = str(e).split(": ")[-1].strip()
        print(error_text)
        return f"{messages[manage_data.selected_language]['you_tube_error_text']}"


def download_long(url, title, ext):
    ytdl_opts = {
        "quiet": True,
        'cachedir': False,
        'outtmpl': f'uploads/audio/{title}.%(ext)s',
        'format': 'worstaudio/worst',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': ext,
            'preferredquality': 'worstaudio[filesize<50M]',
        }],
        'logger': YTDLogger(),
        'progress_hooks': [progress_hook],
    }
    try:
        with YoutubeDL(ytdl_opts) as ydl:
            track_url = extract_single_from_playlist(url)
            if not check_file_on_server(title + '.' + ext):
                ydl.download([track_url])

                # Check it size
                file_size = os.path.getsize(f'uploads/audio/{title}.{ext}')
                if file_size > 50 * 1024 * 1024:
                    print(f"{title} SIZE: {file_size}")
                    return compress_file(title, ext)
                else:
                    return f"uploads/audio/{title}.{ext}"
            return f"uploads/audio/{title}.{ext}"
    except YoutubeDLError as e:
        error_text = str(e).split(": ")[-1].strip()
        print(error_text)
        return f"{messages[manage_data.selected_language]['you_tube_error_text']}"


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
        # print(f"Downloading: {file['filename']}. "
        #       f"Progress: {progress}%. "
        #       # f"Speed {file['speed']}. "
        #       # f"Elapsed {file['elapsed']}. "
        #       # f"ETA: {file['eta']}. "
        #       )


def clear_title(title_string):
    # output_string = re.sub(
    #     r"[^\w\u0400-\u04FF\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u00FF\u0100-\u024F\u1E00-\u1EFF\u3040-\u30FF\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\uFF00-\uFFEF\u2000-\u206F\u2070-\u209F\u20A0-\u20CF\u2100-\u214F\u2150-\u218F\u2190-\u21FF]+",
    #     " ", title_string)
    output_string = re.sub(r"[^a-zA-Zа-яА-Я0-9\s]+", "", title_string)  # Remove non-alphanumeric characters
    output_string = re.sub(r"\s{2,}", " ", output_string)  # Replace multiple spaces with single space
    output_string = re.sub(r"\s+", "_", output_string)  # Replace single spaces with underscore
    return output_string


def compress_file(file_name, file_ext):
    # Define the input and output file paths
    input_file = f"uploads/audio/{file_name}.{file_ext}"
    legacy_file = f"uploads/audio/{file_name}_old.{file_ext}"
    output_file = f"uploads/audio/{file_name}.{file_ext}"

    # Load the audio file
    audio = AudioSegment.from_file(input_file)
    os.rename(input_file, legacy_file)

    # Set the output format and initial compression options
    output_format = file_ext
    compression_options = {'bitrate': '128k'}

    # Iterate over compression options until desired file size is reached
    max_file_size = 50 * 1024 * 1024  # 50 megabytes in bytes
    while True:
        # Export the compressed audio to a temporary file
        temp_output_file = f"uploads/audio/{file_name}_p.{file_ext}"
        audio.export(temp_output_file, format=output_format, bitrate=compression_options['bitrate'])

        # Check the size of the temporary file
        temp_file_size = os.path.getsize(temp_output_file)
        print(f"{file_name} SIZE: {temp_file_size}")
        # If the temporary file is within the desired file size, save it as the final output file and exit the loop
        if temp_file_size <= max_file_size:
            os.rename(temp_output_file, output_file)
            break

        # If the temporary file is too large, reduce the compression options and try again
        compression_options['bitrate'] = str(int(int(compression_options['bitrate'][:-1]) * 0.7)) + 'k'
        print(f"Current bitrate: {compression_options['bitrate']}")
        print(output_file)
    return output_file


if __name__ == '__main__':

    stripped = "Rainy Forest Sounds for Sleeping, Meditation and Study 🌧️ 3 Hours White Noise Gentle Rain (03:02:06)".split("(")[-1][:-1]
    print(stripped)
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
