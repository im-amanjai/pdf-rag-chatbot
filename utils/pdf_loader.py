from pypdf import PdfReader
import re


def fix_spaced_text(text):

    lines = []

    for line in text.split("\n"):

        words = line.split()

        if (
            len(words) > 3
            and all(len(word) == 1 for word in words)
        ):
            line = "".join(words)

        lines.append(line)

    text = "\n".join(lines)

    # Remove excessive whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    )
    text = re.sub(
        r"([a-z])([A-Z])",
        r"\1 \2",
        text
    )

    return text.strip()


def extract_text_from_pdf(uploaded_file):

    reader = PdfReader(uploaded_file)

    pages = []

    for page_num, page in enumerate(
        reader.pages
    ):

        page_text = page.extract_text()

        if page_text:

            page_text = fix_spaced_text(
                page_text
            )

            pages.append(
                {
                    "page": page_num + 1,
                    "text": page_text
                }
            )

    return pages

