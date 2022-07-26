from fastapi import FastAPI as fast
#from typing import Dict, Union
import modelosEntidades as mE
from fastapi.middleware.cors import CORSMiddleware

import logica as lg
from conexionQuery import insertarUsuario as inUsu

app = fast()

origins = [
    
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500",
    "http://127.0.0.1",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/InUsuario")
def ingresarUsuario (usuario: mE.usuario):
    inUsu(usuario.dict())
    return True

@app.post("/InInvolucrado")
def inInvolucrado(involucrado: mE.Involucrado):
    respuesta = lg.ingresarInvolucrado(involucrado.dict())
    return respuesta

@app.post("/agregarContacto")
def inContacto(Contacto: mE.addContacto):
    lg.addContacto(Contacto.dict())
    return True

@app.post("/GuardarAudiencia")
def GuarAudiencia (Audiencia: mE.Caso):
    lg.guardarAudiencia(Audiencia.dict())
    return True

@app.get("/validarUsuario/{usuario},{clave}")
def validarUsuario (usuario, clave):
    credenciales = {}
    credenciales['usuario'] = str(usuario)
    credenciales['clave'] = str(clave)
    respuesta = lg.validarCredenciales(credenciales)
    return respuesta


@app.get("/buscarInvolucrado/{cedula}")
def buscarInvolucrado (cedula):
    respuesta = lg.buscarInvolucrado(cedula)
    return respuesta

@app.get("/proximasAudiencias/{pagina}")
def proximasAudiencias (pagina):
    respuesta = lg.proximasAudiencias(pagina)
    return respuesta

@app.get("/casosTerminados/{pagina}")
def casosTerminados (pagina):
    respuesta = lg.CasosTerminados(pagina)
    return respuesta

@app.get("/casosProceso/{pagina}")
def casosProceso (pagina):
    respuesta = lg.CasosProceso(pagina)
    return respuesta


@app.get("/BuscarAudienciasCaso/{idCaso}")
def traerAudienciasCaso (idCaso):
    respuesta = lg.traerCaso(idCaso)
    return respuesta

@app.get("/BuscarCaso/{idCaso},{idAu}")
def BuscarCaso (idCaso,idAu):
    respuesta = lg.buscarCaso(idCaso,idAu)
    return respuesta

