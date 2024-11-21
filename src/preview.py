import os
import random
import docx2pdf
import fitz
import shutil
import pythoncom
import time
from threading import Thread


class Preview:
    def __init__(self, filepath):
        self.filepath = filepath
        self.ext = self.get_ext()
        self.preview_file_name = self.rand_str()

    @staticmethod
    def rand_str():
        return "".join(random.choices("abcdefghijklmnopqrstuvwxyz1234567890", k=16))

    def get_ext(self):
        return os.path.splitext(self.filepath)[-1]

    def doc2pdf(self):
        try:
            # docx2pdf.convert(self.filepath, self.filepath.replace("docx", "pdf"))
            docx2pdf.convert(self.filepath)
        except Exception as E:
            print(E)

    def pdf2img(self):
        pdf_doc = fitz.open(self.filepath.replace(".docx", ".pdf"))
        try:
            for i in range(len(pdf_doc)):
                page = pdf_doc.load_page(i)
                pix = page.get_pixmap()
                output_file_path = f"{self.preview_file_name}{i + 1}.png"
                pix.save(output_file_path)
        except Exception as E:
            print(E)
        finally:
            pdf_doc.close()

    def move_preview(self):
        preview_files = filter(lambda x: self.preview_file_name in x, os.listdir("."))
        os.mkdir(self.preview_file_name)
        for f in preview_files:
            shutil.move(f, self.preview_file_name)

    def gen_preview(self):
        pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
        try:
            if self.ext == ".docx":
                self.doc2pdf()
                self.pdf2img()
                self.move_preview()
                os.remove(self.filepath.replace("docx", "pdf"))
            elif self.ext == ".pdf":
                self.pdf2img()
                self.move_preview()
        except Exception as E:
            print(E)
        finally:
            pythoncom.CoUninitialize()
