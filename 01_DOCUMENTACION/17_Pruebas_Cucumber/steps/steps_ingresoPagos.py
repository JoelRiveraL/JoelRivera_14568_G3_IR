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

@given('Abrir navegador de ingreso de pagos')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/registroPagos.php')
    screenshot_path = take_screenshot(context, 'open_browser')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")


@when('proporcionar datos válidos en la búsqueda del residente')
def step_impl(context):
    context.driver.find_element(By.NAME, 'idConsulta').send_keys('1722263009')  # Buscar por cédula
    screenshot_path = take_screenshot(context, 'validSearch')
    context.driver.find_element(By.NAME, 'idBuscar').click()  # Botón de búsqueda
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Búsqueda de residente")


@then('verificar mensaje de existencia del residente')
def step_impl(context):
    try:
        mensaje_elemento = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'mensajeUsuarioEncontrado'))
        )
        mensaje_texto = mensaje_elemento.text
        assert "Usuario Encontrado" in mensaje_texto, "El mensaje no es el esperado para residente encontrado."

        screenshot_path = take_screenshot(context, 'verificacion_mensaje_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del mensaje de existencia del residente")

    except Exception as e:
        screenshot_path = take_screenshot(context, 'error_verificacion_mensaje_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path,
                              "Error durante la verificación del mensaje de existencia del residente")
        raise AssertionError(f"Error al verificar el mensaje de existencia del residente: {e}")


@When ('ingresar datos de pago')
def step_impl(context):
    # Solo permitimos ingresar el pago si se confirma que el residente existe
    context.driver.find_element(By.NAME, 'pagos').send_keys('60')
    select_tipo_pago = Select(context.driver.find_element(By.NAME, 'tipo_pago'))
    select_tipo_pago.select_by_visible_text('Alicuota')
    date_input = context.driver.find_element(By.NAME, 'fecha')
    date_input.clear()
    date_input.send_keys('08-03-2024')


    screenshot_path = take_screenshot(context, 'datos_de_pago')
    context.driver.find_element(By.NAME, 'enviarBoton').click()  # Botón de enviar
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Ingreso de datos de pago")


@then('verificar mensaje de confirmación de pago')
def step_impl(context):
    try:
        # Espera a que el mensaje esté presente en la página
        mensaje_elemento = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'mensajePago'))
        )

        # Usa JavaScript para desplazar el mensaje a la vista
        context.driver.execute_script("arguments[0].scrollIntoView(true);", mensaje_elemento)

        # Captura el texto del mensaje
        mensaje_texto = mensaje_elemento.text
        assert "¡Pago Registrado!" in mensaje_texto, "El mensaje no es el esperado para confirmación de pago."

        # Toma una captura de pantalla de la página final
        screenshot_path = take_screenshot(context, 'verificacion_mensaje_pago')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del mensaje de confirmación de pago")

    except Exception as e:
        # Si algo falla, toma una captura de pantalla y registra el error
        screenshot_path = take_screenshot(context, 'error_verificacion_mensaje_pago')
        add_screenshot_to_pdf(context.pdf, screenshot_path,
                              "Error durante la verificación del mensaje de confirmación de pago")
        raise AssertionError(f"Error al verificar el mensaje de confirmación de pago: {e}")

#-----------------------------------------------------------------------------
# Caso 2
#-----------------------------------------------------------------------------

@given('Abrir navegador de ingreso de pagos con nombre')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/registroPagos.php')
    screenshot_path = take_screenshot(context, 'open_browser')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")

@when('proporcionar datos válidos en la búsqueda  con nombre del residente')
def step_impl(context):
    context.driver.find_element(By.NAME, 'nombreConsulta').send_keys('Joel')  # Buscar por cédula
    screenshot_path = take_screenshot(context, 'validSearch')
    context.driver.find_element(By.NAME, 'idBuscarResidente').click()  # Botón de búsqueda
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Búsqueda de residente por nombre")

