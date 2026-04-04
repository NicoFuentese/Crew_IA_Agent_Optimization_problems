from crewai import Agent
from src.config import llm_corto, llm_medio, llm_largo
from src.tools import herramienta_ejecutar_codigo

def crear_agentes():
    #agentes
    consultor_matematico = Agent(
        role='Consultor de Investigación de Operaciones',
        goal='Explicar el {problema} y definir su modelo matemático formal.',
        backstory='Experto en optimización. Traduce problemas reales a modelos matemáticos (FO, Variables, Restricciones).',
        llm=llm_corto,
        verbose=True
    )

    inspector_datos = Agent(
        role='Inspector de Ingeniería Inversa de Datos',
        goal='Deducir el esquema y formato de la instancia basándose en la muestra cruda y el modelo matemático.',
        backstory='Eres un detective de datos. Recibes un montón de números sin formato y, guiándote por la teoría del problema, logras deducir exactamente qué representa cada fila y bloque de texto.',
        llm=llm_corto,
        verbose=True
    )

    analista_datos = Agent(
        role='Analista de Instancias y Datos',
        goal='Desarrollar la función modular leer_instancia(ruta) adaptada al formato deducido por el inspector.',
        backstory='Especialista en parseo de archivos usando lectura plana (flat parsing). Creas estructuras de datos eficientes y a prueba de errores de formato.',
        llm=llm_medio,
        verbose=True
    )

    arquitecto_software = Agent(
        role='Arquitecto de Optimización',
        goal='Diseñar funciones modulares de validación y función objetivo para el {problema}.',
        backstory='Purista del código modular. Separa la lógica de factibilidad de la de rendimiento.',
        llm=llm_medio,
        verbose=True
    )

    desarrollador_algoritmos = Agent(
        role='Ingeniero de Búsqueda Exhaustiva',
        goal='Implementar el motor de fuerza bruta con medición de tiempo y soluciones evaluadas.',
        backstory='Experto en algoritmos. Implementa el motor de búsqueda exhaustiva midiendo performance.',
        llm=llm_medio,
        verbose=True
    )

    ingeniero_qa = Agent(
        role='Ingeniero de QA y Pruebas',
        goal='Verificar la integración del código y asegurar que los componentes encajen.',
        backstory='Guardián de la calidad. Asegura que el algoritmo procese las estructuras del analista correctamente.',
        tools=[herramienta_ejecutar_codigo],
        allow_delegation=True,
        llm=llm_corto,
        verbose=True
    )

    ingeniero_integracion = Agent(
        role='Release Engineer',
        goal='Entregar un único script de Python funcional y limpio sin texto adicional.',
        backstory='Responsable del empaquetado final. Entrega código listo para copiar y pegar.',
        llm=llm_largo,
        verbose=True
    )
    # Retornamos una tupla
    return consultor_matematico, inspector_datos, analista_datos, arquitecto_software, desarrollador_algoritmos, ingeniero_qa, ingeniero_integracion