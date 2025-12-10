import streamlit as st
from utils.visualizations import (
    create_preference_radar, 
    create_family_comparison_chart,
    create_score_gauge,
)

def render_analisis_page():
    if not st.session_state.family_members:
        st.warning("Agrega miembros de familia primero")
        return
    
    st.markdown('<div class="section-title"><i class="fas fa-chart-bar" style="margin-right: 8px;"></i>Análisis Familiar</div>', unsafe_allow_html=True)
    
    # Verificar que haya preferencias
    has_preferences = any(
        len(member.get('preferencias', {})) > 0
        for member in st.session_state.family_members
    )
    
    if not has_preferences:
        st.error("Los miembros no tienen preferencias configuradas")
        return
    
    try:
        # ========== RESUMEN GENERAL ==========
        st.markdown("<h3><i class='fas fa-chart-line' style='margin-right: 10px;'></i>Resumen General</h3>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            total_prefs = sum(
                sum(len(cat) for cat in m.get('preferencias', {}).values())
                for m in st.session_state.family_members
            )

            st.markdown(f"""
                <div style="background: white; border-radius: 8px; padding: 15px; border: 1px solid #e0e0e0; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 5px;">
                        <i class='fas fa-bullseye' style='margin-right: 8px; color: #4361EE;'></i>Preferencias totales
                    </div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: #2c3e50;">
                        {total_prefs}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            all_ratings = []
            for member in st.session_state.family_members:
                for category in member.get('preferencias', {}).values():
                    all_ratings.extend(category.values())
            avg_rating = sum(all_ratings) / len(all_ratings) if all_ratings else 0
            
            st.markdown(f"""
                <div style="background: white; border-radius: 8px; padding: 15px; border: 1px solid #e0e0e0; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 5px;">
                        <i class='fas fa-star' style='margin-right: 8px; color: #FFD700;'></i>Rating promedio
                    </div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: #2c3e50;">
                        {avg_rating:.1f}<span style="font-size: 1rem; color: #999;">/5</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            unique_prefs = set()
            for member in st.session_state.family_members:
                for category, items in member.get('preferencias', {}).items():
                    unique_prefs.update(items.keys())
            
            st.markdown(f"""
                <div style="background: white; border-radius: 8px; padding: 15px; border: 1px solid #e0e0e0; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 5px;">
                        <i class='fas fa-hashtag' style='margin-right: 8px; color: #764ba2;'></i>Actividades únicas
                    </div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: #2c3e50;">
                        {len(unique_prefs)}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        # ========== COMPARACIÓN FAMILIAR ==========
        st.markdown("<h3><i class='fas fa-users' style='margin-right: 10px;'></i>Comparación Familiar</h3>", unsafe_allow_html=True)
        
        col_a, col_b = st.columns([2, 1])
        
        with col_a:
            st.markdown("<h5><i class='fas fa-chart-pie' style='margin-right: 8px;'></i>Distribución de Preferencias</h5>", unsafe_allow_html=True)
            fig_comparison = create_family_comparison_chart(st.session_state.family_members)
            st.plotly_chart(fig_comparison, use_container_width=True, height=400)
        
        with col_b:
            st.markdown("<h5><i class='fas fa-crosshairs' style='margin-right: 8px;'></i>Compatibilidad Familiar</h5>", unsafe_allow_html=True)
            try:
                compatibility_score = avg_rating * 20
                fig_gauge = create_score_gauge(compatibility_score / 20)
                st.plotly_chart(fig_gauge, use_container_width=True, height=300)
            except:
                st.info("Agrega más datos para calcular compatibilidad")
        
        st.markdown("---")
        
        # ========== PERFILES INDIVIDUALES ==========
        st.markdown("<h3><i class='fas fa-user' style='margin-right: 10px;'></i>Perfiles Individuales</h3>", unsafe_allow_html=True)
        
        if len(st.session_state.family_members) <= 3:
            cols = st.columns(len(st.session_state.family_members))
            for idx, member in enumerate(st.session_state.family_members):
                with cols[idx]:
                    with st.container():
                       
                        try:
                            fig_radar = create_preference_radar(member)
                            st.plotly_chart(fig_radar, use_container_width=True, height=300)
                        except:
                            st.info(f"Sin datos suficientes para {member['nombre']}")
        else:
            member_tabs = st.tabs([f"{m['nombre']} ({m['rol']})" for m in st.session_state.family_members])
            for idx, tab in enumerate(member_tabs):
                with tab:
                    member = st.session_state.family_members[idx]
                    try:
                        fig_radar = create_preference_radar(member)
                        st.plotly_chart(fig_radar, use_container_width=True, height=300)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            member_prefs = sum(
                                len(cat) for cat in member.get('preferencias', {}).values()
                            )
                            st.metric("Preferencias", member_prefs)
                        
                        with col2:
                            member_ratings = [
                                rating for cat in member.get('preferencias', {}).values()
                                for rating in cat.values()
                            ]
                            member_avg = sum(member_ratings) / len(member_ratings) if member_ratings else 0
                            st.metric("Rating promedio", f"{member_avg:.1f}/5")
                    except:
                        st.info("Este miembro no tiene preferencias configuradas")
    
    except Exception as e:
        st.error(f"Error al generar análisis: {str(e)}")
        st.info("Intenta agregar más preferencias a los miembros de familia")