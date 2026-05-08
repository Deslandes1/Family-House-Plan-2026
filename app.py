import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="House Blueprint Planner",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# HOUSE LAYOUT DATA  (coordinates in feet)
# ─────────────────────────────────────────────
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
    ("Bedroom 1 (Kid 1)", 0,  26, 36, 50, "#BBDEFB", "🛏️"),
    ("Toilet 1",          0,  12, 14, 26, "#B3E5FC", "🚿"),
    ("Bedroom 2 (Kid 2)", 36, 26, 80, 50, "#C8E6C9", "🛏️"),
    ("Toilet 2",          36, 12, 54, 26, "#A5D6A7", "🚿"),
    ("Bedroom 3 (Kid 3)", 0,   0, 36, 12, "#FFE0B2", "🛏️"),
    ("Toilet 3",          36,  0, 54, 12, "#FFCC80", "🚿"),
    ("Bedroom 4 (Kid 4)", 54,  0, 80, 30, "#F8BBD0", "🛏️"),
    ("Toilet 4",          54, 30, 80, 42, "#F48FB1", "🚿"),
    ("Tech Room (Kids)",  14, 12, 36, 26, "#E1BEE7", "🎮"),
    ("Landing",           36, 40, 54, 50, "#ECEFF1", "🚶"),
]

FM = 15
SITE_X0, SITE_X1 = -FM - 5, HOUSE_W + FM + 5
SITE_Y0, SITE_Y1 = -FM - 18, HOUSE_H + FM + 8


# ─────────────────────────────────────────────
# 2D BLUEPRINT
# ─────────────────────────────────────────────
def draw_2d(floor):
    rooms = GROUND_ROOMS if floor == "Ground Floor" else UPPER_ROOMS
    shapes, annotations = [], []

    if floor == "Ground Floor":
        shapes.append(dict(type="rect",
            x0=SITE_X0, y0=SITE_Y0, x1=SITE_X1, y1=SITE_Y1,
            fillcolor="#D7F5D0", line=dict(color="#2E7D32", width=3, dash="dot")))
        annotations += [
            dict(x=(SITE_X0+SITE_X1)/2, y=SITE_Y0+5,
                 text="🐕  Backyard / Dog House", showarrow=False,
                 font=dict(size=11, color="#2E7D32", family="monospace")),
            dict(x=(SITE_X0+SITE_X1)/2, y=SITE_Y1-4,
                 text="🌳  Front Yard", showarrow=False,
                 font=dict(size=11, color="#1B5E20", family="monospace")),
        ]
        gc = (SITE_X0 + SITE_X1) / 2
        shapes.append(dict(type="rect",
            x0=gc-5, y0=SITE_Y1-1, x1=gc+5, y1=SITE_Y1+3,
            fillcolor="#8D6E63", line=dict(color="#4E342E", width=2)))
        annotations.append(dict(x=gc, y=SITE_Y1+6, text="🚪 GATE",
            showarrow=False, font=dict(size=10, color="#4E342E", family="monospace")))

    # House outline
    shapes.append(dict(type="rect", x0=0, y0=0, x1=HOUSE_W, y1=HOUSE_H,
        fillcolor="rgba(0,0,0,0)", line=dict(color="#0D47A1", width=5)))

    # Rooms
    for name, x0, y0, x1, y1, color, emoji in rooms:
        shapes.append(dict(type="rect", x0=x0, y0=y0, x1=x1, y1=y1,
            fillcolor=color, line=dict(color="#1565C0", width=2)))
        label = name.split("(")[0].strip()
        annotations.append(dict(
            x=(x0+x1)/2, y=(y0+y1)/2,
            text=f"{emoji}<br>{label}",
            showarrow=False,
            font=dict(size=8, color="#1a1a2e", family="monospace"),
            xanchor="center", yanchor="middle", align="center"
        ))

    # Dimension lines
    annotations += [
        dict(x=HOUSE_W/2, y=-2, text=f"<b>← {HOUSE_W} ft →</b>",
             showarrow=False, font=dict(size=9, color="#333", family="monospace")),
        dict(x=-4, y=HOUSE_H/2, text=f"<b>{HOUSE_H} ft</b>",
             showarrow=False, font=dict(size=9, color="#333", family="monospace"),
             textangle=-90),
        dict(x=HOUSE_W+6, y=HOUSE_H-4, text="🧭 N",
             showarrow=False, font=dict(size=15, color="#0D47A1")),
    ]

    xr = [SITE_X0-3, SITE_X1+3] if floor=="Ground Floor" else [-10, HOUSE_W+12]
    yr = [SITE_Y0-6, SITE_Y1+10] if floor=="Ground Floor" else [-8, HOUSE_H+8]

    fig = go.Figure()
    fig.update_layout(
        title=dict(
            text=f"📐 {'GROUND' if floor=='Ground Floor' else 'UPPER'} FLOOR — Blueprint",
            font=dict(size=18, family="monospace", color="#0D47A1")
        ),
        shapes=shapes, annotations=annotations,
        xaxis=dict(range=xr, showgrid=True, gridcolor="#BBDEFB",
                   gridwidth=1, zeroline=False, dtick=10,
                   tickfont=dict(family="monospace", size=8), title="ft"),
        yaxis=dict(range=yr, showgrid=True, gridcolor="#BBDEFB",
                   gridwidth=1, zeroline=False, dtick=10,
                   tickfont=dict(family="monospace", size=8), title="ft"),
        plot_bgcolor="#F0F4FF", paper_bgcolor="#E8EDF8",
        height=680, margin=dict(l=60, r=20, t=60, b=40),
        showlegend=False,
    )
    return fig


