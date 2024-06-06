import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from azure_blob_reader import load_data_from_azure

data = load_data_from_azure()

cancellation_percentages_df = data["cancellation_percentages_df"]
agencia_distribution = data["agencia_distribution"]
canal_distribution = data["canal_distribution"]
median_values = data["median_values"]
mean_values = data["mean_values"]

variable_labels = {
    "h_num_per": "Número de personas",
    "h_num_adu": "Número de adultos",
    "h_num_men": "Número de menores",
    "h_num_noc": "Número de noches",
    "h_tot_hab": "Total de habitaciones",
    "h_tfa_total": "Tarifa total",
    "lead_time": "Tiempo de anticipación (en días)",
    "rate_per_night": "Tarifa por noche",
}

cluster_order = ["Lujo", "Escapada", "Familias", "Grupos"]

fig_cancellations = px.bar(
    cancellation_percentages_df,
    x="cluster_name",
    y="percentage",
    title="Porcentaje de Cancelaciones por Clúster",
    labels={"percentage": "Porcentaje de Cancelaciones", "cluster_name": "Clúster"},
    category_orders={"cluster_name": cluster_order},
)

fig_agencia = px.treemap(
    agencia_distribution,
    path=["cluster_name", "Agencia_nombre"],
    values="percentage",
    title="Distribución de Agencia por Clúster",
)

fig_canal = px.treemap(
    canal_distribution,
    path=["cluster_name", "Canal_nombre"],
    values="percentage",
    title="Distribución de Canal por Clúster",
)

num_cols = [
    "h_num_per",
    "h_num_adu",
    "h_num_men",
    "h_num_noc",
    "h_tot_hab",
    "h_tfa_total",
    "lead_time",
    "rate_per_night",
]

figs_values = {}

for col in num_cols:
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=median_values["cluster_name"],
            y=median_values[col],
            name="Mediana",
            marker_color="blue",
        )
    )
    fig.add_trace(
        go.Bar(
            x=mean_values["cluster_name"],
            y=mean_values[col],
            name="Media",
            marker_color="orange",
        )
    )
    fig.update_layout(
        title=f"Valores Medios y Medianos de {variable_labels[col]} por Clúster",
        xaxis_title="Clúster",
        yaxis_title="Valor",
        barmode="group",
        xaxis={"categoryorder": "array", "categoryarray": cluster_order},
    )
    figs_values[col] = fig

st.set_page_config(page_title="Análisis de Reservaciones de Hotel")

st.title("Dashboard de Análisis de Reservaciones de Hotel")

st.subheader("Porcentaje de Cancelaciones por Clúster")
st.plotly_chart(fig_cancellations)

st.plotly_chart(fig_agencia)
st.plotly_chart(fig_canal)

st.subheader("Valores Medios y Medianos de Columnas Numéricas por Clúster")
for col, fig in figs_values.items():
    st.plotly_chart(fig)
