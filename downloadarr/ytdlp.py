import yt_dlp

def download_youtube_audio_track(link, full_filename, quality):
    try:
        ydl_opts = {
            'quiet': True,
            'noprogress': True,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': str(quality),
            }],
            'outtmpl': full_filename
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
            info_dict = ydl.extract_info(link, download=False)
            final_info = ydl.prepare_filename(info_dict)
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False