# ─────────────────────────────────────────────
# 3D VIEW
# ─────────────────────────────────────────────
def room_box(fig, x0, y0, x1, y1, z0, z1, color, name, opacity=0.6):
    vx = [x0,x1,x1,x0, x0,x1,x1,x0]
    vy = [y0,y0,y1,y1, y0,y0,y1,y1]
    vz = [z0,z0,z0,z0, z1,z1,z1,z1]
    fig.add_trace(go.Mesh3d(
        x=vx, y=vy, z=vz,
        i=[0,0,4,4,0,1], j=[1,2,5,6,4,5], k=[2,3,6,7,5,6],
        color=color, opacity=opacity,
        name=name, showlegend=True,
        hovertemplate=f"<b>{name}</b><extra></extra>"
    ))

def draw_3d(floor):
    fig = go.Figure()
    z0 = 0 if floor == "Ground Floor" else FLOOR_H
    z1 = z0 + FLOOR_H
    rooms = GROUND_ROOMS if floor == "Ground Floor" else UPPER_ROOMS

    for name, x0, y0, x1, y1, color, emoji in rooms:
        room_box(fig, x0, y0, x1, y1, z0, z1, color, f"{emoji} {name}")

    room_box(fig, 0, 0, HOUSE_W, HOUSE_H, z0-0.5, z0, "#CFD8DC", "Floor Slab", opacity=0.95)

    if floor == "Upper Floor":
        rx, rz = HOUSE_W/2, z1+10
        fig.add_trace(go.Mesh3d(
            x=[0, HOUSE_W, HOUSE_W, 0,   rx,     rx    ],
            y=[0, 0,       HOUSE_H, HOUSE_H, 0,   HOUSE_H],
            z=[z1,z1,      z1,      z1,  rz,     rz    ],
            i=[0,0,1,2], j=[1,4,5,5], k=[4,3,4,3],
            color="#B71C1C", opacity=0.75,
            name="🏠 Roof", showlegend=True,
        ))

    if floor == "Ground Floor":
        fx = [SITE_X0, SITE_X1, SITE_X1, SITE_X0, SITE_X0]
        fy = [SITE_Y0, SITE_Y0, SITE_Y1, SITE_Y1, SITE_Y0]
        fig.add_trace(go.Scatter3d(
            x=fx, y=fy, z=[3]*5,
            mode="lines", line=dict(color="#4E342E", width=6),
            name="🚧 Fence"
        ))

    fig.update_layout(
        title=dict(
            text=f"🏗️ 3D View — {floor}",
            font=dict(size=18, family="monospace", color="#0D47A1")
        ),
        scene=dict(
            xaxis=dict(title="Width (ft)", backgroundcolor="#E3F2FD"),
            yaxis=dict(title="Depth (ft)", backgroundcolor="#E8F5E9"),
            zaxis=dict(title="Height (ft)", backgroundcolor="#FFF9C4"),
            camera=dict(eye=dict(x=1.8, y=-2.0, z=1.5)),
            aspectmode="data",
        ),
        paper_bgcolor="#E8EDF8", height=680,
        margin=dict(l=0, r=0, t=60, b=0),
        legend=dict(font=dict(size=9), bgcolor="rgba(255,255,255,0.75)",
                    bordercolor="#ccc", borderwidth=1)
    )
    return fig


