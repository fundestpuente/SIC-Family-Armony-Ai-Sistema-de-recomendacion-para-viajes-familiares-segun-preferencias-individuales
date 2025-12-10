import streamlit as st
import plotly.graph_objects as go
from utils.api_client import APIClient, format_family_data
from utils.helpers import clean_member_preferences

def search_destinations_simple(top_k):
    """Busca destinos de forma simple"""
    try:
        # 1. Limpiar todos los miembros antes de enviar
        clean_members = []
        for member in st.session_state.family_members:
            clean_member = {
                'nombre': str(member.get('nombre', '')).strip(),
                'rol': str(member.get('rol', 'Otro')),
                'preferencias': clean_member_preferences(member)
            }
            clean_members.append(clean_member)
        
        # 2. Actualizar la lista con miembros limpios
        st.session_state.family_members = clean_members
        
        # 3. Formatear para API
        family_data = format_family_data(clean_members)
        
        # 4. Llamar a la API
        result = APIClient.get_recommendations(family_data, top_k)
        
        if result and 'recommendations' in result:
            # 5. Limpiar las recomendaciones recibidas
            clean_recommendations = []
            for rec in result['recommendations']:
                clean_rec = {
                    'nombre': str(rec.get('nombre', '')),
                    'provincia': str(rec.get('provincia', '')),
                    'canton': str(rec.get('canton', '')),
                    'predicted_score': float(rec.get('predicted_score', 0))
                }
                # Limitar score entre 0 y 5
                clean_rec['predicted_score'] = max(0.0, min(5.0, clean_rec['predicted_score']))
                clean_recommendations.append(clean_rec)
            
            st.session_state.recommendations = clean_recommendations
            return True
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
    
    return False

