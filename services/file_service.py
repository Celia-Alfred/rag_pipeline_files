
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
        try:
            reader = PdfReader(file)
        except Exception as error:
            raise ValueError(
                f"Could not read PDF file: {error}"
            ) from error

        pages = []
        empty_pages = []

        for page_number, page in enumerate(
            reader.pages, start=1
        ):
            try:
                try:
                    content = page.extract_text(
                        extraction_mode="layout"
                    ) or ""
                except (TypeError, ValueError, NotImplementedError):
                    content = page.extract_text() or ""

                if content.strip():
                    pages.append({
                        "page": page_number,
                        "content": content.strip()
                    })
                else:
                    empty_pages.append(page_number)

                print(
                    f"[PDF Extraction] Page {page_number}: "
                    f"{len(content)} characters",
                    flush=True
                )

                if content.strip():
                    print(
                        f"[PDF Extraction] Preview: "
                        f"{content[:200]!r}",
                        flush=True
                    )

            except Exception as error:
                print(
                    f"[PDF Extraction] Failed on page "
                    f"{page_number}: {error}",
                    flush=True
                )
                empty_pages.append(page_number)

        if empty_pages:
            print(
                "[PDF Extraction] Pages with no extracted text "
                f"(possibly scanned/image-only): {empty_pages}",
                flush=True
            )

        if not pages:
            raise ValueError(
                "No extractable text found in the PDF. "
                "It may be scanned or image-based and require OCR."
            )

        return pages

    try:
        raw_text = file.read()

        if isinstance(raw_text, bytes):
            content = raw_text.decode(
                "utf-8-sig",
                errors="replace"
            )
        else:
            content = raw_text

    except Exception as error:
        raise ValueError(
            f"Could not read TXT file: {error}"
        ) from error

    if not content.strip():
        raise ValueError("The TXT file is empty.")

    return [{
        "page": None,
        "content": content.strip()
    }]
