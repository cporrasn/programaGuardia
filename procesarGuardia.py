import datetime
from classFile import GuardiaTurno
from pyLoadData import buscarPersona

"""
#NO SE USA
def eliminarPersonasPlanificadas(guardiaActual,estudiantes,trabajadores):
    estudiantes1=[]
    trabajadores1 = []
    for estudiantePlanificado in guardiaActual:
        i = 0
        while i < len(estudiantes):
            if estudiantePlanificado.persona.Nombre == estudiantes[i].Nombre:
                estudiantes1.append(estudiantes[i])
                estudiantes.pop(i)
                i -= 1
            i += 1
        i = 0
        while i < len(trabajadores):
            if estudiantePlanificado.persona.Nombre == trabajadores[i].Nombre:
                trabajadores1.append(trabajadores[i])
                trabajadores.pop(i)

                i -= 1
            i += 1
    return estudiantes1,trabajadores1

#NO SE USA
def obtenerPersonasPorPlanificar(parejas, personas):
    porPlanificar = []
    if len(personas) > 0:
        i = 0
        while i < len(parejas) - 1:
            j = 0
            while j < len(personas):
                if personas[j].Nombre == parejas[i].Nombre:
                    if personas[i].Pareja is not None:
                        porPlanificar.append(personas[j])
                        personas.pop(j)
                        z = 0
                        while z < len(personas):
                            if personas[z].Nombre == parejas[i + 1].Nombre:
                                porPlanificar.append(personas[z])
                                personas.pop(z)
                                break
                            z += 1
                j += 1
            i += 2
        porPlanificar.extend(personas)
    return porPlanificar


def planificarGuardiaNoPlanificados(dictionarie,porPlanificar,monthToManage,days,year,guardiaActual,estudiantes,trabajadores):
    if len(porPlanificar) > 0:
        for i in monthToManage:
            for day in range(1, days):
                for ye in year:
                    try:
                        date = datetime.date(ye, i, day)
                    except:
                        break
                    if diasFeriados(i,day):  # verifico los rangos de fechas
                        count = 0
                        j = 0
                        final=len(dictionarie[date.strftime("%A")][0]) * 2
                        if date.strftime("%A") == "Saturday" or date.strftime("%A") == "Sunday":
                            final+=2
                        while count < final and j < len(porPlanificar):
                            turno = None
                            if porPlanificar[j].Tipo == "ESTUDIANTE":
                                turno = crearTurnoEstudiante(date, porPlanificar[j], dictionarie, guardiaActual)
                            else:
                                turno = crearTurnoTrabajador(date, porPlanificar[j], dictionarie, guardiaActual)
                            if turno is not None:
                                persona=buscarPersona(estudiantes,porPlanificar[j])
                                if persona is None:
                                    persona=buscarPersona(trabajadores,porPlanificar[j])
                                persona.Cantidad+=1
                                guardiaActual.append(turno)
                                porPlanificar.pop(j)
                                print(str(j) + " " + turno.Fecha + " " + turno.Horario + " " + turno.persona.Nombre+" "+str(turno.persona.Cantidad))
                                j -= 1
                                count += 1
                            j += 1
    return guardiaActual"""

########################################################################################################
def crearTurnoEstudiante(date,persona,dict,guardiaActual):
    if persona is not None:
        if persona.Sexo=="MASCULINO":
            if date.strftime("%A")!="Saturday" and date.strftime("%A")!="Sunday":
                count = 0
                for turn in guardiaActual:
                    if turn.Fecha == str(date) and turn.Horario == str(dict[date.strftime("%A")][0][0]):
                        count += 1

                if count < 2:
                    return GuardiaTurno(persona, str(date), dict[date.strftime("%A")][0][0])
            else:
                count = 0
                for turn in guardiaActual:
                    if turn.Fecha == str(date) and turn.Horario == str(dict[date.strftime("%A")][0][1]):
                        count += 1
                    if turn.Fecha == str(date) and (turn.Horario == str(dict[date.strftime("%A")][1][0]) \
                            or turn.Horario == str(dict[date.strftime("%A")][1][1])):
                        count += 2  # aqui se suma dos mas para que no se cree el turno si el horario que ya hay planificado no es de estudiantes
                if count < 2:
                    return GuardiaTurno(persona, str(date), dict[date.strftime("%A")][0][1])
        elif persona.Sexo=="FEMENINO":
            if date.strftime("%A")=="Saturday" or date.strftime("%A")=="Sunday":
                count=0
                for turn in guardiaActual:
                    if turn.Fecha==str(date) :
                        if turn.Horario==str(dict[date.strftime("%A")][0][0]):
                            count+=1
                        if  turn.Horario == str(dict[date.strftime("%A")][1][0]) \
                                or turn.Horario == str(dict[date.strftime("%A")][1][1]):
                            count += 2  #aqui se suma dos mas para que no se cree el turno si el horario que ya hay planificado no es de estudiantes
                if count<2:
                    return GuardiaTurno(persona,str(date),dict[date.strftime("%A")][0][0])
        else:
            return None
    else:
        return None

