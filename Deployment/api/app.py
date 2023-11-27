from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from typing import List
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
PREPROCESSOR = joblib.load("ML_models/preprocessor.pkl")

# Home route redirect to documentation
@app.get("/", include_in_schema=False)
def home() -> str:
    return RedirectResponse(url="/documentation", status_code=status.HTTP_302_FOUND)

# Predict route
@app.post("/predict")
def predict(cars: List[Car]) -> List[CarResponse] :
    '''Prédit le prix par jour d'une location en fonction 
    des caractéristiques d'une voiture.'''

    # Create a dataframe from the car object
    df = pd.DataFrame([x.__dict__ for x in cars])
    
    # Preprocess the dataframe
    data = PREPROCESSOR.transform(df)
    
    # Predict the price
    df["prediction_price"] = ML_MODEL.predict(data)
    
    return df.to_dict(orient="records")

# Si le script est exécuté directement (et non importé), lance le serveur
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)