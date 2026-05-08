import streamlit as st
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# 1. GLOBAL CONFIG & MULTILINGUAL DICTIONARY
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="GlobalInternet.py - House Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

LANG_DICT = {
    "English": {
        "title": "🏠 House Blueprint Planner",
        "subtitle": "Built by GlobalInternet.py",
        "owner": "Built by Gesner Deslandes",
        "specs": "House Specs",
        "controls": "Settings & Controls",
        "view_mode": "Select View Mode",
        "floor_sel": "Select Floor",
        "lang_sel": "Language Selection",
        "pricing": "Market Pricing (Competitive)",
        "blueprint": "2D Blueprint",
        "model": "3D Model View",
        "ground": "Ground Floor",
        "upper": "Upper Floor",
        "total_area": "Total Area",
        "room_details": "Room Dimensions & Details"
    },
    "French": {
        "title": "🏠 Planificateur de Maison",
        "subtitle": "Créé par GlobalInternet.py",
        "owner": "Construit par Gesner Deslandes",
        "specs": "Spécifications",
        "controls": "Réglages et Commandes",
        "view_mode": "Mode d'affichage",
        "floor_sel": "Choisir l'étage",
        "lang_sel": "Choix de la langue",
        "pricing": "Prix du Marché (Compétitif)",
        "blueprint": "Plan 2D",
        "model": "Vue Modèle 3D",
        "ground": "Rez-de-chaussée",
        "upper": "Premier Étage",
        "total_area": "Surface Totale",
        "room_details": "Dimensions et Détails des Pièces"
    },
    "Spanish": {
        "title": "🏠 Planificador de Casas",
        "subtitle": "Creado por GlobalInternet.py",
        "owner": "Construido por Gesner Deslandes",
        "specs": "Especificaciones",
        "controls": "Ajustes y Controles",
        "view_mode": "Modo de Vista",
        "floor_sel": "Seleccionar Piso",
        "lang_sel": "Selección de Idioma",
        "pricing": "Precios de Mercado (Competitivo)",
        "blueprint": "Plano 2D",
        "model": "Vista de Modelo 3D",
        "ground": "Planta Baja",
        "upper": "Piso Superior",
        "total_area": "Área Total",
        "room_details": "Dimensiones y Detalles"
    }
}

# ─────────────────────────────────────────────
# 2. SIDEBAR: LOGO, LANGUAGE & BRANDING
# ─────────────────────────────────────────────
with st.sidebar:
    # 🌍 SPINNING GLOBE LOGO (CSS Animation)
    st.markdown("""
        <div style="text-align: center;">
            <div class="globe-logo">🌍</div>
        </div>
        <style>
            .globe-logo {
                font-size: 80px;
                animation: spin 4s linear infinite;
                display: inline-block;
            }
            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align:center; color:#1E88E5;'>GlobalInternet.py</h2>", unsafe_allow_html=True)
    
    # Language Selection at the top
    lang = st.selectbox("🌐 Language / Langue / Idioma", ["English", "French", "Spanish"])
    T = LANG_DICT[lang] # Current translation dictionary
    
    st.divider()
    st.write(f"👷 **Founder & Chief Engineer:**\nGesner Deslandes")
    st.caption(T["owner"])
    
    st.divider()
    st.subheader(f"⚙️ {T['controls']}")
    view_mode = st.radio(T["view_mode"], [T["blueprint"], T["model"]])
    floor_sel = st.selectbox(T["floor_sel"], [T["ground"], T["upper"]])
    
    # 💰 COMPETITIVE PRICING
    st.divider()
    st.subheader(f"💰 {T['pricing']}")
    st.markdown("""
    | Service | Rate |
    | :--- | :--- |
    | **Basic Draft** | $499 |
    | **Full Blueprint** | $1,250 |
    | **3D Render** | $1,800 |
    *Competitive global rates by GlobalInternet.py*
    """)

# ─────────────────────────────────────────────
# 3. HOUSE DATA & LOGIC
# ─────────────────────────────────────────────
HOUSE_W, HOUSE_H, FLOOR_H = 80, 50, 12

# Rooms lists (keeping original data structure)
GROUND_ROOMS = [("Living Room", 0, 26, 28, 50, "#FFEBEE", "🛋️"), ("Dining Room", 28, 26, 54, 50, "#E8F5E9", "🍽️"), ("Kitchen", 54, 26, 80, 50, "#E1F5FE", "🍳")]
UPPER_ROOMS = [("Bedroom 1", 0, 26, 36, 50, "#FFF3E0", "🛏️"), ("Bedroom 2", 36, 26, 80, 50, "#F3E5F5", "🛏️")]

# ─────────────────────────────────────────────
# 4. MAIN INTERFACE (COLORFUL)
# ─────────────────────────────────────────────
# Colorful Header
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #FF512F 0%, #DD2476 50%, #FF512F 100%); 
                padding: 20px; border-radius: 15px; text-align: center; color: white;">
        <h1 style="margin:0;">{T['title']}</h1>
        <p style="font-weight: bold;">{T['subtitle']} | {T['owner']}</p>
    </div>
""", unsafe_allow_html=True)

# Metrics Row
rooms_now = GROUND_ROOMS if floor_sel == T["ground"] else UPPER_ROOMS
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div style='background:#BBDEFB; padding:10px; border-radius:10px; text-align:center;'><b>{T['total_area']}</b><br>8,000 ft²</div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div style='background:#C8E6C9; padding:10px; border-radius:10px; text-align:center;'><b>{T['floor_sel']}</b><br>{floor_sel}</div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div style='background:#FFF9C4; padding:10px; border-radius:10px; text-align:center;'><b>Status</b><br>Active</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 5. DRAWING FUNCTIONS (Bypassing Python 3.14 validation issues)
# ─────────────────────────────────────────────
def draw_2d():
    fig = go.Figure()
    for name, x0, y0, x1, y1, color, emoji in rooms_now:
        fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, fillcolor=color, line=dict(color="RoyalBlue", width=2))
        fig.add_annotation(x=(x0+x1)/2, y=(y0+y1)/2, text=f"{emoji}<br>{name}", showarrow=False)
    
    fig.update_layout(
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, zeroline=False, range=[-5, 85]),
        yaxis=dict(showgrid=True, zeroline=False, range=[-5, 55]),
        height=600
    )
    return fig

def draw_3d():
    fig = go.Figure()
    z_base = 0 if floor_sel == T["ground"] else 12
    for name, x0, y0, x1, y1, color, emoji in rooms_now:
        # Create 3D Box
        fig.add_trace(go.Mesh3d(
            x=[x0, x1, x1, x0, x0, x1, x1, x0],
            y=[y0, y0, y1, y1, y0, y0, y1, y1],
            z=[z_base, z_base, z_base, z_base, z_base+12, z_base+12, z_base+12, z_base+12],
            i=[0, 0, 4, 4, 0, 1], j=[1, 2, 5, 6, 4, 5], k=[2, 3, 6, 7, 5, 6],
            color=color, opacity=0.7, name=name
        ))
    fig.update_layout(scene=dict(aspectmode="data"), height=700)
    return fig

# Display Chart
if view_mode == T["blueprint"]:
    st.plotly_chart(draw_2d(), use_container_width=True)
else:
    st.plotly_chart(draw_3d(), use_container_width=True)

# Footer
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #777;'>GlobalInternet.py &copy; 2026 | {T['owner']}</p>", unsafe_allow_html=True)
