import streamlit as st
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# CONFIG & SETTINGS
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="House Blueprint Planner",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

HOUSE_W = 80
HOUSE_H = 50
FLOOR_H = 12

# (name, x0, y0, x1, y1, fillcolor, emoji)
GROUND_ROOMS = [
    ("Living Room",   0,  26, 28, 50, "#E3F2FD", "🛋️"),
    ("Dining Room",  28,  26, 54, 50, "#FFF9C4", "🍽️"),
    ("Kitchen",      54,  26, 80, 50, "#F3E5F5", "🍳"),
    ("Library",       0,   0, 26, 26, "#E8F5E9", "📚"),
    ("Tech Lab",     26,   0, 54, 26, "#FBE9E7", "🔬"),
    ("Porch",        54,   0, 80, 14, "#ECEFF1", "🌿"),
    ("Hallway",      54,  14, 80, 26, "#F5F5F5", "🚪"),
]

UPPER_ROOMS = [
    ("Bedroom 1",     0,  26, 36, 50, "#BBDEFB", "🛏️"),
    ("Toilet 1",      0,  12, 14, 26, "#B3E5FC", "🚿"),
    ("Bedroom 2",    36,  26, 80, 50, "#C8E6C9", "🛏️"),
    ("Toilet 2",     36,  12, 54, 26, "#A5D6A7", "🚿"),
    ("Bedroom 3",     0,   0, 36, 12, "#FFE0B2", "🛏️"),
    ("Toilet 3",     36,   0, 54, 12, "#FFCC80", "🚿"),
    ("Bedroom 4",    54,   0, 80, 30, "#F8BBD0", "🛏️"),
    ("Toilet 4",     54,  30, 80, 42, "#F48FB1", "🚿"),
    ("Tech Room",    14,  12, 36, 26, "#E1BEE7", "🎮"),
    ("Landing",      36,  40, 54, 50, "#ECEFF1", "🚶"),
]

FM = 15
SITE_X0, SITE_X1 = -FM - 5, HOUSE_W + FM + 5
SITE_Y0, SITE_Y1 = -FM - 18, HOUSE_H + FM + 8

# ─────────────────────────────────────────────
# VISUALIZATION FUNCTIONS
# ─────────────────────────────────────────────

def draw_2d(floor):
    rooms = GROUND_ROOMS if floor == "Ground Floor" else UPPER_ROOMS
    shapes, annotations = [], []

    if floor == "Ground Floor":
        shapes.append(dict(type="rect", x0=SITE_X0, y0=SITE_Y0, x1=SITE_X1, y1=SITE_Y1,
                           fillcolor="#D7F5D0", line=dict(color="#2E7D32", width=3, dash="dot")))
        annotations += [
            dict(x=(SITE_X0+SITE_X1)/2, y=SITE_Y0+5, text="🐕 Backyard", showarrow=False, font=dict(family="monospace", color="#2E7D32")),
            dict(x=(SITE_X0+SITE_X1)/2, y=SITE_Y1-4, text="🌳 Front Yard", showarrow=False, font=dict(family="monospace", color="#1B5E20"))
        ]
        gc = (SITE_X0 + SITE_X1) / 2
        shapes.append(dict(type="rect", x0=gc-5, y0=SITE_Y1-1, x1=gc+5, y1=SITE_Y1+3, fillcolor="#8D6E63"))

    shapes.append(dict(type="rect", x0=0, y0=0, x1=HOUSE_W, y1=HOUSE_H, fillcolor="rgba(0,0,0,0)", line=dict(color="#0D47A1", width=4)))

    for name, x0, y0, x1, y1, color, emoji in rooms:
        shapes.append(dict(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, fillcolor=color, line=dict(color="#1565C0", width=2)))
        annotations.append(dict(x=(x0+x1)/2, y=(y0+y1)/2, text=f"{emoji}<br>{name.split('(')[0]}", showarrow=False, font=dict(size=9, family="monospace")))

    xr = [SITE_X0-5, SITE_X1+5] if floor=="Ground Floor" else [-10, HOUSE_W+10]
    yr = [SITE_Y0-5, SITE_Y1+5] if floor=="Ground Floor" else [-10, HOUSE_H+10]

    fig = go.Figure()
    # Explicitly set layout to avoid Python 3.14 validation issues
    fig.update_layout(
        title=f"📐 {floor.upper()} BLUEPRINT",
        xaxis=dict(range=xr, scaleanchor="y", scaleratio=1, gridcolor="#BBDEFB"),
        yaxis=dict(range=yr, gridcolor="#BBDEFB"),
        shapes=shapes,
        annotations=annotations,
        plot_bgcolor="#F0F4FF",
        height=700
    )
    return fig

