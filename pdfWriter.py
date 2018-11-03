import PyPDF2
from io import StringIO, BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
pdfmetrics.registerFont(TTFont('MetaBookCapsLFC', 'MetaBookCapsLFC.ttf'))


def TupleSum(x, y):
    z = []
    for i in range(len(x)):
        z.append(x[i] + y[i])
    return tuple(z)

class PdfString():
    def __init__(self, text, begin_point):
        self.begin_point = begin_point
        self.text = text

class Text():
    def __init__(self, font_size, line_spacing, list_size):
        self.strings = []
        self.font_size = font_size
        self.line_spacing = line_spacing
        self.list_size = list_size

    def add_string(self, text):
        x = (self.list_size - stringWidth(text, 'MetaBookCapsLFC', self.font_size)) / 2
        if not self.strings:
            begin_point = (x, 502)
        else:
            begin_point = (x, self.strings[-1].begin_point[1] - self.line_spacing)
        pdf_string = PdfString(text, begin_point)
        self.strings.append(pdf_string)


class HumanToCongratulate():
    def __init__(self, post, full_name, town, school, list_size):
        self.post = post
        self.full_name = full_name
        self.town = town
        self.school = school
        self.list_size = list_size
        self.type = ''
        self.create_normal()
        self.create_longer()
        self.create_longest()

    def create_normal(self):
        text = Text(18, 24, self.list_size)
        first_str = self.post + ' ' + self.school + ' ' + self.town
        second_str = self.full_name
        if (len(first_str) < 40):
            self.type = 'normal'
        text.add_string(first_str)
        text.add_string(second_str)
        self.normal_text = text

    def create_longer(self):
        text = Text(18, 24, self.list_size)
        first_str = self.post + ' ' + self.school
        second_str = self.town
        third_str = self.full_name
        if (len(first_str) < 40 and not self.type):
            self.type = 'longer'
        text.add_string(first_str)
        text.add_string(second_str)
        text.add_string(third_str)
        self.longer_text = text

    def create_longest(self):
        text = Text(16, 20, self.list_size)
        first_str = self.post + ' ' + self.school
        second_str = self.town
        third_str = self.full_name
        if (not self.type):
            self.type = 'longest'
        text.add_string(first_str)
        text.add_string(second_str)
        text.add_string(third_str)
        self.longest_text = text

    def right_text(self):
        if self.type == 'normal':
            return self.normal_text
        elif self.type == 'longer':
            return self.longer_text
        else:
            return self.longest_text

    def template_file(self):
        if self.type == 'normal':
            return "C:/users/killer/Documents/GitHub/ThanksLettersPython/normal.pdf"
        elif self.type == 'longer':
            return "C:/users/killer/Documents/GitHub/ThanksLettersPython/longer.pdf"
        else:
            return "C:/users/killer/Documents/GitHub/ThanksLettersPython/longest.pdf"

    def new_file(self, number):
        return "C:/users/killer/Documents/GitHub/ThanksLettersPython/" + number.__str__() + ') ' + self.full_name + '.pdf'


def CreateLetter(human, number):
    text = human.right_text()
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("MetaBookCapsLFC", text.font_size)
    for string in text.strings:
        can.drawString(string.begin_point[0], string.begin_point[1], string.text)
    can.save()
    packet.seek(0)
    new_pdf = PyPDF2.PdfFileReader(packet)
    existing_pdf = PyPDF2.PdfFileReader(open(human.template_file(), "rb"))
    output = PyPDF2.PdfFileWriter()
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    outputStream = open(human.new_file(number), "wb")
    output.write(outputStream)
    outputStream.close()

packet = BytesIO()
can = canvas.Canvas(packet, pagesize=A4)
human = HumanToCongratulate('Учителю', 'Иванову Ивану Ивановичу', 'города Гомеля', 'ГУО «Гомельский городской лицей №1»', can._pagesize[0])
CreateLetter(human, 1)