@then('verificar tabla de existencia del residente')
def step_impl(context):
    try:
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'tablaConsultaNombre'))
        )

        # Verifica que la tabla tenga datos
        tabla = context.driver.find_element(By.ID, 'tablaConsultaNombre')
        filas = tabla.find_elements(By.TAG_NAME, 'tr')

        assert len(filas) > 1, "La tabla está vacía o no se encontró."

        encabezados = filas[0].find_elements(By.TAG_NAME, 'th')
        nombres_encabezados = [encabezado.text for encabezado in encabezados]
        expected_headers = ["ID", "Nombre", "Apellido", "Lote"]
        assert set(expected_headers).issubset(set(nombres_encabezados)), "Los encabezados de la tabla no coinciden."

        # Captura una captura de pantalla para verificar visualmente
        screenshot_path = take_screenshot(context, 'verificacion_tabla_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de la tabla de residente")

    except Exception as e:
        screenshot_path = take_screenshot(context, 'error_verificacion_tabla_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Error durante la verificación de la tabla de residente")
        raise AssertionError(f"Error al verificar la tabla de existencia del residente: {e}")

@when('proporcionar datos válidos en la búsqueda  con cedula del residente')
def step_impl(context):
    context.driver.find_element(By.NAME, 'idConsulta').send_keys('1722263009')
    screenshot_path = take_screenshot(context, 'validSearch')
    context.driver.find_element(By.NAME, 'idBuscar').click()
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Búsqueda de residente")

@then('verificar mensaje de existencia del residente despues de buscar por nombre')
def step_impl(context):
    try:
        mensaje_elemento = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'mensajeUsuarioEncontrado'))
        )
        mensaje_texto = mensaje_elemento.text
        assert "Usuario Encontrado" in mensaje_texto, "El mensaje no es el esperado para residente encontrado."

        screenshot_path = take_screenshot(context, 'verificacion_mensaje_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del mensaje de existencia del residente")

    except Exception as e:
        screenshot_path = take_screenshot(context, 'error_verificacion_mensaje_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path,
                              "Error durante la verificación del mensaje de existencia del residente")
        raise AssertionError(f"Error al verificar el mensaje de existencia del residente: {e}")


@When ('ingresar datos de pago despues de buscar por nombre')
def step_impl(context):
    # Solo permitimos ingresar el pago si se confirma que el residente existe
    context.driver.find_element(By.NAME, 'pagos').send_keys('60')
    select_tipo_pago = Select(context.driver.find_element(By.NAME, 'tipo_pago'))
    select_tipo_pago.select_by_visible_text('Alicuota')
    date_input = context.driver.find_element(By.NAME, 'fecha')
    date_input.clear()
    date_input.send_keys('08-03-2024')


    screenshot_path = take_screenshot(context, 'datos_de_pago')
    context.driver.find_element(By.NAME, 'enviarBoton').click()  # Botón de enviar
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Ingreso de datos de pago")


@then('verificar mensaje de confirmación de pago despues de buscar por nombre')
def step_impl(context):
    try:
        # Espera a que el mensaje esté presente en la página
        mensaje_elemento = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'mensajePago'))
        )

        # Usa JavaScript para desplazar el mensaje a la vista
        context.driver.execute_script("arguments[0].scrollIntoView(true);", mensaje_elemento)

        # Captura el texto del mensaje
        mensaje_texto = mensaje_elemento.text
        assert "¡Pago Registrado!" in mensaje_texto, "El mensaje no es el esperado para confirmación de pago."

        # Toma una captura de pantalla de la página final
        screenshot_path = take_screenshot(context, 'verificacion_mensaje_pago')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del mensaje de confirmación de pago")

    except Exception as e:
        # Si algo falla, toma una captura de pantalla y registra el error
        screenshot_path = take_screenshot(context, 'error_verificacion_mensaje_pago')
        add_screenshot_to_pdf(context.pdf, screenshot_path,
                              "Error durante la verificación del mensaje de confirmación de pago")
        raise AssertionError(f"Error al verificar el mensaje de confirmación de pago: {e}")


#-----------------------------------------------------------------------------
# Caso 3
#-----------------------------------------------------------------------------

@given('Abrir navegador de ingreso de pagos con nombre incorrecto')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/registroPagos.php')
    screenshot_path = take_screenshot(context, 'open_browser')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")

