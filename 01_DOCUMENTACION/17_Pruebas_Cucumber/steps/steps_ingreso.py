from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from fpdf import FPDF
import os
import time

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

@given('Abrir navegador de ingreso de residentes')
def open_browser(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/registroResidente.php')
    screenshot_path = take_screenshot(context, 'open_browser')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")

@when('proporicionar datos validos en el formulario')
def validUserNameAndPassword(context):
    ensure_pdf_initialized(context)
    context.driver.find_element(By.NAME, 'id').send_keys('1726781402')
    context.driver.find_element(By.NAME, 'nombre').send_keys('Leonardo')
    context.driver.find_element(By.NAME, 'apellido').send_keys('Yaranga')
    context.driver.find_element(By.NAME, 'correo').send_keys('leo@gmail.com')
    context.driver.find_element(By.NAME, 'telefono').send_keys('0962974818')
    context.driver.find_element(By.NAME, 'departamento').send_keys('2')

    screenshot_path = take_screenshot(context, 'validInputs')
    context.driver.find_element(By.NAME, 'enviarResidente').click()
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Proporcionar credenciales válidas")


@then('verificar mensaje de confirmacion de ingreso')
def verificar_mensaje_confirmacion(context):
    ensure_pdf_initialized(context)
    try:
        # Espera a que el mensaje esté presente en la página
        mensaje_elemento = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'mensaje'))
        )
        # Captura el texto del mensaje
        mensaje_texto = mensaje_elemento.text

        # Mensajes esperados según la lógica PHP
        cedula_ya_registrada = "Cedula ya registrada"
        cedula_no_valida = "Cedula no valida"
        registro_exitoso = "¡Datos enviados con éxito!"
        error_ingreso = "Error al insertar datos: "

        # Comprobamos si el mensaje es el esperado
        if cedula_ya_registrada in mensaje_texto:
            assert cedula_ya_registrada in mensaje_texto, "El mensaje no es el esperado para cédula ya registrada."
        elif cedula_no_valida in mensaje_texto:
            assert cedula_no_valida in mensaje_texto, "El mensaje no es el esperado para cédula no válida."
        elif registro_exitoso in mensaje_texto:
            assert registro_exitoso in mensaje_texto, "El mensaje no es el esperado para registro exitoso."
        elif error_ingreso in mensaje_texto:
            assert error_ingreso in mensaje_texto, "El mensaje no es el esperado para error al ingresar datos."
        else:
            raise AssertionError("Mensaje inesperado encontrado: " + mensaje_texto)

        # Toma una captura de pantalla de la página final
        screenshot_path = take_screenshot(context, 'verificacion_mensaje')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del mensaje de confirmación")

    except Exception as e:
        # Si algo falla, toma una captura de pantalla y registra el error
        screenshot_path = take_screenshot(context, 'error_verificacion_mensaje')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Error durante la verificación del mensaje")
        raise AssertionError(f"Error al verificar el mensaje de confirmación: {e}")

#------------------------------------------------------------------------------

@given('Abrir navegador de ingreso de residentes con cedula repetida')
def open_browser(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/registroResidente.php')
    screenshot_path = take_screenshot(context, 'open_browser')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")

@when('proporicionar datos validos en el formulario con cedula repetida')
def validUserNameAndPassword(context):
    ensure_pdf_initialized(context)
    context.driver.find_element(By.NAME, 'id').send_keys('1722263009')
    context.driver.find_element(By.NAME, 'nombre').send_keys('Joel')
    context.driver.find_element(By.NAME, 'apellido').send_keys('Rivera')
    context.driver.find_element(By.NAME, 'correo').send_keys('joelale033@gmail.com')
    context.driver.find_element(By.NAME, 'telefono').send_keys('0962974817')
    context.driver.find_element(By.NAME, 'departamento').send_keys('67')

    screenshot_path = take_screenshot(context, 'validInputs')
    context.driver.find_element(By.NAME, 'enviarResidente').click()
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Proporcionar credenciales válidas")

@then('verificar mensaje de confirmacion de ingreso con cedula repetida')
def verificar_mensaje_confirmacion(context):
    ensure_pdf_initialized(context)
    try:
        # Espera a que el mensaje esté presente en la página
        mensaje_elemento = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'mensaje'))
        )
        # Captura el texto del mensaje
        mensaje_texto = mensaje_elemento.text

        # Mensajes esperados según la lógica PHP
        cedula_ya_registrada = "Cedula ya registrada"
        cedula_no_valida = "Cedula no valida"
        registro_exitoso = "¡Datos enviados con éxito!"
        error_ingreso = "Error al insertar datos: "

        # Comprobamos si el mensaje es el esperado
        if cedula_ya_registrada in mensaje_texto:
            assert cedula_ya_registrada in mensaje_texto, "El mensaje no es el esperado para cédula ya registrada."
        elif cedula_no_valida in mensaje_texto:
            assert cedula_no_valida in mensaje_texto, "El mensaje no es el esperado para cédula no válida."
        elif registro_exitoso in mensaje_texto:
            assert registro_exitoso in mensaje_texto, "El mensaje no es el esperado para registro exitoso."
        elif error_ingreso in mensaje_texto:
            assert error_ingreso in mensaje_texto, "El mensaje no es el esperado para error al ingresar datos."
        else:
            raise AssertionError("Mensaje inesperado encontrado: " + mensaje_texto)

        # Toma una captura de pantalla de la página final
        screenshot_path = take_screenshot(context, 'verificacion_mensaje')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del mensaje de confirmación")

    except Exception as e:
        # Si algo falla, toma una captura de pantalla y registra el error
        screenshot_path = take_screenshot(context, 'error_verificacion_mensaje')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Error durante la verificación del mensaje")
        raise AssertionError(f"Error al verificar el mensaje de confirmación: {e}")

