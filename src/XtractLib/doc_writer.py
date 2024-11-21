import pandas as pd
import csv
from docx import Document
import xlsxwriter
import re

""" Doc-Format changer """

class DocWriter(object):
    def __init__(self, data:list):
        self.data = data

    def to_csv(self, filename: str,encoding: str='utf-8'):
        if ".csv" not in filename:
            filename = filename+".csv"
        else:
            pass
        fields = ["sr.no.", "question", "optionA", "optionB", "optionC", "optionD", "optionE", "answer", "solution",
                  "manual_update","exam_tag","test_id"]
        with open(filename, 'w', newline='', encoding=encoding, errors='ignore') as file:
            try:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                writer.writerows(self.data)
                # print(f"Data has been successfully saved in {filename}")
                return 1
            except Exception as e:
                print(e)
                return -1


    def csv2excel(self, csv_file, excelfilename):
        if ".csv" not in csv_file:
            csv_file = csv_file+".csv"

        try:
            df = pd.DataFrame(self.data)
            writer = pd.ExcelWriter(excelfilename, engine="xlsxwriter")
            df.to_excel(writer, sheet_name="sheet1")
            writer.close()
        except Exception as e:
            print(e)
            return -1

    def write2doc(self, filename):
        try:
            data = self.data
            doc = Document()
            count = 1
            for item in data:
                doc.add_paragraph(f"""Question: {count}
Level: Low
Tag: 
Answer: {item.get('answer', "N/A")}
Hindi:
Q: {item.get('question', "N/A")}
(a) {item.get('optionA', "N/A")}
(b) {item.get('optionB',"N/A")}
(c) {item.get('optionC',"N/A")}
(d) {item.get('optionD',"N/A")}
(e) 
Solution:\n\n""")

            doc.save(filename)
            # print("File has been written successfully")
        except Exception as e:
            print(e)
            return -1


