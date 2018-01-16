import eyed3
from os import path
from tkinter import filedialog


# Python Threading Tutorial https://stackoverflow.com/questions/16199793/simple-threading-event-example
class SongData:
    """Store Song Data and Metada Information"""

    __path = ""

    __title = ""
    __artist = ""
    __album = ""
    __year = ""
    __genre = ""

    def __init__(self, song_file_path):
        self.__path = song_file_path
        self.__process_song_metadata()

    def __process_song_metadata(self):
        audio_file = eyed3.load(self.__path)

        self.__title = audio_file.tag.title
        self.__artist = audio_file.tag.artist
        self.__album = audio_file.tag.album
        self.__genre = audio_file.tag.genre
        self.__year = audio_file.tag.best_release_date

    def print_song_metadata(self):
        print("Title: {0}\n"
              "Artist: {1}\n"
              "Album: {2}\n"
              "Genre: {3}\n"
              "Year: {4}\n"
              .format
              (self.__title,
               self.__artist,
               self.__album,
               self.__genre,
               self.__year))


def main():
    current_path = path.dirname(path.realpath(__file__))

    song_paths = filedialog.askopenfilenames(initialdir=current_path, title="Select file",
                                             filetypes=[("mp3 files", "*.mp3")])

    for song_path in song_paths:
        new_song_data = SongData(song_path)
        new_song_data.print_song_metadata()


if __name__ == '__main__':
    main()
