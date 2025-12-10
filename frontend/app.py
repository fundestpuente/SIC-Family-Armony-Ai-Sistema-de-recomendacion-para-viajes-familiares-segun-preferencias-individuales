import streamlit as st
from utils.config import APP_CONFIG
from utils.api_client import APIClient

# Configuración de la página
st.set_page_config(**APP_CONFIG)

# ========== ESTADO INICIAL ==========
if 'family_members' not in st.session_state:
    st.session_state.family_members = []
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "familia"

# Variables temporales
from utils.config import FAMILY_ROLES
if 'temp_nombre' not in st.session_state:
    st.session_state.temp_nombre = ""
if 'temp_rol' not in st.session_state:
    st.session_state.temp_rol = FAMILY_ROLES[0]
if 'temp_preferences' not in st.session_state:
    st.session_state.temp_preferences = {}

# Css personalizado
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        .section-title {
            font-size: 1.2rem;
            margin: 10px 0 6px 0;
            color: #333;
            font-weight: 600;
            padding-bottom: 4px;
            border-bottom: 2px solid #4361EE;
        }
        
        .destino-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 10px;
            margin: 10px 0;
        }
        
        .destino-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 8px;
            padding: 12px;
            color: white;
            position: relative;
            min-height: 120px;
        }
        
        .pref-card {
            background: white;
            border-radius: 8px;
            padding: 10px;
            margin: 5px 0;
            border: 2px solid #e1e4e8;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .pref-card:hover {
            border-color: #4361EE;
            box-shadow: 0 4px 8px rgba(67, 97, 238, 0.1);
        }
        
        .pref-card.selected {
            border-color: #4361EE;
            background-color: rgba(67, 97, 238, 0.05);
        }
        
        .pref-card .icon {
            font-size: 24px;
            width: 40px;
            text-align: center;
            flex-shrink: 0;
        }
        
        .pref-card .content {
            flex: 1;
            min-width: 0; 
        }
        
        .pref-card .name {
            font-weight: 600;
            font-size: 0.9rem;
            margin: 0;
            white-space: normal; 
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        
        .pref-card .category {
            font-size: 0.75rem;
            color: #666;
            margin: 2px 0 0 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .pref-card .stars {
            display: flex;
            gap: 2px;
            margin-top: 5px;
        }
        
        .pref-card .star {
            font-size: 14px;
            color: #FFD700;
        }
        
        .stSelectbox > div > div {
            padding: 8px 12px !important;
            border-radius: 8px !important;
            min-height: 44px !important;
            display: flex !important;
            align-items: center !important;
        }
        
        .stSelectbox > div > div > div {
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: unset !important;
            text-wrap: pretty !important;
            max-width: 100% !important;
            line-height: 1.4 !important;
            flex: 1 !important;
        }
        
        div[data-testid="stSelectbox"] > div > div {
            min-height: 44px !important;
        }
        
        .stSelectbox > div > div > div:nth-child(2) {
            margin-left: 8px !important;
        }
        
        .stSelectbox [data-baseweb="popover"] > div {
            max-height: 300px !important;
            overflow-y: auto !important;
        }
        
        .stSelectbox [data-baseweb="menu"] > div > div {
            padding: 10px 12px !important;
            white-space: normal !important;
            line-height: 1.4 !important;
        }
        
        /* Estilos para botones con iconos */
        .btn-with-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            text-align: center;
        }
        
        @media (max-width: 768px) {
            .stSelectbox > div > div {
                min-height: 40px !important;
                padding: 6px 10px !important;
            }
            
            .stSelectbox > div > div > div {
                font-size: 0.9rem !important;
            }
        }
        
        /* Estilos para mensajes de estado */
        .api-status {
            padding: 10px 15px;
            border-radius: 6px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .api-connected {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .api-disconnected {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .success-message {
            background-color: #d4edda;
            color: #155724;
            padding: 10px 15px;
            border-radius: 6px;
            margin-bottom: 10px;
            border: 1px solid #c3e6cb;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .info-message {
            background-color: #d1ecf1;
            color: #0c5460;
            padding: 10px 15px;
            border-radius: 6px;
            margin-bottom: 10px;
            border: 1px solid #bee5eb;
        }
    </style>
    """, unsafe_allow_html=True)

# ========== SIDEBAR ==========
def render_sidebar():
    with st.sidebar:
        st.markdown("<h1><i class='fas fa-umbrella-beach' style='margin-right: 10px; color: #4361EE;'></i>Family Harmony</h1>", unsafe_allow_html=True)
        
        # Estado API
        if APIClient.check_api_health():
            st.markdown("""
                <div class="api-status api-connected">
                    <i class='fas fa-check-circle'></i>API Conectada
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="api-status api-disconnected">
                    <i class='fas fa-times-circle'></i>API Desconectada
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navegación 
        st.markdown("<h3><i class='fas fa-map-marker-alt' style='margin-right: 8px;'></i>Navegación</h3>", unsafe_allow_html=True)
        
        paginas = [
            ("Familia", "familia", "fas fa-users"),
            ("Recomendaciones", "recomendaciones", "fas fa-map-marked-alt"),
            ("Análisis", "analisis", "fas fa-chart-bar")
        ]
        
        for display_text, page_id, icon_class in paginas:
            if st.button(
                f"{display_text}", 
                use_container_width=True,
                type="primary" if st.session_state.current_page == page_id else "secondary",
                key=f"nav_{page_id}"
            ):
                st.session_state.current_page = page_id
                st.rerun()
        
        st.markdown("---")
        
        # Info familia
        st.markdown("<h3><i class='fas fa-users' style='margin-right: 8px;'></i>Tu Familia</h3>", unsafe_allow_html=True)
        if st.session_state.family_members:
            for member in st.session_state.family_members:
                pref_count = sum(len(cat) for cat in member.get('preferencias', {}).values())
                st.markdown(f"<i class='fas fa-user-circle' style='margin-right: 5px; color: #666;'></i>{member['nombre']} ({pref_count})", unsafe_allow_html=True)
            st.markdown(f"Total: {len(st.session_state.family_members)}")
        else:
            st.info("Sin miembros")
        
        st.markdown("---")
        
        if st.button("Limpiar Todo", use_container_width=True):
            st.session_state.clear()
            st.session_state.family_members = []
            st.session_state.recommendations = None
            st.session_state.current_page = "familia"
            st.session_state.temp_nombre = ""
            st.session_state.temp_rol = FAMILY_ROLES[0]
            st.session_state.temp_preferences = {}
            
            # Mostrar mensaje de éxito
            st.markdown("""
                <div class="success-message">
                    <i class='fas fa-check'></i>Todo limpiado
                </div>
            """, unsafe_allow_html=True)
            st.rerun()

# ========== APLICACIÓN PRINCIPAL ==========
def main():
    # Sidebar
    render_sidebar()
    
    # Importar páginas
    from pagina.familia_page import render_familia_page
    from pagina.recomendaciones_page import render_recomendaciones_page
    from pagina.analisis_page import render_analisis_page
    
    # Contenido principal
    if st.session_state.current_page == "familia":
        render_familia_page()
    elif st.session_state.current_page == "recomendaciones":
        render_recomendaciones_page()
    elif st.session_state.current_page == "analisis":
        render_analisis_page()
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.9rem; padding: 10px;">
            <i class="fas fa-heart" style="color: #e91e63; margin-right: 5px;"></i>
            Family Harmony • Encuentra destinos perfectos para tu familia
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()