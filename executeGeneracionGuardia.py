# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 18:46:51 2022

@author: HP
"""
import datetime

import pyLoadData
from procesarGuardia import planificarGuardiaNoPlanificadosPorParejas
from operator import itemgetter
import numpy as np

#seleccion de los estudiantes con sus parejas
estudiantes,parejas,guardiaActual= pyLoadData.obtenerListadosEstudiantes()

#seleccion de los trabajadores con sus parejas
trabajadores,parejasT= pyLoadData.obtenerListadosTrabajadores(guardiaActual) #aqui el guardia actual es solo para los nombres, porque desde obtenerListadosEstudiantes ya se cargan todos los trabajadores

#monthToManage=[9,10,11,12] #en 12 es hasta el día 23
#year=[2022]
monthToManage=[1,2,3,4,5,6,7] #en 7 es hasta el día 21
year=[2023]

days=32

#pos 0 es tiempo normal, 12 horas estudiantes
#pos 1 es tiempo normal, 12 horas de lunes a viernes, y fin de semana trabajadores
#pos 2 es vacaciones
dictionarie={"Monday":[["8:00 pm - 8:00 am"],
              ["9:00 am - 2:00 pm",
               "2:00 pm - 7:00 pm"]],
    "Tuesday":[["8:00 pm - 8:00 am"],
               ["9:00 am - 2:00 pm",
                "2:00 pm - 7:00 pm"]],
    "Wednesday":[["8:00 pm - 8:00 am"],
                 ["9:00 am - 2:00 pm",
                  "2:00 pm - 7:00 pm"]],
    "Thursday":[["8:00 pm - 8:00 am"],
                ["9:00 am - 2:00 pm",
                 "2:00 pm - 7:00 pm"]],
    "Friday":[["8:00 pm - 8:00 am"],
              ["9:00 am - 2:00 pm",
               "2:00 pm - 7:00 pm"]],
    "Saturday":[["8:00 am - 8:00 pm",
                 "8:00 pm - 8:00 am"],
                ["9:00 am - 2:00 pm",
                 "2:00 pm - 7:00 pm"]],
    "Sunday":[["8:00 am - 8:00 pm",
               "8:00 pm - 8:00 am"],
              ["9:00 am - 2:00 pm",
               "2:00 pm - 7:00 pm"]]}

print("//////////////////////////////")
personasTotal=estudiantes
personasTotal.extend(trabajadores)
porPlanificarCantidad=[]

porPlanificarCantidad=[personasTotal[i].Cantidad for i in range(len(personasTotal))]
interest_population_sorted_index = np.argsort(porPlanificarCantidad)[::-1]

porPlanificarCantidad = list(itemgetter(*interest_population_sorted_index)(porPlanificarCantidad))
personasTotal = list(itemgetter(*interest_population_sorted_index)(personasTotal))
personasTotal.reverse()

guardiaActual=planificarGuardiaPorParejas(dictionarie,personasTotal,monthToManage,days,year,guardiaActual)

pyLoadData.savePlanificacion(guardiaActual)

print("Terminado")

#////////////////////////CODIGO VIEJO//////////////////////////////
"""
#quito a las personas del listado original a los que ya se les haya planificado una guardia
estudiantesUsados,trabajadoresUsados=eliminarPersonasPlanificadas(guardiaActual,estudiantes,trabajadores)
#for g in guardiaActual:
#    print(g.Fecha+" "+g.persona.Nombre)

#print("//////////////////////////////")

#Tomo las parejas de los trabajadores que hay por planificar
porPlanificarT=obtenerPersonasPorPlanificar(parejasT, trabajadores)

#lo uno con los trabajadores que ya se han planificado para tener el listado total de trabaajdores
trabajadoresUsados.extend(porPlanificarT)

#vuelvo a tener a trabajadores con el ttoal de trabajadores
trabajadores=trabajadoresUsados

#Tomo las parejas de los estudiantes que hya por planificar
porPlanificarE=obtenerPersonasPorPlanificar(parejas, estudiantes)

#lo uno con los estudiantes que ya se han planificado para tener el listado total de estudiantes
estudiantesUsados.extend(porPlanificarE)

#lo uno con los estudiantes que ya se han planificado para tener el listado total de estudiantes
estudiantes=estudiantesUsados

porPlanificar=porPlanificarT
porPlanificar.extend(porPlanificarE)

#se genera la guardia de los que no han tenido guardia nunca
guardiaActual=planificarGuardiaNoPlanificados(dictionarie,porPlanificar,monthToManage,days,year,guardiaActual,estudiantes,trabajadores)

for g in trabajadores:
    print(g.Nombre + " " + str(g.Cantidad)+ " "+ g.Tipo)

"""


