from crews.outline_crew import OutlineCrew
from crews.content_crew import ContentCrew
from services.document_service import DocumentService
from crews.csv_crew import CSVCrew
from services.rag_service import RagService
import os
import argparse


async def main():
    parser = argparse.ArgumentParser(description="Wähle einen Modus aus, um die Anwendung auszuführen.")
    parser.add_argument('--modus', type=str, choices=['gliederung', 'inhalt'], required=True,
                        help="Wähle entweder 'gliederung' oder 'inhalt'.")
    
    parser.add_argument('--titel', type=str, required=False,
                        help="Der Titel der Gliederung (nur erforderlich, wenn der Modus 'gliederung' gewählt wird).")
    

    parser.add_argument('--document_path', type=str, required=False,
                        help="Der absolute Path zu dem Directory mit den Literatur PDF Files")
    
    parser.add_argument('--outline_file_path', type=str, required=False,
                        help="Der absolute Path zu der finalen Gliederung")
    
    
    
    # Argumente parsen
    args = parser.parse_args()

    if args.modus == 'gliederung' and not args.titel:
        parser.error("Das Argument '--titel' ist erforderlich, wenn der Modus 'gliederung' gewählt wird.")

    if args.modus == 'inhalt' and not args.document_path:
        parser.error("Das Argument '--document_path' ist erforderlich, gebe das Verzeichniss an wo deine Literatur PDF Files liegen.")



    # Je nach Modus eine andere Funktion ausführen
    if args.modus == 'gliederung':
        for i in range(3):
            await create_outline(args.titel, str(i+1))
    elif args.modus == 'inhalt':
        await create_content(args.document_path, args.outline_file_path)
        


async def create_outline(titel, index):

    inputs = {
    'seminararbeitthema': titel ,
    'index' : index}
    OutlineCrew().crew().kickoff(inputs=inputs)



async def create_content(literature_dir_path, outline_file_path):
    rag = await setupRag(literature_dir_path)
    
    df_einleitung, df_hauptteil, df_schluss, stringfied_outline = CSVCrew().get_structured_outline(outline_file_path)

    df_einleitung, df_hauptteil, df_schluss, stringfied_outline = CSVCrew().get_structured_outline(outline_file_path)

    #result =  await rag.retrieve_rag_answer("Hat Microsoft ein CLoud angebot ? Außerdem Für was ist Google CLoud besonders bekannt ?")


async def setupRag(literature_dir_path):
    md_dir_path = DocumentService().create_md_from_literature(literature_dir_path)
    rag = RagService() 
    rag.create_index(md_dir_path)
    return rag

if __name__ == "__main__":
    import asyncio
    os.environ["OPENAI_API_KEY"]="____"
    asyncio.run(main())