import csv
from src.modules.book.models import is_new_chapter
from src.tools import open_docx, document_to_paragraph_sections, paragraph_section_to_text

PATH = "C:\\Users\\conta\\PycharmProjects\\Iliauni\\DigitalBooks\\athonite_web_app\\athonite_web_app\\data" \
       "\\Tobit_Greek.docx "

CSV_HEADERS = ["chapter", "verse", "text"]

document = open_docx(PATH)
paragraph_sections = document_to_paragraph_sections(document)

chapter: int = 0
verse: int = 0
text: str

csv_rows = list()


def generate_csv_row(chapter: int, verse: int, text: str) -> dict:
    return {"chapter": chapter, "verse": verse, "text": text}


def list_of_dict_to_csv(list_of_dict: list, file_name: str):
    with open(file_name, "w", newline="", encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(list_of_dict)


for section in paragraph_sections:
    text = paragraph_section_to_text(section).strip()
    # create new chapter and jump to next line
    if is_new_chapter(text):
        # if exists save the previous chapter
        chapter = int(text)
        verse = 0
        continue
    else:
        verse += 1

    print(f"{chapter} {verse} {text}")
    csv_rows.append(generate_csv_row(chapter, verse, text))

list_of_dict_to_csv(csv_rows, "Tobit_Greek.csv")
