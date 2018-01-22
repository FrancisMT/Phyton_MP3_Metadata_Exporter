import eyed3
from time import time
from queue import Queue
from os import path
from tkinter import filedialog, simpledialog
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

# Queue where all the songs metadata will be placed for later processing
song_mt_queue = Queue()


class SongMetaData:
    """Store Metadata"""

    __path = ""

    title = ""
    artist = ""
    album = ""
    year = ""
    genre = ""

    def __init__(self, song_file_path):
        self.__path = song_file_path
        self.__get_song_metadata()

    def __get_song_metadata(self):
        audio_file = eyed3.load(self.__path)

        self.title = audio_file.tag.title
        self.artist = audio_file.tag.artist
        self.album = audio_file.tag.album
        self.genre = audio_file.tag.genre
        self.year = audio_file.tag.best_release_date

    def debug_print_song_metadata(self):
        print("Title: {0}\n"
              "Artist: {1}\n"
              "Album: {2}\n"
              "Genre: {3}\n"
              "Year: {4}\n"
              .format
              (self.title,
               self.artist,
               self.album,
               self.genre,
               self.year))


def add_metadata_to_queue(song_file_path):
    song_metadata = SongMetaData(song_file_path)
    song_mt_queue.put(song_metadata)


def process_csv_filename(csv_file_name):
    if not csv_file_name.endswith(".csv"):
        csv_file_name += ".csv"
        return csv_file_name


def main():
    current_path = path.dirname(path.realpath(__file__))

    song_paths = filedialog.askopenfilenames(initialdir=current_path, title="Select file",
                                             filetypes=[("mp3 files", "*.mp3")])

    start_time = time()

    # Use ProcessPool instead of ThreadPool to get the each song's metadata in parallel.
    # Notes {
    #           * ThreadPool uses one core while  uses multiple cores.
    #           * Rule of thumb:
    #               + IO bound jobs -> ThreadPool
    #               + CPU bound jobs -> ProcessPool
    #       }

    # TODO: Figure out why queues work ThrePools but not with ProcessPool
    with ProcessPoolExecutor() as executor:
        for song_path in song_paths:
            executor.submit(add_metadata_to_queue, song_path)

    #  Get .csv file name from user and process queue
    csv_filename = process_csv_filename(simpledialog.askstring("Metadata exporter", ".csv filename: "))
    while not song_mt_queue.empty():
        metadata = song_mt_queue.get()
        metadata.debug_print_song_metadata()

    end_time = time()
    # print("Finished exporting {0} song(s) to {1}")


if __name__ == '__main__':
    main()
