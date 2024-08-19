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

@given('Abrir navegador busqueda de residentes')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/busquedaR.php')
    screenshot_path = take_screenshot(context, 'open_browser')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")


@then('verificar tabla de existencia de resumen general residentes')
def step_impl(context):
    try:
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'resumen-general'))
        )

        # Verifica que la tabla tenga datos
        tabla = context.driver.find_element(By.ID, 'resumen-general')
        filas = tabla.find_elements(By.TAG_NAME, 'tr')

        assert len(filas) > 1, "La tabla está vacía o no se encontró."

        encabezados = filas[0].find_elements(By.TAG_NAME, 'th')
        nombres_encabezados = [encabezado.text for encabezado in encabezados]
        expected_headers = ["ID Residente", "Cedula", "Nombre", "Apellido", "Correo", "Telefono", "Lote"]
        assert set(expected_headers).issubset(set(nombres_encabezados)), "Los encabezados de la tabla no coinciden."

        # Captura una captura de pantalla para verificar visualmente
        screenshot_path = take_screenshot(context, 'verificacion_tabla_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de la tabla de residente")

    except Exception as e:
        screenshot_path = take_screenshot(context, 'error_verificacion_tabla_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Error durante la verificación de la tabla de residente")
        raise AssertionError(f"Error al verificar la tabla de existencia del residente: {e}")

#---------------------------------------------------------------------------------
# Caso 2
#---------------------------------------------------------------------------------

@given('Abrir navegador busqueda de residente especifico')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/busquedaR.php')
    screenshot_path = take_screenshot(context, 'open_browser')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")

@when('ingresar datos de busqueda del residente cedula')
def step_impl(context):
    context.driver.find_element(By.NAME, 'cedula').send_keys('1722263009')  # Buscar por cédula
    screenshot_path = take_screenshot(context, 'validSearch')
    context.driver.find_element(By.NAME, 'buscarR').click()  # Botón de búsqueda
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Búsqueda de residente por cedula")


@then('verificar tabla de datos del residente especifico')
def step_impl(context):
    try:
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'resumen-residente'))
        )

        # Verifica que la tabla tenga datos
        tabla = context.driver.find_element(By.ID, 'resumen-residente')
        filas = tabla.find_elements(By.TAG_NAME, 'tr')

        assert len(filas) > 1, "La tabla está vacía o no se encontró."

        encabezados = filas[0].find_elements(By.TAG_NAME, 'th')
        nombres_encabezados = [encabezado.text for encabezado in encabezados]
        expected_headers = ["ID Residente", "Cedula", "Nombre", "Apellido", "Correo", "Telefono", "Lote"]
        assert set(expected_headers).issubset(set(nombres_encabezados)), "Los encabezados de la tabla no coinciden."

        # Captura una captura de pantalla para verificar visualmente
        screenshot_path = take_screenshot(context, 'verificacion_tabla_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de la tabla de residente")

    except Exception as e:
        screenshot_path = take_screenshot(context, 'error_verificacion_tabla_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Error durante la verificación de la tabla de residente")
        raise AssertionError(f"Error al verificar la tabla de existencia del residente: {e}")


#---------------------------------------------------------------------------------
# Caso 3
#---------------------------------------------------------------------------------

@given('Abrir navegador busqueda de residente por nombre especifico')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/busquedaR.php')
    screenshot_path = take_screenshot(context, 'open_browser')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")

@when('ingresar datos de busqueda del residente por nombre')
def step_impl(context):
    context.driver.find_element(By.NAME, 'nombre').send_keys('Joel')  # Buscar por cédula
    screenshot_path = take_screenshot(context, 'validSearch')
    context.driver.find_element(By.NAME, 'buscarRNombre').click()  # Botón de búsqueda
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Búsqueda de residente por nombre")


@then('verificar tabla de datos del residente especifico por nombre')
def step_impl(context):
    try:
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'resumen-residente'))
        )

        # Verifica que la tabla tenga datos
        tabla = context.driver.find_element(By.ID, 'resumen-residente')
        filas = tabla.find_elements(By.TAG_NAME, 'tr')

        assert len(filas) > 1, "La tabla está vacía o no se encontró."

        encabezados = filas[0].find_elements(By.TAG_NAME, 'th')
        nombres_encabezados = [encabezado.text for encabezado in encabezados]
        expected_headers = ["ID Residente", "Cedula", "Nombre", "Apellido", "Correo", "Telefono", "Lote"]
        assert set(expected_headers).issubset(set(nombres_encabezados)), "Los encabezados de la tabla no coinciden."

        # Captura una captura de pantalla para verificar visualmente
        screenshot_path = take_screenshot(context, 'verificacion_tabla_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de la tabla de residente")

    except Exception as e:
        screenshot_path = take_screenshot(context, 'error_verificacion_tabla_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Error durante la verificación de la tabla de residente")
        raise AssertionError(f"Error al verificar la tabla de existencia del residente: {e}")

#---------------------------------------------------------------------------------
# Caso 4
#---------------------------------------------------------------------------------

@given('Abrir navegador busqueda de residente especifico datos erroneos')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/busquedaR.php')
    screenshot_path = take_screenshot(context, 'open_browser')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")

@when('ingresar datos de busqueda del residente cedula datos erroneos')
def step_impl(context):
    context.driver.find_element(By.NAME, 'nombre').send_keys('Joe')
    screenshot_path = take_screenshot(context, 'validSearch')
    context.driver.find_element(By.NAME, 'buscarRNombre').click()  # Botón de búsqueda
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Búsqueda de residente por nombre")


@then('verificar mensaje de error datos erroneos')
def step_impl(context):
    try:
        mensaje_elemento = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'noResultados'))
        )
        mensaje_texto = mensaje_elemento.text
        assert "No se encontraron resultados" in mensaje_texto, "El mensaje no es el esperado para no resultados"

        screenshot_path = take_screenshot(context, 'verificacion_mensaje_resultados')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del mensaje de inexistencia de datos")

    except Exception as e:
        screenshot_path = take_screenshot(context, 'error_verificacion_mensaje_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path,
                              "Error durante la verificación del mensaje de existencia del residente")
        raise AssertionError(f"Error al verificar el mensaje de existencia del residente: {e}")

