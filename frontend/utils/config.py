import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la API
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Endpoints
ENDPOINTS = {
    "recommend": f"{API_BASE_URL}/api/family/recommend_destinations",
    "save_record": f"{API_BASE_URL}/api/family/save_family_record",
    "health": f"{API_BASE_URL}/" 
}

# Configuración de la aplicación
APP_CONFIG = {
    "page_title": "Family Harmony AI",
    "page_icon": "🏖️",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Categorías de preferencias mejoradas
PREFERENCE_CATEGORIES = {
    "🏛️ Cultural": [
        "iglesias",
        "museos", 
        "teatros",
        "monumentos",
        "galerias_arte"
    ],
    "🌳 Recreación": [
        "playas",
        "parques", 
        "piscinas",
        "miradores",
        "jardines"
    ],
    "🏨 Alojamiento": [
        "resorts",
        "hoteles_alojamientos", 
        "centros_comerciales"
    ],
    "🍽️ Gastronomía": [
        "restaurantes",
        "pizzerias_hamburgueserias",
        "cafeterias", 
        "juguerias",
        "panaderias"
    ],
    "🎭 Entretenimiento": [
        "zoologicos",
        "bares_pubs",
        "discotecas", 
        "gimnasios",
        "belleza_spas"
    ],
    "🏪 Servicios": [
        "servicios_locales"
    ]
}

# Roles familiares mejorados
FAMILY_ROLES = [
    "👨‍👩‍👧‍👦 Padres",
    "👦👧 Hijos (Adolescentes 13-17)",
    "👩‍🎓👨‍🎓 Hijos (Adultos 18+)",
    "👴👵 Abuelos",
    "👤 Otro"
]

# Iconos para preferencias individuales
PREFERENCE_ICONS = {
    "iglesias": "⛪",
    "resorts": "🏨",
    "playas": "🏖️",
    "parques": "🌳",
    "teatros": "🎭",
    "museos": "🏛️",
    "centros_comerciales": "🛍️",
    "zoologicos": "🐘",
    "restaurantes": "🍽️",
    "bares_pubs": "🍻",
    "servicios_locales": "🏪",
    "pizzerias_hamburgueserias": "🍕",
    "hoteles_alojamientos": "🛏️",
    "juguerias": "🥤",
    "galerias_arte": "🖼️",
    "discotecas": "💃",
    "piscinas": "🏊",
    "gimnasios": "💪",
    "panaderias": "🥐",
    "belleza_spas": "💆",
    "cafeterias": "☕",
    "miradores": "🏞️",
    "monumentos": "🗽",
    "jardines": "🌷"
}

# Nombres amigables para las preferencias
PREFERENCE_NAMES = {
    "iglesias": "Iglesias",
    "resorts": "Resorts",
    "playas": "Playas",
    "parques": "Parques",
    "teatros": "Teatros",
    "museos": "Museos",
    "centros_comerciales": "Centros Comerciales",
    "zoologicos": "Zoológicos",
    "restaurantes": "Restaurantes",
    "bares_pubs": "Bares",
    "servicios_locales": "Servicios",
    "pizzerias_hamburgueserias": "Comida Rápida",
    "hoteles_alojamientos": "Hoteles",
    "juguerias": "Juguerías",
    "galerias_arte": "Arte",
    "discotecas": "Discotecas",
    "piscinas": "Piscinas",
    "gimnasios": "Gimnasios",
    "panaderias": "Panaderías",
    "belleza_spas": "Spas",
    "cafeterias": "Cafeterías",
    "miradores": "Miradores",
    "monumentos": "Monumentos",
    "jardines": "Jardines"
}

# Colores para el tema
THEME_COLORS = {
    "primary": "#4361EE",
    "secondary": "#3A0CA3",
    "accent": "#7209B7",
    "success": "#4CC9F0",
    "warning": "#F72585",
    "light": "#F8F9FA",
    "dark": "#212529"
}