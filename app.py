import streamlit as st
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# 1. MULTILINGUAL DICTIONARY
# ─────────────────────────────────────────────
LANG_DICT = {
    "English": {
        "title": "🏠 House Blueprint Planner",
        "company": "GlobalInternet.py",
        "author": "Gesner Deslandes",
        "role": "Owner, Founder & Chief Engineer",
        "settings": "Settings",
        "view": "View Mode",
        "floor": "Select Floor",
        "pricing": "Competitive Market Pricing",
        "ground": "Ground Floor",
        "upper": "Upper Floor",
        "total_area": "Total Area",
        "rooms": "Rooms",
        "details": "Room Details",
        "blue_2d": "2D Blueprint",
        "model_3d": "3D Model"
    },
    "French": {
        "title": "🏠 Planificateur de Maison",
        "company": "GlobalInternet.py",
        "author": "Gesner Deslandes",
        "role": "Propriétaire, Fondateur et Ingénieur en Chef",
        "settings": "Réglages",
        "view": "Mode d'affichage",
        "floor": "Choisir l'étage",
        "pricing": "Tarification Compétitive",
        "ground": "Rez-de-chaussée",
        "upper": "Premier Étage",
        "total_area": "Surface Totale",
        "rooms": "Pièces",
        "details": "Détails des Pièces",
        "blue_2d": "Plan 2D",
        "model_3d": "Modèle 3D"
    },
    "Spanish": {
        "title": "🏠 Planificador de Casas",
        "company": "GlobalInternet.py",
        "author": "Gesner Deslandes",
        "role": "Propietario, Fundador e Ingeniero Jefe",
        "settings": "Ajustes",
        "view": "Modo de Vista",
        "floor": "Seleccionar Piso",
        "pricing": "Precios Competitivos",
        "ground": "Planta Baja",
        "upper": "Piso Superior",
        "total_area": "Área Total",
        "rooms": "Habitaciones",
        "details": "Detalles de la Habitación",
        "blue_2d": "Plano 2D",
        "model_3d": "Modelo 3D"
    }
}

# ─────────────────────────────────────────────
# 2. CONFIG & HOUSE DATA (UNTOUCHED)
# ─────────────────────────────────────────────
st.set_page_config(page_title="GlobalInternet.py Planner", page_icon="🌍", layout="wide")

HOUSE_W, HOUSE_H, FLOOR_H = 80, 50, 12
FM = 15
SITE_X0, SITE_X1 = -FM - 5, HOUSE_W + FM + 5
SITE_Y0, SITE_Y1 = -FM - 18, HOUSE_H + FM + 8

GROUND_ROOMS = [
    ("Living Room", 0, 26, 28, 50, "#E3F2FD", "🛋️"),
    ("Dining Room", 28, 26, 54, 50, "#FFF9C4", "🍽️"),
    ("Kitchen", 54, 26, 80, 50, "#F3E5F5", "🍳"),
    ("Library", 0, 0, 26, 26, "#E8F5E9", "📚"),
    ("Tech Lab", 26, 0, 54, 26, "#FBE9E7", "🔬"),
    ("Porch", 54, 0, 80, 14, "#ECEFF1", "🌿"),
    ("Hallway", 54, 14, 80, 26, "#F5F5F5", "🚪"),
]

UPPER_ROOMS = [
    ("Bedroom 1", 0, 26, 36, 50, "#BBDEFB", "🛏️"),
    ("Toilet 1", 0, 12, 14, 26, "#B3E5FC", "🚿"),
    ("Bedroom 2", 36, 26, 80, 50, "#C8E6C9", "🛏️"),
    ("Toilet 2", 36, 12, 54, 26, "#A5D6A7", "🚿"),
    ("Bedroom 3", 0, 0, 36, 12, "#FFE0B2", "🛏️"),
    ("Toilet 3", 36, 0, 54, 12, "#FFCC80", "🚿"),
    ("Bedroom 4", 54, 0, 80, 30, "#F8BBD0", "🛏️"),
    ("Toilet 4", 54, 30, 80, 42, "#F48FB1", "🚿"),
    ("Tech Room", 14, 12, 36, 26, "#E1BEE7", "🎮"),
    ("Landing", 36, 40, 54, 50, "#ECEFF1", "🚶"),
]

