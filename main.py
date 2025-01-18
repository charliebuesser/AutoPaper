from crews.outline_crew import OutlineCrew
import os
import argparse


def main():
    parser = argparse.ArgumentParser(description="Wähle einen Modus aus, um die Anwendung auszuführen.")
    parser.add_argument('--modus', type=str, choices=['gliederung', 'inhalt'], required=True,
                        help="Wähle entweder 'gliederung' oder 'inhalt'.")
    
    parser.add_argument('--titel', type=str, required=False,
                        help="Der Titel der Gliederung (nur erforderlich, wenn der Modus 'gliederung' gewählt wird).")
    

    # Argumente parsen
    args = parser.parse_args()

    if args.modus == 'gliederung' and not args.titel:
        parser.error("Das Argument '--titel' ist erforderlich, wenn der Modus 'gliederung' gewählt wird.")

    
    # Je nach Modus eine andere Funktion ausführen
    if args.modus == 'gliederung':
        create_outline(args.titel)
    elif args.modus == 'inhalt':
        create_outline("AI Agents")


def create_outline(titel):

    os.environ["OPENAI_API_KEY"]="_"

    inputs = {
    'seminararbeitthema': titel }
  
    OutlineCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    main()