#---------------------------------------------------------------------------------
# Caso 5
#---------------------------------------------------------------------------------

@given('Abrir navegador busqueda de residente espe cifico cedula erronea')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/busquedaR.php')
    screenshot_path = take_screenshot(context, 'open_browser')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")

@when('ingresar datos de busqueda del residente por cedula incorrecta')
def step_impl(context):
    context.driver.find_element(By.NAME, 'cedula').send_keys('11112312')
    screenshot_path = take_screenshot(context, 'validSearch')
    context.driver.find_element(By.NAME, 'buscarR').click()  # Botón de búsqueda
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Búsqueda de residente por cedula erronea")


@then('verificar mensaje de error cedula incorrecta')
def step_impl(context):
    try:
        mensaje_elemento = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'noResultados'))
        )
        mensaje_texto = mensaje_elemento.text
        assert "No se encontraron resultados" in mensaje_texto, "El mensaje no es el esperado para no resultados"

        screenshot_path = take_screenshot(context, 'verificacion_mensaje_resultados')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del mensaje de inexistencia de datos")

    except Exception as e:
        screenshot_path = take_screenshot(context, 'error_verificacion_mensaje_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path,
                              "Error durante la verificación del mensaje de existencia del residente")
        raise AssertionError(f"Error al verificar el mensaje de existencia del residente: {e}")

#---------------------------------------------------------------------------------
# Caso 6
#---------------------------------------------------------------------------------

@given('Abrir navegador de busqueda de residente especifico campo vacio cedula')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/busquedaR.php')
    screenshot_path = take_screenshot(context, 'open_browser')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")

@when('presionar boton de buscar en el campo de cedula sin ingresar datos')
def step_impl(context):
    context.driver.find_element(By.NAME, 'cedula').send_keys('')
    screenshot_path = take_screenshot(context, 'validSearch')
    context.driver.find_element(By.NAME, 'buscarR').click()  # Botón de búsqueda
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Búsqueda de residente por cedula erronea")


@then('verificar mensaje de error de campo vacio cedula')
def step_impl(context):
    try:
        mensaje_elemento = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'noResultados'))
        )
        mensaje_texto = mensaje_elemento.text
        assert "No se encontraron resultados" in mensaje_texto, "El mensaje no es el esperado para no resultados"

        screenshot_path = take_screenshot(context, 'verificacion_mensaje_resultados')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del mensaje de inexistencia de datos")

    except Exception as e:
        screenshot_path = take_screenshot(context, 'error_verificacion_mensaje_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path,
                              "Error durante la verificación del mensaje de existencia del residente")
        raise AssertionError(f"Error al verificar el mensaje de existencia del residente: {e}")

#---------------------------------------------------------------------------------
# Caso 7
#---------------------------------------------------------------------------------

@given('Abrir navegador busqueda de residente especifico campo vacio nombre')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/busquedaR.php')
    screenshot_path = take_screenshot(context, 'open_browser')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")

@when('presionar boton de buscar en el campo de nombre sin ingresar datos')
def step_impl(context):
    context.driver.find_element(By.NAME, 'cedula').send_keys('')
    screenshot_path = take_screenshot(context, 'validSearch')
    context.driver.find_element(By.NAME, 'buscarR').click()  # Botón de búsqueda
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Búsqueda de residente por cedula erronea")

@then('verificar mensaje de error de campo vacio nombre')
def step_impl(context):
    try:
        mensaje_elemento = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'noResultados'))
        )
        mensaje_texto = mensaje_elemento.text
        assert "No se encontraron resultados" in mensaje_texto, "El mensaje no es el esperado para no resultados"

        screenshot_path = take_screenshot(context, 'verificacion_mensaje_resultados')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del mensaje de inexistencia de datos")

    except Exception as e:
        screenshot_path = take_screenshot(context, 'error_verificacion_mensaje_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path,
                              "Error durante la verificación del mensaje de existencia del residente")
        raise AssertionError(f"Error al verificar el mensaje de existencia del residente: {e}")
