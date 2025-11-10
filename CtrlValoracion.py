import ModValoracion as Modelo

def eventoValorar(dominio, caso, datos_tabla):
    valoracion = Modelo.MetodoValoracion(dominio, caso, datos_tabla)
    return valoracion



