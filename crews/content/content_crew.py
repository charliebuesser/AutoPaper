from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from docling.document_converter import DocumentConverter
from Config import prompt_temeplate
import pandas as pd
import os

@CrewBase
class ContentCrew():
  """Content crew"""

  def __init__(self, rag):
    """Initializes the ContentCrew class"""
    self.rag = rag




  @agent
  def content_creator(self) -> Agent:
    return Agent(
      config=self.agents_config['content_creator'],
      verbose=True,
      tools=[]
    )

  @task
  def write_task(self) -> Task:
    return Task(
    config=self.tasks_config['write_task']
    )
  
  @task
  def write_task_conclusion(self) -> Task:
    return Task(
    config=self.tasks_config['write_task_conclusion']
    )
  
  @task
  def write_task_introduction(self) -> Task:
    return Task(
    config=self.tasks_config['write_task_introduction']
    )

  @crew
  def main_crew(self) -> Crew:
    """Creates the crew"""
    return Crew(
      agents=self.agents, # Automatically created by the @agent decorator
      tasks=[
        self.write_task()
      ], # Automatically created by the @task decorator
      process=Process.sequential,
      verbose=True,
    )
  
  @crew
  def conclusion_crew(self) -> Crew:
    return Crew(
      agents=self.agents,
      tasks=[
        self.write_task_conclusion()
      ],
      process=Process.sequential
    )
  
  @crew
  def introduction_crew(self) -> Crew:
    return Crew(
      agents=self.agents,
      tasks=[
        self.write_task_introduction()
      ],
      process=Process.sequential
    )
  
  async def handle_introduciton(self, titel, gliederung, intro_df, latex_main, latex_conclusion):
    text_latex = latex_main
    text_latex += f"\n {latex_conclusion}"

    introduction_sub_outline = self.create_sub_outline(intro_df)
    introduciton_kapitel = self.get_working_chapter(intro_df, True)
    introduction_no_num = self.get_working_chapter(intro_df, False)
    nummerierung = intro_df.iloc[0]['Nummerierung'].split('.')[0]

    inputs = {
      'titel': titel,
      'gliederung': gliederung,
      'anfangskapitel': introduciton_kapitel,
      'sub_outline': introduction_sub_outline,
      'text': text_latex,
      'anfangskapitel_no_number': introduction_no_num,
      'nummerrierung': nummerierung
    }

    res = str(self.introduction_crew().kickoff(inputs=inputs))
    return res

  async def handle_conclusion(self, titel, gliederung, conc_df, latex_main):
    main_latex = latex_main
    conclusion_sub_outline = self.create_sub_outline(conc_df)
    schlusskapitel = self.get_working_chapter(conc_df, True)
    schlusskapitel_no_num = self.get_working_chapter(conc_df, False)
    nummerierung = conc_df.iloc[0]['Nummerierung'].split('.')[0]

    inputs = {
      'titel': titel,
      'gliederung': gliederung,
      'schlusskapitel': schlusskapitel,
      'sub_outline': conclusion_sub_outline,
      'hauptteil': main_latex,
      'schlusskapitel_no_number': schlusskapitel_no_num,
      'nummerrierung' : nummerierung
    }

    res = str(self.conclusion_crew().kickoff(inputs=inputs))
    return res
  

  async def handle_mainpart(self, titel, gliederung, main_df):
    print("Starting to handle main part")
    main_df['content'] = ''
    
    for index, row in main_df.iterrows():
      if row['Überkapitel'] == 1:
        main_df.at[index, 'content'] = ""
        print("###########SKIP############")
        continue

      chapter_name = row['Kapitelname']

      print(f"Processing chapter: {chapter_name}")
      result_response, cite_list = await self.handle_rag_main(titel, gliederung,chapter_name)

      inputs = {
      'gliederung': gliederung,
      'kapitel' : chapter_name,
      'titel' : titel,
      'bulletpoints' : result_response}
      
      print(f"Inputs prepared for crew kickoff: {inputs}")
      res = str(self.main_crew().kickoff(inputs=inputs))

      res = self.replace_cite(res, cite_list)
      print(f"Received response: {res}")

      main_df.at[index, 'content'] = res
      
    print("Completed handling main part")
    return main_df
  

  def replace_cite(self, content, cite):
     for (index, filename) in cite:
        content = content.replace(f"[{str(index)}]",f"cite({filename.replace(".md", "")})")
     return content

  

  async def handle_rag_main(self, titel, gliederung, chapter_name):
    """Handles the RAG processing for a chapter."""
    print(f"Handling RAG main for chapter: {chapter_name}")
    rag_prompt_template = prompt_temeplate.rag_template_mainpart
    rag_prompt = rag_prompt_template.replace("{thema}", titel).replace("{abschnitt}", chapter_name)#.replace("{gliederung}", gliederung)
    print(f"Generated RAG prompt: {rag_prompt}")
    result = await self.rag.retrieve_rag_answer(rag_prompt)
    print(f"Retrieved RAG result for chapter: {chapter_name}")
    cite_list = self.rag.retrivie_cite(result)
    result_response = result.response
    print(f"Retrieved response and citation list for chapter: {chapter_name}")
    return result_response, cite_list
  

  def get_working_chapter(self ,df , with_num):
    first_row = df.iloc[0]

    # Extract 'Nummerierung' and 'Kapitelname' from the first row
    nummerierung = first_row['Nummerierung']
    kapitelname = first_row['Kapitelname']

    if with_num:
      return f"{nummerierung} {kapitelname}\n"
    return f"{kapitelname}\n"
  

  def create_sub_outline(self, df):
    gliederung_string = ""
    for index, row in df.iterrows():
        nummerierung = row['Nummerierung']
        kapitelname = row['Kapitelname']
        gliederung_string += f"{nummerierung} {kapitelname}\n"
    return gliederung_string
