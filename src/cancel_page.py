import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class CancelAnalysis:
    def __init__(self, data_path):
        self.data_path = data_path
        self.variable_labels = {
            'h_num_per': 'Número de personas',
            'h_num_adu': 'Número de adultos',
            'h_num_men': 'Número de menores',
            'h_num_noc': 'Número de noches',
            'h_tot_hab': 'Total de habitaciones',
            'h_tfa_total': 'Tarifa total',
            'lead_time': 'Tiempo de anticipación (en días)',
            'rate_per_night': 'Tarifa por noche'
        }
        self.cluster_order = ['Lujo', 'Escapada', 'Familias', 'Grupos']
        self.num_cols = ['h_num_per', 'h_num_adu', 'h_num_men', 'h_num_noc', 'h_tot_hab', 'h_tfa_total', 'lead_time', 'rate_per_night']
        
        self.load_data()
        self.create_figures()

    def load_data(self):
        self.cancellation_percentages_df = pd.read_csv(self.data_path + "cancellation_percentages.csv")
        self.agencia_distribution = pd.read_csv(self.data_path + "agencia_distribution.csv")
        self.canal_distribution = pd.read_csv(self.data_path + "canal_distribution.csv")
        self.median_values = pd.read_csv(self.data_path + "median_values.csv")
        self.mean_values = pd.read_csv(self.data_path + "mean_values.csv")

    def create_figures(self):
        self.fig_cancellations = px.bar(
            self.cancellation_percentages_df, 
            x='cluster_name', 
            y='percentage',
            title='Porcentaje de Cancelaciones por Clúster',
            labels={'percentage': 'Porcentaje de Cancelaciones', 'cluster_name': 'Clúster'},
            category_orders={'cluster_name': self.cluster_order}
        )

        self.fig_agencia = px.treemap(
            self.agencia_distribution, 
            path=['cluster_name', 'Agencia_nombre'],
            values='percentage',
            title='Distribución de Agencia por Clúster'
        )

        self.fig_canal = px.treemap(
            self.canal_distribution, 
            path=['cluster_name', 'Canal_nombre'],
            values='percentage',
            title='Distribución de Canal por Clúster'
        )

        self.figs_values = {}
        for col in self.num_cols:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=self.median_values['cluster_name'], 
                y=self.median_values[col], 
                name='Mediana', 
                marker_color='blue'
            ))
            fig.add_trace(go.Bar(
                x=self.mean_values['cluster_name'], 
                y=self.mean_values[col], 
                name='Media', 
                marker_color='orange'
            ))
            fig.update_layout(
                title=f'Valores Medios y Medianos de {self.variable_labels[col]} por Clúster',
                xaxis_title='Clúster',
                yaxis_title='Valor',
                barmode='group',
                xaxis={'categoryorder':'array', 'categoryarray': self.cluster_order}
            )
            self.figs_values[col] = fig

    def render_dashboard_canceled(self):
        st.subheader("Porcentaje de Cancelaciones por Clúster")
        st.plotly_chart(self.fig_cancellations)

        st.plotly_chart(self.fig_agencia)
        st.plotly_chart(self.fig_canal)

        st.subheader("Valores Medios y Medianos de Columnas Numéricas por Clúster")
        for col, fig in self.figs_values.items():
            st.plotly_chart(fig)
