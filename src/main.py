import os
from crewai import Crew, Process
from src.agents import crear_agentes
from src.tasks import crear_tareas
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax

def main():
    ruta_archivo_real = 'data/01_facil.txt'
    problema_actual = 'Problema de la Mochila Multidimensional (MKP)'

    # Lógica de extracción
    try:
        with open(ruta_archivo_real, 'r') as f:
            muestra = f.read(1000)
    except FileNotFoundError:
        muestra = "Asume formato estándar."

    inputs_proyecto = {
        'problema': problema_actual, 
        'ruta_prueba': ruta_archivo_real,
        'muestra_datos': muestra
    }

    # Inicializar componentes
    agentes_tupla = crear_agentes()
    tareas_lista = crear_tareas(agentes_tupla)

    # Ensamblar Crew
    crew = Crew(
        agents=list(agentes_tupla),
        tasks=tareas_lista,
        process=Process.sequential,
        max_rpm=10
    )

    #iniciar consola de Rich
    console = Console()

    console.print(f"[bold cyan]Iniciando flujo para: {problema_actual}...[/bold cyan]\n")
    resultado = crew.kickoff(inputs=inputs_proyecto)

    if hasattr(resultado, 'json_dict') and resultado.json_dict:
        datos = resultado.json_dict
    elif hasattr(resultado, 'pydantic') and resultado.pydantic:
        datos = resultado.pydantic.model_dump()
    else:
        datos = resultado
    
    #renderizado explicacion
    console.print(Markdown("### Teoria del Problema"))
    console.print(Markdown(datos["explicacion"]))

    console.print("\n[bold gray]---[/bold gray]\n")

    #renderizado codigo
    console.print("###Codigo Generado:\n")
    sintaxis_codigo = Syntax(datos["codigo"], "python", theme="monokai", line_numbers=True)
    console.print(sintaxis_codigo)

if __name__ == "__main__":
    main()