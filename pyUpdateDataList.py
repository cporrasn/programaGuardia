from fastDamerauLevenshtein import damerauLevenshtein
from json import load
import os
import re
import csv
import random
import pandas as pd
import datetime
from classFile import GuardiaTurno,Persona


def load_dataEstudiantes(filename):
    xls = pd.ExcelFile(filename)
    sheetX = xls.parse(0)
    nombres=sheetX['Nombre']
    apellidos=sheetX['Apellidos']
    sexo=sheetX['Sexo']
    grupo=sheetX['Grupo']
    estado = sheetX['Estado']
    estudiantes = []
    for i in range(len(nombres)):
        Nombre=nombres[i].upper()+' '+apellidos[i].upper()
        estudiantes.append(Persona(Nombre,grupo[i],sexo[i].upper(),"",0,estado[i].upper(),"ESTUDIANTE",0,None))
    return estudiantes

def load_dataTrabajadores(filename):
    xls = pd.ExcelFile(filename)
    sheetX = xls.parse(0)
    nombres=sheetX['Nombre y Apellidos']
    estado=sheetX['ESTADO']
    trabajadores = []
    for i in range(len(nombres)):
        if estado[i]=="PLANTILLA":
            Nombre=nombres[i].upper()
            trabajadores.append(Persona(Nombre,"","","",0,estado[i],"TRABAJADOR",0,None))
    return trabajadores

def load_dataParejas(filename):
    with open(filename, "r", encoding='Latin1') as file:
        estudiantes = []
        for line in csv.reader(file, delimiter=';'):
            try:
                if line[0]!="Nombre":
                    Nombre=line[0].upper()
                    estudiantes.append(Persona(Nombre,"","","",0,"","",0,None))
            except ValueError:
                pass
    return estudiantes


def load_dataGuardiaActual(filename):
    with open(filename, "r", encoding='Latin1') as file:
        guardiaActual = []
        for line in csv.reader(file, delimiter=';'):
            try:
                if line[0]!="Fecha" and line[2]!="":
                    guardiaActual.append(GuardiaTurno(Persona(line[2].upper()+" "+line[3].upper(),"","","",0,"","",0,None),line[0],line[1]))
            except ValueError:
                pass
    return guardiaActual

def addGroupAndSex(personas,parejas):
    for pareja in parejas:
        similarity=0
        elementSimilar=personas[0]
        for per in personas:
           simWT = damerauLevenshtein(pareja.Nombre, per.Nombre, similarity=True)
           if simWT>similarity:
               similarity=simWT
               elementSimilar=per
        pareja.NombreSimilar=pareja.Nombre
        pareja.Nombre=elementSimilar.Nombre
        pareja.Grupo=elementSimilar.Grupo
        pareja.Sexo=elementSimilar.Sexo
        pareja.Similitud=similarity
        pareja.Estado = elementSimilar.Estado
        pareja.Tipo = elementSimilar.Tipo
        #personas.remove(elementSimilar)

def setNamesGuardiaActual(personas,guardiaActual):
    for guardia in guardiaActual:
        similarity=0
        elementSimilar=personas[0]
        for per in personas:
           simWT = damerauLevenshtein(guardia.persona.Nombre, per.Nombre, similarity=True)
           if simWT>similarity:
               similarity=simWT
               elementSimilar=per
        guardia.persona.NombreSimilar=guardia.persona.Nombre
        guardia.persona.Nombre=elementSimilar.Nombre
        guardia.persona.Grupo=elementSimilar.Grupo
        guardia.persona.Sexo=elementSimilar.Sexo
        guardia.persona.Similitud = similarity
        guardia.persona.Tipo = elementSimilar.Tipo
        guardia.persona.Estado = elementSimilar.Estado

def buscarPersona(personas,persona):
        similarity=0
        elementSimilar=personas[0]
        for per in personas:
           simWT = damerauLevenshtein(persona.Nombre, per.Nombre, similarity=True)
           if simWT>similarity:
               similarity=simWT
               elementSimilar=per
        return elementSimilar

def saveCSVPersonas(personas,tipo):
    results = [['Nombre y apellidos','Nombre Similar','Similitud','Grupo','Sexo','Estado']]
    for per in personas:
        if per.Estado=="ACTIVO" or per.Estado=="PLANTILLA":
            results.append([per.Nombre,per.NombreSimilar,str(per.Similitud),per.Grupo,per.Sexo,per.Estado])
    with open("personas"+tipo+".csv", "w", newline='') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerows(results)

def savePlanificacion(guardia):
    results = [['Fecha','Horario','Nombre y apellidos','Entrada','Salida','Nombre Similar','Similitud','Estado']]
    for per in guardia:
        if per.persona.Estado=="ACTIVO" or per.persona.Estado=="PLANTILLA":
            results.append([per.Fecha,per.Horario,per.persona.Nombre,per.persona.NombreSimilar,str(per.persona.Similitud),per.persona.Estado])
        #print(per.persona.Nombre+";"+per.persona.NombreSimilar+";"+str(per.persona.Similitud)+";"+per.persona.Estado)
    with open("guardiaTotal.csv", "w", newline='') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerows(results)


estudiantes=load_dataEstudiantes("ReporteEstudiantes.xls")
print(len(estudiantes))
guardiaActual=load_dataGuardiaActual("guardiaEstudiantes.csv")
setNamesGuardiaActual(estudiantes,guardiaActual)
parejas=load_dataParejas("ParejasEstudiantes.csv")
print(len(parejas))
addGroupAndSex(estudiantes,parejas)
saveCSVPersonas(parejas,"parejas")
#saveCSVPersonas(estudiantes,"estudiantes")

guardiaActualT=load_dataGuardiaActual("guardiaTrabajadores.csv")
trabajadores=load_dataTrabajadores("ReporteTrabajadores.xls")
print(len(trabajadores))
parejasT=load_dataParejas("ParejasTrabajadores.csv")
print(len(parejasT))
addGroupAndSex(trabajadores,parejasT)
print(len(trabajadores))
setNamesGuardiaActual(trabajadores,guardiaActualT)

saveCSVPersonas(parejasT,"parejasT")
#saveCSVPersonas(trabajadores,"trabajadores")

guardiaActual.extend(guardiaActualT)
savePlanificacion(guardiaActual)