# ─────────────────────────────────────────────
# STREAMLIT APP
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
html,body,[class*="css"]{font-family:'Share Tech Mono',monospace;}
.metric-box{
    background:white;border-radius:10px;padding:14px;text-align:center;
    border-left:4px solid #1565C0;box-shadow:0 2px 8px rgba(0,0,0,0.08);
    margin-bottom:8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background:linear-gradient(135deg,#0D47A1,#1976D2);
            padding:22px 30px;border-radius:14px;margin-bottom:18px;'>
  <h1 style='color:white;margin:0;font-family:monospace;'>🏠 House Blueprint Planner</h1>
  <p style='color:#BBDEFB;margin:6px 0 0;font-size:13px;'>
    2D Blueprint · 3D Walkthrough · 4 Bedrooms with Ensuites · 2 Floors
  </p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ⚙️ Controls")
    mode  = st.radio("View Mode", ["📐 2D Blueprint", "🏗️ 3D View"])
    floor = st.selectbox("Select Floor", ["Ground Floor", "Upper Floor"])
    st.markdown("---")
    st.markdown("### 🏠 House Specs")
    st.markdown(f"""
- **Width:** {HOUSE_W} ft  
- **Depth:** {HOUSE_H} ft  
- **Floors:** 2  
- **Floor Height:** {FLOOR_H} ft  
- **Total Area:** {HOUSE_W*HOUSE_H*2:,} sq ft  
""")
    st.markdown("---")
    st.markdown("""### 📋 Legend
🛋️ Living Room · 🍽️ Dining Room  
🍳 Kitchen · 📚 Library  
🔬 Tech Lab · 🎮 Kids Tech Room  
🛏️ 4 Bedrooms · 🚿 4 Ensuites  
🌿 Porch · 🐕 Backyard · 🚪 Gate
""")

rooms_now  = GROUND_ROOMS if floor == "Ground Floor" else UPPER_ROOMS
total_area = sum(abs(r[3]-r[1])*abs(r[4]-r[2]) for r in rooms_now)

c1,c2,c3,c4 = st.columns(4)
for col, icon, val, label in [
    (c1,"📐",f"{HOUSE_W}×{HOUSE_H} ft","Footprint"),
    (c2,"🏠",len(rooms_now),"Rooms on Floor"),
    (c3,"📏",f"{total_area:,} ft²","Floor Area"),
    (c4,"🛏️","4 + 4","Beds + Ensuites"),
]:
    col.markdown(f"""<div class='metric-box'>
        <div style='font-size:22px'>{icon}</div>
        <div style='font-size:19px;font-weight:bold'>{val}</div>
        <div style='color:#666;font-size:11px'>{label}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

fig = draw_2d(floor) if "2D" in mode else draw_3d(floor)
st.plotly_chart(fig, use_container_width=True)

with st.expander("📊 Room Dimensions Table"):
    data = []
    for name,x0,y0,x1,y1,color,emoji in rooms_now:
        w,d = abs(x1-x0), abs(y1-y0)
        data.append({"Room":f"{emoji} {name}","Width(ft)":w,"Depth(ft)":d,"Area(sq ft)":w*d})
    st.table(data)

with st.expander("📝 Floor Plan Description"):
    if floor == "Ground Floor":
        st.markdown("""
**Ground Floor:**
- 🛋️ **Living Room** (28×24 ft) — spacious family lounge  
- 🍽️ **Dining Room** (26×24 ft) — large family dining space  
- 🍳 **Kitchen** (26×24 ft) — open modern kitchen  
- 📚 **Library** (26×26 ft) — quiet reading & study room  
- 🔬 **Tech Laboratory** (28×26 ft) — science & maker space  
- 🌿 **Porch** (26×14 ft) — chill-out porch for the family  
- 🚶 **Hallway** (26×12 ft) — connects porch to all rooms  
- 🐕 **Fenced Backyard** — dog house + outdoor play area  
- 🚪 **Gated Front Yard** — secure entrance gate + fence  
""")
    else:
        st.markdown("""
**Upper Floor:**
- 🛏️ **Bedroom 1 – Kid 1** (36×24 ft) + 🚿 Ensuite  
- 🛏️ **Bedroom 2 – Kid 2** (44×24 ft) + 🚿 Ensuite  
- 🛏️ **Bedroom 3 – Kid 3** (36×12 ft) + 🚿 Ensuite  
- 🛏️ **Bedroom 4 – Kid 4** (26×30 ft) + 🚿 Ensuite  
- 🎮 **Kids Tech Room** (22×14 ft) — gaming & media den  
- 🚶 **Landing** (18×10 ft) — staircase landing  
""")

st.markdown("---")
st.markdown("<div style='text-align:center;color:#888;font-size:11px;font-family:monospace;'>🏠 House Blueprint Planner · Built with Streamlit + Plotly</div>", unsafe_allow_html=True)
