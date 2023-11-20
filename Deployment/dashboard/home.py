import streamlit as st
import plotly.express as px
from utils import *

st.set_page_config(
  page_title="Analyses des retards de checkouts",
  page_icon="🚗",
  layout="wide"
)

# Title
st.image("https://fr.getaround.com/packs/images/shared/getaround-logo-8ceb724cd27ec56904d95ba679f8d866.svg")
st.title("Analyses des retards de checkouts")

# Load global data
data = load_data()

# Raw data
if st.checkbox('Voir un extrait des données'):
    st.write(data)


# Global analysis

st.header("Analyse globale")
col1, col2, col3 = st.columns(3)

with col1:
  st.text("Type de checkin")
  st.pyplot(display_pie_chart(data.checkin_type))
  
with col2:
  st.text("Proportion de retard au checkout")
  st.pyplot(display_pie_chart(data.delay_state))
  
with col3:
  st.text("Distribution des retards")
  fig = px.histogram(
      data.sort_values(['late_category']), 
      x="late_category", 
      nbins=7,
      color="checkin_type"
  )
  fig.update_xaxes(title=None)
  fig.update_yaxes(title=None)
  st.plotly_chart(fig, use_container_width=True)