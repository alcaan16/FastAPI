#la siguiente linea es para una API con un solo archivo
#from fastapi import FastAPI

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter(prefix="/usuarios",
                    tags= ["usuarios"],
                    responses= {404: {"message": "usuario no encontrado"}})

#entidad user
class Usuario(BaseModel):
    id: int
    nombre: str
    apellido: str
    url: str
    edad: int

#lista con los usuarios con la clase gracias basemodel
lista_usuarios = [Usuario(id= 1, nombre="angel", apellido="alferez", url="angel.com", edad= 35),
         Usuario(id= 2,nombre="pepe", apellido="dos", url="pepe2.com", edad=20),
         Usuario(id= 3,nombre="juan", apellido="tres", url="juan3.com", edad=30)]

#esto seria mandarlo tipo json
@router.get("/usuarios_json")
async def usuarios_json():
    return [{"nombre": "angel", "apellido": "alferez", "url": "angel.com", "edad": 35},
            {"nombre": "pepe", "apellido": "dos", "url": "pepe2.com", "edad": 20},
            {"nombre": "juan", "apellido": "tres", "url": "juan3.com", "edad": 30}]

#direccion que devuelve la lista de usuarios
@router.get("/")
async def usuarios():
    return lista_usuarios

#funcion que devuleve el resultado de una busqueda por id
def buscador_usuario(id: int):

    busq_usuario = filter(lambda Usuario: Usuario.id == id, lista_usuarios)
    #esta linea de codigo de filter devuelve el "usuario", cuando el "id" sea el mismo que hemos dado, desde la "lista_usuarios"
    #basicamente es un for en busca de una coincidencia
    
    try:
        #devuelve una lista de los resultados, pero solo elegimos el index 0 (el primero)
        return list(busq_usuario)[0]
    except:
        return {"error": "no se a encontrado el usuario"}
    
#metodo patch (parametro obligatorio)
@router.get("/{id}", response_model=Usuario)
async def usuario(id: int):
    return buscador_usuario(id)

#metodo query. parametro NO obligatorio.se accede mediante "?" y se concatena con "&". aqui por ejemplo, usuario/?id=1
@router.get("/")
async def usuario(id: int):
    return buscador_usuario(id)

#añadir datos
@router.post("/", status_code=201, response_model=Usuario)
async def usuario(usuario: Usuario):
    if type(buscador_usuario(usuario.id)) == Usuario:
        #return {"error": "el usuario ya existe"}
        raise HTTPException(status_code=404, detail="el usuario ya existe") #devolvemos el error. hay que importar HTTPException
    
    lista_usuarios.append(usuario) #añade el usuario.
    return usuario
    
#modificar datos    
@router.put("/", response_model=Usuario)
async def usuario(usuario: Usuario):
    encontrado = False
    for index, list_usua in enumerate(lista_usuarios): #IMPORTANTE, recorre la los usuarios pero asigna a cada uno un index
        if list_usua.id == usuario.id:
            lista_usuarios[index] = usuario #sobreescribe el usuario
            encontrado = True
            return "usuario modificado correctamente"
    if not encontrado:
        return {"error": "ERROR al modificar el usuario"}
        
#eliminar datos        
@router.delete("/{id}")
async def usuario(id: int): 
    encontrado = False
    for index, list_usua in enumerate(lista_usuarios): #IMPORTANTE, recorre la los usuarios pero asigna a cada uno un index
        if list_usua.id == id:
            del lista_usuarios[index] #borra el usuario
            encontrado = True
            return "usuario eliminado correctamente"
    if not encontrado:
        return {"error": "ERROR al eliminar el usuario"}

    
