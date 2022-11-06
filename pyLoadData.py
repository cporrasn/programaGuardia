from fastDamerauLevenshtein import damerauLevenshtein
from json import load
import os
import re
import csv
import random
import pandas as pd
import datetime
from classFile import GuardiaTurno,Persona

excepciones=["ENMANUEL DE JESUS DIAZ ALVAREZ","DENZEL ISRAEL COMPANIONI MIRANDA"]

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
        if estado[i].upper()=="ACTIVO":
            Nombre=nombres[i].upper()+' '+apellidos[i].upper()
            if excepciones.count(Nombre)==0:
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
                if line[0]!="Nombre y apellidos":
                    Nombre=line[0].upper()
                    estudiantes.append(Persona(Nombre,"","","",0,"","ESTUDIANTE",0,None))
            except ValueError:
                pass
    return estudiantes


def load_dataGuardiaActual(filename):
    with open(filename, "r", encoding='Latin1') as file:
        guardiaActual = []
        for line in csv.reader(file, delimiter=';'):
            try:
                if line[0]!="Fecha" and line[2]!="":
                    guardiaActual.append(GuardiaTurno(Persona(line[2].upper(),"","","",0,"","",1,None),line[0],line[1]))
            except ValueError:
                pass
    return guardiaActual

def addGroupAndSex(personas,parejas):
    for pareja in parejas:
        similarity=0
        for per in personas:
           simWT = damerauLevenshtein(pareja.Nombre, per.Nombre, similarity=True)
           if simWT == 1.0:
               elementSimilar = per
               pareja.NombreSimilar=pareja.Nombre
               pareja.Nombre=elementSimilar.Nombre
               pareja.Grupo=elementSimilar.Grupo
               pareja.Sexo=elementSimilar.Sexo
               pareja.Similitud=similarity
               pareja.Estado = elementSimilar.Estado
               pareja.Tipo=elementSimilar.Tipo
               pareja.Cantidad = elementSimilar.Cantidad
               #personas.remove(elementSimilar)
               break

def setNamesGuardiaActual(personas,guardiaActual):
    for guardia in guardiaActual:
        similarity=0
        for per in personas:
           simWT = damerauLevenshtein(guardia.persona.Nombre, per.Nombre, similarity=True)
           if simWT==1.0:
               elementSimilar=per
               guardia.persona.NombreSimilar=guardia.persona.Nombre
               guardia.persona.Nombre=elementSimilar.Nombre
               guardia.persona.Grupo=elementSimilar.Grupo
               guardia.persona.Sexo=elementSimilar.Sexo
               guardia.persona.Similitud = similarity
               guardia.persona.Estado = elementSimilar.Estado
               guardia.persona.Tipo = elementSimilar.Tipo
               guardia.persona.Cantidad = elementSimilar.Cantidad
               elementSimilar.Cantidad += 1
               #personas.remove(elementSimilar)
               break

def buscarPersona(personas,persona):
        elementSimilar=None
        for per in personas:
           simWT = damerauLevenshtein(persona.Nombre, per.Nombre, similarity=True)
           if simWT == 1.0:
               elementSimilar = per
               break
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
    results = [['Fecha','Horario','Nombre y apellidos','Grupo','Entrada','Salida']]
    for per in guardia:
        if per.persona.Estado=="ACTIVO" or per.persona.Estado=="PLANTILLA":
            grupo =per.persona.Tipo
            if per.persona.Tipo == "ESTUDIANTE":
                grupo=str(per.persona.Grupo)
            results.append([per.Fecha,per.Horario,per.persona.Nombre,grupo])

        #print(per.persona.Nombre+";"+per.persona.NombreSimilar+";"+str(per.persona.Similitud)+";"+per.persona.Estado)
    with open("guardiaNueva.csv", "w", newline='') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerows(results)

def pintarEstudiantes(estudiantes):
    for per in estudiantes:
        print(per.Nombre+";"+per.Grupo)

def adicionarPareja(personas,parejas):
    i = 0
    while i < len(parejas) - 1:
        j = 0
        while j < len(personas):
            if personas[j].Nombre == parejas[i].Nombre:
                if personas[j].Pareja is None:
                    personas[j].Pareja=parejas[i + 1]
                z = 0
                while z < len(personas):
                    if personas[z].Nombre == parejas[i + 1].Nombre:
                        if personas[z].Pareja is None:
                            personas[z].Pareja = parejas[i]
                            break
                    z += 1
            j += 1
        i += 2

def obtenerListadosEstudiantes():
    estudiantes=load_dataEstudiantes("ReporteEstudiantes.xls")
    guardiaActual = load_dataGuardiaActual("guardiaTotal.csv")
    parejas=load_dataParejas("personasparejas.csv")

    addGroupAndSex(estudiantes,parejas)
    setNamesGuardiaActual(estudiantes,guardiaActual)
    adicionarPareja(estudiantes,parejas)

    return estudiantes,parejas,guardiaActual

def obtenerListadosTrabajadores(guardiaActual):
    trabajadores=load_dataTrabajadores("ReporteTrabajadores.xls")

    parejas=load_dataParejas("personasparejasT.csv")
    addGroupAndSex(trabajadores,parejas)

    #guardiaActual.extend(load_dataGuardiaActual("guardiaTotal.csv"))
    setNamesGuardiaActual(trabajadores,guardiaActual)
    adicionarPareja(trabajadores, parejas)

    return trabajadores,parejas


#pintarEstudiantes(estudiantes)

"""print(len(guardiaActual))
print(len(parejas))
print(len(estudiantes))

print("")"""
"""trabajadores=load_dataTrabajadores("Trabajadores.xlsx")
parejasT=load_dataParejas("Trabajadores.csv")
addGroupAndSex(trabajadores,parejasT)"""
