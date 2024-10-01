import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, messagebox
from utils.file_reader import read_text
from afd.afd import SQLInjectionAFD
from afd.afd_last import SQLInjectionAFD
import csv
import os
from tkinter import ttk

class MainWindow():

    def __init__(self, master):
        self.master = master
        master.title("SQL Injection Detector")
        master.geometry('900x700')
        
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12), padding=10)
        style.configure('TLabel', font=('Helvetica', 12))
        style.configure('TFrame', background='#f5f5f5')

        self.text_file = []
        self.results = {}
        self.results_excel_html = []
        self.extension = None

        self.create_widgets()

    def create_widgets(self):
        
        self.frame = ttk.Frame(self.master, padding="20")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.load_text_button = ttk.Button(
            self.frame, text="Cargar archivo de Texto", command=self.load_text_file)
        self.load_text_button.pack(pady=10)

        self.analyze_button = ttk.Button(
            self.frame, text="Iniciar Análisis", command=self.analyze)
        self.analyze_button.pack(pady=10)

        self.results_area = ScrolledText(self.frame, height=15, width=90, font=('Helvetica', 16))
        self.results_area.pack(pady=10)

        self.export_button = ttk.Button(
            self.frame, text="Exportar Resultados a CSV", command=self.export_results)
        self.export_button.pack(pady=10)

    def load_text_file(self):

        file_path = filedialog.askopenfilename(title="Seleccionar Archivo de Patrones", filetypes=[
                                               ("Archivos soportados", "*.csv *.xlsx *.xls *.docx *.html *.htm *.txt")])
        if file_path:

            try:

                _, ext = os.path.splitext(file_path)
                self.extension = ext.lower()

                content = read_text(file_path)
                self.text_file = content

                messagebox.showinfo("INFO", "Archivo cargado correctamente")

            except Exception as e:

                messagebox.showerror(
                    "Error", f"No se pudo cargar el archivo de texto {str(e)}")

    def analyze(self):

        if not self.text_file:
            messagebox.showwarning(
                "Advertencia", "Debe cargar un archivo primero")
            return

        afd = SQLInjectionAFD()

        if self.extension == '.txt' or self.extension == '.docx':

            for index, case in enumerate(self.text_file):
                result = afd.process(case)
                if result:
                    print(f"Input: {case} => Detected SQLi: {result}")
                    self.results[index] = case
                    self.results_area.insert('end', case + '\n')                

        elif self.extension == '.csv' or self.extension == '.xlsx' or self.extension == '.xls':
            
            for case in self.text_file:
                result = afd.process(case[2])
                print(f"Input: {case} => Detected SQLi: {result}")
                if result:
                    
                    self.results_area.insert(
                        'end', f'{case[0]} {case[1]} {case[2]}' + '\n')
                    self.results_excel_html.append(case)
                    
        elif self.extension == '.html':
            
            for case in self.text_file:
                result = afd.process(case)
                if result:
                    
                    self.results_area.insert(
                        'end', f'Patrón detectado -> {case}' + '\n'
                    )
                    
                    self.results_excel_html.append(case)

    def export_results(self):

        if len(self.results) > 0 or len(self.results_excel_html) > 0:

            archivo_csv = 'resultados.csv'

            if self.extension == '.txt' or self.extension == '.docx':

                with open(archivo_csv, mode='w', newline='', encoding='utf-8') as file:

                    writer_csv = csv.writer(file)

                    for index, value in self.results.items():
                        print([index, value])
                        writer_csv.writerow([index, value])

            if self.extension == '.csv' or  self.extension == '.xlsx' or self.extension == '.xls':

                with open(archivo_csv, mode='w', newline='', encoding='utf-8') as file:
                    writer_csv = csv.writer(file)

                    for i in self.results_excel_html:
                        writer_csv.writerow([i[0], i[1], i[2]])
                        
            if self.extension == '.html':
                
                with open(archivo_csv, mode='w', newline='', encoding='utf-8') as file:
                    writer_csv = csv.writer(file)

                    for i in self.results_excel_html:
                        writer_csv.writerow([i])
                

            messagebox.showinfo(
                "Exitoso", f"El archivo ha sido guardado en {archivo_csv}")
            self.results_excel_html = []
            self.results = []

        else:

            messagebox.showwarning(
                "Advertencia", "Aún no hay resultados para exportar")
