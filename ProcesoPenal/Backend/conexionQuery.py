from conexionDb import conexion as con

cursor = con.cursor()


def ultimoInsert(tableName):
    id = "Id"+tableName
    query = f'''SELECT * FROM "{tableName}" ORDER BY "{id}" DESC LIMIT 1'''
    #query = f'SELECT * FROM {tableName} ORDER BY {id} DESC LIMIT 1'
    cursor.execute(query)
    row = cursor.fetchone()
    if(row==None):
        respaldo = [0]
        return respaldo
    else:
      return row
    # añadir verificacion se row es de tipo None
#METODOS ACTUALIZAR 
def actualizarCaso(caso):
    query = ""
    if(caso["fechaFinCaso"]!=""):
        query = f"""UPDATE "Casos"
        SET "EstadoCaso"='{caso["EstadoCaso"]}', "Categoria"='{caso["Categoria"]}', "FechaFin"='{caso["fechaFinCaso"]}'
        WHERE "IdCasos"={caso["IdCasos"]};
        """
    else:
        query = f"""UPDATE "Casos"
        SET "EstadoCaso"='{caso["EstadoCaso"]}', "Categoria"='{caso["Categoria"]}'
        WHERE "IdCasos"={caso["IdCasos"]};
        """
    cursor.execute(query)
    con.commit()
    return True

def actualizarAudiencia(audiencia):

    query = f"""UPDATE "Audiencias"
    SET "DireccionLugar"='{audiencia["direccionAudiencia"]}', "NombreLugar"='{audiencia["lugarAudiencia"]}', "FechaAudiencia"='{audiencia["fechaAudiencia"]}'
    , "HoraAudiencia"='{audiencia["horaAudiencia"]}', "DescripcionAudiencia"='{audiencia["descripcionAudiencia"]}'
    WHERE "IdAudiencias"={audiencia["IdAudiencias"]};
    """
    cursor.execute(query)
    con.commit()
    return True

def actualizarEstadoAudienciaPrxima(idAu,estado):

    query = f"""UPDATE "Audiencias"
    SET "EstadoAudiencia"='{estado}'
    WHERE "IdAudiencias"={idAu};
    """
    cursor.execute(query)
    con.commit()
    return True

def actualizarEstadoCaso(idCa,estado,fechaFin):
    query=""
    if(fechaFin ==""):
        query = f"""UPDATE "Casos"
        SET "EstadoCaso"='{estado}'
        WHERE "IdCasos"={idCa};
        """
    else:
        query = f"""UPDATE "Casos"
        SET "EstadoCaso"='{estado}',"FechaFin"='{fechaFin}'
        WHERE "IdCasos"={idCa};
        """
    cursor.execute(query)
    con.commit()
    return True


#METODOS INSERTAR
def insertarPersonas(persona):
    LastInsert = ultimoInsert("Personas")
    lastId = LastInsert[0]+1
    query = """INSERT INTO public."Personas"(
	"IdPersonas", apellidos, nombres, cedula)
	VALUES (%s, %s, %s, %s);"""
    cursor.execute(
        query, (lastId, persona["apellidos"], persona["nombres"], persona["cedula"]))
    con.commit()
    return lastId


def insertarContacto(contactoPersona, idPersona):
    LastInsert = ultimoInsert("Contactos")
    lastId = LastInsert[0]+1
    query = """INSERT INTO "Contactos"
    ("IdContactos", "IdPersona", "TipoContacto", 
    "ValorContacto") VALUES (%s, %s, %s, %s);"""
    cursor.execute(
        query, (lastId, idPersona, contactoPersona["tipoContacto"], contactoPersona["ValorContacto"]))
    con.commit()
    return True


def ActulizarContacto(contactoPersona, idPersona):
    query = f"""UPDATE "Contactos"
	SET "TipoContacto"='{contactoPersona["tipoContacto"]}', "ValorContacto"='{contactoPersona["ValorContacto"]}'
	WHERE "IdPersona"={idPersona};
    """
    cursor.execute(query)
    con.commit()
    return True


