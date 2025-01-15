#la siguiente linea es para una API con un solo archivo
#from fastapi import FastAPI

from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/productos",
                    tags= ["productos"],
                    responses= {404: {"message": "producto no encontrado"}})

lista_productos = ["producto1", "producto2", "producto3", "producto4"]

@router.get("/")
async def productos():

    return lista_productos


@router.get("/{id}")
async def productos(id:int):
    if id < 1 or id > len(lista_productos):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="el producto no existe") #devolvemos el error. hay que importar HTTPException
    return lista_productos[id-1]
