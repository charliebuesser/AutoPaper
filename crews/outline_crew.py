# src/latest_ai_development/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class OutlineCrew():
  """Outline crew"""

  @agent
  def outline_creator(self) -> Agent:
    return Agent(
      config=self.agents_config['outline_creator'],
      verbose=True,
      tools=[]
    )

  @task
  def outline_task(self) -> Task:
    return Task(
    config=self.tasks_config['outline_task']
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
