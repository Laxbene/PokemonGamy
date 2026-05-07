import streamlit as st
import random

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
