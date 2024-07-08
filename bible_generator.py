from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A5
from reportlab.pdfbase import pdfmetrics

from bible_parser import BibleParser


class BibleGenerator:
    def __init__(self,
                 title,
                 subtitle,
                 size=A5,
                 font_normal_original="Times New Roman",
                 font_bold_original="Times New Roman",
                 font_normal_translated="Times New Roman",
                 font_bold_translated="Times New Roman",
                 font_size=8,
                 char_spacing=2,
                 line_spacing=4,
                 margin_top=25,
                 margin_bottom=40,
                 margin_left=35,
                 margin_right=35,
                 margin_inner=10):
        self.__canvas = Canvas(f"{title}.pdf", pagesize=size)

        self.subtitle = subtitle
        self.width, self.height = size

        self.font_normal_original = font_normal_original
        self.font_bold_original = font_bold_original
        self.font_normal_translated = font_normal_translated
        self.font_bold_translated = font_bold_translated
        self.font_normal_height_original = None
        self.font_bold_height_original = None
        self.font_normal_height_translated = None
        self.font_bold_height_translated = None
        self.font_size = font_size
        self.font_size_bold_original = None
        self.font_size_bold_translated = None
        self.char_spacing = char_spacing
        self.line_spacing = line_spacing

        self.margin_top = margin_top
        self.margin_bottom = margin_bottom
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.margin_inner = margin_inner

        self.__set_font()

        self.data_original = None
        self.data_translated = None

    def set_original_data(self, version, book):
        parser = BibleParser(version, book)
        self.data_original = parser.get_data()

    def set_translated_data(self, version, book):
        parser = BibleParser(version, book)
        self.data_translated = parser.get_data()

    def __set_font(self):
        pdfmetrics.registerFont(TTFont("Times New Roman", "times.ttf"))

        face = pdfmetrics.getFont(self.font_normal_original).face
        self.font_normal_height_original = face.capHeight / 1000 * self.font_size
        face = pdfmetrics.getFont(self.font_bold_original).face
        h = face.capHeight / 1000
        l = self.font_size
        r = self.font_size * 4
        t = (l + r) / 2
        delta = h * t - (self.font_normal_height_original * 2 + self.line_spacing)
        while round(delta, 6) != 0:
            t = (l + r) / 2
            delta = h * t - (self.font_normal_height_original * 2 + self.line_spacing)
            if delta >= 0:
                r = t
            else:
                l = t
        self.font_size_bold_original = t
        self.font_bold_height_original = h * t

        face = pdfmetrics.getFont(self.font_normal_translated).face
        self.font_normal_height_translated = face.capHeight / 1000 * self.font_size
        face = pdfmetrics.getFont(self.font_bold_translated).face
        h = face.capHeight / 1000
        l = self.font_size
        r = self.font_size * 4
        t = (l + r) / 2
        delta = h * t - (self.font_normal_height_translated * 2 + self.line_spacing)
        while round(delta, 6) != 0:
            t = (l + r) / 2
            delta = h * t - (self.font_normal_height_translated * 2 + self.line_spacing)
            if delta >= 0:
                r = t
            else:
                l = t
        self.font_size_bold_translated = t
        self.font_bold_height_translated = h * t

    # 화면과 객체의 좌측 하단 좌표가 (0,0)인 표시방법을 사용함
    def __draw_page(self, page_num, title, data_original, data_translated):
        self.__canvas.setFont(self.font_normal_original, self.font_size)
        self.__canvas.drawString(self.margin_left,
                                 self.height - self.margin_top - self.font_normal_height_original,
                                 str(page_num * 2 - 1))
        temp_width = self.__canvas.stringWidth(str(page_num * 2), fontSize=self.font_size)
        self.__canvas.drawString(self.width - self.margin_right - temp_width,
                                 self.height - self.margin_top - self.font_normal_height_original,
                                 str(page_num * 2))
        temp_width = self.__canvas.stringWidth(title, fontSize=self.font_size)
        self.__canvas.drawString((self.width - temp_width) / 2,
                                 self.height - self.margin_top - self.font_normal_height_original, title)
        self.__canvas.setLineWidth(0.5)
        self.__canvas.line(self.margin_left,
                           self.height - self.margin_top - self.font_normal_height_original - 1,
                           self.width - self.margin_right,
                           self.height - self.margin_top - self.font_normal_height_original - 1)
        self.__canvas.line((self.width - self.margin_left - self.margin_right) / 2 + self.margin_left - 0.25,
                           self.height - self.margin_top - self.font_normal_height_original - 1,
                           (self.width - self.margin_left - self.margin_right) / 2 + self.margin_left - 0.25,
                           self.margin_bottom)

        self.__draw_data(data_original,
                         self.margin_left,
                         self.height - self.margin_top - self.font_normal_height_original - 1.5 - self.line_spacing,
                         self.font_size_bold_original,
                         self.font_normal_original,
                         self.font_bold_original,
                         self.font_normal_height_original,
                         self.font_bold_height_original)
        self.__draw_data(data_translated,
                         (self.width - self.margin_left - self.margin_right) / 2 + self.margin_left + self.margin_inner,
                         self.height - self.margin_top - self.font_normal_height_original - 1.5 - self.line_spacing,
                         self.font_size_bold_translated,
                         self.font_normal_translated,
                         self.font_bold_translated,
                         self.font_normal_height_translated,
                         self.font_bold_height_translated)

        self.__canvas.showPage()

    def __draw_data(self, data, x, y, font_size_bold, font_normal, font_bold, font_normal_height, font_bold_height):
        v = 0
        idx_width = 0
        first_verse_y = -1
        for item in data:
            if item["verse"] != v:
                v = item["verse"]
                if item["verse"] == 1:
                    self.__canvas.setFont(font_bold, font_size_bold)
                    self.__canvas.drawString(x, y - font_bold_height, str(item['chapter']))
                    idx_width = self.__canvas.stringWidth(str(item['chapter']),
                                                          fontSize=font_size_bold) + self.char_spacing
                    self.__canvas.setFont(font_normal, self.font_size)
                    first_verse_y = y - font_bold_height
                    y = first_verse_y + font_normal_height * 2 + self.line_spacing
                else:
                    self.__canvas.setFont(font_normal, self.font_size)
                    if first_verse_y != -1 and first_verse_y < y:
                        y -= font_normal_height + self.line_spacing
                    self.__canvas.drawString(x, y - font_normal_height, str(item['verse']))
                    idx_width = self.__canvas.stringWidth(str(item['verse']),
                                                          fontSize=self.font_size) + self.char_spacing
            self.__canvas.drawString(x + idx_width, y - font_normal_height, item["text"])
            y -= font_normal_height + self.line_spacing

    # 띄어쓰기 기준으로 라인을 나누는 방식을 사용함: 중국어, 일본어 사용 시 새로운 방법 찾아야 함
    # LTR 언어에 적합하도록 구현함: RTL 언어 사용 시 적합한 방법을 추가해야 함
    def generate(self):
        if self.data_original is None or self.data_translated is None:
            return
        if len(self.data_original) != len(self.data_original):
            return

        page_num = 1
        chapter = 0
        chapter_updatable = True
        data_original = []
        data_translated = []

        max_width = (self.width - self.margin_left - self.margin_right) / 2 - self.margin_inner
        max_height = self.height - self.margin_top - self.margin_bottom - self.font_normal_height_original - 1.5 - self.line_spacing
        lines_available_original = int(max_height / (self.font_normal_height_original + self.line_spacing))
        lines_available_translated = int(max_height / (self.font_normal_height_translated + self.line_spacing))
        idx = 0
        while idx < len(self.data_original):
            item_original = self.data_original.iloc[idx]
            items_original = []
            if chapter == 0:
                chapter = item_original["chapter"]
            if item_original["verse"] == 1:
                if chapter_updatable:
                    chapter_updatable = False
                    chapter = item_original["chapter"]
                this_max_width = max_width - self.__canvas.stringWidth(str(item_original["chapter"]),
                                                                       self.font_bold_original,
                                                                       self.font_size_bold_original) - self.char_spacing

            else:
                this_max_width = max_width - self.__canvas.stringWidth(str(item_original["verse"]),
                                                                       self.font_normal_original,
                                                                       self.font_size) - self.char_spacing
            texts = item_original["text"].split(" ")
            text = ""
            for t in texts:
                if text == "":
                    temp_text = t
                else:
                    temp_text = text + " " + t
                content_width = self.__canvas.stringWidth(temp_text, self.font_normal_original, self.font_size)
                if content_width > this_max_width:
                    items_original.append(
                        {"chapter": item_original["chapter"], "verse": item_original["verse"], "text": text})
                    text = t
                else:
                    text = temp_text
            if text != "":
                items_original.append(
                    {"chapter": item_original["chapter"], "verse": item_original["verse"], "text": text})
            if len(data_original) + len(items_original) > lines_available_original:
                self.__draw_page(page_num, f"{self.subtitle}{chapter}", data_original, data_translated)
                page_num += 1
                chapter = 0
                chapter_updatable = True
                data_original = []
                data_translated = []
                continue

            item_translated = self.data_translated.iloc[idx]
            items_translated = []
            if item_translated["verse"] == 1:
                this_max_width = max_width - self.__canvas.stringWidth(str(item_translated["chapter"]),
                                                                       self.font_bold_translated,
                                                                       self.font_size_bold_translated) - self.char_spacing

            else:
                this_max_width = max_width - self.__canvas.stringWidth(str(item_translated["verse"]),
                                                                       self.font_normal_translated,
                                                                       self.font_size) - self.char_spacing
            texts = item_translated["text"].split(" ")
            text = ""
            for t in texts:
                if text == "":
                    temp_text = t
                else:
                    temp_text = text + " " + t
                content_width = self.__canvas.stringWidth(temp_text, self.font_normal_translated, self.font_size)
                if content_width > this_max_width:
                    items_translated.append(
                        {"chapter": item_translated["chapter"], "verse": item_translated["verse"], "text": text})
                    text = t
                else:
                    text = temp_text
            if text != "":
                items_translated.append(
                    {"chapter": item_translated["chapter"], "verse": item_translated["verse"], "text": text})
            if len(data_translated) + len(items_translated) > lines_available_translated:
                self.__draw_page(page_num, f"{self.subtitle}{chapter}", data_original, data_translated)
                page_num += 1
                chapter = 0
                chapter_updatable = True
                data_original = []
                data_translated = []
                continue

            for item in items_original:
                data_original.append(item)
            for item in items_translated:
                data_translated.append(item)
            idx += 1
        self.__draw_page(page_num, f"{self.subtitle}{chapter}", data_original, data_translated)

    def save(self):
        self.__canvas.showPage()
        self.__canvas.save()
