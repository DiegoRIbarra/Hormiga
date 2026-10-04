#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime
from dotenv import load_dotenv # Importante para leer el .env

from hormiga.crew import Hormiga

# --- CONFIGURACIÓN CENTRALIZADA ---
# 1. Intenta leer el TOPIC desde el archivo .env
# 2. Si no existe en .env, usa el valor por defecto "AI LLMs"
load_dotenv() 
TOPIC = """Crear un proyecto en Python y PySide6 dentro de la carpeta 'proyecto' para resolver el problema de la hormiga usando el algoritmo BFS. 
Requerimientos técnicos estrictos:
1. Lógica de BFS: Implementar el camino más corto usando 'collections.deque' para la cola de exploración, asegurando que la hormiga evite obstáculos y encuentre la comida.
2. Interfaz Gráfica: Usar PySide6. El movimiento de la hormiga debe ser animado y fluido mediante el uso de 'QTimer', evitando que la interfaz se congele durante la búsqueda.
3. Interactividad: 
   - El usuario debe poder configurar el tamaño del laberinto y colocar obstáculos.
   - Implementar funcionalidad de 'Drag and Drop' real (usando mousePressEvent, mouseMoveEvent y mouseReleaseEvent) para mover a la hormiga y la comida en tiempo real.
4. Control: Incluir un botón de 'Reiniciar' que limpie el camino y permita nuevas configuraciones.
5. Salida: El código debe estar modularizado (lógica de BFS separada de la interfaz gráfica)."""
# ---------------------------------

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def get_inputs():
    """Función auxiliar para centralizar los inputs de todas las ejecuciones"""
    return {
        'topic': TOPIC,
        'current_year': str(datetime.now().year)
    }

def run():
    """
    Run the crew.
    """
    inputs = get_inputs()
    print(f"Iniciando flujo para el topic: {inputs['topic']}")

    try:
        Hormiga().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = get_inputs()
    try:
        Hormiga().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Hormiga().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = get_inputs()
    try:
        Hormiga().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = get_inputs()
    inputs["crewai_trigger_payload"] = trigger_payload

    try:
        result = Hormiga().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")

if __name__ == "__main__":
    # Para ejecutarlo desde terminal: python main.py run
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "run": run()
        elif cmd == "train": train()
        elif cmd == "replay": replay()
        elif cmd == "test": test()
        elif cmd == "run_with_trigger": run_with_trigger()
    else:
        run()