def room_box(fig, x0, y0, x1, y1, z0, z1, color, name):
    # Standard cube vertices
    vx = [x0, x1, x1, x0, x0, x1, x1, x0]
    vy = [y0, y0, y1, y1, y0, y0, y1, y1]
    vz = [z0, z0, z0, z0, z1, z1, z1, z1]
    fig.add_trace(go.Mesh3d(
        x=vx, y=vy, z=vz,
        i=[0, 0, 4, 4, 0, 1], j=[1, 2, 5, 6, 4, 5], k=[2, 3, 6, 7, 5, 6],
        color=color, opacity=0.6, name=name, showlegend=True
    ))

def draw_3d(floor):
    fig = go.Figure()
    z0 = 0 if floor == "Ground Floor" else FLOOR_H
    z1 = z0 + FLOOR_H
    rooms = GROUND_ROOMS if floor == "Ground Floor" else UPPER_ROOMS

    for name, x0, y0, x1, y1, color, emoji in rooms:
        room_box(fig, x0, y0, x1, y1, z0, z1, color, f"{emoji} {name}")

    if floor == "Upper Floor":
        # Simplified Roof
        fig.add_trace(go.Mesh3d(
            x=[0, HOUSE_W, HOUSE_W, 0, HOUSE_W/2],
            y=[0, 0, HOUSE_H, HOUSE_H, HOUSE_H/2],
            z=[z1, z1, z1, z1, z1+10],
            i=[0, 0, 1, 2], j=[1, 4, 4, 4], k=[4, 3, 2, 3],
            color="#B71C1C", opacity=0.8, name="Roof"
        ))

    fig.update_layout(
        scene=dict(
            xaxis_title="Width (ft)", yaxis_title="Depth (ft)", zaxis_title="Height (ft)",
            aspectmode="data",
            camera=dict(eye=dict(x=1.5, y=-1.5, z=1.2))
        ),
        height=700, margin=dict(l=0, r=0, t=40, b=0)
    )
    return fig

# ─────────────────────────────────────────────
# INTERFACE
# ─────────────────────────────────────────────
st.markdown("<style>.metric-box{background:white; border-radius:10px; padding:15px; text-align:center; border-left:5px solid #1565C0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}</style>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Settings")
    view_mode = st.radio("View", ["2D Blueprint", "3D Model"])
    floor_sel = st.selectbox("Floor", ["Ground Floor", "Upper Floor"])
    st.divider()
    st.info(f"**House Size:** {HOUSE_W}' x {HOUSE_H}'\n\n**Total Area:** {HOUSE_W*HOUSE_H*2:,} sq ft")

# Metrics
rooms_list = GROUND_ROOMS if floor_sel == "Ground Floor" else UPPER_ROOMS
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"<div class='metric-box'>🏙️<br><b>{floor_sel}</b></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-box'>🚪<br><b>{len(rooms_list)} Rooms</b></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-box'>📐<br><b>{HOUSE_W*HOUSE_H} ft²</b></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='metric-box'>🏗️<br><b>{view_mode}</b></div>", unsafe_allow_html=True)

st.write("")

# Render Logic
if view_mode == "2D Blueprint":
    st.plotly_chart(draw_2d(floor_sel), use_container_width=True)
else:
    st.plotly_chart(draw_3d(floor_sel), use_container_width=True)

# Documentation
with st.expander("📖 Room Details"):
    cols = st.columns(2)
    for i, (name, x0, y0, x1, y1, _, emoji) in enumerate(rooms_list):
        target_col = cols[i % 2]
        w, d = abs(x1-x0), abs(y1-y0)
        target_col.write(f"{emoji} **{name}**: {w}' x {d}' ({w*d} sq ft)")
