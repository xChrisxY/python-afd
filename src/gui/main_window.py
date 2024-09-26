import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, messagebox
from utils.file_reader import read_text
from afd.afd import SQLInjectionAFD
import csv
import os

class MainWindow():
    
    def __init__(self, master):
        self.master = master
        master.title("SQL Injection Detector")

        self.text_file = []
        #self.afd = None
        self.results = {}
        self.results_excel = []
        self.extension = None

        self.create_widgets()

    def create_widgets(self):

        self.load_text_button = tk.Button(
            self.master, text="Cargar archivo de Texto", command=self.load_text_file)
        self.load_text_button.pack(pady=5)

        self.analyze_button = tk.Button(
            self.master, text="Iniciar Análisis", command=self.analyze)
        self.analyze_button.pack(pady=5)

        self.results_area = ScrolledText(self.master, height=10, width=80)
        self.results_area.pack(pady=5)

        self.export_button = tk.Button(
            self.master, text="Exportar Resultados a CSV", command=self.export_results)
        self.export_button.pack(pady=5)

    def load_text_file(self):

        file_path = filedialog.askopenfilename(title="Seleccionar Archivo de Patrones", filetypes=[("Archivos soportados", "*.csv *.xlsx *.xls *.docx *.html *.htm *.txt")])
        if file_path:

            try:
                
                _, ext = os.path.splitext(file_path)
                self.extension = ext.lower()

                content = read_text(file_path)
                self.text_file = content
                
                messagebox.showinfo("INFO","Archivo cargado correctamente")

            except Exception as e:

                messagebox.showerror(
                    "Error", f"No se pudo cargar el archivo de texto {str(e)}")

    def analyze(self):
        
        if not self.text_file:
            messagebox.showwarning(
                "Advertencia", "Debe cargar un archivo primero")
            return
        
        afd = SQLInjectionAFD()

        if self.extension == '.txt':
            
            for index, case in enumerate(self.text_file):
                result = afd.process(case)
                if result:
                    print(f"Input: {case} => Detected SQLi: {result}")
                    self.results[index] = case                    
                    self.results_area.insert('end', case + '\n')
                    
        elif self.extension == '.csv':
            
            for case in self.text_file:
                result = afd.process(case[2])
                if result:
                    print(f"Input: {case} => Detected SQLi: {result}")                  
                    self.results_area.insert('end', f'{case[0]} {case[1]} {case[2]}' + '\n')
                    self.results_excel.append(case)
                    

    def export_results(self):

        if len(self.results) > 0 or len(self.results_excel):
            
            archivo_csv = 'resultados.csv'
            
            if self.extension == '.txt':
                
                with open(archivo_csv, mode='w', newline='', encoding='utf-8') as file:
                    
                    writer_csv = csv.writer(file)
                
                    for index, value in self.results.items():
                        writer_csv.writerow([index, value])                                          
                    
            if self.extension == '.csv':
                
                with open(archivo_csv, mode='w', newline='', encoding='utf-8') as file:
                    writer_csv = csv.writer(file)
                    
                    for i in self.results_excel:
                        writer_csv.writerow([i[0],i[1],i[2]])
                        
            messagebox.showinfo("Exitoso", f"El archivo ha sido guardado en {archivo_csv}")
            
        else:
            
            messagebox.showwarning(
                "Advertencia", "Aún no hay resultados para exportar")
            
        
