import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, messagebox
from utils.file_reader import read_text
from utils.read_all_file import read_all_text
#from afd.afd import SQLInjectionAFD
from afd.afd_last import SQLInjectionAFD
import csv
import os
from tkinter import ttk

class MainWindow():

    def __init__(self, master):
        self.master = master
        master.title("SQL Injection Detector")
        master.geometry('1150x700')
        master.configure(bg="#2E2E2E")
        
        style = ttk.Style()
        
        style.theme_use("clam") 
        style.configure('TButton', 
                        font=('Helvetica', 14, 'bold'), 
                        padding=10, 
                        foreground="#ffffff", 
                        background="#094293",
                        borderwidth=2,
                        relief="flat")  
        
        style.map("TButton", 
                  background=[("active", "#29487d")], 
                  foreground=[("disabled", "#a9a9a9"), ("pressed", "#ffffff")])

        # Estilo de la etiqueta
        style.configure('TLabel', 
                        font=('Helvetica', 12, 'bold'), 
                        foreground="#ffffff", 
                        background="#2E2E2E")

        style.configure('TFrame', background='#2E2E2E')

        style.configure('TScrolledText', background='#1E1E1E', foreground="#FFFFFF")

        self.text_file = []
        self.text_to_analyze = ""
        self.results = {}
        self.results_excel_html = []
        self.results_from_all_text = []
        self.extension = None

        self.create_widgets()

    def create_widgets(self):
        
        self.frame = ttk.Frame(self.master, padding="20")
        #self.frame.pack(fill=tk.BOTH, expand=True)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.load_text_button = ttk.Button(
            self.frame, text="Cargar lista de patrones", command=self.load_text_file)
        #self.load_text_button.pack(pady=10)   
        self.load_text_button.grid(row=0, column=0, padx=10, pady=20, sticky="w")
        
        self.load_text_button = ttk.Button(
            self.frame, text="Cargar archivo con patrones", command=self.load_text_with_patterns)
        #self.load_text_button.pack(pady=10)
        self.load_text_button.grid(row=0, column=1, padx=10, pady=20, sticky="w")
        
        self.analyze_button = ttk.Button(
            self.frame, text="Iniciar Análisis", command=self.analyze)
        #self.analyze_button.pack(pady=10)   
        self.analyze_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.results_area = ScrolledText(self.frame, height=15, width=90, font=('Helvetica', 16), bg='#2E2E2E', fg='#FFFFFF', insertbackground='white', 
                                      selectbackground='#3b5998')
        #self.results_area.pack(pady=10)
        self.results_area.grid(row=1, column=0, columnspan=3, padx=10, pady=20)
        self.results_area.tag_configure("margin", lmargin1=15, lmargin2=25, rmargin=25)
        
        self.results_area.tag_configure("margin", lmargin1=25, lmargin2=25, rmargin=25)

        self.export_button = ttk.Button(
            self.frame, text="Exportar Resultados a CSV", command=self.export_results)
        #self.export_button.pack(pady=10)
        self.export_button.grid(row=2, column=0, columnspan=3, pady=20)
        
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def load_text_file(self):

        file_path = filedialog.askopenfilename(title="Seleccionar Archivo de Patrones", filetypes=[
                                               ("Archivos soportados", "*.csv *.xlsx *.xls *.docx *.html *.htm *.txt")])
        if file_path:

            try:

                _, ext = os.path.splitext(file_path)
                self.extension = ext.lower()

                content = read_text(file_path)
                print("The content is in load list file")
                print(content)
                self.text_file = content

                messagebox.showinfo("INFO", "Archivo cargado correctamente")

            except Exception as e:

                messagebox.showerror(
                    "Error", f"No se pudo cargar el archivo de texto {str(e)}")
                
    def load_text_with_patterns(self):
        
        file_path = filedialog.askopenfilename(title="Seleccionar Archivo de Patrones", filetypes=[("Archivos soportados", "*.docx *.txt")])
        
        if file_path:

            try:

                _, ext = os.path.splitext(file_path)
                self.extension = ext.lower()
                content = read_all_text(file_path)
                print("The content is")
                print(content)
                self.text_to_analyze = content

                messagebox.showinfo("INFO", "Archivo cargado correctamente")

            except Exception as e:

                messagebox.showerror(
                    "Error", f"No se pudo cargar el archivo de texto {str(e)}")

    def analyze(self):
        
        if self.text_to_analyze:
            self.analyze_from_all_text()
            return 

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
                    
    def analyze_from_all_text(self):
        
        if not self.text_to_analyze:
            messagebox.showwarning(
                "Advertencia", "Debe cargar un archivo primero")
            return
        
        afd = SQLInjectionAFD()

        if self.extension == '.txt' or self.extension == '.docx':
            result, values = afd.process_of_text(self.text_to_analyze)
            if result:
                self.results_from_all_text = values
                for i in values:
                    self.results_area.insert('end', i + '\n')
        

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
            
        elif len(self.results_from_all_text) > 0:
            
            archivo_csv = 'resultados.csv'

            if self.extension == '.txt' or self.extension == '.docx':

                with open(archivo_csv, mode='w', newline='', encoding='utf-8') as file:

                    writer_csv = csv.writer(file)

                    for value in self.results_from_all_text:                    
                        writer_csv.writerow([value])                        
                        
                messagebox.showinfo(
                "Exitoso", f"El archivo ha sido guardado en {archivo_csv}")

        else:

            messagebox.showwarning(
                "Advertencia", "Aún no hay resultados para exportar")
