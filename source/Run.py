"""
    PF2 to CSV Converter Project

    Project Description: Converts a '.pf2' file to a '.csv'

    Python Version(s): 3.11.0, 3.12

    Output: Output '.csv' File will be in the Same 'Folder' / 'Directory' as the Original '.pf2' File

    Dependencies:
        None

    Author:
        run.py - Mason Motschke (Zvolvium)
"""
from csv import DictWriter
from time import sleep
from tkinter import *
from tkinter import filedialog


class PF2CsvConverter:
    def __init__(self, file_path=None):
        if file_path is None:
            self.win = Tk()
            self.win.geometry("50x25")
            Label(self.win, text="File Dialog", font='Arial 16 bold').pack(pady=15)

            file_path = filedialog.askopenfilename(title="Open a PF2 file",
                                                   filetypes=(("pf2 files", "*.pf2"), ("all files", "*.*")))

        try:
            self.check_file_extension(file_path)
        except ValueError as ve:
            print(f"\n!!EXCEPTION: {ve}\n    -> {file_path}")
            return

        self.pf2_file = file_path
        self.csv_file = self.get_new_filename(file_path)

    @staticmethod
    def open_stream(file, mode='r'):
        return open(str(file), str(mode))

    @staticmethod
    def close_stream(stream):
        stream.close()

    @staticmethod
    def check_file_extension(path, extension='pf2'):
        temp = path.strip().split('.')
        if temp[-1] != extension:
            raise ValueError(f'File Selected is not a {extension.upper()} file!')

    @staticmethod
    def build_row(headers, data):
        row = {}
        i = 0

        for head in headers:
            row[head] = data[i]
            i += 1

        return row

    @staticmethod
    def get_new_filename(path, extension='csv'):
        temp = path.strip().split('.')
        temp.pop(-1)
        temp.append(extension)
        return '.'.join(temp)

    @staticmethod
    def get_field_names(field_name_line):
        return field_name_line[7:-1].strip().split(', ')

    def get_file_data(self, stream):
        data = []
        field_name_line = ''
        i = 0

        for line in stream:
            if line.startswith('Data:'):
                field_name_line = line.strip()
            elif line[0].isnumeric():
                line = line.strip().split(', ')
                data.append(line)
                i += 1

        self.close_stream(stream)
        return [data, i, self.get_field_names(field_name_line)]

    def run(self):
        try:
            Tuple = self.get_file_data(self.open_stream(self.pf2_file))

            with open(self.csv_file, 'w', newline='') as converted_file:
                writer = DictWriter(converted_file, fieldnames=Tuple[2])
                writer.writeheader()

                for j in range(0, Tuple[1]):
                    writer.writerow(self.build_row(Tuple[2], Tuple[0][j]))

            self.close_stream(converted_file)
            print("\nSuccessfully converted the PF2 file to CSV")
            print("\n -- Application closing in 5 seconds...")
            sleep(5)
        except Exception as e:
            print(f"\n!!EXCEPTION: {e}")
            print("\n -- Application closing in 30 seconds...")
            sleep(30)


if __name__ == "__main__":
    # Without argument
    PF2CsvConverter1 = PF2CsvConverter()
    PF2CsvConverter1.run()

    # With argument
    # win = Tk()
    # win.geometry("50x25")
    # Label(win, text="File Dialog", font='Arial 16 bold').pack(pady=15)
    #
    # file_path = filedialog.askopenfilename(title="Open a PF2 file",
    #                                        filetypes=(("pf2 files", "*.pf2"), ("all files", "*.*")))
    #
    # PF2CsvConverter2 = PF2CsvConverter(file_path)
    # PF2CsvConverter2.run()
