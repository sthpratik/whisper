from youtube_dl import YoutubeDL

def download_audio(video_url):
    ydl_opts = {'format': 'bestaudio/best'}
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        ydl.download([info_dict['webpage_url']])

# Example usage
video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'  # Replace with your YouTube video URL
download_audio(video_url)
