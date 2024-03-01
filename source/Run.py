"""
    PF2 to CSV Converter Project

    Project Description: Converts a '.pf2' file to a '.csv'

    Python Version: 3.11.0

    Output: Output '.csv' File will be in the Same 'Folder' / 'Directory' as the Original '.pf2' File

    Dependencies:
        None

    Author:
        run.py - Mason Motschke
"""
from csv import DictWriter
from time import sleep
from tkinter import *
from tkinter import filedialog


class PF2CsvConverter:
    def __init__(self, filename):
        self.pf2_file = filename
        self.csv_file = None
        self.run()

    def openStream(self, file, mode='r'):
        return open(str(file), str(mode))

    def closeStream(self, stream):
        stream.close()

    def buildRow(self, headers, data):
        row = {}
        i = 0

        for head in headers:
            row[head] = data[i]
            i += 1

        return row

    def getCsvFileName(self):
        temp = self.pf2_file.strip().split('.')
        temp.append('csv')
        temp.pop(-2)
        self.csv_file = '.'.join(temp)

    def getFieldNames(self, fieldNameLine):
        return fieldNameLine[7:-1].strip().split(', ')

    def getPF2Data(self, stream):
        data = []
        i = 0

        for line in stream:
            if line.startswith('Data:'):
                fieldNameLine = line.strip()
            elif line[0].isnumeric():
                line = line.strip().split(', ')
                data.append(line)
                i += 1

        self.closeStream(stream)
        return [data, i, self.getFieldNames(fieldNameLine)]

    def run(self):
        try:
            tuple = self.getPF2Data(self.openStream(self.pf2_file))
            self.getCsvFileName()

            with open(self.csv_file, 'w', newline='') as converted_file:
                writer = DictWriter(converted_file, fieldnames=tuple[2])
                writer.writeheader()

                for j in range(0, tuple[1]):
                    writer.writerow(self.buildRow(tuple[2], tuple[0][j]))

            self.closeStream(converted_file)
            print("Successfully converted the PF2 file to CSV")
            sleep(5)
        except Exception as e:
            print(e)
            print(" -- Error: An UNEXPECTED ERROR has occured during the conversion of the file!\n\n")
            sleep(20)


if __name__ == "__main__":
    win = Tk()
    win.geometry("50x25")
    Label(win, text="File Dialog", font='Arial 16 bold').pack(pady=15)

    filePath = filedialog.askopenfilename(title="Open a PF2 file",
                                          filetypes=(("pf2 files", "*.pf2"), ("all files", "*.*")))

    PF2CsvConverter = PF2CsvConverter(filePath)