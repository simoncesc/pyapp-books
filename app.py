import streamlit as st
import pandas as pd

# Config
st.set_page_config(page_title="Libreria Interattiva", layout="wide")
PLACEHOLDER = "https://via.placeholder.com/200x300?text=Nessuna+Immagine"

# Carica dati da Excel (cache per performance)
@st.cache_data
def carica_dati():
    df = pd.read_excel("Library of Middle Earth.xlsx", sheet_name = "Bibliografia Tolkien Italia")
    # Rimuovi spazi accidentali nei nomi colonne
    df.columns = df.columns.str.strip()
    return df

df = carica_dati()

# Controllo colonne minime richieste
required_cols = ["Titolo", "Autore", "Casa Editrice", "Rilegatura", "Prima Edizione", "Lingua", "Copertina"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Mancano colonne richieste nel file Excel: {missing}. Colonne trovate: {list(df.columns)}")
    st.stop()

# Inizializza la lista custom nella sessione
if "lista_custom" not in st.session_state:
    st.session_state.lista_custom = []

# Sidebar - navigazione
pagina = st.sidebar.radio("📚 Naviga tra le pagine", ["Home", "Bibliografia Italiana"])

# -----------------------------
# HOME
# -----------------------------
if pagina == "Home":
    st.title("📚 Tolkien Books Italia")

    st.subheader("Scegli i libri che possiedi")
    libro_scelto = st.selectbox("Seleziona un libro:", df["Titolo"].dropna().unique())

    if st.button("➕ Aggiungi alla mia lista"):
        if libro_scelto not in st.session_state.lista_custom:
            st.session_state.lista_custom.append(libro_scelto)
            st.success(f"'{libro_scelto}' aggiunto alla tua lista!")
        else:
            st.warning(f"'{libro_scelto}' è già nella tua lista.")

    st.subheader("📖 La mia lista personalizzata")
    if st.session_state.lista_custom:
        for i, titolo in enumerate(st.session_state.lista_custom):
            col1, col2 = st.columns([4, 1])
            col1.write(titolo)
            if col2.button("❌ Rimuovi", key=f"rm_{i}"):
                st.session_state.lista_custom.remove(titolo)
                st.experimental_rerun()
    else:
        st.info("Non hai ancora aggiunto nessun libro.")

    with st.expander("📊 Visualizza catalogo completo"):
        st.dataframe(df)

# -----------------------------
# CATALOGO LIBRI
# -----------------------------
elif pagina == "Bibliografia Italiana":
    st.title("📘 Catalogo dei Libri")

    # Filtri (gestire eventuali NaN)
    autori = ["Tutti"] + sorted(df["Autore"].dropna().unique().tolist())
    case_editrici = ["Tutti"] + sorted(df["Casa Editrice"].dropna().unique().tolist())

    autore = st.selectbox("Filtra per autore:", autori)
    case_editrici = st.selectbox("Filtra per casa editrice:", case_editrici)

    libri_filtrati = df.copy()
    if autore != "Tutti":
        libri_filtrati = libri_filtrati[libri_filtrati["Autore"] == autore]
    if case_editrici != "Tutti":
        libri_filtrati = libri_filtrati[libri_filtrati["Casa Editrice"] == case_editrici]

    # Mostra in griglia
    num_colonne = 3
    rows = libri_filtrati.reset_index(drop=True)

    for start in range(0, len(rows), num_colonne):
        chunk = rows.iloc[start:start + num_colonne]
        cols = st.columns(num_colonne)
        for col_idx in range(num_colonne):
            if col_idx < len(chunk):
                row = chunk.iloc[col_idx]
                with cols[col_idx]:
                    # Dati del libro
                    titolo = row["Titolo"]
                    autore_row = row["Autore"]
                    anno = int(row["Prima Edizione"]) if not pd.isna(row["Prima Edizione"]) else "N/D"
                    img_url = row["Copertina"] if pd.notna(row["Copertina"]) else "https://via.placeholder.com/200x300?text=Nessuna+Immagine"

                    # HTML del box
                    box_html = f"""
                    <div style="
                        background-color: #2E2E2E;
                        border-radius: 15px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        padding: 15px;
                        text-align: center;
                        margin-bottom: 20px;
                    ">
                        <img src="{img_url}" style="width:180px; height:270px; object-fit:cover; border-radius:10px; margin-bottom:10px;" />
                        <h4 style="margin-bottom:4px;">{titolo}</h4>
                        <p style="color: #555; margin:0;">👤 {autore_row}</p>
                        <p style="color: #777; font-size: 0.9em;">📅 {anno}</p>
                    </div>
                    """

                    st.markdown(box_html, unsafe_allow_html=True)

                    # Pulsante per aggiungere alla lista
                    key_add = f"add_{start}_{col_idx}"
                    if titolo not in st.session_state.lista_custom:
                        if st.button("➕ Aggiungi", key=key_add):
                            st.session_state.lista_custom.append(titolo)
                            st.success("Aggiunto alla tua lista!")
                            st.experimental_rerun()
                    else:
                        st.button("✅ Già nella lista", key=f"added_{key_add}", disabled=True)





