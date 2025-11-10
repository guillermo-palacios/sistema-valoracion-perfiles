# 🧠 Sistema Experto de Valoración de Perfiles (Python/PyQt5/OWL)

Este proyecto es una aplicación de escritorio desarrollada en Python que actúa como un sistema para la valoración de perfiles. Es capaz de evaluar a un candidato (para becas o puestos de trabajo) contra un conjunto de reglas de negocio definidas mediante el uso de ontologías OWL.

La aplicación carga dinámicamente las reglas y atributos (ej. "Beca MEC" vs. "Puesto de Trabajo"), permite al usuario introducir los datos del candidato y devuelve una valoración (Aceptado/Rechazado) con una puntuación y una explicación detallada de los criterios cumplidos y fallados.



## 🏛️ Arquitectura de Software: Modelo-Vista-Controlador (MVC)

El proyecto está construido desde cero siguiendo el patrón de diseño **Modelo-Vista-Controlador (MVC)** para garantizar la separación de responsabilidades:

* **`ModValoracion.py` (Modelo):**
    * Es el "cerebro" de la aplicación. Contiene toda la lógica de negocio.
    * Es responsable de cargar las ontologías (`.owl`) con `owlready2`.
    * Ejecuta el motor de inferencia y el bucle de valoración (comprobando criterios, puntuando y generando la explicación).

* **`VtsValoracion.py` (Vista):**
    * Es la capa de presentación (la GUI).
    * Construida con **PyQt5**, incluye todos los *widgets* (tablas, botones, menús desplegables).
    * Es responsable de consultar la ontología usando `rdflib` y **SPARQL** para rellenar dinámicamente los menús y descripciones de criterios.
    * Recoge los datos del usuario y se los pasa al Controlador.

* **`CtrlValoracion.py` (Controlador):**
    * Actúa como intermediario.
    * Contiene una única función, `eventoValorar`, llamada desde la Vista.
    * Esta función recibe los datos de la Vista y se los pasa al Modelo.
    * Recibe el resultado del Modelo y se lo devuelve a la Vista.
    * Garantiza que el Modelo y la Vista nunca se comuniquen directamente.

* **`appValoracion.py`:**
    * Es el punto de entrada de la aplicación (`__main__`).
    * Su único trabajo es instanciar la `QApplication` y la Vista (`VtsValoracion`) para lanzar el programa.

## ✨ Características Principales

* **GUI Completa:** Interfaz gráfica de usuario funcional creada con **PyQt5**.
* **Motor de Valoración Basado en Reglas:** Utiliza la lógica de la ontología para evaluar criterios numéricos (rangos de notas) y categóricos (nivel de inglés).
* **Carga Dinámica de Dominios:** Carga diferentes conjuntos de reglas (`Becas.owl`, `Puesto_trabajo.owl`) desde un esquema base (`Esq_dom.owl`).
* **Consultas SPARQL:** La Vista usa `rdflib` y consultas **SPARQL** para leer y mostrar las descripciones de los criterios de la ontología.
* **Explicabilidad:** El sistema no solo da un resultado, sino que genera una justificación paso a paso de por qué se ha aceptado o rechazado el caso.

## 🛠️ Tecnologías Utilizadas

* **Python**
* **PyQt5:** Para la interfaz gráfica de usuario (GUI).
* **Arquitectura MVC:** Como patrón de diseño de software.
* **Owlready2:** Para cargar, manipular e instanciar las ontologías (`.owl`).
* **RDFlib:** Para ejecutar consultas **SPARQL** contra los grafos de conocimiento.
* **OWL (Web Ontology Language):** Como lenguaje para modelar el conocimiento (Web Semántica).

## 🏃 Cómo Ejecutar el Proyecto

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/guillermo-palacios/sistema-valoracion-perfiles.git](https://github.com/guillermo-palacios/sistema-valoracion-perfiles.git)
    cd sistema-valoracion-perfiles
    ```

2.  **Instalar dependencias:**
    *(Es recomendable hacerlo en un entorno virtual)*
    ```bash
    pip install PyQt5 owlready2 rdflib
    ```

3.  **Ejecutar la aplicación:**
    ```bash
    python3 appValoracion.py
    ```
