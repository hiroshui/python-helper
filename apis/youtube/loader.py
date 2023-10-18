import sys
from pytube import YouTube

class Loader:
    """
    A class for downloading YouTube videos.

    Methods:
    --------
    download_video(url, output_path):
        Downloads a YouTube video given its URL and saves it to the specified output path.
    """

    def download_video(url, output_path):
        """
        Downloads a YouTube video given its URL and saves it to the specified output path.

        Parameters:
        -----------
        url : str
            The URL of the YouTube video to download.
        output_path : str
            The path where the downloaded video will be saved.
        """
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path)

if __name__ == '__main__':
    url = ""
    if len(sys.argv) < 2:
        print("Warning: Input file name not provided. Will download gangnam style.")
        url = 'https://www.youtube.com/watch?v=9bZkp7q19f0' #gangman style
    else:
        url = sys.argv[1]
    output_path = 'downloads'
    Loader.download_video(url, output_path)