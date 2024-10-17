#la siguiente linea es para una API con un solo archivo
#from fastapi import FastAPI

from fastapi import APIRouter, HTTPException, status
from db.models.user import Usuario
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/usuarios_db",
                    tags= ["usuarios_db"],
                    responses= {status.HTTP_404_NOT_FOUND: {"message": "usuario no encontrado"}})





#funcion que devuleve el resultado de una busqueda por email
def buscador_usuario(campo: str, valor):
    try:
        usuario_encontrado = db_client.users.find_one({campo: valor})#busca un valor
        
        return Usuario(**user_schema(usuario_encontrado))#importante los **. le indicamos que puede ser cualquier campo
    except:
        return {"error": "no se a encontrado el usuario"}
    
#direccion que devuelve la lista de usuarios
@router.get("/", response_model=list[Usuario])
async def usuarios():
    return users_schema(db_client.users.find())

#metodo patch (parametro obligatorio)
@router.get("/{id}")
async def usuario(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="error en el ObjectId")
    return buscador_usuario("_id", ObjectId(id)) #el ObjectId convierte el objeto _id en uno manipulable

#metodo query. parametro NO obligatorio.se accede mediante "?" y se concatena con "&". aqui por ejemplo, usuario/?id=1
@router.get("/")
async def usuario(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail="error en el ObjectId")
    return buscador_usuario("_id", ObjectId(id))

#añadir datos
@router.post("/", response_model=Usuario, status_code=status.HTTP_201_CREATED)
async def usuario(usuario: Usuario):
    if type(buscador_usuario("email", usuario.email)) == Usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="el usuario ya existe") #devolvemos el error. hay que importar HTTPException
    
    user_dict = dict(usuario)
    del user_dict["id"]
    #estas lineas transformamos el usuario en un diccionario para manipularlo mejor
    #y luego le eliminamos el id porque no lo queremos

    identificador = db_client.users.insert_one(user_dict).inserted_id #inserta un usuario
    
    new_user = user_schema(db_client.users.find_one({"_id": identificador})) #busca un usuario
    
    return Usuario(**new_user)

#modificar datos    
@router.put("/", response_model=Usuario)
async def usuario(usuario: Usuario):
        
    user_dict = dict(usuario)
    del user_dict["id"]
    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(usuario.id)}, user_dict,)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="el usuario no se a actualizado")    
    return buscador_usuario("_id", ObjectId(usuario.id))

        
#eliminar datos        
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def usuario(id: str): 

    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail="error en el ObjectId")

    encontrado = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    if not encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="el usuario no existe")
    

