from crewai import Task
from src.models import EntregableFinal

def crear_tareas(agentes):
    consultor_matematico, inspector_datos, analista_datos, arquitecto_software, desarrollador_algoritmos, ingeniero_qa, ingeniero_integracion = agentes

    #tasks
    t1_teoria = Task(
        description='Explica el {problema} y define su modelo matemático (Variables, FO y Restricciones).',
        expected_output='Reporte matemático detallado.',
        agent=consultor_matematico
    )

    t2_inspeccion = Task(
        description='''Revisa la teoría matemática del agente anterior para entender las variables del {problema}.
        Luego, analiza esta muestra cruda del archivo de la instancia:
        
        MUESTRA DEL ARCHIVO:
        {muestra_datos}
        
        Tu tarea es deducir el formato exacto del archivo. Explica en lenguaje claro qué representan las primeras líneas y los bloques de números (ej. "Los dos primeros valores son n y m. El siguiente bloque de n números son los costos...", etc.).''',
        expected_output='Una guía clara con el formato deducido del archivo.',
        agent=inspector_datos,
        context=[t1_teoria]
    )

    t3_lectura = Task(
        description='''Crea la función `leer_instancia(ruta_archivo)`.
        Debes seguir ESTRICTAMENTE el formato deducido por el 'Inspector de Ingeniería Inversa de Datos'.
        Usa técnicas de lectura plana (`f.read().split()`) para evitar errores por saltos de línea irregulares.
        Incluye también `imprimir_info_instancia(instancia)`.''',
        expected_output='Código de lectura de archivos robusto.',
        agent=analista_datos,
        context=[t1_teoria, t2_inspeccion]
    )

    #control de punto t3
    t3_revision = Task(
        description='Revisa el código de lectura. Si falla o no sigue el formato, delega al Analista para que lo corrija. Solo aprueba cuando sea perfecto.',
        expected_output='Código de lectura validado.',
        agent=ingeniero_qa, # El QA
        context=[t3_lectura]
    )

    t4_modulos = Task(
        description='Crea las funciones `verificar_restricciones()` y `calcular_funcion_objetivo()`.',
        expected_output='Funciones modulares de evaluación.',
        agent=arquitecto_software,
        context=[t1_teoria, t3_lectura]
    )

    #control de punto t4
    t4_revision = Task(
        description='Revisa las funciones modulares. ¿Están separadas? ¿Respetan la teoría? Si no, delega al Arquitecto.',
        expected_output='Funciones modulares validadas.',
        agent=ingeniero_qa,
        context=[t4_modulos]
    )

    t5_fuerza_bruta = Task(
        description='Implementa `resolver_fuerza_bruta()` midiendo tiempo en segundos y conteo de iteraciones.',
        expected_output='Algoritmo de búsqueda exhaustiva funcional.',
        agent=desarrollador_algoritmos,
        context=[t3_lectura, t4_modulos]
    )

    t6_qa = Task(
        description='''Verifica que todo el sistema integrado funcione.
        INSTRUCCIÓN CRÍTICA:
        1. Ensambla mentalmente las funciones de lectura, módulos y fuerza bruta.
        2. USA la herramienta 'Ejecutar_Codigo_Python' para correr el script completo.
        3. Si la herramienta retorna un error (Traceback), DELEGA inmediatamente la corrección al Desarrollador o Arquitecto indicando el error.
        4. NO apruebes el código hasta que la herramienta de ejecución retorne "Ejecución Exitosa".''',
        expected_output='Aprobación final tras una compilación y ejecución sin errores.',
        agent=ingeniero_qa,
        context=[t3_lectura, t4_modulos, t5_fuerza_bruta]
    )

    t7_entrega = Task(
        description='''Une el trabajo. Debes devolver un JSON estricto con dos claves: 
        "explicacion": Aquí va el texto teórico con formato Markdown. REGLA: Utiliza saltos de línea explícitos (\\n\\n) para separar párrafos, usar viñetas y mantener el formato matemático legible.
        "codigo": Aquí va el código en Python.

        REQUISITOS:
        1. Incluye la teoría y el modelo matematico de la Tarea 1 como Docstring inicial.
        2. El modelo matemático debe ir estructura y separado por saltos de linea de forma legible.
        3. NO agregues explicaciones fuera del bloque de código.
        
        EL BLOQUE MAIN DEBE SER EXACTAMENTE ASÍ:
        if __name__ == "__main__":
            ruta_archivo = "{ruta_prueba}" 
            try:
                print("Leyendo instancia desde:", ruta_archivo)
                instancia = leer_instancia(ruta_archivo)
                imprimir_info_instancia(instancia)
                
                print("\\nIniciando optimización por fuerza bruta...")
                mejor_sol, mejor_val, tiempo, iteraciones = resolver_fuerza_bruta(instancia)
                
                print("\\n--- RESULTADOS ---")
                print("Mejor Solución:", mejor_sol)
                print("Valor Objetivo:", mejor_val)
                print("Tiempo de ejecución:", round(tiempo, 4), "segundos")
                print("Soluciones evaluadas:", iteraciones)
            except Exception as e:
                print("ERROR:", e)''',
        expected_output='Un JSON con las claves "explicacion" y "codigo".',
        output_json=EntregableFinal, #modelo json
        agent=ingeniero_integracion,
        context=[t1_teoria, t3_lectura, t4_modulos, t5_fuerza_bruta, t6_qa]
    )
    
    return [t1_teoria, t2_inspeccion, t3_lectura, t3_revision, t4_modulos, t4_revision, t5_fuerza_bruta, t6_qa, t7_entrega]