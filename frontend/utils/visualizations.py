import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Dict
import folium
from streamlit_folium import folium_static

def create_preference_radar(member_data: Dict) -> go.Figure:
    """
    Crea un gráfico de radar con las preferencias de un miembro
    
    Args:
        member_data: Dict con nombre, rol y preferencias del miembro
        
    Returns:
        Figura de Plotly
    """
    categories = []
    values = []
    
    for category, items in member_data.get('preferencias', {}).items():
        for item, rating in items.items():
            categories.append(item.replace('_', ' ').title())
            values.append(rating)
    
    # Cerrar el radar
    categories.append(categories[0])
    values.append(values[0])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=member_data['nombre'],
        line_color='#1f77b4'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        showlegend=True,
        title=f"Preferencias de {member_data['nombre']} ({member_data['rol']})",
        height=400
    )
    
    return fig

def create_family_comparison_chart(members: List[Dict]) -> go.Figure:

    """
    Crea un gráfico de barras comparando preferencias de toda la familia
    
    Args:
        members: Lista de miembros con sus preferencias
        
    Returns:
        Figura de Plotly
    """
    data = []
    
    for member in members:
        for category, items in member.get('preferencias', {}).items():
            for item, rating in items.items():
                data.append({
                    'Miembro': member['nombre'],
                    'Categoría': item.replace('_', ' ').title(),
                    'Calificación': rating
                })
    
    df = pd.DataFrame(data)
    
    fig = px.bar(
        df,
        x='Categoría',
        y='Calificación',
        color='Miembro',
        barmode='group',
        title='Comparación de Preferencias Familiares',
        height=500
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


def create_score_gauge(score: float, max_score: float = 5.0) -> go.Figure:
    """
    Crea un medidor de puntuación para un destino
    
    Args:
        score: Puntuación predicha
        max_score: Puntuación máxima posible
        
    Returns:
        Figura de Plotly
    """
    # Normalizar el score a escala 0-100
    normalized_score = (score / max_score) * 100
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=normalized_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Compatibilidad Familiar", 'font': {'size': 20}},
        delta={'reference': 70, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1},
            'bar': {'color': "#1f77b4"},
            'steps': [
                {'range': [0, 50], 'color': "#ffebee"},
                {'range': [50, 75], 'color': "#fff9c4"},
                {'range': [75, 100], 'color': "#c8e6c9"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

