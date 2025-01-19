from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from docling.document_converter import DocumentConverter
import os

class DocumentService():

  def create_md_from_literature(self, dir_path):
    try:
        # Überprüfen, ob der Pfad ein Verzeichnis ist
        if not os.path.isdir(dir_path):
            raise ValueError(f"Der angegebene Pfad '{dir_path}' ist kein Verzeichnis.")
        
        markdown_dir = os.path.join(dir_path, 'markdown')
        if not os.path.exists(markdown_dir):
            os.makedirs(markdown_dir)
            print(f"Verzeichnis 'markdown' wurde erstellt: {markdown_dir}")
        else:
            print(f"Verzeichnis 'markdown' existiert bereits: {markdown_dir}")


        # Liste alle Dateien im Verzeichnis auf
        pdf_files = [
    (os.path.join(dir_path, file), file) for file in os.listdir(dir_path) if file.endswith('.pdf')
]


        # Iteriere durch die PDF-Dateien
        for pdf_file_path, filename in pdf_files:
           markdown = self.pdf_to_md(pdf_file_path)
           self.create_markdown_file(markdown_dir , markdown, filename)

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

    return markdown_dir


  def create_markdown_file(self, directory_path, content, filename):
    """
    Erstellt eine Markdown-Datei im Unterverzeichnis 'markdown' mit dem angegebenen Inhalt.

    :param directory_path: Pfad zu dem Hauptverzeichnis
    :param content: Inhalt der Markdown-Datei
    """
    try:
  
        markdown_file_path = os.path.join(directory_path, f"{filename}.md")
        with open(markdown_file_path, 'w', encoding='utf-8') as md_file:
            md_file.write(content)
        print(f"Markdown-Datei wurde erstellt: {markdown_file_path}")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    
    

  def pdf_to_md(self, source):
    converter = DocumentConverter()
    result = converter.convert(source)
    return result.document.export_to_markdown()
   