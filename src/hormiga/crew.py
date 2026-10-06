from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class Hormiga():
    """Hormiga crew"""

    _OLLAMA_URL = "http://localhost:11434"
    _NUM_CTX = 32768 

    llm_supervisor = LLM(model="ollama/qwen2.5-coder:14b", base_url=_OLLAMA_URL, extra_body={"num_ctx": _NUM_CTX})
    llm_interface = LLM(model="ollama/llama3.1:latest", base_url=_OLLAMA_URL, extra_body={"num_ctx": _NUM_CTX})
    llm_programmer = LLM(model="ollama/qwen2.5-coder:14b", base_url=_OLLAMA_URL, extra_body={"num_ctx": _NUM_CTX})

    @agent
    def programador(self) -> Agent:
        return Agent(
            config=self.agents_config['Programador'],
            llm=self.llm_programmer,
            tools=[], # SIN HERRAMIENTAS
            verbose=True
        )

    @agent
    def interfaz(self) -> Agent:
        return Agent(
            config=self.agents_config['Desarrollador'],
            llm=self.llm_interface,
            tools=[], # SIN HERRAMIENTAS
            verbose=True
        )

    @agent
    def supervisor(self) -> Agent:
        return Agent(
            config=self.agents_config['Supervisor'],
            llm=self.llm_supervisor,
            tools=[], # SIN HERRAMIENTAS
            verbose=True
        )

    @task
    def backend_task(self) -> Task:
        return Task(config=self.tasks_config['backend_task'])

    @task
    def interface_task(self) -> Task:
        return Task(config=self.tasks_config['interface_task'])

    @task
    def review_task(self) -> Task:
        return Task(config=self.tasks_config['review_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
