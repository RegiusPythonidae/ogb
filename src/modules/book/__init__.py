from src.tools.docx_processor import (
    document_to_paragraph_sections,
    open_docx,
    paragraph_section_to_text,
    split_paragraph_on_comma,
)


class Book:
    def __init__(
        self,
        title,
        file_path,
        edition=None,
        editor=None,
        email=None,
        publisher=None,
        publication_place=None,
        publication_date=None,
        source=None,
        location=None,
        date=None,
        additional_details=None,
    ):

        self.title = title
        self.file_path = file_path

        self.edition = edition
        self.editor = editor
        self.email = email
        self.publisher = publisher
        self.publication_place = publication_place
        self.publication_date = publication_date
        self.source = source
        self.location = location
        self.date = date
        self.additional_details = additional_details

        self.chapters = []
        self.length = 0

        self.__document = None

    def read_file(self):
        self.__document = open_docx(self.file_path)

        paragraph_sections = document_to_paragraph_sections(self.__document)

        chapter = None
        previous_index = 0
        paragraph = None
        for section in paragraph_sections[:100]:
            text = paragraph_section_to_text(section)
            # find chapter
            if len(text) == 1 and text != " ":
                if chapter is not None:
                    self.add_chapter(chapter)

                chapter = Chapter(int(text))
                continue

            # if paragraph contains text to process
            if parts := split_paragraph_on_comma(text):
                #         print(previous_index,parts)
                # read index and content of paragraph
                current_index, current_text = parts
                # if new index
                if previous_index != current_index:
                    if paragraph is not None:
                        chapter.add_paragraph(paragraph)
                    paragraph = Paragraph(current_index, current_text, chapter.index)
                    previous_index = current_index
                else:
                    paragraph.notes = current_text

        # save the last paragraph
        chapter.add_paragraph(paragraph)

    def __len__(self):
        return self.length

    def __repr__(self):
        return f"{self.title}"

    def add_chapter(self, chapter):
        self.chapters.append(chapter)
        self.length += 1




class Chapter:
    def __init__(self, index):
        self.index = index
        self.paragraphs = []
        self.length = 0

    def __len__(self):
        return self.length

    def __repr__(self):
        return f"Chapter {self.index}"

    def add_paragraph(self, paragraph):
        self.paragraphs.append(paragraph)
        self.length += 1

    def clear(self):
        self.paragraphs.clear()
        self.length = 0


class Paragraph:
    def __init__(self, index, text, chapter_index=0):
        self.index = index
        self.chapter_index = chapter_index

        self.text = text
        self.notes = ""

    def __repr__(self):
        return f"{self.index}. ტექსტი: {self.text} \n\tანოტაცია: {self.notes}"

