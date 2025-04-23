# -*- coding: utf-8 -*-

import os
import sys
from PySide6.QtCore import QCoreApplication, QRect
from PySide6.QtWidgets import (
    QApplication, QComboBox, QLineEdit, QPushButton,
    QWidget, QMessageBox, QInputDialog, QFileDialog
)
from controladores import crearinforme


class Ui_Form(object):
    """Interfaz gráfica para la generación de informes a partir de archivos .jrxml."""

    def setupUi(self, Form):
        """Configura los componentes de la interfaz de usuario.

        Args:
            Form (QWidget): Widget principal donde se añadirán los componentes.
        """
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)

        self.btnGenInforme = QPushButton(Form)
        self.btnGenInforme.setObjectName(u"btnGenInforme")
        self.btnGenInforme.setGeometry(QRect(270, 100, 111, 23))

        self.comboBoxFicheros = QComboBox(Form)
        self.comboBoxFicheros.setObjectName(u"comboBoxFicheros")
        self.comboBoxFicheros.setGeometry(QRect(20, 100, 231, 23))

        self.cdrTxtRutaSalida = QLineEdit(Form)
        self.cdrTxtRutaSalida.setObjectName(u"cdrTxtRuta")
        self.cdrTxtRutaSalida.setGeometry(QRect(40, 180, 281, 23))

        self.cdrTxtRutaEntrada = QLineEdit(Form)
        self.cdrTxtRutaEntrada.setObjectName(u"cdrTxtRuta_2")
        self.cdrTxtRutaEntrada.setGeometry(QRect(20, 40, 281, 23))

        ruta_base = os.getcwd()
        self.cdrTxtRutaEntrada.setText(ruta_base)
        self.cdrTxtRutaSalida.setText(ruta_base)

        self.retranslateUi(Form)

        # Conexiones de señales
        self.cdrTxtRutaEntrada.returnPressed.connect(self.cambiar_ruta)
        self.btnGenInforme.clicked.connect(self.generar_informe)

        # Sobrescritura de eventos
        self.cdrTxtRutaEntrada.mousePressEvent = self.abrir_explorador_ruta_entrada
        self.cdrTxtRutaSalida.mousePressEvent = self.abrir_explorador_ruta_salida

        # Carga inicial de ficheros
        try:
            items = [f for f in os.listdir(self.cdrTxtRutaEntrada.text()) if f.endswith('.jrxml')]
            items.sort()
            self.comboBoxFicheros.addItems(items)
        except FileNotFoundError:
            self.aviso("Aviso ruta de entrada", "Indica la ruta de los ficheros jrxml")
        except Exception as e:
            self.aviso("Error inicial", f"Ocurrió un error al cargar la lista de archivos: {e}")

    def retranslateUi(self, Form):
        """Configura los textos traducibles de la interfaz.

        Args:
            Form (QWidget): Widget principal cuya interfaz se va a traducir.
        """
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Generar Informes Fábrica", None))
        self.btnGenInforme.setText(QCoreApplication.translate("Form", u"Generar Informe", None))
        self.cdrTxtRutaSalida.setPlaceholderText(QCoreApplication.translate("Form", u"Ruta ficheros generados", None))
        self.cdrTxtRutaEntrada.setPlaceholderText(QCoreApplication.translate("Form", u"Ruta ficheros jrxml", None))
        self.cdrTxtRutaEntrada.setToolTip(QCoreApplication.translate("Form", u"Pulsar enter para actualizar la lista de ficheros", None))

    def abrir_explorador_ruta_entrada(self, event):
        """Abre un diálogo para seleccionar la ruta de entrada de archivos .jrxml.

        Args:
            event: Evento de mouse que disparó la acción.
        """
        ruta = QFileDialog.getExistingDirectory(
            None,
            "Selecciona la carpeta de los ficheros jrxml",
            self.cdrTxtRutaEntrada.text()
        )
        if ruta:
            self.cdrTxtRutaEntrada.setText(ruta)
            self.cambiar_ruta()

    def abrir_explorador_ruta_salida(self, event):
        """Abre un diálogo para seleccionar la ruta de salida de los informes.

        Args:
            event: Evento de mouse que disparó la acción.
        """
        ruta = QFileDialog.getExistingDirectory(
            None,
            "Selecciona la carpeta de destino para los PDF",
            self.cdrTxtRutaSalida.text()
        )
        if ruta:
            self.cdrTxtRutaSalida.setText(ruta)

    def aviso(self, titulo, texto):
        """Muestra un mensaje de aviso al usuario.

        Args:
            titulo (str): Título del diálogo.
            texto (str): Contenido del mensaje.
        """
        dialogo = QMessageBox(self)
        dialogo.setWindowTitle(titulo)
        dialogo.setText(texto)
        dialogo.exec()

    def pedir_parametros(self, pLista):
        """Solicita parámetros al usuario mediante un diálogo.

        Args:
            pLista (list|str): Lista de opciones o texto de prompt.

        Returns:
            str|None: Valor introducido por el usuario o None si canceló.
        """
        pTitulo = "Parámetro Requerido"
        pTexto = "Introduce el valor para el parámetro:"

        if isinstance(pLista, list) and pLista:
            pTexto = "Selecciona un valor de la lista:"
            sel, conf = QInputDialog.getItem(self, pTitulo, pTexto, pLista, 0, False)
            return sel if conf else None
        else:
            prompt_texto = str(pLista) if isinstance(pLista, str) and pLista else pTexto
            text, conf = QInputDialog.getText(self, pTitulo, prompt_texto)
            return text if conf else None

    def error(self, pLista):
        """Función placeholder para manejo de errores.

        Args:
            pLista: Parámetro no utilizado.

        Returns:
            str: Cadena vacía.
        """
        return ""

    def generar_informe(self):
        """Genera un informe PDF a partir del archivo .jrxml seleccionado."""
        sel_param = {
            'Informe_4_1_1_1_parametro_texto': ('Comentario', self.pedir_parametros, ""),
            'Informe_4_1_1_filtrado_datos': ('Ciudad', self.pedir_parametros,
                                             ['Almendralejo', 'Cáceres', 'Madrid', 'Salamanca', 'Santander', 'Sevilla']),
            'Informe_4_1_1_ordenar_datos': ('Orden', self.pedir_parametros,
                                           ['Ciudad', 'Direccion', 'Nombre']),
            'Informe_4_7_1_Graficos': ('Titulo', self.pedir_parametros, ""),
            'Informe_4_5_1_InformePrincipal': ('Titulo', self.pedir_parametros, ""),
            'clientes':('param_cliente', self.pedir_parametros, ""),
        }
        mens_error_param_info = ("", self.error, "")

        selected_jrxml = self.comboBoxFicheros.currentText()
        if not selected_jrxml:
            self.aviso("Error", "No hay archivo JRXML seleccionado en la lista.")
            return

        ficheroEntrada = os.path.join(self.cdrTxtRutaEntrada.text(), selected_jrxml)
        ficheroSalidaBase = os.path.splitext(selected_jrxml)[0]
        ficheroSalida = os.path.join(self.cdrTxtRutaSalida.text(), ficheroSalidaBase)

        if not os.path.exists(self.cdrTxtRutaSalida.text()):
            self.aviso("Atención", f"El directorio de salida no existe. Usando directorio de entrada.")
            ficheroSalida = os.path.join(self.cdrTxtRutaEntrada.text(), ficheroSalidaBase)

        fichero_sel_base = os.path.splitext(selected_jrxml)[0]
        param_info = sel_param.get(fichero_sel_base, mens_error_param_info)

        param_name = param_info[0]
        param_dialog_func = param_info[1]
        param_list_or_prompt = param_info[2]

        parametros = {}
        if param_name:
             param_value = param_dialog_func(param_list_or_prompt)
             if param_value is not None:
                 parametros[param_name] = param_value
             else:
                 self.aviso("Cancelado", "Generación cancelada por el usuario.")
                 return

        try:
            crearinforme.advanced_example_using_database(ficheroEntrada, ficheroSalida, parametros)
            self.aviso("Éxito", f"Informe generado en: {ficheroSalida}.pdf")
        except Exception as e:
            self.aviso("Error", f"Error al generar el informe: {e}")

    def cambiar_ruta(self):
        """Actualiza la lista de archivos .jrxml cuando cambia la ruta de entrada."""
        try:
            self.comboBoxFicheros.clear()
            items = [f for f in os.listdir(self.cdrTxtRutaEntrada.text()) if f.endswith('.jrxml')]
            items.sort()
            self.comboBoxFicheros.addItems(items)
        except FileNotFoundError:
            self.aviso("Error", f"Directorio no encontrado: {self.cdrTxtRutaEntrada.text()}")
            self.comboBoxFicheros.clear()
        except Exception as e:
            self.aviso("Error", f"Error al cargar archivos: {e}")
            self.comboBoxFicheros.clear()