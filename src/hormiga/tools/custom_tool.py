import os
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

# --- INPUTS ---
class FileReadInput(BaseModel):
    """Input para leer archivos de la base de datos."""
    filename: str = Field(..., description="Nombre del archivo a leer en la carpeta 'datos base'")

class FileWriteInput(BaseModel):
    """Input para escribir archivos en la carpeta del proyecto."""
    filename: str = Field(..., description="Nombre del archivo a crear en la carpeta 'proyecto' (ej: 'main.py')")
    content: str = Field(..., description="El código fuente completo a escribir en el archivo")

# --- HERRAMIENTA DE LECTURA ---
class KnowledgeBaseTool(BaseTool):
    name: str = "KnowledgeBaseTool"
    description: str = "Útil para leer el contenido de los archivos en la carpeta 'datos base' (cpp, json, pdf, etc.)"
    args_schema: Type[BaseModel] = FileReadInput

    def _run(self, filename: str) -> str:
        # Ruta hacia 'datos base'
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../datos base"))
        file_path = os.path.join(base_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            return f"Error al leer el archivo {filename}: {str(e)}"

# --- HERRAMIENTA DE ESCRITURA ---
class ProjectWriteTool(BaseTool):
    name: str = "ProjectWriteTool"
    description: str = "Útil para guardar el código desarrollado en la carpeta 'proyecto'. Crea o sobrescribe archivos .py."
    args_schema: Type[BaseModel] = FileWriteInput

    def _run(self, filename: str, content: str) -> str:
        # Ruta hacia 'proyecto'
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../proyecto"))
        
        # Asegurar que la carpeta existe
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            
        file_path = os.path.join(base_path, filename)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Archivo {filename} guardado exitosamente en la carpeta proyecto."
        except Exception as e:
            return f"Error al escribir el archivo {filename}: {str(e)}"
