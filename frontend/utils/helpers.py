import pandas as pd
import streamlit as st
from utils.config import FAMILY_ROLES

def clean_member_preferences(member):
    """Limpia las preferencias de un miembro"""
    cleaned = {}
    
    if 'preferencias' not in member:
        return cleaned
    
    for category, items in member['preferencias'].items():
        if not items:
            continue
            
        cleaned_items = {}
        for item, rating in items.items():
            try:
                rating_num = float(rating)
                if pd.isna(rating_num) or rating_num == float('inf') or rating_num == float('-inf'):
                    rating_num = 0.0
                rating_num = max(0.0, min(5.0, rating_num))
                cleaned_items[item] = rating_num
            except (ValueError, TypeError):
                cleaned_items[item] = 0.0
        
        if cleaned_items:
            cleaned[category] = cleaned_items
    
    return cleaned

def render_stars(rating):
    """Renderiza estrellas visualmente"""
    stars = ""
    for i in range(5):
        if i < rating:
            stars += "★"
        else:
            stars += "☆"
    return stars

def save_member_simple():
    """Guarda miembro de forma simple"""
    nombre = st.session_state.get('temp_nombre', '').strip()
    
    if not nombre:
        st.error("Ingresa un nombre")
        return False
    
    # Limpiar preferencias temporales
    cleaned_prefs = {}
    total_selected = 0
    
    for category, items in st.session_state.get('temp_preferences', {}).items():
        if items:
            cleaned_items = {}
            for item, rating in items.items():
                try:
                    rating_num = float(rating)
                    if pd.isna(rating_num):
                        rating_num = 0.0
                    rating_num = max(0.0, min(5.0, rating_num))
                    cleaned_items[item] = rating_num
                    if rating_num > 0:
                        total_selected += 1
                except:
                    cleaned_items[item] = 0.0
            
            if cleaned_items:
                cleaned_prefs[category] = cleaned_items
    
    if total_selected < 3:
        st.error(f"Necesitas al menos 3 preferencias (tienes {total_selected})")
        return False
    
    # Crear miembro limpio
    member = {
        'nombre': nombre,
        'rol': st.session_state.get('temp_rol', FAMILY_ROLES[0]),
        'preferencias': cleaned_prefs
    }
    
    # Agregar a la lista
    if 'family_members' not in st.session_state:
        st.session_state.family_members = []
    
    st.session_state.family_members.append(member)
    
    # Limpiar recomendaciones anteriores
    st.session_state.recommendations = None
    
    # Limpiar temporales
    st.session_state.temp_nombre = ""
    st.session_state.temp_preferences = {}
    
    st.success(f"{nombre} guardado con {total_selected} preferencias")
    return True