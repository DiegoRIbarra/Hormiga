from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
# Importamos ambas herramientas desde tu archivo custom_tool.py
from hormiga.tools.custom_tool import KnowledgeBaseTool, ProjectWriteTool

@CrewBase
class Hormiga():
    """Hormiga crew"""

    # Definición de los modelos específicos
    llm_supervisor = LLM(model="ollama/deepseek-r1:14b", base_url="http://localhost:11434")
    llm_interface = LLM(model="ollama/llama3.1:latest", base_url="http://localhost:11434") 
    llm_programmer = LLM(model="ollama/qwen2.5-coder:14b", base_url="http://localhost:11434")

    @agent
    def programador(self) -> Agent:
        return Agent(
            config=self.agents_config['Programador'],
            llm=self.llm_programmer,
            # Ahora puede leer la base de datos y escribir archivos en la carpeta proyecto
            tools=[KnowledgeBaseTool(), ProjectWriteTool()], 
            verbose=True
        )

    @agent
    def interfaz(self) -> Agent:
        return Agent(
            config=self.agents_config['Desarrollador'],
            llm=self.llm_interface,
            # Ahora puede leer la base de datos y escribir archivos en la carpeta proyecto
            tools=[KnowledgeBaseTool(), ProjectWriteTool()],
            verbose=True
        )

    @agent
    def supervisor(self) -> Agent:
        return Agent(
            config=self.agents_config['Supervisor'],
            llm=self.llm_supervisor,
            tools=[KnowledgeBaseTool()],
            verbose=True
        )

    @task
    def backend_task(self) -> Task:
        return Task(
            config=self.tasks_config['backend_task'],
        )

    @task
    def interface_task(self) -> Task:
        return Task(
            config=self.tasks_config['interface_task'],
        )

    @task
    def review_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_task'],
            output_file='veredicto_final.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, # Automáticamente toma los decorados con @agent
            tasks=self.tasks,   # Automáticamente toma los decorados con @task
            process=Process.sequential,
            verbose=True,
        )
