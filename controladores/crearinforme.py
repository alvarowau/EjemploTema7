import os
import pyreportjasper


def compiling():
    """
    Compila un archivo JRXML a un archivo Jasper.

    Esta función busca el archivo 'Agrupamiento.jrxml' dentro de la carpeta 'informes'
    y lo compila utilizando la biblioteca pyreportjasper.

    Args:
        None

    Returns:
        None
    """
    input_file = os.path.join(os.path.dirname(__file__), '..', 'informes', 'Agrupamiento.jrxml')
    jasper = pyreportjasper.PyReportJasper()
    jasper.config(input_file)
    jasper.compile()


def processing():
    """
    Procesa un archivo JRXML y genera archivos PDF y RTF.

    Esta función busca el archivo 'Agrupamiento.jrxml' en la carpeta 'informes' y lo procesa
    generando un archivo PDF y RTF en la misma carpeta.

    Args:
        None

    Returns:
        None
    """
    input_file = os.path.join(os.path.dirname(__file__), '..', 'informes', 'Agrupamiento.jrxml')
    output = os.path.join(os.path.dirname(__file__), '..', 'informes', 'pdf')

    jasper = pyreportjasper.PyReportJasper()
    jasper.process(
        input_file,
        output_file=output,
        format_list=["pdf", "rtf"]
    )


def listing_parameters():
    """
    Lista los parámetros de un informe JRXML.

    Esta función busca el archivo 'Listado_clientes_param_filtrado.jrxml' en la carpeta 'informes'
    y lista los parámetros asociados a ese archivo.

    Args:
        None

    Returns:
        None
    """
    input_file = os.path.join(os.path.dirname(__file__), '..', 'informes', 'Listado_clientes_param_filtrado.jrxml')
    jasper = pyreportjasper.PyReportJasper()
    jasper.config(input_file=input_file)
    output = jasper.list_report_params()
    print(output)


def xml_to_pdf():
    """
    Convierte un archivo XML a PDF utilizando un archivo JRXML.

    Esta función utiliza el archivo 'CancelAck.jrxml' y 'CancelAck.xml' para generar un archivo PDF
    en la carpeta 'output'.

    Args:
        None

    Returns:
        None
    """
    base_path = os.path.join(os.path.dirname(__file__), '..')
    input_file = os.path.join(base_path, 'examples', 'CancelAck.jrxml')
    output = os.path.join(base_path, 'output', '_CancelAck')
    data_file = os.path.join(base_path, 'examples', 'CancelAck.xml')

    jasper = pyreportjasper.PyReportJasper()

    jasper.process(
        input_file=input_file,
        output=output,
        format_list=["pdf"],
        parameters={},
        db_connection={
            'data_file': data_file,
            'driver': 'xml',
            'xml_xpath': '/CancelResponse/CancelResult/ID',
        },
        locale='es_ES'
    )

    print('PDF generado en:')
    print(output + '.pdf')


def json_to_pdf():
    """
    Convierte un archivo JSON a PDF utilizando un archivo JRXML.

    Esta función utiliza el archivo 'json.jrxml' y 'contacts.json' para generar un archivo PDF
    en la carpeta 'output'.

    Args:
        None

    Returns:
        None
    """
    base_path = os.path.join(os.path.dirname(__file__), '..')
    input_file = os.path.join(base_path, 'examples', 'json.jrxml')
    output = os.path.join(base_path, 'output', '_Contacts')
    data_file = os.path.join(base_path, 'examples', 'contacts.json')

    jasper = pyreportjasper.PyReportJasper()
    jasper.process(
        input_file=input_file,
        output=output,
        format_list=["pdf"],
        parameters={},
        db_connection={
            'data_file': data_file,
            'driver': 'json',
            'json_query': 'contacts.person',
        },
        locale='es_ES'
    )

    print('PDF generado en:')
    print(output + '.pdf')


def buscar_logo():
    """
    Busca un archivo de imagen llamado 'logo.png' dentro de una carpeta llamada 'img'
    en cualquier parte del proyecto. Retorna la ruta absoluta si se encuentra.

    Args:
        None

    Returns:
        str: La ruta absoluta del archivo 'logo.png', o None si no se encuentra.
    """
    nombre_archivo = 'logo.png'
    carpeta_base = 'img'

    for root, dirs, files in os.walk('.'):
        if carpeta_base in root and nombre_archivo in files:
            print("Ruta del logo:", os.path.abspath(os.path.join(root, nombre_archivo)))
            return os.path.abspath(os.path.join(root, nombre_archivo))

    return None


def advanced_example_using_database(fichero_entrada, fichero_salida, parametros):
    """
    Procesa un archivo JRXML utilizando una base de datos MySQL y parámetros proporcionados.

    Esta función procesa el archivo JRXML de entrada utilizando los parámetros proporcionados,
    incluyendo una conexión a una base de datos MySQL y un posible archivo de logo.

    Args:
        fichero_entrada (str): La ruta al archivo JRXML de entrada.
        fichero_salida (str): La ruta al archivo de salida.
        parametros (dict): Un diccionario con los parámetros para el informe.

    Returns:
        None
    """
    input_file = os.path.abspath(fichero_entrada)
    output_file = os.path.abspath(fichero_salida)

    logo_path = buscar_logo()
    if logo_path:
        parametros['LOGO_PATH'] = logo_path

    con = {
        'driver': 'mysql',
        'username': 'luis',
        'password': 'Brianda20',
        'host': 'localhost',
        'database': 'fabrica',
        'schema': '',
        'port': '3306',
        'jdbc_driver': 'com.mysql.cj.jdbc.Driver',
        'jdbc_dir': os.path.join(os.path.dirname(__file__), 'mysql-connector-java-8.0.30.jar'),
        'jdbc_url': 'jdbc:mysql://localhost:3306/fabrica?serverTimezone=Europe/Madrid'
    }

    jasper = pyreportjasper.PyReportJasper()
    jasper.process(
        input_file=input_file,
        output_file=output_file,
        format_list=["pdf"],
        parameters=parametros,
        db_connection=con,
        locale='es_ES'
    )
