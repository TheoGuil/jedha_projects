from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import starlette.status as status
import uvicorn

# Création de l'application FastAPI
app = FastAPI(
    title="Price Optimisation API",
    description="",
    version="1.0.0",
    openapi_tags=[],
    docs_url=None, redoc_url="/documentation"
)

# Route pour prévisualiser les données
@app.get("/", include_in_schema=False)
def home() -> str:
    return RedirectResponse(url="/documentation", status_code=status.HTTP_302_FOUND)

# Si le script est exécuté directement (et non importé), lance le serveur
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)