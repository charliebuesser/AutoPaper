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

  @crew
  def crew(self) -> Crew:
    """Creates the crew"""
    return Crew(
      agents=self.agents, # Automatically created by the @agent decorator
      tasks=self.tasks, # Automatically created by the @task decorator
      process=Process.sequential,
      verbose=True,
    )
  
  async def handle_mainpart(self, titel, gliederung, main_df):
    print("Starting to handle main part")
    main_df['content'] = ''
    main_df['cite'] = ''
    
    for index, row in main_df.iterrows():
      chapter_name = row['Kapitelname']
      print(f"Processing chapter: {chapter_name}")
      result_response, cite_list = await self.handle_rag_main(titel, gliederung,chapter_name)

      inputs = {
      'gliederung': gliederung,
      'kapitel' : chapter_name,
      'titel' : titel,
      'bulletpoints' : result_response}
      
      print(f"Inputs prepared for crew kickoff: {inputs}")
      res = str(self.crew().kickoff(inputs=inputs))
      print(f"Received response: {res}")

      main_df.at[index, 'content'] = res
      main_df.at[index, 'cite'] = repr(cite_list)
      
      print(f"Updated row content and cite for chapter: {chapter_name}")
      
    print("Completed handling main part")
    return main_df

  async def handle_rag_main(self, titel, gliederung, chapter_name):
    """Handles the RAG processing for a chapter."""
    print(f"Handling RAG main for chapter: {chapter_name}")
    rag_prompt_template = prompt_temeplate.rag_template_mainpart
    rag_prompt = rag_prompt_template.replace("{thema}", titel).replace("{gliederung}", gliederung).replace("{abschnitt}", chapter_name)
    print(f"Generated RAG prompt: {rag_prompt}")
    result = await self.rag.retrieve_rag_answer(rag_prompt)
    print(f"Retrieved RAG result for chapter: {chapter_name}")
    cite_list = self.rag.retrivie_cite(result)
    result_response = result.response
    print(f"Retrieved response and citation list for chapter: {chapter_name}")
    return result_response, cite_list
  

  

  def parse_cite_from_dataframe(self, index, row):
      import ast
      cite_str = row['cite']
      cite = ast.literal_eval(cite_str)
      return cite
