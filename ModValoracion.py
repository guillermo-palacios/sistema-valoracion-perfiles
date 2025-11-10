from owlready2 import *

def MetodoValoracion(dominio, caso, datos_tabla):
    # Cargamos el dominio
    archivo_owl = dominio + ".owl"
    nuevo_mundo = World()
    onto = nuevo_mundo.get_ontology('Esq_dom.owl').load()
    nuevo_mundo.get_ontology(archivo_owl).load()

    criterios = onto.Criterio
    valoraciones = onto.Valoracion

    puntuacion_valoracion = 0.0

    # Buscamos la puntuación mínima necesaria para aceptar el caso
    for valoracion in valoraciones.instances():
        if valoracion.name == caso:
            puntuacion_valoracion = float(valoracion.puntuacion[0])

    criterios_validos = []

    criterio_cumplido = False

    puntuacion_total = 0.0

    resolucion = ""
    explicacion = ""

    #Nos quedamos con los criterios que se aplican al caso
    for criterio in criterios.instances():
        if criterio.valoracion[0].name == caso:
            criterios_validos.append(criterio)

    print(f"\nComenzando proceso de valoración del caso: {caso}")
    print("==================================================\n\n")

    explicacion += f"Comenzando proceso de valoración del caso: {caso}\n"
    explicacion += f"==================================================\n\n\n"
    
    # Comenzamos a evaluar los criterios
    for criterio in criterios_validos:
        print(f"----------------------------------------")
        print(f"Evaluando criterio: {criterio.nombre[0]}")
        print(f"----------------------------------------")

        explicacion += f"----------------------------------------\n"
        explicacion += f"Evaluando criterio: {criterio.nombre[0]}\n"
        explicacion += f"----------------------------------------\n"

        valor = datos_tabla[criterio.atributo[0].nombre[0]]
        valor_criterio = criterio.valor[0]
        tipo_comparacion = criterio.tipoComparacion[0]

        # Determinamos el tipo de comparacion del criterio
        if(tipo_comparacion == 'categorica'):
            # Determinamos si se cumple el criterio
            if valor == valor_criterio:
                criterio_cumplido = True
            else:
                criterio_cumplido = False
        else:
            # Determinamos si se cumple el criterio
            rango_str = valor_criterio.strip("[]")
            limites = [float(x) for x in rango_str.split(",")]
            valor_num = float(valor)
            if limites[0] <= valor_num < limites[1]:
                criterio_cumplido = True
            else:
                criterio_cumplido = False

        # Si se cumple el criterio, sumamos la puntuación
        if criterio_cumplido:
            puntuacion_total += float(criterio.puntuacion[0])
            print(f"Criterio {criterio.nombre[0]} cumplido con valor {valor}")
            print(f"Sumando {criterio.puntuacion[0]} puntos")
            print(f"Total acumulado: {puntuacion_total}\n\n")
            explicacion += f"Criterio {criterio.nombre[0]} cumplido con valor {valor}\n"
            explicacion += f"Sumando {criterio.puntuacion[0]} puntos\n"
            explicacion += f"Total acumulado: {puntuacion_total}\n\n\n"
        # Si no se cumple el criterio, comprobamos si es obligatorio
        else:
            # Si es un criterio terminal obligatorio, no se puede continuar
            if(criterio.obligatoria[0] == 'true'):
                print(f"Criterio terminal no cumplido")
                print(f"El valor necesario para cumplirlo es: {criterio.valor[0]}\n\n")
                explicacion += "Criterio terminal no cumplido\n"
                explicacion += f"El valor necesario para cumplirlo es: {criterio.valor[0]}\n\n\n"
                puntuacion_total = 0.0
                break
            print(f"Criterio {criterio.nombre[0]} no cumplido, valor obtenido: {valor}")
            print(f"El valor necesario para cumplirlo es: {criterio.valor[0]}\n\n")
            explicacion += f"Criterio {criterio.nombre[0]} no cumplido, valor obtenido: {valor}\n"
            explicacion += f"El valor necesario para cumplirlo es: {criterio.valor[0]}\n\n\n"
    
    # Comprobamos si se ha alcanzado la puntuación necesaria
    if puntuacion_total >= puntuacion_valoracion:
        resolucion += "Caso aceptado\n"
    else:
        resolucion += "Caso no aceptado\n"
    resolucion += "----------------------\n"
    resolucion += f"Puntuación obtenida --> {puntuacion_total}\n"
    resolucion += f"Puntuación necesaria --> {puntuacion_valoracion}\n"

    print(f"RESOLUCION FINAL:")
    print(resolucion)

    return {
        "resolucion": resolucion,
        "explicacion": explicacion,
    }