@when('proporcionar datos válidos en la búsqueda  con nombre incorrecto del residente')
def step_impl(context):
    context.driver.find_element(By.NAME, 'nombreConsulta').send_keys('Joe')  # Buscar por cédula
    screenshot_path = take_screenshot(context, 'validSearch')
    context.driver.find_element(By.NAME, 'idBuscarResidente').click()  # Botón de búsqueda
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Búsqueda de residente por nombre")

@then('verificar mensaje de nombre incorrecto')
def step_impl(context):
    try:
        mensaje_elemento = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'mensajeNoUsuarioN'))
        )
        mensaje_texto = mensaje_elemento.text
        assert "Usuario No Encontrado" in mensaje_texto, "El mensaje no es el esperado para residente encontrado."

        screenshot_path = take_screenshot(context, 'verificacion_mensaje_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del mensaje de existencia del residente")

    except Exception as e:
        screenshot_path = take_screenshot(context, 'error_verificacion_mensaje_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path,
                              "Error durante la verificación del mensaje de existencia del residente")
        raise AssertionError(f"Error al verificar el mensaje de existencia del residente: {e}")

#-----------------------------------------------------------------------------
# Caso 4
#-----------------------------------------------------------------------------

@given('Abrir navegador de ingreso de pagos incorrecto')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/registroPagos.php')
    screenshot_path = take_screenshot(context, 'open_browser')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")


@when('proporcionar datos válidos en la búsqueda del residente y pagos incorrecto')
def step_impl(context):
    context.driver.find_element(By.NAME, 'idConsulta').send_keys('1722263009')  # Buscar por cédula
    screenshot_path = take_screenshot(context, 'validSearch')
    context.driver.find_element(By.NAME, 'idBuscar').click()  # Botón de búsqueda
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Búsqueda de residente")


@then('verificar mensaje de existencia del residente de pago incorrecto')
def step_impl(context):
    try:
        mensaje_elemento = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'mensajeUsuarioEncontrado'))
        )
        mensaje_texto = mensaje_elemento.text
        assert "Usuario Encontrado" in mensaje_texto, "El mensaje no es el esperado para residente encontrado."

        screenshot_path = take_screenshot(context, 'verificacion_mensaje_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del mensaje de existencia del residente")

    except Exception as e:
        screenshot_path = take_screenshot(context, 'error_verificacion_mensaje_residente')
        add_screenshot_to_pdf(context.pdf, screenshot_path,
                              "Error durante la verificación del mensaje de existencia del residente")
        raise AssertionError(f"Error al verificar el mensaje de existencia del residente: {e}")


@when('ingresar datos de pago incorrecto')
def step_impl(context):
    # Solo permitimos ingresar el pago si se confirma que el residente existe
    context.driver.find_element(By.NAME, 'pagos').send_keys('60')
    # Omite el tipo de pago
    date_input = context.driver.find_element(By.NAME, 'fecha')
    date_input.clear()
    date_input.send_keys('08-03-2024')

    screenshot_path = take_screenshot(context, 'sin_tipo_pago')
    context.driver.find_element(By.NAME, 'enviarBoton').click()
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Ingreso de datos de pago sin el tipo")

@then('verificar mensaje de pago incorrecto')
def step_impl(context):
    try:
        # Comprueba que el campo teléfono está vacío
        telefono_field = context.driver.find_element(By.NAME, 'tipo_pago')
        assert telefono_field.get_attribute('value') == '', "El campo tipo_pago no está vacío."

        submit_button = context.driver.find_element(By.NAME, 'enviarBoton')
        submit_button.click()

        time.sleep(2)

        # Captura la pantalla de la notificación de validación
        screenshot_path = take_screenshot(context, 'campo_requerido_mensaje')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de mensaje de campo requerido")

        telefono_field.click()

        current_url = context.driver.current_url
        expected_url = 'http://localhost/UrbanizationTreasury_P2/Principal/registroPagos.php'
        assert current_url == expected_url, "El formulario fue enviado, pero no debería haberlo sido."

        # También podemos verificar si el atributo validity está incorrecto, pero Selenium no tiene acceso directo a esto
        assert not telefono_field.get_attribute('validity').valid, "El campo teléfono fue validado incorrectamente."

    except Exception as e:
        add_screenshot_to_pdf(context.pdf, "Error durante la verificación del mensaje de campo requerido")
        raise AssertionError(f"Error al verificar el mensaje de campo requerido: {e}")