def crearTurnoTrabajador(date,persona,dict,guardiaActual):
    if persona is not None:
        if date.strftime("%A")=="Saturday" or date.strftime("%A")=="Sunday":
            count=0
            for turn in guardiaActual:
                if turn.Fecha==str(date) and (turn.Horario==str(dict[date.strftime("%A")][0][0])
                                                  or turn.Horario==str(dict[date.strftime("%A")][1][0])):
                    count+=1
                if turn.Fecha==str(date) and turn.Horario == str(dict[date.strftime("%A")][0][0]):
                    count += 2 #si ya hay un estudiante, aumentarlo a 2 para que no se cree un turno de trabajador
            if count<2:
                return GuardiaTurno(persona,str(date),dict[date.strftime("%A")][1][0])
            count = 0
            for turn in guardiaActual:
                if turn.Fecha == str(date) and (turn.Horario==str(dict[date.strftime("%A")][0][0])
                                                  or turn.Horario == str(dict[date.strftime("%A")][1][1])):
                    count += 1
                if turn.Fecha==str(date) and turn.Horario == str(dict[date.strftime("%A")][0][0]):
                    count += 2 #si ya hay un estudiante, aumentarlo a 2 para que no se cree un turno de trabajador
            if count < 2:
                return GuardiaTurno(persona, str(date), dict[date.strftime("%A")][1][1])
        else:
            return None
    else:
        return None

def diasFeriados(mes, dia):
    #En el mes 11, 3 y 6 no hya días feriados, se planifica todo
    #En el mes 9 hay que hacer la guardia a partir del primer día de clases
    #En el mes 12, se planifica hasta el día anterior al del receso docente
    #En el mes 1 se planifica a partir del primer día de clases
    #En el mes 4 se excluye la semana de la victoria
    #En el mes 2 se excluye el 14 de febrero
    #En el mes 10 se excluye el 10 de octubre
    #En el mes 5 se excluye el 1ro de mayo
    #En el mes 7 se planifica hasta el día antes de las vacaciones
    #El mes 8 se planifica a mano, al igual que la semana anterior de empezar el curso que es laborable, y se planifica con trabajadores

    if (mes==11 or mes==3 or mes==6) \
        or (mes == 9 and dia >= 4) \
        or (mes == 12 and dia <= 23) \
        or (mes==10 and dia!=10) \
        or (mes==1 and dia>2) \
        or (mes == 4 and 17 > dia > 23) \
        or (mes==2 and dia!=14) \
        or (mes==7 and dia < 22)\
        or (mes==5 and dia!=1):
        return True
    return False

def planificarGuardiaNoPlanificadosPorParejas(dictionarie,porPlanificar,monthToManage,days,year,guardiaActual):
    if len(porPlanificar) > 0:
        for i in monthToManage:
            for day in range(1, days):
                for ye in year:
                    try:
                        date = datetime.date(ye, i, day)
                    except:
                        break
                    if diasFeriados(i,day):  # verifico los rangos de fechas SI NO ES UN DIA FERIADO
                        count = 0
                        j = 0
                        jaux=[]
                        final = len(dictionarie[date.strftime("%A")][0]) * 2
                        if date.strftime("%A") != "Saturday" and date.strftime("%A") != "Sunday":
                            final += 2  #SI SON FINES DE SEMANA SE ADICIONAN 2 TURNOS MÁS, YA QUE COMO MAXIMO UN FIN DE SEMANA TENDRA 6 TURNOS
                        while count < final and j < len(porPlanificar):
                            if count % 2 != 0 and \
                                guardiaActual[len(guardiaActual)-1].persona.Pareja is None and \
                                porPlanificar[j].Pareja is not None:
                                jaux.append(j)  # SE VALIDA QUE EL DIA QUE AÚN NO SE HA TERMINADO DE PLANIFICAR SE COMPLETE CON PERSONAS QUE NO TENGAN PAREJA,
                                                # Y SE VAN GUARDANDO LAS POSICIONES DE LOS QUE NO SE PUDIERON PONER PARA QUE, AL ENCONTRAR UNO QUE SI SÉ PUEDA,
                                                # SE PUEDA REGRESAR A LA SIGUIENTE PERSONA QUE SE DEBE PLANIFICAR
                            else:
                                if porPlanificar[j].Tipo == "ESTUDIANTE":
                                    turno = crearTurnoEstudiante(date, porPlanificar[j], dictionarie, guardiaActual)
                                    turno1= crearTurnoEstudiante(date, porPlanificar[j].Pareja, dictionarie, guardiaActual)
                                else:
                                    turno = crearTurnoTrabajador(date, porPlanificar[j], dictionarie, guardiaActual)
                                    turno1 = crearTurnoTrabajador(date, porPlanificar[j].Pareja, dictionarie, guardiaActual)
                                if turno is not None:
                                    guardiaActual.append(turno)
                                    porPlanificar.pop(j)
                                    j -= 1
                                    count += 1
                                    print(str(j) + " " + turno.Fecha + " " + turno.Horario + " " + turno.persona.Nombre + " " + str(
                                        turno.persona.Cantidad))
                                    if len(jaux) > 0: # SI EL TURNO SE PUO CREAR SE VACIA LA LISTA DE PENDIENTES
                                        j = jaux[0]   # Y SE REINICIA LA J PARA SEGUIR A LA PRIMERA PERSONA QUE NO SE PUDO
                                        jaux.clear()  # PLANIFICAR DEBIDO A QUE NO SE PODÍA COMPLETAR LOS TURNOS DEL DÍA
                                if turno1 is not None:  #ESTE TURNO SOLO SE VA A CREAR SI LA PERSONA TIENEN PAREJA Y QUEDAN HUECOS EN EL DÍA
                                    guardiaActual.append(turno1)
                                    persona=buscarPersona(porPlanificar,turno1.persona)
                                    indice=porPlanificar.index(persona)
                                    porPlanificar.pop(indice)
                                    if indice==j:
                                        j -= 1
                                    count += 1
                                    print(str(j) + " " + turno1.Fecha + " " + turno1.Horario + " " + turno1.persona.Nombre+ " " + str(
                                        turno.persona.Cantidad))
                            j += 1
    return guardiaActual
