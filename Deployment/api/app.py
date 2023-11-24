from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import starlette.status as status
import joblib
import pandas as pd
import uvicorn

from car import *

description = """
**🔹 Description**

Cette application permet de prédire un prix journalier de location pour une voiture en fonction de ses caractéristiques (modèle, kilométrage, nb de chevaux, type de carburant, couleur de la carroserie, categories, de l'équipement...).

---
**🔹 Information**

Le modèle explique ≃70% de la variation du prix (R² = 0.70 ± 0.04) et a une erreur moyenne de ≃12€ (17%).

![Prédictions vs Réalité](/img/real_vs_predict.png)

![Prédictions vs Résidus standardisés](/img/residus_prediction_graph.png)

---



"""

# Création de l'application FastAPI
app = FastAPI(
    title="Price Optimisation API",
    description=description,
    version="1.0.0",
    openapi_tags=[],
    docs_url=None, redoc_url="/documentation"
)
app.mount("/img", StaticFiles(directory="img"), name="img")

ML_MODEL = joblib.load("ML_models/ridge_cv.pkl")

# Home route redirect to documentation
@app.get("/", include_in_schema=False)
def home() -> str:
    return RedirectResponse(url="/documentation", status_code=status.HTTP_302_FOUND)

# Predict route
@app.post("/predict")
def predict(car: Car):
    '''Predict a price'''
    # Create a dataframe from the car object
    df = pd.DataFrame.from_dict(car, orient="columns").T
    print(df.head())
    return df.head()
    


# Si le script est exécuté directement (et non importé), lance le serveur
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)