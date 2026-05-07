import streamlit as st
import random

# --- KONFIGURATION ---
st.set_page_config(page_title="Pokémon Streamlit-Edition", page_icon="🌿", layout="centered")

# --- STYLE ---
st.markdown("""
    <style>
    .map-cell { width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; border: 1px solid #ddd; font-size: 24px; }
    .player { background-color: #ffcccb; border-radius: 5px; }
    .grass { background-color: #90ee90; }
    .wall { background-color: #555; }
    .pokemon-card { padding: 20px; border-radius: 10px; background-color: #f0f2f6; text-align: center; border: 2px solid #ed1c24; }
    </style>
    """, unsafe_allow_html=True)

# --- DATEN ---
POKEMON_DATA = {
    "Glumanda": {"Typ": "Feuer", "HP": 39, "Angriff": 52, "Bild": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png"},
    "Schiggy": {"Typ": "Wasser", "HP": 44, "Angriff": 48, "Bild": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png"},
    "Bisasam": {"Typ": "Pflanze", "HP": 45, "Angriff": 49, "Bild": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"},
    "Pikachu": {"Typ": "Elektro", "HP": 35, "Angriff": 55, "Bild": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"}
}

MAP_SIZE = 6
# 0 = Leer, 1 = Gras (Begegnung möglich), 2 = Wand
GAME_MAP = [
    [2, 2, 2, 2, 2, 2],
    [2, 0, 0, 1, 1, 2],
    [2, 0, 0, 1, 1, 2],
    [2, 1, 1, 0, 0, 2],
    [2, 1, 1, 0, 0, 2],
    [2, 2, 2, 2, 2, 2],
]

# --- INITIALISIERUNG ---
if 'pos' not in st.session_state:
    st.session_state.pos = [1, 1] # Startposition [y, x]
    st.session_state.battle = False
    st.session_state.player_pkmn = None

# --- FUNKTIONEN ---
def move_player(dy, dx):
    new_y = st.session_state.pos[0] + dy
    new_x = st.session_state.pos[1] + dx
    if GAME_MAP[new_y][new_x] != 2: # Keine Wand
        st.session_state.pos = [new_y, new_x]
        # Check für Wild-Begegnung im Gras (Typ 1)
        if GAME_MAP[new_y][new_x] == 1 and random.random() < 0.3:
            start_battle()

def start_battle():
    enemy_name = random.choice(list(POKEMON_DATA.keys()))
    st.session_state.enemy_pkmn = POKEMON_DATA[enemy_name].copy()
    st.session_state.enemy_pkmn["Name"] = enemy_name
    st.session_state.enemy_hp = st.session_state.enemy_pkmn["HP"]
    st.session_state.player_hp = st.session_state.player_pkmn["HP"]
    st.session_state.battle = True
    st.session_state.logs = [f"Ein wildes {enemy_name} greift an!"]

# --- UI LOGIK ---
st.title("🚶 Pokémon Welt-Modus")

if st.session_state.player_pkmn is None:
    st.subheader("Wähle deinen Begleiter:")
    choice = st.selectbox("Pokémon", list(POKEMON_DATA.keys()))
    if st.button("Start"):
        st.session_state.player_pkmn = POKEMON_DATA[choice].copy()
        st.session_state.player_pkmn["Name"] = choice
        st.rerun()

elif st.session_state.battle:
    # --- KAMPF-MODUS (Dein alter Code hier integriert) ---
    st.warning("⚔️ KAMPF!")
    col1, col2 = st.columns(2)
    with col1:
        st.image(st.session_state.player_pkmn["Bild"], caption=f"Du ({st.session_state.player_hp} HP)")
    with col2:
        st.image(st.session_state.enemy_pkmn["Bild"], caption=f"Gegner ({st.session_state.enemy_hp} HP)")
    
    if st.button("💥 Angriff"):
        dmg = random.randint(5, 15)
        st.session_state.enemy_hp -= dmg
        if st.session_state.enemy_hp <= 0:
            st.success("Gegner besiegt!")
            st.session_state.battle = False
        else:
            st.session_state.player_hp -= random.randint(5, 10)
        st.rerun()

else:
    # --- MAP-MODUS ---
    col_map, col_ctrl = st.columns([2, 1])

    with col_map:
        for y in range(MAP_SIZE):
            cols = st.columns(MAP_SIZE)
            for x in range(MAP_SIZE):
                cell_type = GAME_MAP[y][x]
                content = ""
                css_class = "map-cell"
                
                if [y, x] == st.session_state.pos:
                    content = "🚶"
                    css_class += " player"
                elif cell_type == 1:
                    content = "🌿"
                    css_class += " grass"
                elif cell_type == 2:
                    content = "🌲"
                    css_class += " wall"
                
                cols[x].markdown(f"<div class='{css_class}'>{content}</div>", unsafe_allow_html=True)

    with col_ctrl:
        st.write("Steuerung:")
        if st.button("🔼 Oben"): move_player(-1, 0); st.rerun()
        c1, c2 = st.columns(2)
        if c1.button("◀️ Links"): move_player(0, -1); st.rerun()
        if c2.button("▶️ Rechts"): move_player(0, 1); st.rerun()
        if st.button("🔽 Unten"): move_player(1, 0); st.rerun()
        
        st.info("Laufe durch das hohe Gras (🌿) für Kämpfe!")

# --- KONFIGURATION & STYLES ---
st.set_page_config(page_title="Pokémon Streamlit-Edition", page_icon="🔥")

st.markdown("""
    <style>
    .pokemon-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        text-align: center;
        border: 2px solid #ed1c24;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATENMODELL ---
# Typen-Effektivität: Wer schlägt wen?
# 2.0 = Sehr effektiv, 0.5 = Nicht sehr effektiv, 1.0 = Normal
TYPE_CHART = {
    "Feuer": {"Pflanze": 2.0, "Wasser": 0.5, "Feuer": 0.5, "Elektro": 1.0},
    "Wasser": {"Feuer": 2.0, "Pflanze": 0.5, "Wasser": 0.5, "Elektro": 1.0},
    "Pflanze": {"Wasser": 2.0, "Feuer": 0.5, "Pflanze": 0.5, "Elektro": 1.0},
    "Elektro": {"Wasser": 2.0, "Pflanze": 1.0, "Feuer": 1.0, "Elektro": 0.5}
}

POKEMON_DATA = {
    "Glumanda": {"Typ": "Feuer", "HP": 39, "Angriff": 52, "Bild": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png"},
    "Schiggy": {"Typ": "Wasser", "HP": 44, "Angriff": 48, "Bild": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png"},
    "Bisasam": {"Typ": "Pflanze", "HP": 45, "Angriff": 49, "Bild": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"},
    "Pikachu": {"Typ": "Elektro", "HP": 35, "Angriff": 55, "Bild": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"}
}

# --- LOGIK ---
def calculate_damage(attacker, defender):
    base_dmg = attacker["Angriff"] // 5
    
    # Typen-Effektivität berechnen
    atk_type = attacker["Typ"]
    def_type = defender["Typ"]
    
    multiplier = TYPE_CHART.get(atk_type, {}).get(def_type, 1.0)
    
    variation = random.randint(-2, 2)
    final_dmg = int((base_dmg + variation) * multiplier)
    
    return max(1, final_dmg), multiplier

# --- SESSION STATE INITIALISIERUNG ---
if 'battle' not in st.session_state:
    st.session_state.battle = False
    st.session_state.logs = []

# --- UI: HAUPTMENÜ ---
st.title("🔥 Pokémon Feuerrot: Streamlit-Edition")

if not st.session_state.battle:
    st.subheader("Wähle dein Start-Pokémon")
    cols = st.columns(len(POKEMON_DATA))
    
    for i, (name, data) in enumerate(POKEMON_DATA.items()):
        with cols[i]:
            st.image(data["Bild"])
            if st.button(f"Wähle {name}"):
                st.session_state.player_pkmn = data.copy()
                st.session_state.player_pkmn["Name"] = name
                st.session_state.player_hp = data["HP"]
                
                enemy_name = random.choice(list(POKEMON_DATA.keys()))
                st.session_state.enemy_pkmn = POKEMON_DATA[enemy_name].copy()
                st.session_state.enemy_pkmn["Name"] = enemy_name
                st.session_state.enemy_hp = st.session_state.enemy_pkmn["HP"]
                
                st.session_state.battle = True
                st.session_state.logs = [f"Ein wildes {enemy_name} erscheint!"]
                st.rerun()

# --- UI: KAMPFMODUS ---
else:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"<div class='pokemon-card'><h3>Dein {st.session_state.player_pkmn['Name']}</h3>", unsafe_allow_html=True)
        st.image(st.session_state.player_pkmn["Bild"], width=150)
        st.progress(max(0.0, float(st.session_state.player_hp / st.session_state.player_pkmn["HP"])))
        st.write(f"HP: {st.session_state.player_hp} / {st.session_state.player_pkmn['HP']}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div class='pokemon-card'><h3>Gegner: {st.session_state.enemy_pkmn['Name']}</h3>", unsafe_allow_html=True)
        st.image(st.session_state.enemy_pkmn["Bild"], width=150)
        st.progress(max(0.0, float(st.session_state.enemy_hp / st.session_state.enemy_pkmn["HP"])))
        st.write(f"HP: {st.session_state.enemy_hp} / {st.session_state.enemy_pkmn['HP']}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    if st.session_state.player_hp > 0 and st.session_state.enemy_hp > 0:
        c1, c2 = st.columns(2)
        if c1.button("💥 Angriff"):
            # Spieler greift an
            dmg, mult = calculate_damage(st.session_state.player_pkmn, st.session_state.enemy_pkmn)
            st.session_state.enemy_hp -= dmg
            msg = f"{st.session_state.player_pkmn['Name']} verursacht {dmg} Schaden!"
            if mult > 1: msg += " (Sehr effektiv! ✨)"
            if mult < 1: msg += " (Nicht sehr effektiv... 💧)"
            st.session_state.logs.append(msg)
            
            # Gegner greift an
            if st.session_state.enemy_hp > 0:
                e_dmg, e_mult = calculate_damage(st.session_state.enemy_pkmn, st.session_state.player_pkmn)
                st.session_state.player_hp -= e_dmg
                e_msg = f"{st.session_state.enemy_pkmn['Name']} schlägt zurück mit {e_dmg} Schaden!"
                if e_mult > 1: e_msg += " (Sehr effektiv! ⚡)"
                st.session_state.logs.append(e_msg)
            st.rerun()
            
        if c2.button("🏃 Flucht"):
            st.session_state.battle = False
            st.rerun()

    else:
        if st.session_state.enemy_hp <= 0:
            st.success(f"Sieg! {st.session_state.enemy_pkmn['Name']} wurde besiegt!")
        else:
            st.error("Dein Pokémon ist besiegt...")
            
        if st.button("Zurück zum Menü"):
            st.session_state.battle = False
            st.rerun()

    with st.expander("Kampf-Logbuch", expanded=True):
        for log in reversed(st.session_state.logs):
            st.write(log)
