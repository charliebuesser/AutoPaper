# Erstelle erste Entwürfe für wissenschaftliche Arbeiten

# SetUp:
### Create a new Conda environment with Python 3.12
`conda create --name abschlussarbeit python=3.12`

### Activate the new environment
`conda activate abschlussarbeit`

### Install all dependencies from requirements.txt
`pip install -r requirements.txt`


# Betriebsmodi
Das Programm kann in zwei verschiedenen Modi betrieben werden:

### Modus : Gliederung (gliederung)
Im Gliederung-Modus werden basierend auf dem Titel der wissenschaftlichen Arbeit drei verschiedene Gliederungen erstellt.

#### Start Modus :
`python main.py --modus gliederung`

#### Benötigte Konfigurationsvariablen:

**Global**:

**openai_api_key**: API-Schlüssel für die Nutzung der OpenAI-Dienste.
**titel**: Der Titel der wissenschaftlichen Arbeit.

**Gliederung:**

**gliederung_dir**: Das Verzeichnis, in dem die generierte Gliederung gespeichert wird.

#### Funktionsweise:
Das Programm prüft, ob alle notwendigen Konfigurationsvariablen gesetzt sind.
Es werden drei Gliederungen erstellt und im angegebenen Verzeichnis (gliederung_dir) gespeichert.



### Modus : Inhalt-Modus (inhalt)
Im Inhalt-Modus wird der Inhalt der wissenschaftlichen Arbeit basierend auf einer vorgegebenen Gliederung und den bereitgestellten Dokumenten generiert.

#### Start Modus :
`python main.py --modus inhalt`

#### Benötigte Konfigurationsvariablen:
**Global**:

**openai_api_key**: API-Schlüssel für die Nutzung der OpenAI-Dienste.
**titel**: Der Titel der wissenschaftlichen Arbeit.


**Inhalt:**

**latex_output_path**: Pfad, wohin die Latex Kapitel -Ausgabedateien gespeichert werden.
**document_path**: Pfad zu den Literatur Dokumenten (pdf format !), die als Basis für den Inhalt dienen.
**outline_file_path**: Pfad zur Datei mit der Gliederung (wird von einem LLM geparsed, muss daher keinen standard entsprechen).
**base_meta_info**: Metainformationen, die im Latex-Dokument verwendet werden:
**kursbezeichnung**: Bezeichnung des Kurses.
**studiengang**: Studiengang.
**name**: Vorname und Nachname des Autors.
**matrikelnummer**: Matrikelnummer des Autors.
**name_tutor**: Name des Tutors.
**arbeit_art**: Art der Arbeit (z.B. Seminararbeit, Bachelorarbeit).



# Weitere Informationen
### Latex
Damit das LaTeX richtig gerendert werden kann, muss noch eine zusätzliche `literatur.bib` Datei erzeugt werden.
Die Literaturverweise im LaTeX-Dokument werden mit dem Namen der Dateien referenziert, jedoch ohne die .pdf-Endung. 
Beispiel:
Dateiname: `quelle1.pdf` Referenz im LaTeX-Dokument: `\citep{quelle1}`

Das bedeutet, im `literatur.bib`-File müssen die Quellen mit den entsprechenden Namen versehen werden.


### Config
Ein Beispiel-Config-File ist unter `config.example.json` hinterlegt.


### Tipp
- Gliederungen aus mehreren Hauptkapiteln führen zu besseren Resultaten als Hauptkapitel mit vielen Unterkapiteln.
- Der Modus --modus inhalt kann auch ohne vorherigen Aufruf von --modus gliederung gestartet werden, sofern schon eine Gliederung vorhanden ist.