def insertarPersonasAudiencia(involucrado):
    LastInsert = ultimoInsert("PersonasAudiencia")
    lastId = LastInsert[0]+1
    query = """INSERT INTO public."PersonasAudiencia"(
	"IdPersonas", "IdAudiencias", "RolPersona")
	VALUES (%s, %s, %s);"""
    cursor.execute(
        query, (lastId, involucrado["IdPersonas"], involucrado["RolPersona"], involucrado["ValorContacto"]))
    con.commit()
    return True


def insertarUsuario(usuario):
    LastInsert = ultimoInsert("Usuarios")
    lastId = LastInsert[0]+1
    idPersona = insertarPersonas(usuario)
    query = """INSERT INTO public."Usuarios"(
	"IdUsuarios", "IdPersona", "RolUsuario", "Usuario", "Clave")
	VALUES (%s, %s, %s, %s, %s);"""
    cursor.execute(query, (lastId, idPersona,
                   usuario["rol"], usuario["usuario"], usuario["clave"]))
    con.commit()


def insertarCaso(caso):
    LastInsert = ultimoInsert("Casos")
    lastId = LastInsert[0]+1
    if(caso["fechaFinCaso"]==""):
        query = """INSERT INTO public."Casos"(
	"IdCasos", "NombreCaso", "EstadoCaso", "Categoria", "FechaCreacion", "CodigoProceso")
	VALUES (%s, %s, %s, %s, %s, %s);"""
        cursor.execute(query, (lastId, caso["NombreCaso"], caso["EstadoCaso"], caso["Categoria"],
                   caso["fechaCreacionCaso"], caso["CodigoCaso"]))
    else:
        query = """INSERT INTO public."Casos"(
	"IdCasos", "NombreCaso", "EstadoCaso", "Categoria", "FechaCreacion", "FechaFin", "CodigoProceso")
	VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        cursor.execute(query, (lastId, caso["NombreCaso"], caso["EstadoCaso"], caso["Categoria"],
                   caso["fechaCreacionCaso"], caso["fechaFinCaso"], caso["CodigoCaso"]))
    con.commit()
    return lastId

def insertarAudiencia(audiencia):
    LastInsert = ultimoInsert("Audiencias")
    lastId = LastInsert[0]+1
    query = """INSERT INTO public."Audiencias"(
	"IdAudiencias", "IdCasos", "DireccionLugar", "NombreLugar", "FechaAudiencia", "FechaCreacion", "HoraAudiencia", "DescripcionAudiencia", "EstadoAudiencia", "NumeroAudiencia")
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    cursor.execute(query, (lastId, audiencia["IdCasos"], audiencia["direccionAudiencia"], audiencia["lugarAudiencia"], audiencia["fechaAudiencia"],
                   audiencia["fechaCreacionAudiencia"], audiencia["horaAudiencia"], audiencia["descripcionAudiencia"], audiencia["estadoAudiencia"], audiencia["numeroAudiencia"]))
    con.commit()
    return lastId


def insertarPersonasAudiencia(personasAudiencia, idAudiencia):
    query = """INSERT INTO public."PersonasAudiencia"(
	"IdPersonas", "IdAudiencias", "RolPersona")
	VALUES (%s, %s, %s);"""
    cursor.execute(
        query, (personasAudiencia["IdPersona"], idAudiencia, personasAudiencia["RolPersona"]))
    con.commit()

#metodos Buscar
def buscarUltimaAudienciaIdCaso(idCaso):
    query = f"""SELECT * FROM public."Audiencias"
    WHERE "IdCaso" = {idCaso} ORDER BY "IdAudiencias" DESC LIMIT 1"""
    cursor.execute(query)
    row = cursor.fetchone()
    return row


def buscarUsuarioCorreo(credenciales):
    usuario = credenciales['usuario']
    query = f"""SELECT * FROM public."Usuarios"
    WHERE "Usuario" = '{usuario}' """
    cursor.execute(query)
    row = cursor.fetchone()
    return row


def buscarPersonCedula(cedula):
    query = f"""SELECT * FROM public."Personas"
    WHERE "cedula" = '{cedula}' """
    cursor.execute(query)
    row = cursor.fetchone()
    return row

