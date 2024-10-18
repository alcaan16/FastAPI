from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



router = APIRouter(prefix="/basicauth",
                   tags=["basicauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


#entidad Usuario
class Usuario(BaseModel):
    username: str
    nombre_completo: str
    email: str
    activo: bool

#entidad UsuarioDB(usuario mas el password)
class UsuarioDB(Usuario):
    password: str

# diccionario con los usuarios
Usuarios_db = {
    "angel": {
        "username": "angel",
        "nombre_completo": "angel alferez",
        "email": "angel@email.com",
        "activo": False,
        "password": "123456"
    },
    "angel2": {
        "username": "angel2",
        "nombre_completo": "angel alferez2",
        "email": "angel2@email.com",
        "activo": True,
        "password": "987654"
    }
}

def busqueda_usuario_db (username: str): #funcion para buscar los usuarios con el passsword
    if username in Usuarios_db:
        return UsuarioDB(**Usuarios_db[username]) #importante los **, para pasarle cualquier atributo de la clase
    
def busqueda_usuario (username: str): #funcion para buscar los usuarios sin el passsword
    if username in Usuarios_db:
        return Usuario(**Usuarios_db[username])#importante los **, para pasarle cualquier atributo de la clase
    
async def usuario_actual(token: str = Depends(oauth2)): 
    #funcion que se utiliza para saber si tenemos el usuario en la BD.
    #depende del token que le pasemos con oauth2
    usuario = busqueda_usuario (token)
    if not usuario: #buscamos si esta en la BD
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="credenciales incorrectas",
                            headers= {"WWW-Authenticate": "Bearer"})
    
    if not usuario.activo: #buscamos si esta activo
        #ejemplo de devoluvion del excepciones
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="usuario inactivo",
                            headers= {"WWW-Authenticate": "Bearer"})
    
    return usuario
    
    
@router.post("/login1")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    #funcion que no depende de nada y que espera un formulario
    usuario_db = Usuarios_db.get(form.username)#obtiene los datos del formulario 
    if not usuario_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="usuario incorrecto")
    
    usuario = busqueda_usuario_db(form.username)
   
    if not form.password == usuario.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="contraseña incorrecta")
    
    return {"access_token": usuario.username, "token_type": "bearer"} 
    #devuelve el token de acceso y el tipo de token

@router.get("/usuarios1/yo")
async def yo(usuario:Usuario = Depends(usuario_actual)):
    return usuario