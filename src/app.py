import logging
import streamlit as st
from cancel_page import CancelAnalysis
from loyalty_page import LoyaltyAnalysis
import os

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)

#main class for grouping all classes into one and using same attributes
class Main(CancelAnalysis, LoyaltyAnalysis):
    def __init__(self, data_path):
        # Call constructor of canceled
        try:
            CancelAnalysis.__init__(self, data_path)
            LoyaltyAnalysis.__init__(self, data_path)  
        
        # Call constructor of loyalty
        #loyalty.__init__(self, model)    
        except Exception as e:
            logging.error("Error initializing Main", exc_info=True)
            raise

    def display_app(self):
        option = st.sidebar.selectbox("Tipo de cluster", ("Home", "Lealtad", "Cancelaciones"))
        return option


if __name__ == "__main__":
    try:
        st.set_page_config(page_title='Análisis de Reservaciones de Hotel')

        MainObj = Main(data_path="data/")   
        page = MainObj.display_app()

        if page == "Cancelaciones":
            MainObj.render_dashboard_canceled()
        elif page == 'Lealtad':
            MainObj.render_dashboard_loyalty()
        else:
            st.title("Dashboard de Análisis de Reservaciones de Hotel")

    except Exception as e:
        logging.error("Failed to run main script", exc_info=True)

