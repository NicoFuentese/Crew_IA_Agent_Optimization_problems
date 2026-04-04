import os
from dotenv import load_dotenv
from crewai import LLM

# Cargar variables desde el archivo .env
load_dotenv()

MODELO = "gemini/gemini-3.1-flash-lite-preview"
API_KEY = os.getenv("GOOGLE_API_KEY")

# Perfiles de LLM modulares
llm_corto = LLM(model=MODELO, 
            api_key=API_KEY, 
            max_tokens=800, 
            temperature=0.2
            )

llm_medio = LLM(model=MODELO, 
            api_key=API_KEY, 
            max_tokens=1500, 
            temperature=0.2
            )

llm_largo = LLM(model=MODELO, 
            api_key=API_KEY, 
            max_tokens=4000, 
            temperature=0.2
            )
