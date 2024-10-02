import os
from docx import Document

def read_text_from_txt(file_path):
      
      content = ""
      
      with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                  content += line
                  
      return content

def read_text_from_docx(file_path):
      
      content = ""
      doc = Document(file_path)
      for para in doc.paragraphs:
            content += para.text
            
      return content

def read_all_text(file_path):
      _, ext = os.path.splitext(file_path)
      ext = ext.lower()
      
      if ext == '.txt':
        return read_text_from_txt(file_path)
      elif ext == '.docx':
        return read_text_from_docx(file_path)
      else:
        raise ValueError("Formato de archivo no soportado.")
