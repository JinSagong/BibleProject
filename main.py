from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from bible_generator import BibleGenerator

# pip install reportlab
if __name__ == '__main__':
    book = "John"
    original = "kjv"
    translated = "hindi"

    # 글꼴 등록 (설정 > 글꼴 > ttf 파일 등록 > 사용)
    pdfmetrics.registerFont(TTFont("Times New Roman", "times.ttf"))
    pdfmetrics.registerFont(TTFont("Nirmala", "nirmala.ttf"))

    bible_generator = BibleGenerator(title=f"{book}({original},{translated})",
                                     subtitle=book,
                                     font_normal_original="Times New Roman",
                                     font_bold_original="Times New Roman",
                                     font_normal_translated="Nirmala",
                                     font_bold_translated="Nirmala")
    bible_generator.set_original_data(version=original, book=book)
    bible_generator.set_translated_data(version=translated, book=book)
    bible_generator.generate()
    bible_generator.save()