def render_recomendaciones_page():
    # Validar
    if not st.session_state.family_members:
        st.warning("Primero agrega miembros de familia para obtener recomendaciones.")
        return
    
    total_prefs = sum(
        sum(len(cat) for cat in m.get('preferencias', {}).values())
        for m in st.session_state.family_members
    )
    
    if total_prefs < 3:
        st.error(f"Necesitas al menos 3 preferencias en total. Tienes {total_prefs}.")
        return
    
    # Título principal
    st.markdown("""
        <h2 style="margin-bottom: 20px; color: #2c3e50; font-weight: 600;">
            <i class="fas fa-map-marked-alt" style="margin-right: 10px;"></i>Recomendaciones de Destinos
        </h2>
    """, unsafe_allow_html=True)
    
    # Sección de configuración de búsqueda
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 12px; margin-bottom: 25px;">
            <h4 style="color: white; margin: 0; display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-sliders-h"></i>Configurar Búsqueda
            </h4>
        </div>
    """, unsafe_allow_html=True)
    
    # Configuración de búsqueda
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Barra de progreso
        progress_value = min(total_prefs / 20, 1.0)
        st.markdown(f"""
            <div style="margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
                <i class="fas fa-chart-line" style="color: #4361EE;"></i>
                <strong>Completitud de datos:</strong>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="background: #e0e0e0; border-radius: 10px; height: 12px; margin-bottom: 5px;">
                <div style="background: linear-gradient(90deg, #4CAF50, #8BC34A); 
                            width: {progress_value*100}%; height: 100%; 
                            border-radius: 10px;"></div>
            </div>
            <div style="font-size: 0.85rem; color: #666; display: flex; align-items: center; gap: 10px;">
                <span><i class="fas fa-users"></i> {len(st.session_state.family_members)} miembros</span>
                <span>•</span>
                <span><i class="fas fa-heart"></i> {total_prefs} preferencias</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        top_k = st.selectbox(
            "Número de destinos",
            [3, 5, 10],
            format_func=lambda x: f"{x} destinos",
            help="Selecciona cuántos destinos quieres ver"
        )
    
    with col3:
        st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
        # Botón con icono de búsqueda
        if st.button("Buscar Destinos", type="primary", use_container_width=True):
            with st.spinner("Analizando preferencias familiares..."):
                if search_destinations_simple(top_k):
                    st.success(f"Encontrados {len(st.session_state.recommendations)} destinos")
                else:
                    st.error("No se pudieron encontrar destinos. Intenta nuevamente.")
    
    st.markdown("---")
    
    # Mostrar resultados si existen
    if st.session_state.recommendations:
        st.markdown("""
            <h3 style="margin: 25px 0 15px 0; color: #2c3e50; display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-star" style="color: #FFD700;"></i>Destinos Recomendados para tu Familia
            </h3>
        """, unsafe_allow_html=True)
        
        # Mostrar destinos
        for idx, dest in enumerate(st.session_state.recommendations):
            # Colores para las tarjetas (alternando)
            card_colors = [
                "linear-gradient(135deg, #667eea 10%, #764ba2 90%)",
                "linear-gradient(135deg, #f093fb 10%, #f5576c 90%)", 
                "linear-gradient(135deg, #4facfe 10%, #00f2fe 90%)",
                "linear-gradient(135deg, #43e97b 10%, #38f9d7 90%)",
                "linear-gradient(135deg, #fa709a 10%, #fee140 90%)"
            ]
            
            color_idx = idx % len(card_colors)
            score = dest.get('predicted_score', 0)
            
            stars_full = int(score)
            stars_half = 1 if (score - stars_full) >= 0.5 else 0
            stars_empty = 5 - stars_full - stars_half
            
            stars_display = "★" * stars_full + "☆" * stars_half + "☆" * stars_empty
            
            # Tarjeta de destino
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                    <div style="
                        background: {card_colors[color_idx]};
                        border-radius: 12px;
                        padding: 20px;
                        color: white;
                        margin-bottom: 15px;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <h3 style="margin: 0 0 10px 0; color: white; font-size: 1.3rem;">
                                    <i class="fas fa-map-pin" style="margin-right: 8px;"></i>{idx+1}. {dest.get('nombre', '')}
                                </h3>
                                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                                    <i class="fas fa-map-marker-alt" style="font-size: 0.9rem; opacity: 0.9;"></i>
                                    <span style="font-size: 0.9rem; opacity: 0.9;">
                                        {dest.get('provincia', '')}, {dest.get('canton', '')}
                                    </span>
                                </div>
                                <div style="font-size: 1.1rem; margin-top: 5px;">
                                    {stars_display}
                                </div>
                            </div>
                            <div style="
                                background: rgba(255,255,255,0.2); 
                                padding: 8px 15px; 
                                border-radius: 20px;
                                font-weight: bold;
                                font-size: 1.1rem;
                                display: flex;
                                align-items: center;
                                gap: 5px;
                            ">
                                <i class="fas fa-chart-bar"></i>{score:.1f}/5
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    
    else:
        # Estado cuando no hay recomendaciones
        st.markdown(f"""
            <div style="
                text-align: center;
                padding: 60px 20px;
                background: #f8f9fa;
                border-radius: 12px;
                margin-top: 30px;
            ">
                <div style="font-size: 3rem; margin-bottom: 20px; color: #4CAF50;">
                    <i class="fas fa-umbrella-beach"></i>
                </div>
                <h3 style="color: #2c3e50; margin-bottom: 10px;">
                    Listo para encontrar destinos perfectos
                </h3>
                <p style="color: #666; max-width: 500px; margin: 0 auto;">
                    Haz clic en "Buscar Destinos" para encontrar recomendaciones personalizadas basadas en las preferencias de tu familia.
                </p>
                <div style="margin-top: 30px; color: #999; font-size: 0.9rem; display: flex; align-items: center; justify-content: center; gap: 10px;">
                    <i class="fas fa-chart-pie"></i>
                    Basado en el análisis de {len(st.session_state.family_members)} miembros familiares
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Consejos adicionales
        if total_prefs < 10:
            st.info(f"""
                **Sugerencia:** Agrega más preferencias ({10 - total_prefs} más) 
                para obtener recomendaciones más precisas.
            """)