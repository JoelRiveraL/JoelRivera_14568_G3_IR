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

@given('abrir navegador')
def open_browser(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/CodigoR1/index.html')
    screenshot_path = take_screenshot(context, 'open_browser')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")

@when('proporcionando un nombre de usuario y contraseña válidos')
def validUserNameAndPassword(context):
    ensure_pdf_initialized(context)
    context.driver.find_element(By.NAME, 'usuario').send_keys('Patricia123')
    context.driver.find_element(By.NAME, 'password').send_keys('Patricia123')
    screenshot_path = take_screenshot(context, 'validUserNameAndPassword')
    context.driver.find_element(By.NAME, 'submit').click()
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Proporcionar credenciales válidas")

@then('Verificando pagina')
def verificacion_AdminHome(context):
    ensure_pdf_initialized(context)
    WebDriverWait(context.driver, 10).until(EC.title_is("Admin"))
    assert context.driver.title == "Admin"
    screenshot_path = take_screenshot(context, 'verificacion_AdminHome')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de la página de administrador")

# Residente

@given('abrir navegador residente')
def open_browser_residente(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/CodigoR1/index.html')
    screenshot_path = take_screenshot(context, 'open_browser_residente')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador para residente")

@when('proporcionando un nombre de usuario y contraseña válidos residente')
def validUserNameAndPassword_residente(context):
    ensure_pdf_initialized(context)
    context.driver.find_element(By.NAME, 'usuario').send_keys('User123')
    context.driver.find_element(By.NAME, 'password').send_keys('User123')
    screenshot_path = take_screenshot(context, 'validUserNameAndPassword_residente')
    context.driver.find_element(By.NAME, 'submit').click()
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Proporcionar credenciales de residente")

@then('Verificando pagina residente')
def verificacion_ResidenteHome(context):
    ensure_pdf_initialized(context)
    WebDriverWait(context.driver, 10).until(EC.title_is("Residente"))
    assert context.driver.title == "Residente"
    screenshot_path = take_screenshot(context, 'verificacion_ResidenteHome')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de la página de residente")

# Incorrecto Usuario

@given('abrir navegador incorrecto usuario')
def open_browser_invalid(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/CodigoR1/index.html')
    screenshot_path = take_screenshot(context, 'open_browser_invalid')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador con usuario incorrecto")

@when('proporcionando un nombre de usuario incorrecto y contraseña')
def invalidUserNameAndPassword(context):
    ensure_pdf_initialized(context)
    context.driver.find_element(By.NAME, 'usuario').send_keys('OOOOOOOOO')
    context.driver.find_element(By.NAME, 'password').send_keys('Patricia123')
    screenshot_path = take_screenshot(context, 'invalidUserNameAndPassword')
    context.driver.find_element(By.NAME, 'submit').click()
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Proporcionar credenciales incorrectas")

@then('Verificando pagina incorrecto usuario')
def verificar_mensaje_error(context):
    ensure_pdf_initialized(context)
    alert = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'customAlert'))
    )
    assert alert.is_displayed(), "El mensaje de error no se muestra."
    assert "Usuario o contraseña incorrectos" in alert.text, "El texto del mensaje de error no coincide."
    screenshot_path = take_screenshot(context, 'verificar_mensaje_error')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del mensaje de error")


@given('abrir navegador incorrecto password')
def open_browser_invalid(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/CodigoR1/index.html')
    screenshot_path = take_screenshot(context, 'open_browser_invalid')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador con contraseña incorrecta")

@when('proporcionando un nombre de incorrecto y contraseña incorrecta')
def invalidUserNameAndPassword(context):
    ensure_pdf_initialized(context)
    context.driver.find_element(By.NAME, 'usuario').send_keys('User123')
    context.driver.find_element(By.NAME, 'password').send_keys('User12w4')
    screenshot_path = take_screenshot(context, 'invalidUserNameAndPassword')
    context.driver.find_element(By.NAME, 'submit').click()
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Proporcionar contraseña incorrecta")

@then('Verificando pagina incorrecto contraseña')
def verificar_mensaje_error(context):
    ensure_pdf_initialized(context)
    alert = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'customAlert'))
    )
    assert alert.is_displayed(), "El mensaje de error no se muestra."
    assert "Usuario o contraseña incorrectos" in alert.text, "El texto del mensaje de error no coincide."
    screenshot_path = take_screenshot(context, 'verificar_mensaje_error')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del mensaje de error")


@given('abrir navegador contraseña y usuario incorrectos')
def open_browser_invalid(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/CodigoR1/index.html')
    screenshot_path = take_screenshot(context, 'open_browser_invalid')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador con contraseña y usuario incorrectos")

@when('proporcionando un nombre de incorrecto y contraseña incorrectos')
def invalidUserNameAndPassword(context):
    ensure_pdf_initialized(context)
    context.driver.find_element(By.NAME, 'usuario').send_keys('aaaaa')
    context.driver.find_element(By.NAME, 'password').send_keys('usuario12356')
    screenshot_path = take_screenshot(context, 'invalidUserNameAndPassword')
    context.driver.find_element(By.NAME, 'submit').click()
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Proporcionar contraseña y usuario incorrectos")

@then('Verificando pagina incorrecto contraseña y usuario')
def verificar_mensaje_error(context):
    ensure_pdf_initialized(context)
    alert = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'customAlert'))
    )
    assert alert.is_displayed(), "El mensaje de error no se muestra."
    assert "Usuario o contraseña incorrectos" in alert.text, "El texto del mensaje de error no coincide."
    screenshot_path = take_screenshot(context, 'verificar_mensaje_error')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación del mensaje de error")


@given('abrir navegador con url erronea')
def open_browser_invalid(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/CodigoR1/indes.html')
    screenshot_path = take_screenshot(context, 'open_browser_invalid')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador con url erronea")

@then('Verificar pagina error 404')
def verificacion_AdminHome(context):
    ensure_pdf_initialized(context)
    WebDriverWait(context.driver, 10).until(EC.title_is("Error"))
    assert context.driver.title == "Error"
    screenshot_path = take_screenshot(context, 'verificacion_404Error')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificación de la página de Error pagina no encontrada")
