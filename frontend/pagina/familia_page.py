import streamlit as st
import pandas as pd
from utils.config import PREFERENCE_CATEGORIES, FAMILY_ROLES, PREFERENCE_ICONS, PREFERENCE_NAMES
from utils.api_client import format_family_data

def render_familia_page():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-title"> + Agregar Miembro</div>', unsafe_allow_html=True)
        
        # Formulario simple
        nombre = st.text_input(
            "Nombre",
            value=st.session_state.temp_nombre,
            placeholder="Ej: Juan, María..."
        )
        st.session_state.temp_nombre = nombre
        
        rol = st.selectbox("Rol", FAMILY_ROLES, 
                          index=FAMILY_ROLES.index(st.session_state.temp_rol) 
                          if st.session_state.temp_rol in FAMILY_ROLES else 0)
        st.session_state.temp_rol = rol
        
        # Preferencias
        st.markdown("Preferencias")
        st.caption("Haz clic en la tarjeta** para seleccionar (5 estrellas por defecto) o elige el rating exacto")
        
        # Contador de preferencias seleccionadas
        pref_count = 0
        
        for category, items in PREFERENCE_CATEGORIES.items():
            with st.expander(f" {category}", expanded=False):
                cols = st.columns(2)
                
                for idx, item in enumerate(items):
                    col = cols[idx % 2]
                    with col:
                        # Obtener rating actual
                        current_rating = st.session_state.temp_preferences.get(category, {}).get(item, 0)
                        
                        # Contar si está seleccionado
                        if current_rating > 0:
                            pref_count += 1
                        
                        # Crear tarjeta visual
                        icon = PREFERENCE_ICONS.get(item, "⭐")
                        name = PREFERENCE_NAMES.get(item, item.replace('_', ' ').title())
                        
                        card_class = "pref-card selected" if current_rating > 0 else "pref-card"
                        
                        st.markdown(f"""
                        <div class="{card_class}" style="cursor: pointer;" onclick="this.nextElementSibling.click()">
                            <div class="icon">{icon}</div>
                            <div class="content">
                                <p class="name">{name}</p>
                                <p class="category">{category.split(' ')[-1]}</p>
                                <div class="stars">
                                    {render_stars(current_rating)}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(
                            "Seleccionar",
                            key=f"btn_{category}_{item}",
                            help=f"Seleccionar {name} con 5 estrellas",
                            type="primary" if current_rating == 5 else "secondary",
                            use_container_width=True
                        ):
                            # Inicializar categoría si no existe
                            if category not in st.session_state.temp_preferences:
                                st.session_state.temp_preferences[category] = {}
                            
                            # Si ya está seleccionado con 5, poner 0, sino poner 5
                            new_rating = 0 if current_rating == 5 else 5
                            st.session_state.temp_preferences[category][item] = new_rating
                            st.rerun()
                        
                        # mostrar selectbox si está seleccionado (rating > 0)
                        if current_rating > 0:
                            rating_options = ["1", "2", "3", "4", "5"]
                            
                            # Ajustar índice (0-4 para 1-5)
                            selected_index = current_rating - 1 if current_rating > 0 else 0
                            
                            selected_option = st.selectbox(
                                f"Rating para {name[:20]}...",  
                                rating_options,
                                index=selected_index,
                                key=f"select_{category}_{item}",
                                help=f"Selecciona rating de 1 a 5 para {name}",
                                label_visibility="visible" 
                            )
                            
                            new_rating = int(selected_option)
                            
                            if new_rating != current_rating:
                                st.session_state.temp_preferences[category][item] = new_rating
                                st.rerun()
                        else:
                            st.caption("Selecciona primero la tarjeta arriba")
        
        # Botón guardar
        nombre_valido = nombre and nombre.strip()
        puede_guardar = nombre_valido and pref_count >= 3
        
        if st.button(
            " Guardar Miembro",
            disabled=not puede_guardar,
            use_container_width=True,
            type="primary"
        ):
            if save_member_simple():
                st.rerun()
        
        # Mostrar estado
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Preferencias", pref_count)
        with col_b:
            if pref_count < 3:
                st.error(f"Faltan {3 - pref_count}")
    
    with col2:
        st.markdown('<div class="section-title"> Miembros</div>', unsafe_allow_html=True)
        
        if not st.session_state.family_members:
            st.info("Aún no hay miembros")
        else:
            for idx, member in enumerate(st.session_state.family_members):
                pref_count_member = sum(len(cat) for cat in member.get('preferencias', {}).values())
                
                col_n, col_d = st.columns([3, 1])
                with col_n:
                    st.write(f"**{member['nombre']}**")
                    st.caption(f"{member['rol']} • {pref_count_member} pref")
                
                with col_d:
                    if st.button("Eliminar", key=f"del_{idx}"):
                        st.session_state.family_members.pop(idx)
                        # Limpiar recomendaciones si se elimina un miembro
                        st.session_state.recommendations = None
                        st.rerun()
            
            # Estadísticas
            total_members = len(st.session_state.family_members)
            total_prefs = sum(
                sum(len(cat) for cat in m.get('preferencias', {}).values())
                for m in st.session_state.family_members
            )
            
            st.markdown("---")
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                st.metric("Miembros", total_members)
            with col_stat2:
                st.metric("Preferencias", total_prefs)
            
            # Botón para buscar destinos
            if total_prefs >= 3:
                if st.button(" Buscar Destinos →", use_container_width=True):
                    st.session_state.current_page = "recomendaciones"
                    st.rerun()

# Importar funciones necesarias del app.py
from utils.helpers import save_member_simple, render_stars
