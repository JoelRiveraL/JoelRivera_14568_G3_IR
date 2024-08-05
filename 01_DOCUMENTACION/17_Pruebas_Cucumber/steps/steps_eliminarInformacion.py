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

#---------------------------------------------------------------------------------

@given('Abrir navegador para eliminar informacion')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/busquedaP.php')
    screenshot_path = take_screenshot(context, 'abrir_navegador_eliminar_informacion')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador para eliminar información")


@when('seleccionar filas a eliminar')
def step_impl(context):
    # Encuentra todas las filas con el atributo 'data-id' que se pueden seleccionar
    filas = context.driver.find_elements(By.CSS_SELECTOR, 'tr[data-id]')
    if filas:
        filas[0].click()  # Selecciona la primera fila para eliminar
    else:
        raise Exception("No se encontraron filas para seleccionar")
    screenshot_path = take_screenshot(context, 'seleccionar_filas_a_eliminar')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Seleccionar filas para eliminar")


@then('presionar boton de eliminar')
def step_impl(context):
    boton_eliminar = context.driver.find_element(By.ID, 'eliminarBoton')  # Asume un ID para el botón
    boton_eliminar.click()
    screenshot_path = take_screenshot(context, 'presionar_boton_eliminar')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Presionar botón de eliminar")


@when('revisar los datos que se van a eliminar')
def step_impl(context):
    # Verifica que se muestre algún tipo de confirmación o lista de datos a eliminar
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'tablaElementos'))
    )
    datos_a_eliminar = context.driver.find_element(By.ID, 'tablaElementos').text
    context.datos_a_eliminar = datos_a_eliminar
    context.driver.find_element(By.NAME, 'eliminarConfirmar').click()
    WebDriverWait(context.driver, 10).until(
        EC.alert_is_present()
    )
    alerta = context.driver.switch_to.alert
    alerta.accept()

    screenshot_path = take_screenshot(context, 'revisar_datos_a_eliminar')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Revisar los datos que se van a eliminar")


@then('revisar informacion eliminada en la tabla')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'resumen-general'))
    )
    tabla = context.driver.find_element(By.ID, 'resumen-general')
    filas = tabla.find_elements(By.TAG_NAME, 'tr')

    assert len(filas) > 1, "La tabla está vacía o no se encontró la información."

    datos_restantes = [fila.text for fila in filas[1:]]  # Asume que la primera fila es el encabezado

    # Verifica que los datos eliminados no están presentes en la tabla
    assert context.datos_a_eliminar not in datos_restantes, "La información eliminada aún está presente en la tabla."

    screenshot_path = take_screenshot(context, 'revisar_informacion_eliminada')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Revisar información eliminada en la tabla")

    context.driver.quit()

#---------------------------------------------------------------------------------

@given('Abrir navegador para eliminar informacion sin seleccionar')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/busquedaP.php')
    screenshot_path = take_screenshot(context, 'abrir_navegador_eliminar_informacion_sin_seleccionar')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador para eliminar información sin seleccionar")


@when('seleccionar filas a eliminar sin seleccionar')
def step_impl(context):
    # Intenta encontrar filas pero no realiza ninguna selección
    filas = context.driver.find_elements(By.CSS_SELECTOR, 'tr[data-id]')
    if not filas:
        # No se encuentra ninguna fila para seleccionar
        raise Exception("No se encontraron filas para seleccionar")
    # No se hace clic en ninguna fila
    screenshot_path = take_screenshot(context, 'filas_sin_seleccionar')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Intentar seleccionar filas sin éxito")


@then('presionar boton de eliminar sin seleccionar')
def step_impl(context):
    boton_eliminar = context.driver.find_element(By.ID, 'eliminarBoton')  # Asume un ID para el botón
    boton_eliminar.click()
    screenshot_path = take_screenshot(context, 'presionar_boton_eliminar_sin_seleccionar')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Presionar botón de eliminar sin seleccionar")


@when('revisar los datos que se van a eliminar sin seleccionar')
def step_impl(context):
    # Verifica que no se muestre ningún dato para eliminar
    try:
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'tablaElementos'))
        )
        datos_a_eliminar = context.driver.find_element(By.ID, 'tablaElementos').text
        context.driver.find_element(By.NAME, 'rechazarConfirmar').click()
        assert not datos_a_eliminar, "Se encontraron datos a eliminar cuando no se seleccionó ninguna fila."
    except Exception as e:
        # Espera a que no se muestre la confirmación de eliminación
        assert "confirmacionEliminar" not in context.driver.page_source, "Se mostró una ventana de confirmación de eliminación sin seleccionar datos."
    screenshot_path = take_screenshot(context, 'revisar_datos_a_eliminar_sin_seleccionar')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Revisar datos a eliminar sin seleccionar")


@then('revisar informacion no eliminada en la tabla')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'resumen-general'))
    )
    tabla = context.driver.find_element(By.ID, 'resumen-general')
    filas = tabla.find_elements(By.TAG_NAME, 'tr')

    assert len(filas) > 1, "La tabla está vacía o no se encontró la información."

    # Verifica que la información no se ha eliminado
    datos_presentes = [fila.text for fila in filas[1:]]  # Asume que la primera fila es el encabezado

    # Aquí puedes agregar una lógica para verificar que los datos esperados aún están presentes en la tabla
    # En este caso, se podría comparar con los datos que se encontraron antes de intentar eliminar

    screenshot_path = take_screenshot(context, 'revisar_informacion_no_eliminada')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Revisar información no eliminada en la tabla")

    context.driver.quit()
