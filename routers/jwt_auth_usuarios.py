from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256" #tipo de algoritnmo de encriptacion
ACCESS_TOKEN_DURATION = 1 #la duracion del token de acceso
SECRET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" #palabra secreta para encriptar
router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
#variable en la que indicamos la url que se encarga de gestionar

crypt = CryptContext(schemes=["bcrypt"])
#variable que se encarga de la crypto


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
        "password": "$2a$12$mFhLceDeJ74x0L7/apa/7.y5aUNx.PSwIP8zgl72roGzOqoAa7IHW"
    },
    "angel2": {
        "username": "angel2",
        "nombre_completo": "angel alferez2",
        "email": "angel2@email.com",
        "activo": True,
        "password": "$2a$12$Wve3enRzMd0KOvklp46cRu7c8SHDIECMXwYDYOxIpNlrbhV0TlgMK"
    }
}

#funcion para buscar los usuarios con el passsword
def busqueda_usuario_db (username: str):
    if username in Usuarios_db:
        return UsuarioDB(**Usuarios_db[username])#importante los **, para pasarle cualquier atributo de la clase
    
#funcion para buscar los usuarios sin el passsword    
def busqueda_usuario (username: str):
    if username in Usuarios_db:
        return Usuario(**Usuarios_db[username])#importante los **, para pasarle cualquier atributo de la clase

async def usuario_autenticado(token: str = Depends(oauth2)):
#funcion para comprobar si esta autenticado el usuario. depende el token
    exception = HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="credenciales incorrectas",
                                headers= {"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
        #decodificamos el username. le pasamos el token, la palabra secreta, el algoritmo.
        # y utilizamos el get para obtener el "sub" que el el propio nombre del usuario 
        if username is None:
            raise exception
    except JWTError:
        raise exception
    
    return busqueda_usuario (username)

async def usuario_actual(usuario: Usuario = Depends(usuario_autenticado)):
     #funcion que se utiliza para saber si tenemos el usuario en la BD.
    #depende del token que le pasemos con oauth2
    if not usuario.activo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="usuario inactivo",
                            headers= {"WWW-Authenticate": "Bearer"})
    
    return usuario

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    usuario_db = Usuarios_db.get(form.username)#obtenemos el username del formulario
    if not usuario_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="usuario incorrecto")
    
    usuario = busqueda_usuario_db(form.username)
    
    if not crypt.verify(form.password, usuario.password): #verificamos el usuario encriptado  
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="contraseña incorrecta")
    
    #el timedelta define lo que indicamos entre parentesis
    #token de acceso: le pasamos el propio username(sub) y el tiempo a expirar. seria ahora mas la variable que le dimos
    access_token = { "sub": usuario.username,
                    "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_DURATION)}               

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM) , "token_type": "bearer"}
    #codificamos el token. el propio token , la palabra secreta, y el algoritmo. todo con el tipo de token bearer

@router.get("/usuarios/yo")
async def yo(usuario:Usuario = Depends(usuario_actual)):
    return usuario
