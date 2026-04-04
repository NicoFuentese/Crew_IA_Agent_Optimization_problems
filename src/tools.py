import sys
import io
import traceback
from crewai.tools import tool

@tool("Ejecutar_Codigo_Python")
def herramienta_ejecutar_codigo(codigo: str) -> str:
    """Ejecuta un script de Python y retorna la consola o el Traceback."""
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    try:
        exec(codigo, {})
        salida = redirected_output.getvalue()
        return f"Ejecución exitosa. Salida de consola:\n{salida}"
    except Exception as e:
        error = traceback.format_exc()
        return f"Error critico. Arregla este traceback:\n{error}"
    finally:
        sys.stdout = old_stdout