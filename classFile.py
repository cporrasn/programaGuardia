def contarBySexo(estudiantes,sexo):
    count=0
    for per in estudiantes:
        if per.Sexo==sexo:
            count+=1
    return count

class Persona:
    def __init__(self,Nombre,Grupo,Sexo,NombreSimilar,similitud,estado,tipo,cantidad,pareja,fechaUltimaGuardia):
        self.Nombre=Nombre
        self.Grupo=Grupo
        self.Sexo=Sexo
        self.NombreSimilar = NombreSimilar #Nombre con la mayor distancia de damerau
        self.Similitud=similitud   #distance de Damerau con el nombre del ReporteEstudiantes.xls
        self.Estado=estado  #PLANTILLA O ACTIVO
        self.Tipo=tipo  #TRABAJADOR O ESTUDIANTE
        self.Cantidad = cantidad  #cantidad de guardias realizadas
        self.Pareja=pareja
        self.FechaUltimaGuardia=fechaUltimaGuardia

    def isActive(self):
        return (self.tipo == "ESTUDIANTE" and self.estado=="ACTIVO") or (self.tipo== "TRABAJADOR" and self.estado=="PLANTILLA")

class GuardiaTurno:
    def __init__(self,persona,Fecha,Horario):
        self.persona=persona
        self.Fecha=Fecha  
        self.Horario=Horario

