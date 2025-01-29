import json
import os
import argparse
from datetime import datetime
import asyncio

from crews.outline.outline_crew import OutlineCrew
from crews.content.content_crew import ContentCrew
from crews.finetune_content.finetune_crew import FinetuneCrew
from services.document_service import DocumentService
from crews.csv.csv_crew import CSVCrew
from services.rag_service import RagService

async def main():
    parser = argparse.ArgumentParser(description="Wähle einen Modus aus, um die Anwendung auszuführen.")
    parser.add_argument('--modus', type=str, choices=['gliederung', 'inhalt'], required=True,
                        help="Wähle entweder 'gliederung' oder 'inhalt'.")
    
    # Argumente parsen
    args = parser.parse_args()

    # Load configuration
    with open('config.json') as config_file:
        config = json.load(config_file)

    global_config = config["global"]
    gliederung_config = config["gliederung"]
    inhalt_config = config["inhalt"]
    os.environ["OPENAI_API_KEY"] = global_config["openai_api_key"]

    if args.modus == 'gliederung':
        if not global_config.get('titel'):
            parser.error("Das 'titel' Feld in der config.json ist erforderlich, wenn der Modus 'gliederung' gewählt wird.")
        if not gliederung_config.get('gliederung_dir'):
            parser.error("Das 'gliederung_dir' Feld in der config.json ist erforderlich, wenn der Modus 'gliederung' gewählt wird.")
        for i in range(3):
            await create_outline(global_config['titel'], gliederung_config['gliederung_dir'], str(i+1))

    elif args.modus == 'inhalt':
        required_fields = ['document_path', 'outline_file_path', 'latex_output_path', 'base_meta_info']
        missing_fields = [field for field in required_fields if not inhalt_config.get(field)]

        if 'base_meta_info' in inhalt_config:
            meta_info_fields = ['kursbezeichnung', 'studiengang', 'name', 'matrikelnummer', 'name_tutor', 'arbeit_art']
            missing_meta_fields = [field for field in meta_info_fields if not inhalt_config['base_meta_info'].get(field)]
            missing_fields.extend(missing_meta_fields)

        if missing_fields:
            parser.error(f"Die folgenden Felder fehlen in der config.json: {', '.join(missing_fields)}")

        await create_content(global_config, inhalt_config)

async def create_outline(titel, dir, index):
    path = f"{dir}/outline_{index}"
    
    inputs = {
        'seminararbeitthema': titel,
        'path': path}
    OutlineCrew().crew().kickoff(inputs=inputs)

async def create_content(global_config, inhalt_config):
    outline_file_path = inhalt_config['outline_file_path']
    titel = global_config['titel']

    print("Starte den Erstellungsvorgang für den Inhalt.")

    print("Richte RAG-Service ein.")
    if os.path.isdir(inhalt_config.get('markdown_path', '')):
        rag = await setupRag(inhalt_config['markdown_path'], True)
    else:
        rag = await setupRag(inhalt_config['document_path'], False)
        
    print("RAG-Service wurde erfolgreich eingerichtet.")

    print(f"Lese die Gliederung aus: {outline_file_path}")
    df_einleitung, df_hauptteil, df_schluss, stringfied_outline = CSVCrew().get_structured_outline(outline_file_path)
    print("Gliederung erfolgreich gelesen.")

    print("Erstelle ContentCrew mit RAG-Service.")
    content_crew = ContentCrew(rag)

    print("Beginne die Bearbeitung des Hauptteils.")
    new_main_df = await content_crew.handle_mainpart(titel, stringfied_outline, df_hauptteil)
    print("Bearbeitung des Hauptteils abgeschlossen.")

    main_part_latex = FinetuneCrew().handle_finetuning_mainpart(new_main_df, titel, stringfied_outline)

    conclusion_part_latex = await content_crew.handle_conclusion(titel, stringfied_outline, df_schluss, main_part_latex)

    introduction_part_latex = await content_crew.handle_introduciton(titel, stringfied_outline, df_einleitung, main_part_latex, conclusion_part_latex)

    paper = f"{introduction_part_latex}\n{main_part_latex}\n{conclusion_part_latex}"

    with open("latex_final/base_latex.txt", 'r', encoding='utf-8') as file:
        content = file.read()

    updated_content = content.replace("{content}", paper.replace("cite", "citep"))
    updated_content = updated_content.replace("{titel}", titel)
    updated_content = updated_content.replace("{kursbezeichnung}", inhalt_config["base_meta_info"]["kursbezeichnung"])
    updated_content = updated_content.replace("{studiengang}", inhalt_config["base_meta_info"]["studiengang"])
    updated_content = updated_content.replace("{date}", datetime.now().strftime("%d.%m.%Y"))
    updated_content = updated_content.replace("{name}", inhalt_config["base_meta_info"]["name"])
    updated_content = updated_content.replace("{matrikelnummer}", inhalt_config["base_meta_info"]["matrikelnummer"])
    updated_content = updated_content.replace("{name_tutor}", inhalt_config["base_meta_info"]["name_tutor"])
    updated_content = updated_content.replace("{arbeit_art}", inhalt_config["base_meta_info"]["arbeit_art"])

    output_file_path = os.path.join(inhalt_config["latex_output_path"], "output.latex")
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

async def setupRag(content_dir_path, parsed_already):
    rag = RagService() 
    if parsed_already:
        rag.create_index(content_dir_path)
        return rag

    md_dir_path = DocumentService().create_md_from_literature(content_dir_path)
    rag.create_index(md_dir_path)
    return rag

if __name__ == "__main__":
    asyncio.run(main())