# ─────────────────────────────────────────────
# 3. SIDEBAR: SPINNING GLOBE & BRANDING
# ─────────────────────────────────────────────
st.markdown("""
    <style>
    @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    .spinning-globe { font-size: 50px; text-align: center; animation: rotate 5s linear infinite; display: block; margin: auto; }
    .metric-box { background:white; border-radius:10px; padding:15px; text-align:center; border-left:5px solid #FF4B4B; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: black; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="spinning-globe">🌍</div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>GlobalInternet.py</h2>", unsafe_allow_html=True)
    
    # Language Selection
    selected_lang = st.selectbox("🌐 Language / Langue / Idioma", ["English", "French", "Spanish"])
    T = LANG_DICT[selected_lang]
    
    st.divider()
    st.write(f"**{T['author']}**")
    st.caption(T['role'])
    
    st.divider()
    st.header(f"⚙️ {T['settings']}")
    view_mode = st.radio(T['view'], [T['blue_2d'], T['model_3d']])
    floor_input = st.selectbox(T['floor'], [T['ground'], T['upper']])
    # Convert display name back to logic name
    floor_sel = "Ground Floor" if floor_input == T['ground'] else "Upper Floor"
    
    st.divider()
    st.subheader(f"💰 {T['pricing']}")
    st.markdown("""
    - **Draft:** $250
    - **Full Plan:** $750
    - **3D Interactive:** $1,500
    """)

# ─────────────────────────────────────────────
# 4. VISUALIZATION FUNCTIONS (LOGIC PRESERVED)
# ─────────────────────────────────────────────
def draw_2d(floor):
    rooms = GROUND_ROOMS if floor == "Ground Floor" else UPPER_ROOMS
    shapes, annotations = [], []
    if floor == "Ground Floor":
        shapes.append(dict(type="rect", x0=SITE_X0, y0=SITE_Y0, x1=SITE_X1, y1=SITE_Y1, fillcolor="#D7F5D0", line=dict(color="#2E7D32", width=3, dash="dot")))
    shapes.append(dict(type="rect", x0=0, y0=0, x1=HOUSE_W, y1=HOUSE_H, fillcolor="rgba(0,0,0,0)", line=dict(color="#0D47A1", width=4)))
    for name, x0, y0, x1, y1, color, emoji in rooms:
        shapes.append(dict(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, fillcolor=color, line=dict(color="#1565C0", width=2)))
        annotations.append(dict(x=(x0+x1)/2, y=(y0+y1)/2, text=f"{emoji}<br>{name}", showarrow=False, font=dict(size=9)))
    fig = go.Figure()
    fig.update_layout(title=f"📐 {floor.upper()}", xaxis=dict(range=[SITE_X0-5, SITE_X1+5], scaleanchor="y", scaleratio=1), yaxis=dict(range=[SITE_Y0-5, SITE_Y1+5]), shapes=shapes, annotations=annotations, height=700)
    return fig

def draw_3d(floor):
    fig = go.Figure()
    z0 = 0 if floor == "Ground Floor" else FLOOR_H
    rooms = GROUND_ROOMS if floor == "Ground Floor" else UPPER_ROOMS
    for name, x0, y0, x1, y1, color, emoji in rooms:
        vx, vy, vz = [x0, x1, x1, x0, x0, x1, x1, x0], [y0, y0, y1, y1, y0, y0, y1, y1], [z0, z0, z0, z0, z0+FLOOR_H, z0+FLOOR_H, z0+FLOOR_H, z0+FLOOR_H]
        fig.add_trace(go.Mesh3d(x=vx, y=vy, z=vz, i=[0, 0, 4, 4, 0, 1], j=[1, 2, 5, 6, 4, 5], k=[2, 3, 6, 7, 5, 6], color=color, opacity=0.6, name=name))
    fig.update_layout(scene=dict(xaxis_title="Width", yaxis_title="Depth", zaxis_title="Height", aspectmode="data"), height=700)
    return fig

# ─────────────────────────────────────────────
# 5. MAIN INTERFACE (COLORFUL)
# ─────────────────────────────────────────────
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #FF4B4B, #448AFF); padding: 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 25px;">
        <h1 style="margin:0;">{T['title']}</h1>
        <h3 style="margin:0; opacity: 0.9;">{T['company']} - {T['author']}</h3>
    </div>
""", unsafe_allow_html=True)

rooms_list = GROUND_ROOMS if floor_sel == "Ground Floor" else UPPER_ROOMS
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='metric-box'>🏗️<br><b>{floor_input}</b></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='metric-box'>🚪<br><b>{len(rooms_list)} {T['rooms']}</b></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='metric-box'>📐<br><b>{HOUSE_W*HOUSE_H} ft²</b></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='metric-box'>🌍<br><b>{selected_lang}</b></div>", unsafe_allow_html=True)

st.write("")

if view_mode == T['blue_2d']:
    st.plotly_chart(draw_2d(floor_sel), use_container_width=True)
else:
    st.plotly_chart(draw_3d(floor_sel), use_container_width=True)

with st.expander(f"📖 {T['details']}"):
    cols = st.columns(2)
    for i, (name, x0, y0, x1, y1, _, emoji) in enumerate(rooms_list):
        w, d = abs(x1-x0), abs(y1-y0)
        cols[i % 2].write(f"{emoji} **{name}**: {w}' x {d}' ({w*d} sq ft)")

st.divider()
st.markdown(f"<p style='text-align:center; color:gray;'>{T['company']} - Built by Gesner Deslandes | {T['role']}</p>", unsafe_allow_html=True)
