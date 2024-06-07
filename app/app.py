import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from azure_blob_reader import load_data_from_azure
import pandas as pd
import numpy as np
import pickle


def dashboard_canceled():
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

    cluster_order = ['Clúster 1', 'Clúster 2', 'Clúster 3', 'Clúster 4']

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
            title=f"{variable_labels[col]} ",
            xaxis_title="Clúster",
            yaxis_title="Valor",
            barmode="group",
            xaxis={"categoryorder": "array", "categoryarray": cluster_order},
        )
        figs_values[col] = fig

    st.title("Análisis de Reservaciones (Cancelaciones)")

    st.plotly_chart(fig_cancellations)

    st.plotly_chart(fig_agencia)
    st.plotly_chart(fig_canal)

    st.subheader("Media y Mediana de Columnas Numéricas por Clúster")
    for col, fig in figs_values.items():
        st.plotly_chart(fig)


def dashboard_loyalty(model):
    st.title("Análisis de Reservaciones (Loyalty)")
    data_path = 'data/'
    cluster_order = ['Clúster 1', 'Clúster 2', 'Clúster 3', 'Clúster 4']

    X = np.load(data_path + 'X_loyalty_preprocessed.npy')
    X_clustered_optimal = model.fit_predict(X)
    df_loyalty = pd.read_csv(data_path + 'df_loyalty.csv')
    df_loyalty['cluster'] = X_clustered_optimal
    

    total_reservations_counts = df_loyalty.groupby('cluster')['loyalty'].count() 
    non_loyal_counts = df_loyalty[df_loyalty['loyalty'] == 1].groupby('cluster')['loyalty'].count()
    loyal_percentages = (1 - (non_loyal_counts / total_reservations_counts)) * 100
    loyal_percentages_df = loyal_percentages.reset_index(name='percentage')
    

    fig_loyalty = px.bar(
            loyal_percentages_df, 
            x='cluster', 
            y='percentage',
            title='Porcentaje de Lealtad por Clúster',
            labels={'percentage': 'Porcentaje de Lealtad', 'cluster_name': 'Clúster'},
            category_orders={'cluster': cluster_order}
        )
    
    st.subheader("Porcentaje de Lealtad por Clúster")
    st.plotly_chart(fig_loyalty)
    

    st.subheader('Agrupación por media, variables numéricas:')
    df_loyalty_mean = df_loyalty[[
            'cluster','loyalty', 'h_num_per', 'h_num_adu', 'h_num_men', 'h_num_noc',
            'h_tot_hab', 'por_noche', 'h_tfa_total', 'lead_time'
            ]].groupby('cluster').apply(lambda x: x.mean())
    
    fig_per = px.bar(
            df_loyalty_mean, 
            x='cluster', 
            y='h_num_per',
            title='Media de personas',
            labels={'mean': 'Media de personas', 'cluster_name': 'Clúster'},
            category_orders={'cluster': cluster_order}
        )
    st.plotly_chart(fig_per)

    fig_noc = px.bar(
            df_loyalty_mean, 
            x='cluster', 
            y='h_num_noc',
            title='Media de número de noches',
            labels={'mean': 'Media de número de noches', 'cluster_name': 'Clúster'},
            category_orders={'cluster': cluster_order}
        )
    st.plotly_chart(fig_noc)

    fig_tfa = px.bar(
            df_loyalty_mean, 
            x='cluster', 
            y='h_tfa_total',
            title='Media de tarifa total',
            labels={'mean': 'Media de tarifa total', 'cluster_name': 'Clúster'},
            category_orders={'cluster': cluster_order}
        )
    st.plotly_chart(fig_tfa)

    
    st.subheader('Agrupación por moda, variables categóricas:')
    df_loyalty_mode = df_loyalty[[
            'cluster', 'loyalty', 'ID_canal', 'ID_Agencia', 'h_fec_reg_day', 'h_fec_reg_month',
            'h_fec_lld_day', 'h_fec_lld_month', 'is_canceled'
            ]].groupby('cluster').apply(lambda x: x.mode())

    fig_tfa = px.bar(
            df_loyalty_mode, 
            x='cluster', 
            y='h_fec_lld_month',
            title='Moda de mes de llegada',
            labels={'mean': 'Moda de mes de llegada', 'cluster_name': 'Clúster'},
            category_orders={'cluster': cluster_order}
        )
    st.plotly_chart(fig_tfa)
    

if __name__ == "__main__":
    with open('models/gmm_model.pkl', 'rb') as f:
        gmm_loyalty = pickle.load(f)

    page = st.sidebar.selectbox("Tipo de cluster", ("Cancelaciones", "Lealtad"))
    
    if page == "Cancelaciones":
        dashboard_canceled()
    elif page == 'Lealtad':
        dashboard_loyalty(gmm_loyalty)
    else:
        st.title("Análisis de Reservaciones")