def buscarPersonId(idPersona):
    query = f"""SELECT * FROM public."Personas"
    WHERE "IdPersonas" = '{idPersona}' """
    cursor.execute(query)
    row = cursor.fetchone()
    return row


def buscarContactosPersona(Idpersona):
    query = f"""SELECT * FROM public."Contactos"
    WHERE "IdPersona" = '{Idpersona}' """
    cursor.execute(query)
    lista = cursor.fetchall()
    return lista


def buscarCasoId(idCaso):
    query = f"""SELECT * FROM public."Casos"
    WHERE "IdCasos" = '{idCaso}' """
    cursor.execute(query)
    row = cursor.fetchone()
    return row


def buscarCasosPaginas(offset):
    query = f"""SELECT *
    FROM public."Casos"
    ORDER BY "FechaCreacion"  DESC
	LIMIT 20 OFFSET {offset}"""
    cursor.execute(query)
    lista = cursor.fetchall()
    return lista

def buscarCasosEstado(offset,estado):
    query = f"""SELECT *
    FROM public."Casos"
    WHERE "EstadoCaso" = '{estado}'
    ORDER BY "IdCasos"  DESC
	LIMIT 20 OFFSET {offset}"""
    cursor.execute(query)
    lista = cursor.fetchall()
    return lista

def buscarAudienciasProximas (offset):
    query = f"""SELECT *
    FROM "Audiencias"  
    WHERE "EstadoAudiencia" = 'proxima' ORDER BY 
    "FechaAudiencia" DESC 
    LIMIT 20 OFFSET {offset}"""
    cursor.execute(query)
    row = cursor.fetchall()
    return row

def buscarUltimaAudienciaIdCaso (IdCaso):
    query = f"""SELECT "NumeroAudiencia","IdAudiencias"
    FROM "Audiencias"  
    WHERE "IdCasos" = {IdCaso} 
    ORDER BY "NumeroAudiencia" 
    DESC LIMIT 1"""
    cursor.execute(query)
    row = cursor.fetchone()
    return row

def buscarAudienciasIdCaso (IdCaso):
    query = f"""SELECT *
    FROM "Audiencias"  
    WHERE "IdCasos" = {IdCaso} 
    ORDER BY "NumeroAudiencia" 
    ASC """
    cursor.execute(query)
    row = cursor.fetchall()
    return row
def buscarAudienciasIdAu (IdAu):
    query = f"""SELECT *
    FROM "Audiencias"  
    WHERE "IdAudiencias" = {IdAu}  
    """
    cursor.execute(query)
    row = cursor.fetchone()
    return row

def buscarInvolucradosIdAudiencia (IdAudiencia):
    query = f"""SELECT *
    FROM "PersonasAudiencia"  
    WHERE "IdAudiencias" = {IdAudiencia}
    ORDER BY "IdAudiencias"
    """
    cursor.execute(query)
    row = cursor.fetchall()
    return row



def EliminarPersonasAudienciaIdAu(idAudiencia):
    query = f"""DELETE FROM  "PersonasAudiencia"
    WHERE "IdAudiencias" = {idAudiencia}
    """
    cursor.execute(query)
    con.commit()

def EliminarPersonaAudienciaidPe(idAudiencia, idPersona):
    query = f"""DELETE FROM  "PersonasAudiencia"
    WHERE "IdAudiencias" = {idAudiencia} AND "IdPersonas" = {idPersona}
    """
    cursor.execute(query)
    con.commit()

def EliminarPersonasAudienciaIdAu(idAudiencia):
    query = f"""DELETE FROM  "PersonasAudiencia"
    WHERE "IdAudiencias" = {idAudiencia}
    """
    cursor.execute(query)
    con.commit()

def cerrarConexion():
    con.close()


'''usuario={
"apellidos":"JARAMILLO JURADO",
"nombres":"CRISTIAN CARLOS",
"cedula":"1105182477",
"usuario":"cristian@gmail.com",
"clave":"12345",
"rol":"usuario"
}
insertarUsuario(usuario)
cerrarConexion()
#ultimoId = ultimoInsert("Usuarios")
#print(ultimoId[0])'''
