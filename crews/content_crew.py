from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from docling.document_converter import DocumentConverter
from ..Config import prompt_temeplate
import os

@CrewBase
class ContentCrew():
  """Content crew"""

  def __init__(self, rag):
    """Initializes the ContentCrew class"""
    self.rag = rag




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
    """Creates the LatestAiDevelopment crew"""
    return Crew(
      agents=self.agents, # Automatically created by the @agent decorator
      tasks=self.tasks, # Automatically created by the @task decorator
      process=Process.sequential,
      verbose=True,
    )
  
  def handle_mainpart(self, titel, gliederung):
    rag_prompt = prompt_temeplate.rag_template_mainpart.replace("{thema}",titel)
    rag_prompt = rag_prompt.replace("{gliederung}",gliederung)

    

    result = self.rag.retrieve_rag_answer("")
