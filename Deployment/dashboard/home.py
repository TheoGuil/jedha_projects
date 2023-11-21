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
  st.text("Type de checkins")
  st.pyplot(display_pie_chart(data.checkin_type))
  
with col2:
  st.text("Proportion de retards au checkout")
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
  
# Checkout delay analysis
preprocessed_data = load_preprocess_data(data)
st.header("Analyse des retards")
st.markdown('*$$^{(1)}$$ seules les locations suivant une précédente location ont été conservées*')

col1, col2, col3 = st.columns(3)

with col1:
  st.text("Retards se répercutant sur le prochain checkin")
  st.pyplot(display_pie_chart(preprocessed_data.late_for_next_checkin))
  
with col2:
  st.text("Retards au checkin causés par le retard au checkout de la précédente location")
  fig = px.histogram(
      preprocessed_data.sort_values(['delta_checkout_next_checkin']), 
      x="delta_checkout_next_checkin", 
      nbins=7,
      color="checkin_type"
  )
  fig.update_xaxes(title=None)
  fig.update_yaxes(title=None)
  st.plotly_chart(fig, use_container_width=True)
  
with col3:
  with st.form("prevision"):
      THRESHOLD = st.slider(
                'Seuil (en minutes) ?', 
                min_value=0, max_value=60*24, 
                value=15, step=5,
                help="Seuil à partir du quel une prochaine location peut être réserver")
              
      SCOPE = st.selectbox('Pour quel type de checkin ?',
                           ("mobile", "connect", "tous"))
      
      submit = st.form_submit_button("Confirmer")
      
      if (submit):
        preprocessed_data["is_removed_by_new_rules"] = (preprocessed_data["time_delta_in_minutes"] < THRESHOLD) & (preprocessed_data["checkin_type"] == SCOPE)
        nb_rent_removed = preprocessed_data.loc[preprocessed_data["is_removed_by_new_rules"]].count().iloc[0]
        percent_rent_removed = (preprocessed_data.loc[preprocessed_data["is_removed_by_new_rules"]].count().iloc[0] / preprocessed_data.count() * 100).iloc[0] + ' %'
        
        st.metric("Nb de location retiré", nb_rent_removed, percent_rent_removed, "off")
  