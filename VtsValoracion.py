import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton,
                            QLabel, QComboBox, QTableWidget, QListWidget,
                            QTextEdit, QHeaderView, QHBoxLayout, QTableWidgetItem)
from PyQt5.QtCore import Qt
from owlready2 import *
from rdflib import Graph
from rdflib.namespace import RDF
import CtrlValoracion as Controlador


class VtsValoracion(QWidget):
    def __init__(self):
        super().__init__()
        self.Gui()

    def Gui(self):
        # Combobox Dominio
        self.comboboxDominio = QComboBox(self)
        self.dominios = ['Becas', 'Puesto_trabajo']
        self.comboboxDominio.addItems(self.dominios)
        self.comboboxDominio.currentTextChanged.connect(self.actualizarDatosPorDominio)

        # Combobox Valoracion
        self.comboboxValoracion = QComboBox(self)
        self.comboboxValoracion.currentTextChanged.connect(self.eliminarInformacionCriterios)

        # Creación de la tabla
        self.tablaCaso = QTableWidget()
        self.tablaCaso.setColumnCount(2)
        self.tablaCaso.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablaCaso.setHorizontalHeaderLabels(["ATRIBUTO", "VALOR"])

        # Creación de la lista de criterios
        self.listaCriterios = QListWidget()
        self.listaCriterios.currentItemChanged.connect(self.actualizarDescripcion)

        # Creación cuadros de texto
        self.editorDescripcion = QTextEdit("")
        self.editorDescripcion.setReadOnly(True)
        self.editorResultado = QTextEdit("")
        self.editorResultado.setReadOnly(True)
        self.editorJustificacion = QTextEdit("")
        self.editorJustificacion.setReadOnly(True)

        # Creación de labels
        self.labelDominio = QLabel("Dominio", self)
        self.labelValoracion = QLabel("Valoracion", self)
        self.labelCaso = QLabel("Caso", self)
        self.labelCriterios = QLabel("Criterios", self)
        self.labelDescripcion = QLabel("Descripción del criterio", self)
        self.labelResultado = QLabel("Resultado final", self)
        self.labelJustificacion = QLabel("Justificación de la valoración", self)

        # Creación de botones
        self.btnValidar = QPushButton("Validar", self)
        self.btnValidar.resize(self.btnValidar.sizeHint())
        self.btnSalir = QPushButton("Salir", self)
        self.btnSalir.resize(self.btnSalir.sizeHint())
        self.btnBorrar = QPushButton("Borrar", self)
        self.btnBorrar.resize(self.btnBorrar.sizeHint())

        # Asociar botones con funciones
        self.btnSalir.clicked.connect(self.close)
        self.btnValidar.clicked.connect(self.valorarDatos)
        self.btnBorrar.clicked.connect(self.borrar)

        # Crear el layout
        gridlayout = QGridLayout()

        # Posicionar elementos columna 1
        gridlayout.addWidget(self.labelDominio, 1, 1, 1, 1)
        gridlayout.addWidget(self.comboboxDominio, 2, 1, 1, 5)
        gridlayout.addWidget(self.labelValoracion, 3, 1, 1, 1)
        gridlayout.addWidget(self.comboboxValoracion, 4, 1, 1, 5)
        gridlayout.addWidget(self.labelCaso, 5, 1, 1, 1)
        gridlayout.addWidget(self.tablaCaso, 6, 1, 8, 5)
        gridlayout.addWidget(self.labelCriterios, 14, 1, 1, 1)
        gridlayout.addWidget(self.listaCriterios, 15, 1, 5, 5)
        gridlayout.addWidget(self.labelDescripcion, 20, 1, 1, 1)
        gridlayout.addWidget(self.editorDescripcion, 21, 1, 8, 5)

        # Posicionar elementos columna 2
        gridlayout.addWidget(self.labelResultado, 1, 6, 1, 1)
        gridlayout.addWidget(self.editorResultado, 2, 6, 12, 6)
        gridlayout.addWidget(self.labelJustificacion, 14, 6, 1, 1)
        gridlayout.addWidget(self.editorJustificacion, 15, 6, 14, 6)

        # Posicionar botones
        layout_botones = QHBoxLayout()
        layout_botones.addStretch(1)
        layout_botones.addWidget(self.btnValidar)
        layout_botones.addWidget(self.btnBorrar)
        layout_botones.addWidget(self.btnSalir)
        layout_botones.addStretch(1)
        gridlayout.addLayout(layout_botones, 30, 1, 1, 11)

        #Llamamos a la funcion de actualizarDatosPorDominio ya que nos carga todos los datos del dominio seleccioando
        self.actualizarDatosPorDominio()
        self.setLayout(gridlayout)
        self.setGeometry(250, 150, 1200, 850)
        self.show()
    

    def actualizarDatosPorDominio(self):
        # Cargar la ontología OWL en un nuevo mundo para que no se acumulen las distintas ontologias
        archivo_owl = self.comboboxDominio.currentText() + ".owl"
        nuevo_mundo = World()
        onto = nuevo_mundo.get_ontology('Esq_dom.owl').load()
        nuevo_mundo.get_ontology(archivo_owl).load()

        # Obtener las clases de la ontología
        atributos = onto.Atributo
        valoraciones = onto.Valoracion
        criterios = onto.Criterio

        #Añadimos las valoraciones
        self.comboboxValoracion.clear()
        for valoracion in valoraciones.instances():
            self.comboboxValoracion.addItem(valoracion.name)

        #Añadimos los atributos
        self.tablaCaso.clearContents()
        self.tablaCaso.setRowCount(len(atributos.instances()))
        
        for i, atributo in enumerate(atributos.instances()):
            item_atributo = QTableWidgetItem(atributo.nombre[0])  # Nombre del atributo
            item_atributo.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Solo lectura

            # Dependiendo del tipo de atributo, asignamos el valor
            if atributo.tipo[0] == 'multiple' or atributo.tipo[0] == 'bool':
                # Si el atributo tiene opciones múltiples, usamos un ComboBox
                combo_valor = QComboBox()
                # Si el atributo es de tipo 'bool' se le asignan los valores 'True' y 'False'
                if atributo.tipo[0] == 'bool':
                    atributo.posiblesValores = ['True', 'False']
                combo_valor.addItems(atributo.posiblesValores)  # Opciones disponibles
                combo_valor.setCurrentText(atributo.valorInicial[0])  # Seleccionar el valor actual
                self.tablaCaso.setCellWidget(i, 1, combo_valor)  # Poner el ComboBox en la celda

            else:
                item_valor = QTableWidgetItem(atributo.valorInicial[0])
                item_valor.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)  # Editable
                self.tablaCaso.setItem(i, 1, item_valor)  # Poner el valor en la tabla

            # Agregar el nombre del atributo
            self.tablaCaso.setItem(i, 0, item_atributo)

        self.listaCriterios.clear()

        #Añadimos los criterios
        for criterio in criterios.instances():
            if criterio.valoracion[0].name == self.comboboxValoracion.currentText():
                self.listaCriterios.addItem(criterio.nombre[0])
        
    def actualizarDescripcion(self, current):
        if current:
            archivo_owl = self.comboboxDominio.currentText() + ".owl"
            seleccion = self.listaCriterios.currentItem().text()
            valoracion = self.comboboxValoracion.currentText()

            # Cargar ambas ontologías
            g = Graph()
            g.parse("Esq_dom.owl", format="xml")
            g.parse(archivo_owl, format="xml")

            query = f"""
            PREFIX : <http://example.org/esq_dom#>
            PREFIX rdf: <{RDF}>

            SELECT ?nombre ?tipoComparacion ?tipoResultado ?puntuacion ?valor ?obligatoria ?val_id
            WHERE {{
                ?criterio rdf:type :Criterio ;
                        :nombre ?nombre ;
                        :tipoComparacion ?tipoComparacion ;
                        :tipoResultado ?tipoResultado ;
                        :puntuacion ?puntuacion ;
                        :valor ?valor ;
                        :obligatoria ?obligatoria ;
                        :valoracion ?val .

                BIND(STRAFTER(STR(?val), "#") AS ?val_id)

                FILTER(str(?nombre) = "{seleccion}" && str(?val_id) = "{valoracion}")
            }}
            """

            resultados = g.query(query)

            for row in resultados:
                desc = (
                    f"Nombre:\t\t{row.nombre}\n"
                    f"Comparación:\t{row.tipoComparacion}\n"
                    f"Tipo de resultado:\t{row.tipoResultado}\n"
                    f"Puntuación:\t{row.puntuacion}\n"
                    f"Valor:\t\t{row.valor}\n"
                    f"Terminal:\t\t{row.obligatoria}"
                )
                self.editorDescripcion.setText(desc)
                break
            

    def valorarDatos(self):
        dominio = self.comboboxDominio.currentText()  # Obtener el dominio seleccionado
        caso = self.comboboxValoracion.currentText()  # Obtener la valoración seleccionada
        datos_tabla = self.obtenerDatosTabla()  # Obtener los datos de la tabla

        valoracion = Controlador.eventoValorar(dominio, caso, datos_tabla)
        # Comprobamos el resultado de la valoracion y cambiamos el color del texto
        if "Caso aceptado" in valoracion['resolucion']:
            self.editorResultado.setStyleSheet("color: green;")
        else:
            self.editorResultado.setStyleSheet("color: red;")
            
        self.editorResultado.setText(valoracion['resolucion'])
        self.editorJustificacion.setText(valoracion['explicacion'])

    def obtenerDatosTabla(self):
        datos = {}
        for fila in range(self.tablaCaso.rowCount()):
            atributo = self.tablaCaso.item(fila, 0).text()
            # Verifica si la celda es un QComboBox (para atributos múltiples o bool)
            widget = self.tablaCaso.cellWidget(fila, 1)
            if widget and isinstance(widget, QComboBox):
                valor = widget.currentText()
            else:
                valor = self.tablaCaso.item(fila, 1).text()
            datos[atributo] = valor
        return datos

    def borrar(self):
        self.editorResultado.clear()
        self.editorJustificacion.clear()

    def eliminarInformacionCriterios(self):
        #Quitamos la seleccion de la lista de criterios
        self.listaCriterios.clearSelection()
        self.listaCriterios.setCurrentRow(-1)
        #Vaciamos la informacion del texto que muestra la descripcion del criterio
        self.editorDescripcion.clear()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VtsValoracion()
    ex.show()
    sys.exit(app.exec_())
