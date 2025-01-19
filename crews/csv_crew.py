from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from docling.document_converter import DocumentConverter
import pandas as pd
from io import StringIO
import os

@CrewBase
class CSVCrew():
  """Content crew"""

  @agent
  def outline_creator(self) -> Agent:
    return Agent(
      config=self.agents_config['outline_creator'],
      verbose=True,
      tools=[]
    )

  @task
  def csv_task(self) -> Task:
    return Task(
    config=self.tasks_config['csv_task']
    )

  @crew
  def crew(self) -> Crew:
    """Creates the crew"""
    return Crew(
      agents=self.agents, # Automatically created by the @agent decorator
      tasks=self.tasks, # Automatically created by the @task decorator
      process=Process.sequential,
      verbose=True,
    )
  


  def get_structured_outline(self, file_to_outline):
    outline = self.read_file(file_to_outline)

    inputs = {
      'gliederung': outline,}
      
    res = str(self.crew().kickoff(inputs=inputs))

    print("ORGINAL :")
    print(res)

    # Use StringIO to turn the string into a file-like object
    csv_data = StringIO(res)
    # Create a DataFrame from the CSV string
    df = pd.read_csv(csv_data, delimiter=';')
    df.columns = df.columns.str.strip()
    return self.split_dataframe(df)


  def read_file(self, file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print("The specified file was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

  def split_dataframe(self, df):
    # Normalize the "Arbeitsabschnitt" column to lower case and strip whitespace.
    if 'Arbeitsabschnitt' not in df.columns:
        raise ValueError("Spalte 'Arbeitsabschnitt' fehlt im DataFrame.")

    # Strip spaces and convert to lower case for consistency
    df['Arbeitsabschnitt'] = df['Arbeitsabschnitt'].str.strip().str.lower()

    # Create the three DataFrames based on the cleaned "Arbeitsabschnitt" column.
    valid_sections = ['einleitung', 'hauptteil', 'schluss']
    df_einleitung = df[df['Arbeitsabschnitt'] == 'einleitung']
    df_hauptteil = df[df['Arbeitsabschnitt'] == 'hauptteil']
    df_schluss = df[df['Arbeitsabschnitt'] == 'schluss']

    # Optionally handle invalid entries.
    df_invalid = df[~df['Arbeitsabschnitt'].isin(valid_sections)]
    if not df_invalid.empty:
        print(f"Warnung: Ungültige Arbeitsabschnitt-Werte gefunden:\n{df_invalid}")

    # Return the three DataFrames.
    return df_einleitung, df_hauptteil, df_schluss, self.gliederung_zu_string(df)
  
  def gliederung_zu_string(self, df):
    gliederung_string = ""
    for index, row in df.iterrows():
        nummerierung = row['Nummerierung']
        kapitelname = row['Kapitelname']
        gliederung_string += f"{nummerierung} {kapitelname}\n"