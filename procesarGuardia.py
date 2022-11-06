import datetime
from classFile import GuardiaTurno
from pyLoadData import buscarPersona


def eliminarEstudiantesPlanificados(guardiaActual,estudiantes,trabajadores):
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
    #estudiantes.extend(estudiantes1)
    #trabajadores.extend(trabajadores1)
    return estudiantes1,trabajadores1

def obtenerPersonasPorPlanificar(parejas, personas):
    porPlanificar = []
    if len(personas) > 0:
        i = 0
        while i < len(parejas) - 1:
            j = 0
            while j < len(personas):
                if personas[j].Nombre == parejas[i].Nombre:
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
                if count < 2:
                    return GuardiaTurno(persona, str(date), dict[date.strftime("%A")][0][1])
        elif persona.Sexo=="FEMENINO":
            if date.strftime("%A")=="Saturday" or date.strftime("%A")=="Sunday":
                count=0
                for turn in guardiaActual:
                    if turn.Fecha==str(date) :
                        if turn.Horario==str(dict[date.strftime("%A")][0][0]) \
                                or turn.Horario==str(dict[date.strftime("%A")][1][0]) \
                                or turn.Horario == str(dict[date.strftime("%A")][1][1]):
                            count+=1
                if count<2:
                    #print(dict[date.strftime("%A")][0][0])
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
            if count<2:
                return GuardiaTurno(persona,str(date),dict[date.strftime("%A")][1][0])
            count = 0
            for turn in guardiaActual:
                if turn.Fecha == str(date) and (turn.Horario==str(dict[date.strftime("%A")][0][0])
                                                  or turn.Horario == str(dict[date.strftime("%A")][1][1])):
                    count += 1
            if count < 2:
                return GuardiaTurno(persona, str(date), dict[date.strftime("%A")][1][1])
        else:
            return None
    else:
        return None

def planificarGuardiaNoPlanificados(dictionarie,porPlanificar,monthToManage,days,year,guardiaActual,estudiantes,trabajadores):
    if len(porPlanificar) > 0:
        for i in monthToManage:
            for day in range(1, days):
                for ye in year:
                    try:
                        date = datetime.date(ye, i, day)
                    except:
                        break
                    if (i==11 or i==3) \
                            or (i == 9 and day >= 4) \
                            or (i == 12 and day <= 23) \
                            or (i==10 and day!=10) \
                            or (i==1 and day>2) \
                            or (i==2 and day!=14):  # verifico los rangos de fechas
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
    return guardiaActual

def planificarGuardiaNoPlanificadosPorParejas(dictionarie,porPlanificar,monthToManage,days,year,guardiaActual):
    if len(porPlanificar) > 0:
        for i in monthToManage:
            for day in range(1, days):
                for ye in year:
                    try:
                        date = datetime.date(ye, i, day)
                    except:
                        break
                    if (i==11 or i==3) \
                            or (i == 9 and day >= 4) \
                            or (i == 12 and day <= 23) \
                            or (i==10 and day!=10) \
                            or (i==1 and day>2) \
                            or (i==2 and day!=14):  # verifico los rangos de fechas
                        count = 0
                        j = 0
                        final = len(dictionarie[date.strftime("%A")][0]) * 2
                        if date.strftime("%A") != "Saturday" and date.strftime("%A") != "Sunday":
                            final += 2
                        while count < final and j < len(porPlanificar):
                            turno = None
                            turno1 = None
                            if porPlanificar[j].Tipo == "ESTUDIANTE":
                                turno = crearTurnoEstudiante(date, porPlanificar[j], dictionarie, guardiaActual)
                                turno1= crearTurnoEstudiante(date, porPlanificar[j].Pareja, dictionarie, guardiaActual)
                            else:
                                turno = crearTurnoTrabajador(date, porPlanificar[j], dictionarie, guardiaActual)
                                turno1 = crearTurnoTrabajador(date, porPlanificar[j].Pareja, dictionarie, guardiaActual)
                            if turno is not None:
                                guardiaActual.append(turno)
                                porPlanificar.pop(j)
                                print(str(j) + " " + turno.Fecha + " " + turno.Horario + " " + turno.persona.Nombre+" "+str(turno.persona.Cantidad) )
                                j -= 1
                                count += 1
                            if turno1 is not None:
                                guardiaActual.append(turno1)
                                persona=buscarPersona(porPlanificar,turno1.persona)
                                indice=porPlanificar.index(persona)
                                porPlanificar.pop(indice)
                                print(str(j) + " " + turno1.Fecha + " " + turno1.Horario + " " + turno1.persona.Nombre)
                                if indice==j:
                                    j -= 1
                                count += 1
                            j += 1
    return guardiaActual
