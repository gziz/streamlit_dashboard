import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pickle

def open_model():
    with open('models/gmm_model.pkl', 'rb') as f:
            return pickle.load(f)

class LoyaltyAnalysis:
    def __init__(self, data_path):
        self.data_path = data_path
        self.model = open_model()
        self.cluster_order = ['Clúster 1', 'Clúster 2', 'Clúster 3', 'Clúster 4']

        self.load_data()
        self.create_figures()

    def load_data(self):
        X = np.load(self.data_path + 'X_loyalty_preprocessed.npy')
        self.X_clustered_optimal = self.model.fit_predict(X)
        self.df_loyalty = pd.read_csv(self.data_path + 'df_loyalty.csv')
        self.df_loyalty['cluster'] = self.X_clustered_optimal

    def create_figures(self):
        """
        from the prediction get the the percentage of loyalty and generate chart
        """
        total_reservations_counts = self.df_loyalty.groupby('cluster')['loyalty'].count() 
        non_loyal_counts = self.df_loyalty[self.df_loyalty['loyalty'] == 1].groupby('cluster')['loyalty'].count()
        loyal_percentages = (1 - (non_loyal_counts / total_reservations_counts)) * 100
        loyal_percentages_df = loyal_percentages.reset_index(name='percentage')

        self.fig_loyalty = px.bar(
            loyal_percentages_df, 
            x='cluster', 
            y='percentage',
            title='Porcentaje de Lealtad por Clúster',
            labels={'percentage': 'Porcentaje de Lealtad', 'cluster_name': 'Clúster'},
            category_orders={'cluster_name': self.cluster_order}
        )

    def render_dashboard_loyalty(self):
        """
        Display chart and get the variables mean per cluster
        """

        st.subheader("Porcentaje de Lealtad por Clúster")
        st.plotly_chart(self.fig_loyalty)
        
        st.subheader('Agrupación por media, variables numéricas:')
        st.text(self.df_loyalty[[
            'cluster', 'loyalty', 'h_num_per', 'h_num_adu', 'h_num_men', 'h_num_noc',
            'h_tot_hab', 'por_noche', 'h_tfa_total', 'lead_time'
            ]].groupby('cluster').apply(lambda x: x.mean()))

        st.subheader('Agrupación por moda, varaibles categóricas:')
        st.text(self.df_loyalty[[
            'cluster', 'loyalty', 'ID_canal', 'ID_Agencia', 'h_fec_reg_day', 'h_fec_reg_month',
            'h_fec_lld_day', 'h_fec_lld_month', 'is_canceled'
            ]].groupby('cluster').apply(lambda x: x.mode()))


