import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def create_plot(df_graph, selected_columns):
    # Berechne die Anzahl der Subplots
    subplot_count = len(selected_columns)

    # Erstellen der Subplots
    fig = make_subplots(rows=subplot_count, cols=1, shared_xaxes=True, vertical_spacing=0.05)

    # Hinzufügen der Subplots
    for index, col in enumerate(selected_columns):
        fig.add_trace(go.Scatter(x=df_graph.index[:200], y=df_graph[col][:200], mode='lines', name=col), row=index+1, col=1)

    # Hinzufügen von MOAAS Subplot
    if 'MOAAS' in df_graph.columns:
        fig.add_trace(go.Scatter(x=df_graph.index[:200], y=df_graph['MOAAS'][:200], mode='lines+markers', name='MOAAS'), row=subplot_count, col=1)
    
    fig.update_layout(height=200*subplot_count, showlegend=True)
    
    # Anzeigen des Plots in der Streamlit-Anwendung
    st.plotly_chart(fig,use_container_width=True)

# Streamlit Titel
st.title('Plotly Subplots Beispiel')

# Datei-Upload-Button
uploaded_file = st.file_uploader("CSV-Datei hochladen", type="csv")

if uploaded_file is not None:
    df_graph = pd.read_csv(uploaded_file)

    # Spaltenauswahl
    st.sidebar.title("Spaltenauswahl")
    available_columns = df_graph.columns.tolist()
    selected_columns = st.sidebar.multiselect("Wählen Sie die Spalten aus, die geplottet werden sollen:", available_columns, default=available_columns)

    # Erstellen und anzeigen des Plots
    if len(selected_columns) > 0:
        create_plot(df_graph, selected_columns)
    else:
        st.warning("Bitte wählen Sie mindestens eine Spalte aus.")
else:
    st.warning("Bitte laden Sie eine CSV-Datei hoch.")
