import re
from pdfminer.high_level import extract_pages, extract_text

def remove_empty_lines(text):
    lines = [line for line in text.splitlines() if line.strip()]
    return '\n'.join(lines)

text = extract_text("ib_lek.pdf")
text = remove_empty_lines(text)
print(text)