from crews.outline_crew import OutlineCrew
from crews.create_content_crew import CreateContentCrew
import os
import argparse


def main():
    parser = argparse.ArgumentParser(description="Wähle einen Modus aus, um die Anwendung auszuführen.")
    parser.add_argument('--modus', type=str, choices=['gliederung', 'inhalt'], required=True,
                        help="Wähle entweder 'gliederung' oder 'inhalt'.")
    
    parser.add_argument('--titel', type=str, required=False,
                        help="Der Titel der Gliederung (nur erforderlich, wenn der Modus 'gliederung' gewählt wird).")
    

    parser.add_argument('--document_path', type=str, required=False,
                        help="Der absolute Path zu dem Directory mit den Literatur PDF Files")
    
    
    
    # Argumente parsen
    args = parser.parse_args()

    if args.modus == 'gliederung' and not args.titel:
        parser.error("Das Argument '--titel' ist erforderlich, wenn der Modus 'gliederung' gewählt wird.")

    if args.modus == 'inhalt' and not args.document_path:
        parser.error("Das Argument '--document_path' ist erforderlich, gebe das Verzeichniss an wo deine Literatur PDF Files liegen.")



    # Je nach Modus eine andere Funktion ausführen
    if args.modus == 'gliederung':
        for i in range(3):
            create_outline(args.titel, str(i+1))
    elif args.modus == 'inhalt':
        create_content(args.document_path)
        


def create_outline(titel, index):

    inputs = {
    'seminararbeitthema': titel ,
    'index' : index}
    OutlineCrew().crew().kickoff(inputs=inputs)


def create_content(literature_dir_path):
    md_path = CreateContentCrew().create_md_from_literature(literature_dir_path)




if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"]="_"
    main()