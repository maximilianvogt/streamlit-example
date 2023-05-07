import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def create_plot(df_graph, selected_columns):
    # Gruppierte Spalten
    grouped_columns = ['I', 'II', 'III']

    # Berechne die Anzahl der Subplots
    subplot_count = len(selected_columns) - len([col for col in grouped_columns if col in selected_columns]) + 1 if any(col in selected_columns for col in grouped_columns) else 0

    # Erstellen der Subplots
    fig = make_subplots(rows=subplot_count, cols=1, shared_xaxes=True, vertical_spacing=0.02)

    row_idx = 1
    for col in selected_columns:
        if col in grouped_columns:
            if any(gr_col in selected_columns for gr_col in grouped_columns):
                fig.add_trace(go.Scatter(x=df_graph.index, y=df_graph[col], mode='lines', name=col), row=row_idx, col=1)
                continue
        else:
            fig.add_trace(go.Scatter(x=df_graph.index, y=df_graph[col], mode='lines', name=col), row=row_idx, col=1)
            row_idx += 1

    if 'V6' in df_graph.columns:
        moaas_x = df_graph.index
        moaas_y = df_graph['V6']

        # Ermitteln der Bereiche, in denen MOAAS kleiner als 3 ist
        moaas_low_areas = [(x, y) for x, y in zip(moaas_x, moaas_y) if y < 0]

        # Zeichnen der gelben Bereiche
        if moaas_low_areas:
            for x, y in moaas_low_areas:
                fig.add_shape(
                    type='rect',
                    xref='x',
                    yref='y2',
                    x0=x - 0.5,
                    x1=x + 0.5,
                    y0=0,
                    y1=max(moaas_y),
                    fillcolor='yellow',
                    opacity=0.5,
                    layer='below',
                    line_width=0
                )

        # Zeichnen der MOAAS-Werte
        fig.add_trace(go.Scatter(x=moaas_x, y=moaas_y, mode='lines+markers', name='V6', yaxis='y2'), row=subplot_count, col=1)

    # Aktualisieren der Größe und Darstellung des Plots
    fig.update_layout(height=150*subplot_count, showlegend=True)

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
