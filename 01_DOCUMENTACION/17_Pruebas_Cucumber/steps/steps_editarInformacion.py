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
    context.driver.find_element(By.ID, 'montoEditable').send_keys('1')

    # Agregar más campos según sea necesario

    context.driver.find_element(By.NAME, 'modificarConfirmar').click()  # Asume un botón para guardar cambios
    screenshot_path = take_screenshot(context, 'editar_informacion')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Editar información con datos correctos")


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
    assert '1' in datos_editados, "El dato editado no se encontró en la columna especificada."

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

    # Agregar más campos según sea necesario

    context.driver.find_element(By.NAME, 'modificarConfirmar').click()  # Asume un botón para guardar cambios
    screenshot_path = take_screenshot(context, 'editar_informacion')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Editar información con datos correctos")


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

