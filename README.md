# AI Optimization Crew

Este repositorio contiene un sistema multi-agente basado en [CrewAI](https://crewai.com/) diseñado para automatizar la resolución de problemas de optimización matemática (como el Problema de la Mochila Multidimensional - MKP). 

El sistema utiliza agentes de Inteligencia Artificial impulsados por Google Gemini para:
1. **Modelar matemáticamente** el problema (Función Objetivo y Restricciones).
2. **Realizar ingeniería inversa** sobre archivos planos de instancias de datos.
3. **Escribir código modular** en Python (lectura, evaluación y algoritmos de fuerza bruta).
4. **Ejecutar QA autónomo**, probando el código generado en un entorno aislado para corregir errores antes de la entrega final.

## Estructura del Proyecto

El proyecto está diseñado de forma modular para facilitar su escalabilidad:

```text
optimizacion-agentes-ia/
├── data/                 # Archivos .txt con las instancias de prueba (ej. 01_facil.txt)
├── reports/              # Reportes generados automáticamente (.md) con teoría y código
├── src/                  # Código fuente del sistema multi-agente
│   ├── __init__.py
│   ├── config.py         # Configuración de LLMs y variables de entorno
│   ├── models.py         # Modelos de validación estructurada (Pydantic)
│   ├── tools.py          # Herramientas de ejecución (Ejecutor de Python para QA)
│   ├── agents.py         # Perfiles y prompts de los agentes
│   ├── tasks.py          # Definición del flujo de trabajo
│   └── main.py           # Orquestador principal
├── .env                  # Variables de entorno (No incluido en el control de versiones)
├── .gitignore            # Archivos ignorados por Git
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Esta documentación
```
## Arquitectura Crew

%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#e1f5fe', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#fff'}}}%%
graph TD
    %% --- ENTRADAS DE USUARIO ---
    Start[<b>INICIO:</b> Definición del Problema Knapsack MKP] -->|Variable 'problema'| T1_Teoria
    Start -->|Variable 'ruta_prueba' .txt| T2_Inspeccion
    Muestra[Extracción de Muestra de Datos: cruda 1000 chars] -->|Variable 'muestra_datos'| T2_Inspeccion

    %% --- SUBGRAPH: GRUPO DE TEORÍA Y ESQUEMA ---
    subgraph Sub_Teoria [1. Fase de Contexto y Esquema]
        T1_Teoria[<b>T1: Reporte Matemático</b><br/>Definir FO, Variables, Restricciones]
        T2_Inspeccion[<b>T2: Inspección Inversa</b><br/>Deducir esquema de datos de la Muestra]
        
        %% Mapeo de Agentes y Modelos
        Ag_Consultor(<img src='https://cdn-icons-png.flaticon.com/512/3208/3208815.png' width='30'/> <b>Consultor IO</b><br/>Profile: llm_corto<br/>Temp: 0.0) -.-> T1_Teoria
        Ag_Inspector(<img src='https://cdn-icons-png.flaticon.com/512/1082/1082831.png' width='30'/> <b>Inspector Datos</b><br/>Profile: llm_corto<br/>Temp: 0.0) -.-> T2_Inspeccion
    end

    %% --- FLUJO SECUENCIAL Y INTEGRACIÓN ---
    T1_Teoria -->|Contexto Teórico| T2_Inspeccion
    T2_Inspeccion -->|Esquema de Datos Deducido| T3_Lectura

    %% --- SUBGRAPH: CICLO DE DESARROLLO Y SUPERVISIÓN (CI/CD) ---
    subgraph Sub_Desarrollo [2. Fase de Desarrollo y Revisión Continua CI/CD]
        %% Tareas de Desarrollo
        T3_Lectura[<b>T3: Función de Lectura</b><br/>Código 'leer_instancia']
        T4_Modulos[<b>T4: Módulos de Evaluación</b><br/>Código Restricciones y FO]
        T5_FuerzaBruta[<b>T5: Motor Algorítmico</b><br/>Código Fuerza Bruta 2^n]

        %% Mapeo de Desarrolladores
        Ag_Analista(<img src='https://cdn-icons-png.flaticon.com/512/2620/2620708.png' width='30'/> <b>Analista Datos</b><br/>Profile: llm_medio<br/>Temp: 0.0) -.-> T3_Lectura
        Ag_Arquitecto(<img src='https://cdn-icons-png.flaticon.com/512/1055/1055660.png' width='30'/> <b>Arquitecto SW</b><br/>Profile: llm_medio<br/>Temp: 0.0) -.-> T4_Modulos
        Ag_Desarrollador(<img src='https://cdn-icons-png.flaticon.com/512/606/606240.png' width='30'/> <b>Desarrollador Alg</b><br/>Profile: llm_medio<br/>Temp: 0.0) -.-> T5_FuerzaBruta

        %% AGENTE SUPERVISOR QA Y HERRAMIENTA
        Ag_QA(<img src='https://cdn-icons-png.flaticon.com/512/10319/10319597.png' width='30'/> <b>Ingeniero QA<br/>SUPERVISOR FACTUAL</b><br/>Profile: llm_corto<br/>Temp: 0.0)
        Tool_Exec{{🛠️ Tool: Ejecutar_Codigo_Python<br/>[exec() interceptando stdout]}}
        Ag_QA ==>|Usa Herramienta| Tool_Exec

        %% PUNTOS DE CONTROL INTERCALADOS (SUPERVISIÓN)
        T3_Lectura ==>|Validar Sintaxis/Formato| Ag_QA
        Ag_QA -.->|Aprobación T3| T4_Modulos
        Ag_QA --x|Rechazo T3: Exigir Corrección| T3_Lectura
        
        T4_Modulos ==>|Validar Lógica/Numpy| Ag_QA
        Ag_QA -.->|Aprobación T4| T5_FuerzaBruta
        Ag_QA --x|Rechazo T4: Exigir Corrección| T4_Modulos
        
        T5_FuerzaBruta ==>|Validar Integración/Performance| Ag_QA
    end

    %% --- FASE FINAL DE INTEGRACIÓN ---
    Ag_QA -.->|Aprobación Final de Código Unificado| T7_Entrega

    subgraph Sub_Salida [3. Fase de Empaquetado Final]
        T7_Entrega[<b>T7: Empaquetado JSON</b><br/>Pydantic BaseModel]
        Ag_Integrador(<img src='https://cdn-icons-png.flaticon.com/512/9126/9126075.png' width='30'/> <b>Release Engineer</b><br/>Profile: llm_largo<br/>Temp: 0.0) -.-> T7_Entrega
    end

    T7_Entrega --> Final_Output[<b>RESULTADO FINAL:</b><br/>JSON con claves 'explicacion' y 'codigo']

    %% --- ESTILOS ---
    classDef usuario fill:#fff3e0,stroke:#ff9800,stroke-width:2px,color:#e65100;
    classDef agente fill:#e1f5fe,stroke:#0277bd,stroke-width:1px,rx:10,ry:10;
    classDef tarea fill:#f1f8e9,stroke:#558b2f,stroke-width:1px;
    classDef supervisor fill:#fce4ec,stroke:#c2185b,stroke-width:2px,color:#c2185b;
    classDef tool fill:#ede7f6,stroke:#5e35b1,stroke-width:2px,stroke-dasharray: 5 5;
    classDef output fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px,color:#1b5e20;

    class Start,Muestra usuario;
    class Ag_Consultor,Ag_Inspector,Ag_Analista,Ag_Arquitecto,Ag_Desarrollador,Ag_Integrador agente;
    class T1_Teoria,T2_Inspeccion,T3_Lectura,T4_Modulos,T5_FuerzaBruta,T7_Entrega tarea;
    class Ag_QA supervisor;
    class Tool_Exec tool;
    class Final_Output output;

    %% Link styles para supervisión
    linkStyle 10,13,16,17 stroke:#c2185b,stroke-width:2px,stroke-dasharray: 3 3;
    linkStyle 12,15 stroke:#ef5350,stroke-width:2px;

## Requisitos prevos
- Python 3.10 o superior
- uv (si decides ambientar con el)
- API KEY valida de Google AI Studio (Gemini)

## Configuración
Sigue estos pasos para levantar el proyecto localmente utilizando un entorno virtual tradicional (venv).

### 1. Crear y activar el entorno virtual:
Tienes 3 formas de crear el entorno virtual, con venv o uv.

#### 1.1 Ambiente virtual con python-venv

#### *Creamos ambiente virtual*
```PowerShell
#Windows
python -m venv .venv
.venv\Scripts\activate

#Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

#### *Instalar dependencias*
```PowerShell
pip install -r requirements.txt
```

#### 1.2 Ambiente virtual con uv
Es mucho mas rapido que el python-venv tradicional. No es necesario activacion manual, al correr el proyecto se activa solo.

#### *Creamos ambiente virtual venv*
```PowerShell
uv venv
```

### *Activamos el .venv*
```PowerShell
.venv\Scripts\activate

#Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

#### *Instalacion de dependencias*
```PowerShell
uv pip install -r requirements.txt
```

#### 1.3 Proyecto uv
```PowerShell
uv sync
```

### 2. Configurar variables de entorno
```PowerShell
GOOGLE_API_KEY=tu_api_key_aqui
```

## Uso
Para iniciar el flujo autónomo de los agentes y procesar una instancia de optimización, ejecuta el módulo principal desde la raíz del proyecto:

## *Si usaste venv*
```PowerShell
python -m src.main
```

## *Si usaste proyecto uv y .venv con uv*
```PowerShell
uv run python -m src.main
```

## Resultados de la Crew
El sistema proporciona feedback visual en tiempo real a través de la terminal utilizando la librería Rich. Una vez que el ingeniero de QA aprueba el código, se printeara en terminal una explicacion del problema con el modelo matemático y el Codigo Generado por el equipo.
