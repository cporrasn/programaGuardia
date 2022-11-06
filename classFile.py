def contarBySexo(estudiantes,sexo):
    count=0
    for per in estudiantes:
        if per.Sexo==sexo:
            count+=1
    return count

class Persona:
    def __init__(self,Nombre,Grupo,Sexo,NombreSimilar,similitud,estado,tipo,cantidad,pareja):
        self.Nombre=Nombre
        self.Grupo=Grupo
        self.Sexo=Sexo
        self.NombreSimilar = NombreSimilar
        self.Similitud=similitud
        self.Estado=estado
        self.Tipo=tipo
        self.Cantidad = cantidad
        self.Pareja=pareja

class GuardiaTurno:
    def __init__(self,persona,Fecha,Horario):
        self.persona=persona
        self.Fecha=Fecha  #convertir en un date
        self.Horario=Horario

