import csv
import logging

import requests


class CSVFile:
    def __init__(self, file_path):
        """Initializes a CSVFile object"""
        self.url = file_path
        self.header = None
        self.csv_reader = None

        # read the csv file
        self._init_csv_reader()

    def _init_csv_reader(self):
        """Reads a csv file from a url without pandas"""

        response = requests.get(self.url)
        reader = csv.DictReader(response.text.splitlines())
        # self.header = next(reader)
        self.csv_reader = reader

    def get_paragraph(self, chapter_id, verse_id) -> str:
        """Returns the greek text of a paragraph"""
        try:
            for row in self.csv_reader:
                if int(row['chapter']) == chapter_id and int(row['verse']) == verse_id:
                    return row['text']
            # if not found
            raise IndexError("Not found")
        except Exception as error:
            message = f"Error at {chapter_id} : {verse_id} - {error}"
            # TODO: create logger function
            # current_app.logger.error(message)
            logging.error(message)
            return message


if __name__ == "__main__":
    url = 'https://gist.githubusercontent.com/Tamarae/da51f7fdab1106524657be69d6b3d918/raw/224d7c8bc30dbf776894083c0865c88273fcc269/Tobit_greek'
    file = CSVFile(url)
    text1 = file.get_paragraph(40, 1)
    logging.debug(text1)
