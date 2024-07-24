import fitz


def format_text(text: str) -> str:
    clean = text.replace("\n", " ").strip()
    print(clean)
    return clean


def get_text(file):
    file.seek(0)
    doc = fitz.open(stream=file.read(), filetype='pdf')
    for pg in doc:
        print(f"_____{pg.number}_____ \n\n")
        text = format_text(pg.get_text())
        pagewise_text = {"doc": file.name,
                         "page_num": pg.number,
                         "text": text
                         }
    return pagewise_text
