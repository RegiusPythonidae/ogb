# specific to extracting information from word documents
import logging

import xml.etree.ElementTree as ET
import zipfile

# Microsoft's XML makes heavy use of XML namespaces; thus, we'll need to reference that in our code
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def open_docx(file_name: str):
    doc = zipfile.ZipFile(file_name)

    if "word/document.xml" not in doc.namelist():
        message = f"File {file_name} is unsupported. Use supported DOCX file."
        logging.error(message)
        raise Exception(message)

    document = doc.read("word/document.xml")
    return document


def document_to_paragraph_sections(document):
    root = ET.fromstring(document)

    body = root.find("w:body", NS)  # find the XML "body" tag
    p_sections = body.findall(
        "w:p", NS
    )  # under the body tag, find all the paragraph sections
    return p_sections


def paragraph_section_to_text(paragraph_section) -> str:
    text_elems = paragraph_section.findall(".//w:t", NS)
    text = "".join([t.text for t in text_elems])
    return text


def split_paragraph_on_comma(text: str) -> (int, str):
    parts = text.split(".")
    if len(parts) > 1:
        num_length = len(str(parts[0])) + 1 # +1 to account for the period
        return int(parts[0]), text[num_length:].strip()
