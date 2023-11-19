import streamlit as st
import pandas as pd
from utils import *

st.set_page_config(
  page_title="Analyses des retards de checkouts",
  page_icon="🚗",
  layout="wide"
)

st.image("https://fr.getaround.com/packs/images/shared/getaround-logo-8ceb724cd27ec56904d95ba679f8d866.svg")
st.title("Analyses des retards de checkouts")


URL_DELAY = "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx"

@st.cache_data(show_spinner="Chargement des données")
def load_data():
  df = pd.read_excel(URL_DELAY, sheet_name='rentals_data', engine="openpyxl")
  df = df.loc[df["state"] == "ended", :]
  df["delay_state"] = df["delay_at_checkout_in_minutes"].apply(get_delay_state)
  df["late_category"] = df.delay_at_checkout_in_minutes.apply(late_category)
  df["late_category"] = pd.Categorical(df["late_category"], ordered=True,
                   categories=late_category_ordered)
  df = pd.merge(left=df, right=df, how="left", 
                     left_on="previous_ended_rental_id", right_on="rental_id", suffixes=('', '_previous'))

  df = df.drop(["car_id", "state", "delay_at_checkout_in_minutes", "rental_id_previous", "car_id_previous", 
                "previous_ended_rental_id_previous", "time_delta_with_previous_rental_in_minutes_previous", 
                "state_previous"], axis=1)

  df = df.rename({
      "time_delta_with_previous_rental_in_minutes": "time_delta_in_minutes"
      }, axis=1)

  df = df.loc[df.previous_ended_rental_id.isna() == False, :]
  df["delay_at_checkout_in_minutes_previous"] = df["delay_at_checkout_in_minutes_previous"].apply(lambda x: x if x > 0 else 0)
  df["delta_checkout_next_checkin"] = (df["time_delta_in_minutes"] - df["delay_at_checkout_in_minutes_previous"]) * -1
  df["late_for_next_checkin"] = df["delta_checkout_next_checkin"] > 0
  df["delta_checkout_next_checkin"] = df["delta_checkout_next_checkin"].apply(late_category)
  df["delta_checkout_next_checkin"] = pd.Categorical(df["delta_checkout_next_checkin"], ordered=True,
                   categories=late_category_ordered)
  return df

data = load_data()

if st.checkbox('Voir un extrait des données'):
    st.write(data)
