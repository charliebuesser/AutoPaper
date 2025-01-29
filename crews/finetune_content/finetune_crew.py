from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class FinetuneCrew():
  """Finetune crew"""

  @agent
  def fine_tune_creator(self) -> Agent:
    return Agent(
      config=self.agents_config['fine_tune_creator'],
      verbose=True,
      llm="o1-preview",
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
  

  def handle_finetuning_mainpart(self, main_df, titel, gliederung):
    latex_results = []
    sub_dfs = self.split_into_subdfs(main_df)
    for chapter_index, df in sub_dfs.items():
        sub_outline = self.create_sub_outline(df)
        content = self.create_sub_content(df)
        working_chapter = self.get_working_chapter(df, True)
        working_chapter_no_number = self.get_working_chapter(df, False)
        inputs = {
        'gliederung': gliederung,
        'hauptkapitel' : working_chapter,
        'sub_outline' : sub_outline,
        'text' : content,
        'titel' : titel,
        'nummerrierung' : chapter_index,
        'hauptkapitel_No_Number' : working_chapter_no_number}
        res = str(self.crew().kickoff(inputs=inputs))
        latex_results.append(res)
      
    return "\n".join(latex_results)

 
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
  

  def create_sub_content(self, df):
    content = ""
    for index, row in df.iterrows():
        nummerierung = row['Nummerierung']
        kapitelname = row['Kapitelname']
        content += f"{nummerierung} : {kapitelname}\n"
        content += f"{row['content']} \n \n \n"
    return content



  def split_into_subdfs(self, df):
    sub_dfs = {}
    
    for index, row in df.iterrows():
        main_punkt = str(row['Nummerierung']).split('.')[0]  # Get the main section number
        if main_punkt not in sub_dfs:
            sub_dfs[main_punkt] = df[df['Nummerierung'].str.startswith(main_punkt + '.')]
    
    return sub_dfs

