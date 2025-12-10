import requests
import streamlit as st
from typing import List, Dict, Optional
from utils.config import ENDPOINTS

class APIClient:
    """Cliente para interactuar con la API de Family Harmony"""
    
    @staticmethod
    def get_recommendations(family_data: Dict, top_k: int = 3) -> Optional[Dict]:
        """
        Obtiene recomendaciones de destinos para una familia
        
        Args:
            family_data: Diccionario con la estructura de la familia
            top_k: Número de recomendaciones a retornar
            
        Returns:
            Dict con las recomendaciones o None si hay error
        """
        try:
            # URL 
            url = ENDPOINTS["recommend"]
            response = requests.post(
                url,
                json=family_data,
                params={"top_k": top_k},  
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.ConnectionError:
            st.error("No se pudo conectar con el servidor. Verifica que la API esté corriendo en http://localhost:8000")
            return None
        except requests.exceptions.Timeout:
            st.error("La solicitud tardó demasiado tiempo. Intenta nuevamente.")
            return None
        except requests.exceptions.HTTPError as e:
            st.error(f"Error HTTP {e.response.status_code}: {e.response.text[:100]}...")
            return None
        except Exception as e:
            st.error(f"Error inesperado: {str(e)}")
            return None
    
    @staticmethod
    def check_api_health() -> bool:
        """
        Verifica si la API está disponible
        
        Returns:
            True si la API responde, False en caso contrario
        """
        try:
            # Intentar conectar al endpoint raíz o de salud
            response = requests.get(
                ENDPOINTS["recommend"].replace('/api/family/recommend_destinations', ''),
                timeout=3
            )
            return response.status_code == 200
        except:
            # Intentar directamente con el endpoint
            try:
                response = requests.head(
                    ENDPOINTS["recommend"],
                    timeout=3
                )
                return True
            except:
                return False


def format_family_data(members: List[Dict]) -> Dict:
    """
    Formatea los datos de la familia para enviar a la API
    Envía SOLO preferencias con rating > 0
    """
    formatted_members = []
    
    for member in members:
        flat_preferences = {}
        
        pref_mapping = {
            "iglesias": "Calif promedio iglesias",
            "resorts": "Calif promedio resorts",
            "playas": "Calif promedio playas",
            "parques": "Calif promedio parques",
            "teatros": "Calif promedio teatros",
            "museos": "Calif promedio museos",
            "centros_comerciales": "Calif promedio centros_comerciales",
            "zoologicos": "Calif promedio zoologicos",
            "restaurantes": "Calif promedio restaurantes",
            "bares_pubs": "Calif promedio bares_pubs",
            "servicios_locales": "Calif promedio servicios_locales",
            "pizzerias_hamburgueserias": "Calif promedio pizzerias_hamburgueserias",
            "hoteles_alojamientos": "Calif promedio hoteles_alojamientos",
            "juguerias": "Calif promedio juguerias",
            "galerias_arte": "Calif promedio galerias_arte",
            "discotecas": "Calif promedio discotecas",
            "piscinas": "Calif promedio piscinas",
            "gimnasios": "Calif promedio gimnasios",
            "panaderias": "Calif promedio panaderias",
            "belleza_spas": "Calif promedio belleza_spas",
            "cafeterias": "Calif promedio cafeterias",
            "miradores": "Calif promedio miradores",
            "monumentos": "Calif promedio monumentos",
            "jardines": "Calif promedio jardines"
        }
        
        # Solo agregar preferencias con rating > 0
        for category, items in member.get('preferencias', {}).items():
            for item, rating in items.items():
                if item in pref_mapping and rating > 0:
                    col_name = pref_mapping[item]
                    flat_preferences[col_name] = float(rating)
        
        formatted_member = {
            "nombre": member['nombre'],
            "rol": member['rol'],
            "preferencias": flat_preferences
        }
        
        formatted_members.append(formatted_member)
    
    return {"miembros": formatted_members}