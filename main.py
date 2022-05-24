from importlib import reload
from fastapi import FastAPI
from config import engine
import uvicorn
import model
import router
from routes.v2 import router_maestras
from routes.v2 import router_transacciones
from routes.v2 import router_images

# generate model to table postgresql
db_init = model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    docs_url="/documentacion", redoc_url='/doc',
    title='API Integracion WMS', 
    version='1.0.0', 
    description='Api para integrar el sistema de WMS con los diferentes ERPs 🚀',
    terms_of_service='/',
    contact={
        'name': 'Bex Soluciones', 
        'url': 'https://bexsoluciones.com/', 
        'email': 'simon.trillos@bexsoluciones.com'})

@app.get('/')
async def Home():
    return "Welcome Home"

app.include_router(router.router)
app.include_router(router_maestras.router)
app.include_router(router_transacciones.router, prefix="/version1")
app.include_router(router_images.router)


"""
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
"""