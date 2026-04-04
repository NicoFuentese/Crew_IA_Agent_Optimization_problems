from pydantic import BaseModel

class EntregableFinal(BaseModel):
    explicacion: str
    codigo: str