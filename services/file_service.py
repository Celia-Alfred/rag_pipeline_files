
from pathlib import Path
from pypdf import PdfReader


ALLOWED_EXTENSIONS = {".pdf", ".txt"}


def extract_file_content(file):
    filename = Path(file.filename or "").name
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Only PDF and TXT files are supported."
        )

    if extension == ".pdf":
        reader = PdfReader(file)
        pages = []

        for page_number, page in enumerate(
            reader.pages, start=1
        ):
            content = page.extract_text() or ""

            if content.strip():
                pages.append({
                    "page": page_number,
                    "content": content
                })

        if not pages:
            raise ValueError(
                "No extractable text found in the PDF."
            )

        return pages

    raw_text = file.read()

    if isinstance(raw_text, bytes):
        content = raw_text.decode(
            "utf-8-sig", errors="replace"
        )
    else:
        content = raw_text

    if not content.strip():
        raise ValueError("The TXT file is empty.")

    return [{
        "page": None,
        "content": content
    }]
