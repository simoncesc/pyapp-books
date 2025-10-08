import streamlit as st
from data.bibliografia_inglese import carica_dati as bi_en
from data.bibliografia_italiana import carica_dati as bi_it

from pages.pg_b_it import mostra_bi_it as bi_pg_mostra



# Config
st.set_page_config(page_title="Libreria Interattiva", layout="wide")
PLACEHOLDER = "https://via.placeholder.com/200x300?text=Nessuna+Immagine"

df_it = bi_it()
df_en = bi_en()

# Sidebar - navigazione

if "lista_custom" not in st.session_state:
    st.session_state.lista_custom = []

pagina = st.sidebar.radio("📚 Naviga tra le pagine", ["Home", "Bibliografia Italiana"])

# -----------------------------
# HOME
# -----------------------------
if pagina == "Home":
    st.title("📚 Tolkien Books Italia")

    st.subheader("Scegli i libri che possiedi")
    libro_scelto = st.selectbox("Seleziona un libro:", df_it["Titolo"].dropna().unique())

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
        st.dataframe(df_it)

# -----------------------------
# CATALOGO LIBRI
# -----------------------------
elif pagina == "Bibliografia Italiana":
    bi_pg_mostra(df_it)
