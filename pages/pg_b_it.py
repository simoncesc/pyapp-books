import streamlit as st
import pandas as pd

import data.bibliografia_italiana as bi



# Carica dati da Excel (cache per performance)

def mostra_bi_it(df):

    #hero

    h_col1, h_col2 = st.columns([1, 2])  # rapporto 1:2 tra immagine e testo

    with h_col1:
        st.image("images/copertina_bg_it.jpg", use_container_width=True)

    with h_col2:
        st.markdown("""
        <div style='padding: 40px;'>
            <h1 style='margin-bottom: 0;'>📚 Bibliografia Italiana</h1>
            <h3 style='margin-top: 5px;'>Scopri, aggiungi, colleziona</h3>
            <p>
                Benvenuto nella sezione dedicata alle opere italiane.  
                Sfoglia i titoli, consulta le copertine e costruisci la tua collezione personale.
            </p>
        </div>
    """, unsafe_allow_html=True)
        
    #filtri
    
    #aggiungo il filtro cerca
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)

    with f_col1:
        query = st.text_input(label = 'Cerca:', icon = '🔎',width = 200)

    if query:
        df_filtrato = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    else:
        df_filtrato = df

    # Filtri (gestire eventuali NaN)
    titoli = ["Tutti"] + sorted(df["Titolo"].dropna().unique().tolist())
    case_editrici = ["Tutti"] + sorted(df["Casa Editrice"].dropna().unique().tolist())
    anni = ["Tutti"] + sorted(df["Prima Edizione"].dropna().unique().tolist())
    with f_col2:
        titolo = st.selectbox("Filtra per Titolo:", titoli)
    with f_col3:
        casa_editrice = st.selectbox("Filtra per casa editrice:", case_editrici)
    with f_col4:
        anno = st.selectbox("Filtra per Anno pubblicazione:", anni)
    libri_filtrati = df_filtrato.copy()
    if titolo != "Tutti":
        libri_filtrati = libri_filtrati[libri_filtrati["Titolo"] == titolo]
    if casa_editrice != "Tutti":
        libri_filtrati = libri_filtrati[libri_filtrati["Casa Editrice"] == casa_editrice]
    if anno != "Tutti":
        libri_filtrati = libri_filtrati[libri_filtrati["Prima Edizione"] == anno]
    # Mostra in griglia
    num_colonne = 4
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
                    casa_editrice_row = row["Casa Editrice"]
                    rilegatura = row["Rilegatura"]
                    anno = int(row["Prima Edizione"]) if not pd.isna(row["Prima Edizione"]) else "N/D"
                    img_url = row["Copertina"] if pd.notna(row["Copertina"]) else "https://via.placeholder.com/200x300?text=Nessuna+Immagine"
                    # HTML del box
                    box_html = f"""
                   <div style="
                        background-color: #2E2E2E;
                        border-radius: 15px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        padding: 15px;
                         margin-bottom: 20px;
                        width: auto;
                    ">
                        <img src="{img_url}" style="width:180px; height:270px; object-fit:cover; border-radius:10px; margin-bottom:10px;display:block; margin-left:auto; margin-right:auto;" />
                        <p style="text-align:left; margin:0; color:#6BC282; text-transform: uppercase;">{rilegatura}</p>
                        <h5 style="text-align:left; margin:5px 0;">{titolo}</h5>
                        <div style="display:flex; justify-content:space-between; color:#BDBDBD; margin-top:5px;">
                            <p style="margin:0">{casa_editrice_row}</p>
                            <p style="margin:0">{anno}</p>
                        </div>
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
