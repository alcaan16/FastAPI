### Hola Mundo ###

# Documentación oficial: https://fastapi.tiangolo.com/es/

# Instala FastAPI: pip install "fastapi[all]"

#la siguiente linea es para una API con un solo archivo
#from fastapi import FastAPI

from fastapi import FastAPI
from routers import productos, usuarios, basic_auth_usuarios, jwt_auth_usuarios, usuarios_db #importamos el archivo 
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#router. acceso a los demas archivos
app.include_router(productos.router)
app.include_router(usuarios.router)
app.include_router(usuarios_db.router)

app.include_router(basic_auth_usuarios.router)
app.include_router(jwt_auth_usuarios.router)


#montar un archivo estatico
app.mount ("/static", StaticFiles(directory="static"), name="static")

# Url local: http://127.0.0.1:8000


@app.get("/")
async def root():
    return "Hola FastAPI!"

# Url local: http://127.0.0.1:8000/url


@app.get("/url")
async def url():
    return {"la url de prueba": "https://mouredev.com/python"}

# Inicia el server: uvicorn main:app --reload
# Detener el server: CTRL+C

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc