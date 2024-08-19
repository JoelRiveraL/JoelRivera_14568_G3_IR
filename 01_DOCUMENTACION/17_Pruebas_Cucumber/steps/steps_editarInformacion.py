from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from fpdf import FPDF
import os
import time

# Especifica la ruta del webdriver aquí
CHROME_DRIVER_PATH = r'C:\Users\joela\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe'

# Ruta para guardar capturas de pantalla
SCREENSHOTS_DIR = 'screenshots'

# Especifica la ruta del webdriver aquí
CHROME_DRIVER_PATH = r'C:\Users\joela\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe'

# Ruta para guardar capturas de pantalla
SCREENSHOTS_DIR = 'screenshots'

def ensure_pdf_initialized(context):
    if not hasattr(context, 'pdf'):
        context.pdf = FPDF()
        context.pdf.set_auto_page_break(auto=True, margin=15)


def setup_browser(context):
    service = Service(CHROME_DRIVER_PATH)
    context.driver = webdriver.Chrome(service=service)
    context.driver.maximize_window()
    # Crea el directorio de capturas si no existe
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def take_screenshot(context, name):
    """Captura una pantalla y la guarda con el nombre proporcionado."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_path = os.path.join(SCREENSHOTS_DIR, f'{name}_{timestamp}.png')
    context.driver.save_screenshot(screenshot_path)
    return screenshot_path

def add_screenshot_to_pdf(pdf, image_path, step_description):
    """Agrega una captura de pantalla al PDF."""
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, step_description, 0, 1, 'C')
    pdf.ln(10)  # Agrega un salto de línea
    pdf.image(image_path, x=10, y=pdf.get_y(), w=190)


@given('Abrir navegador editar informacion')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/busquedaP.php')
    screenshot_path = take_screenshot(context, 'abrir_navegador_editar_informacion')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador para editar información")


@when('seleccionar filas a editar')
def step_impl(context):
    # Encuentra todas las filas con el atributo 'data-id' que se pueden seleccionar
    filas = context.driver.find_elements(By.CSS_SELECTOR, 'tr[data-id]')
    if filas:
        filas[0].click()
    else:
        raise Exception("No se encontraron filas para seleccionar")
    screenshot_path = take_screenshot(context, 'seleccionar_filas')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar filas para editar")

@then('presionar boton de editar')
def step_impl(context):
    boton_editar = context.driver.find_element(By.ID, 'modificarBoton')  # Asume un ID para el botón
    boton_editar.click()
    screenshot_path = take_screenshot(context, 'presionar_boton_editar')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Presionar botón de editar")


@when('editar informacion con datos correctos')
def step_impl(context):
    context.driver.find_element(By.ID, 'montoEditable').clear()
    context.driver.find_element(By.ID, 'montoEditable').send_keys('5')
    screenshot_path = take_screenshot(context, 'editar_informacion')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Editar información con datos correctos")
    context.driver.find_element(By.NAME, 'modificarConfirmar').click()


@then('revisar informacion editada en la tabla')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'resumen-general'))
    )
    tabla = context.driver.find_element(By.ID, 'resumen-general')
    filas = tabla.find_elements(By.TAG_NAME, 'tr')

    assert len(filas) > 1, "La tabla está vacía o no se encontró la información editada."

    encabezados = filas[0].find_elements(By.TAG_NAME, 'th')
    columna_dato_editado = None
    for i, encabezado in enumerate(encabezados):
        if 'Monto' in encabezado.text:
            columna_dato_editado = i
            break

    assert columna_dato_editado is not None, "No se encontró la columna con el dato editado."

    datos_editados = [fila.find_elements(By.TAG_NAME, 'td')[columna_dato_editado].text for fila in filas[1:]]
    assert '5' in datos_editados, "El dato editado no se encontró en la columna especificada."

    screenshot_path = take_screenshot(context, 'revisar_informacion_editada')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Revisar información editada en la tabla")

    context.driver.quit()

#-----------------------------------------------------------------------------------

@given('Abrir navegador editar informacion incorrecta')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/busquedaP.php')
    screenshot_path = take_screenshot(context, 'abrir_navegador_editar_informacion')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador para editar información")


@when('seleccionar filas a editar informacion incorrecta')
def step_impl(context):
    # Encuentra todas las filas con el atributo 'data-id' que se pueden seleccionar
    filas = context.driver.find_elements(By.CSS_SELECTOR, 'tr[data-id]')
    if filas:
        filas[0].click()
    else:
        raise Exception("No se encontraron filas para seleccionar")
    screenshot_path = take_screenshot(context, 'seleccionar_filas')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar filas para editar")

@then('presionar boton de editar informacion incorrecta')
def step_impl(context):
    boton_editar = context.driver.find_element(By.ID, 'modificarBoton')  # Asume un ID para el botón
    boton_editar.click()
    screenshot_path = take_screenshot(context, 'presionar_boton_editar')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Presionar botón de editar")


@when('editar informacion con datos incorrecta')
def step_impl(context):
    context.driver.find_element(By.ID, 'montoEditable').clear()
    context.driver.find_element(By.ID, 'montoEditable').send_keys('aa')
    screenshot_path = take_screenshot(context, 'editar_informacion')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Editar información con datos correctos")
    context.driver.find_element(By.NAME, 'modificarConfirmar').click()


@then('revisar informacion incorrecta editada en la tabla')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'resumen-general'))
    )
    tabla = context.driver.find_element(By.ID, 'resumen-general')
    filas = tabla.find_elements(By.TAG_NAME, 'tr')

    assert len(filas) > 1, "La tabla está vacía o no se encontró la información editada."

    encabezados = filas[0].find_elements(By.TAG_NAME, 'th')
    columna_dato_editado = None
    for i, encabezado in enumerate(encabezados):
        if 'Monto' in encabezado.text:
            columna_dato_editado = i
            break

    assert columna_dato_editado is not None, "No se encontró la columna con el dato editado."

    datos_editados = [fila.find_elements(By.TAG_NAME, 'td')[columna_dato_editado].text for fila in filas[1:]]
    assert '1' in datos_editados, "El dato editado no se encontró en la columna especificada."

    screenshot_path = take_screenshot(context, 'revisar_informacion_editada')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Revisar información editada en la tabla")

    context.driver.quit()

#-----------------------------------------------------------------------------------

@given('Abrir navegador editar sin datos')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/busquedaP.php')
    screenshot_path = take_screenshot(context, 'abrir_navegador_editar_sin_datos')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador para editar sin datos")


@when('No seleccionar filas a editar informacion')
def step_impl(context):
    # No selecciona ninguna fila para edición
    screenshot_path = take_screenshot(context, 'no_seleccionar_filas')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "No seleccionar filas para editar información")


@then('presionar boton de editar sin datos')
def step_impl(context):
    boton_editar = context.driver.find_element(By.ID, 'modificarBoton')
    boton_editar.click()
    screenshot_path = take_screenshot(context, 'presionar_boton_editar_sin_datos')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Presionar botón de editar sin datos")


@when('editar informacion sin datos')
def step_impl(context):
    # No realiza cambios en los campos
    context.driver.find_element(By.NAME, 'rechazarConfirmar').click()
    screenshot_path = take_screenshot(context, 'editar_informacion_sin_datos')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Editar información sin datos")


@then('revisar informacion no editada en la tabla')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'resumen-general'))
    )
    tabla = context.driver.find_element(By.ID, 'resumen-general')
    filas = tabla.find_elements(By.TAG_NAME, 'tr')

    assert len(filas) > 1, "La tabla está vacía o no se encontró la información."

    # Verifica que la tabla contiene los datos originales sin cambios
    datos_originales = [fila.text for fila in filas[1:]]  # Asume que la primera fila es el encabezado

    # Aquí podrías añadir una verificación adicional si tienes datos esperados específicos
    # Para este ejemplo, simplemente comprobamos que hay datos en la tabla
    assert any(datos_originales), "No se encontró información en la tabla."

    screenshot_path = take_screenshot(context, 'revisar_informacion_no_editada')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Revisar información no editada en la tabla")

    context.driver.quit()

#-----------------------------------------------------------------------------------

@given('Abrir navegador editar informacion monto')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/busquedaP.php')
    screenshot_path = take_screenshot(context, 'abrir_navegador_editar_monto')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador para editar información de monto")


@when('seleccionar filas a editar el monto')
def step_impl(context):
    # Selecciona la primera fila de la tabla para edición
    fila = context.driver.find_element(By.XPATH, '//table[@id="resumen-general"]/tbody/tr[2]')  # Asume que la primera fila es encabezado
    fila.click()
    screenshot_path = take_screenshot(context, 'seleccionar_filas_editar_monto')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar filas para editar el monto")


@then('presionar boton de editar informacion')
def step_impl(context):
    boton_editar = context.driver.find_element(By.ID, 'modificarBoton')
    boton_editar.click()
    screenshot_path = take_screenshot(context, 'presionar_boton_editar_informacion')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Presionar botón de editar información")


@when('editar informacion de monto con valores menores a veinte')
def step_impl(context):
    campo_monto = context.driver.find_element(By.NAME, 'monto')
    campo_monto.clear()
    campo_monto.send_keys('10')  # Ingresa un valor menor a veinte
    context.driver.find_element(By.NAME, 'rechazarConfirmar').click()
    screenshot_path = take_screenshot(context, 'editar_monto_menor_veinte')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Editar monto con valor menor a veinte")


@then('revisar informacion no editada en la tabla y mensaje de error')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'resumen-general'))
    )
    tabla = context.driver.find_element(By.ID, 'resumen-general')
    filas = tabla.find_elements(By.TAG_NAME, 'tr')

    assert len(filas) > 1, "La tabla está vacía o no se encontró la información."

    # Verifica que la tabla contiene los datos originales sin cambios
    datos_originales = [fila.text for fila in filas[1:]]  # Asume que la primera fila es el encabezado

    assert any(datos_originales), "No se encontró información en la tabla."

    # Verifica si se muestra el mensaje de error esperado
    mensaje_error = context.driver.find_element(By.ID, 'mensajeError')  # Asegúrate de que este ID sea correcto
    assert mensaje_error.is_displayed(), "No se mostró el mensaje de error."

    screenshot_path = take_screenshot(context, 'revisar_informacion_no_editada_mensaje_error')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Revisar información no editada y mensaje de error")

    context.driver.quit()
#-----------------------------------------------------------------------------------

@given('Abrir navegador editar informacion campos vacios')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/busquedaP.php')
    screenshot_path = take_screenshot(context, 'abrir_navegador_editar_campos_vacios')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador para editar información con campos vacíos")


@when('seleccionar filas a editar con campos vacios')
def step_impl(context):
    # Selecciona la primera fila de la tabla para edición
    fila = context.driver.find
    (By.XPATH, '//table[@id="resumen-general"]/tbody/tr[2]')  # Asume que la primera fila es encabezado
    fila.click()
    screenshot_path = take_screenshot(context, 'seleccionar_filas_editar_campos_vacios')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar filas para editar con campos vacíos")


@then('presionar boton a editar con campos vacios')
def step_impl(context):
    boton_editar = context.driver.find_element(By.ID, 'modificarBoton')
    boton_editar.click()
    screenshot_path = take_screenshot(context, 'presionar_boton_editar_campos_vacios')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Presionar botón de editar con campos vacíos")


@when('editar informacion dejando los campos vacios')
def step_impl(context):
    campo_monto = context.driver.find_element(By.NAME, 'monto')
    campo_monto.clear()  # Deja el campo vacío
    context.driver.find_element(By.NAME, 'rechazarConfirmar').click()
    screenshot_path = take_screenshot(context, 'editar_informacion_campos_vacios')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Editar información dejando los campos vacíos")


@then('verificar mensaje de error por campos vacios')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'mensajeError'))
    )
    mensaje_error = context.driver.find_element(By.ID, 'mensajeError')
    assert mensaje_error.is_displayed(), "No se mostró el mensaje de error por campos vacíos."

    screenshot_path = take_screenshot(context, 'verificar_mensaje_error_campos_vacios')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificar mensaje de error por campos vacíos")


@when('cerrar ventaja emergente de editar informacion')
def step_impl(context):
    cerrar_ventana = context.driver.find_element(By.CLASS_NAME, 'cerrarVentana')  # Asegúrate de que el selector es correcto
    cerrar_ventana.click()
    screenshot_path = take_screenshot(context, 'cerrar_ventana_emergente')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Cerrar ventana emergente de editar información")


@then('revisar informacion no editada con campos vacios')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'resumen-general'))
    )
    tabla = context.driver.find_element(By.ID, 'resumen-general')
    filas = tabla.find_elements(By.TAG_NAME, 'tr')

    assert len(filas) > 1, "La tabla está vacía o no se encontró la información."

    # Verifica que la tabla contiene los datos originales sin cambios
    datos_originales = [fila.text for fila in filas[1:]]  # Asume que la primera fila es el encabezado

    assert any(datos_originales), "No se encontró información en la tabla."

    screenshot_path = take_screenshot(context, 'revisar_informacion_no_editada_campos_vacios')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Revisar información no editada con campos vacíos")

    context.driver.quit()
