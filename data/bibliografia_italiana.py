import streamlit as st
import pandas as pd



def carica_dati():
    df = pd.read_excel("Library of Middle Earth.xlsx", sheet_name = "Bibliografia Tolkien Italia")
    # Rimuovi spazi accidentali nei nomi colonne
    df.columns = df.columns.str.strip()
    return df