#------------------------------------------------------------------------------

@given('Abrir navegador de ingreso de residentes con cedula no valida')
def open_browser(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/registroResidente.php')
    screenshot_path = take_screenshot(context, 'open_browser')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")

@when('proporicionar datos validos en el formulario con cedula no valida')
def validUserNameAndPassword(context):
    ensure_pdf_initialized(context)
    context.driver.find_element(By.NAME, 'id').send_keys('1722263010')
    context.driver.find_element(By.NAME, 'nombre').send_keys('Joel')
    context.driver.find_element(By.NAME, 'apellido').send_keys('Rivera')
    context.driver.find_element(By.NAME, 'correo').send_keys('joelale033@gmail.com')
    context.driver.find_element(By.NAME, 'telefono').send_keys('0962974817')
    context.driver.find_element(By.NAME, 'departamento').send_keys('67')

    screenshot_path = take_screenshot(context, 'validInputs')
    context.driver.find_element(By.NAME, 'enviarResidente').click()
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Proporcionar credenciales válidas")

@then('verificar mensaje de confirmacion de ingreso con cedula no valida')
def verificar_mensaje_confirmacion(context):
    ensure_pdf_initialized(context)
    try:
        # Espera a que el mensaje esté presente en la página
        mensaje_elemento = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'mensaje'))
        )
        # Captura el texto del mensaje
        mensaje_texto = mensaje_elemento.text

        # Mensajes esperados según la lógica PHP
        cedula_ya_registrada = "Cedula ya registrada"
        cedula_no_valida = "Cedula no valida"
        registro_exitoso = "¡Datos enviados con éxito!"
        error_ingreso = "Error al insertar datos: "

        # Comprobamos si el mensaje es el esperado
        if cedula_ya_registrada in mensaje_texto:
            assert cedula_ya_registrada in mensaje_texto, "El mensaje no es el esperado para cédula ya registrada."
        elif cedula_no_valida in mensaje_texto:
            assert cedula_no_valida in mensaje_texto, "El mensaje no es el esperado para cédula no válida."
        elif registro_exitoso in mensaje_texto:
            assert registro_exitoso in mensaje_texto, "El mensaje no es el esperado para registro exitoso."
        elif error_ingreso in mensaje_texto:
            assert error_ingreso in mensaje_texto, "El mensaje no es el esperado para error al ingresar datos."
        else:
            raise AssertionError("Mensaje inesperado encontrado: " + mensaje_texto)

        # Toma una captura de pantalla de la página final
        screenshot_path = take_screenshot(context, 'verificacion_mensaje')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del mensaje de confirmación")

    except Exception as e:
        # Si algo falla, toma una captura de pantalla y registra el error
        screenshot_path = take_screenshot(context, 'error_verificacion_mensaje')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Error durante la verificación del mensaje")
        raise AssertionError(f"Error al verificar el mensaje de confirmación: {e}")


#---------------------------------------------------------------------------------

@given('Abrir navegador de ingreso de residentes con datos incompletos')
def open_browser(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/UrbanizationTreasury_P2/Principal/registroResidente.php')
    screenshot_path = take_screenshot(context, 'open_browser')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")


@when('proporicionar datos validos en el formulario con datos incompletos')
def step_impl(context):
    context.driver.find_element(By.NAME, 'id').send_keys('1726781402')
    context.driver.find_element(By.NAME, 'nombre').send_keys('Leonardo')
    context.driver.find_element(By.NAME, 'apellido').send_keys('Yaranga')
    context.driver.find_element(By.NAME, 'correo').send_keys('leo@gmail.com')
    context.driver.find_element(By.NAME, 'departamento').send_keys('2')
    # No llenamos el campo 'telefono' para desencadenar la validación

    screenshot_path = take_screenshot(context, 'missingPhone')
    context.driver.find_element(By.NAME, 'enviarResidente').click()
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Intentar enviar formulario sin teléfono")

@then('verificar mensaje de confirmacion de ingreso con datos incompletos')
def step_impl(context):
    # Aquí es donde verificamos que el mensaje de validación nativo del navegador esté presente.
    # Para esto, verificamos si el campo no ha sido enviado y esperamos la presencia de la notificación.

    try:
        # Comprueba que el campo teléfono está vacío
        telefono_field = context.driver.find_element(By.NAME, 'telefono')
        assert telefono_field.get_attribute('value') == '', "El campo teléfono no está vacío."

        submit_button = context.driver.find_element(By.NAME, 'enviarResidente')
        submit_button.click()

        # Espera a que el navegador muestre la validación nativa
        time.sleep(1)  # Puede variar según la velocidad del navegador

        # Captura la pantalla de la notificación de validación
        screenshot_path = take_screenshot(context, 'campo_requerido_mensaje')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de mensaje de campo requerido")

        telefono_field.click()

        current_url = context.driver.current_url
        expected_url = 'http://localhost/UrbanizationTreasury_P2/Principal/registroResidente.php'
        assert current_url == expected_url, "El formulario fue enviado, pero no debería haberlo sido."

        # También podemos verificar si el atributo validity está incorrecto, pero Selenium no tiene acceso directo a esto
        assert not telefono_field.get_attribute('validity').valid, "El campo teléfono fue validado incorrectamente."

    except Exception as e:
        add_screenshot_to_pdf(context.pdf, "Error durante la verificación del mensaje de campo requerido")
        raise AssertionError(f"Error al verificar el mensaje de campo requerido: {e}")