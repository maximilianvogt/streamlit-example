
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Erstellen eines Beispieldatenframes
data = {
    'EEG3': [1, 2, 3, 4, 5, 6, 7, 8],
    'EEG4': [2, 3, 4, 5, 6, 7, 8, 9],
    'ECG': [3, 4, 5, 6, 7, 8, 9, 10],
    'MOAAS': [1, 2, 3, 4, 5, 6, 7, 8]
}

df_graph = pd.DataFrame(data)

# Streamlit Titel
st.title('Plotly Subplots Beispiel')

# Berechne die Anzahl der Subplots
subplot_count = len(df_graph.columns[:-1])

# Erstellen der Subplots
fig = make_subplots(rows=subplot_count, cols=1, shared_xaxes=True, vertical_spacing=0.05)

# Hinzufügen der Subplots
for index, col in enumerate(df_graph.columns[:-1]):
    fig.add_trace(go.Scatter(x=df_graph.index[:200], y=df_graph[col][:200], mode='lines', name=col), row=index+1, col=1)

# Hinzufügen von MOAAS Subplot
fig.add_trace(go.Scatter(x=df_graph.index[:200], y=df_graph['MOAAS'][:200], mode='lines+markers', name='MOAAS'), row=subplot_count, col=1)

# Anzeigen des Plots in der Streamlit-Anwendung
st.plotly_chart(fig,use_container_width=True)
