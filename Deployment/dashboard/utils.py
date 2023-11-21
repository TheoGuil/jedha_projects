import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

# %% Utils functions
def get_delay_state(minutes):
    if (minutes < 0):
        return "En avance"
    elif (minutes > 0 ):
        return "En retard"
    else:
        return "A l'heure"
    
def late_category(x):
    if (x > 60*24):
        return "> 1 jour"
    elif (x > 60*2):
        return "> 2 heures"
    elif (x > 60):
        return "entre 1h & 2h"
    elif (x > 30):
        return "entre 30min & 1h"
    elif (x > 15):
        return "entre 15min & 30min"
    elif (x > 0):
        return "< 15min"
    else:
        return "A l'heure"

late_category_ordered = ["A l'heure", "< 15min", "entre 15min & 30min", "entre 30min & 1h",
                               "entre 1h & 2h", "> 2 heures", "> 1 jour"]
    
def display_pie_chart(series):
    fig, ax = plt.subplots()
    ax.pie(series.value_counts(), 
            labels=series.value_counts().index,
            autopct=lambda p:f'{p:.2f}%\n({p*sum(series.value_counts())/100 :.0f})')
    plt.figlegend(series.value_counts().index)
    return fig

# %% Data Preprocessing
URL_DELAY = "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx"

@st.cache_data(show_spinner="Chargement des données")
def load_data():
  df = pd.read_excel(URL_DELAY, sheet_name='rentals_data', engine="openpyxl")
  df = df.loc[df["state"] == "ended", :]
  df["delay_state"] = df["delay_at_checkout_in_minutes"].apply(get_delay_state)
  df["late_category"] = df.delay_at_checkout_in_minutes.apply(late_category)
  df["late_category"] = pd.Categorical(df["late_category"], ordered=True,
                   categories=late_category_ordered)
  return df


@st.cache_data(show_spinner="Chargement des données")
def load_preprocess_data(df):
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
  df["late_for_next_checkin"] = df["delta_checkout_next_checkin"].apply(lambda x: "Impacté" if x > 0 else "Non-impacté")
  df["delta_checkout_next_checkin"] = df["delta_checkout_next_checkin"].apply(late_category)
  df["delta_checkout_next_checkin"] = pd.Categorical(df["delta_checkout_next_checkin"], ordered=True,
                   categories=late_category_ordered)
  return df