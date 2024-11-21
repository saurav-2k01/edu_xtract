import os
import shutil
from src.XtractLib.doc_reader import DocReader
from src.XtractLib.analyser import Analyser
from src.XtractLib.doc_writer import DocWriter
import zipfile

class EduXtract:
    reader = DocReader
    analyser = Analyser
    writer = DocWriter

    def __init__(self, filepath = None, read_latex=False, threshold=0.75, output_dir:str ="outputs"):
        self.filepath = filepath
        self.filename = os.path.basename(self.filepath)
        self.data_block = []
        self.read_latex = read_latex
        self.threshold = threshold
        self.zipfilename = None
        self.output_dir = output_dir
        self.output_filepath = None
        self.read_file()


    def read_file(self):
        self.reader = self.reader(self.filepath)
        text = self.reader.read_file(self.read_latex)
        mapped_data = self.reader.map_data(text)
        self.data_block = self.reader.make_blocks(mapped_data)




    def get_QOA(self):
        seperated_QOA = self.reader.qoa_seperator(self.data_block)
        # self.reader.remove_key(seperated_QOA, "sr.no.", "exam_tag")
        return self.reader.make_dict(seperated_QOA)

    def get_info(self):
        self.analyser = self.analyser(self.data_block)
        report = self.analyser.check_pattern()
        lang = self.analyser.get_language()
        return {"report":report, "language":lang}

    def write_files(self, *args):
        self.writer = self.writer(self.get_QOA())
        files_types = args[0]
        os.makedirs("outputs", exist_ok=True)

        to_zip = []
        if ".docx" in files_types:
            docx_modified_filename = self.filename.replace(".docx", "_modified.docx")
            print(self.filename)
            self.writer.write2doc(docx_modified_filename)
            to_zip.append(docx_modified_filename)
        if ".xlsx" in files_types:
            csv_filename = self.filename.replace(".docx", ".csv")
            excel_filename = self.filename.replace(".docx", ".xlsx")
            self.writer.to_csv(csv_filename)
            self.writer.csv2excel(csv_filename, excel_filename)
            to_zip.append(excel_filename)
            os.remove(csv_filename)
        if ".csv" in files_types:
            csv_filename = self.filename.replace(".docx", ".csv")
            self.writer.to_csv(csv_filename)
            to_zip.append(csv_filename)

        zipfile_path = self.filename.split(".")[0]+".zip"
        self.zipfilename = zipfile_path
        zipfile_path = os.path.join(self.output_dir, self.zipfilename)
        try:
            with zipfile.ZipFile(zipfile_path, "w") as zipf:
                for f in to_zip:
                    zipf.write(f)
                    os.remove(f)
            self.output_filepath = zipfile_path

        except Exception as e:
            self.output_filepath = zipfile_path
