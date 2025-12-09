from pydantic import BaseModel
from typing import Dict, List

class MemberBase(BaseModel):
    """
    Define un miembro de la familia con su nombre, rol y preferencias
    """
    nombre: str
    rol: str
    preferencias: Dict[str, float]  # ejemplo: {"calif promedio playas":5, "calif promedio resorts":4}

class FamilyBase(BaseModel):
    """
    Representa la familia completa con todos los miembros
    """
    miembros: List[MemberBase]
