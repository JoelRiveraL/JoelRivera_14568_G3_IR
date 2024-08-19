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


@given('Abrir navegador de gestión de soporte')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/gestionsoporte/index.html')
    screenshot_path = take_screenshot(context, 'open_browser')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")


@when('agrego un soporte con los siguientes datos')
def step_impl(context):
    data = context.table.rows
    for row in data:
        nombre = row['nombre']
        imagen = row['imagen']
        contacto = row['contacto']
        numero = row['número']
        descripcion = row['descripción']

        # Abre el modal de agregar soporte
        context.driver.find_element(By.ID, 'add-support-btn').click()

        # Rellena el formulario
        context.driver.find_element(By.ID, 'name').send_keys(nombre)
        context.driver.find_element(By.ID, 'image').send_keys(imagen)
        context.driver.find_element(By.ID, 'contact').send_keys(contacto)
        context.driver.find_element(By.ID, 'phone').send_keys(numero)
        context.driver.find_element(By.ID, 'description').send_keys(descripcion)
        screenshot_path = take_screenshot(context, 'added_support')

        # Envía el formulario
        context.driver.find_element(By.XPATH, "//button[text()='Agregar']").click()

        # Captura de pantalla
        add_screenshot_to_pdf(context.pdf, screenshot_path, f"Agregar soporte: {nombre}")


@then('el soporte "{nombre}" debería estar en la lista')
def step_impl(context, nombre):
    try:
        # Espera que el soporte aparezca en la lista
        mensaje_elemento = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//h3[text()='{nombre}']"))
        )
        assert mensaje_elemento.is_displayed(), f"El soporte '{nombre}' no se encontró en la lista."

        # Captura de pantalla
        screenshot_path = take_screenshot(context, 'support_list')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Lista de soportes después de agregar")

    except Exception as e:
        screenshot_path = take_screenshot(context, 'error_verificacion_soporte')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Error durante la verificación del soporte")
        raise AssertionError(f"Error al verificar el soporte: {e}")

# ---------------------------------------------------------------------------------

@given('Abrir navegador de gestión de soporte con campos incompletos y validar errores')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/gestionsoporte/index.html')
    screenshot_path = take_screenshot(context, 'abrir_navegador_gestion_soporte')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador de gestión de soporte")


@when('intento agregar un soporte con los siguientes datos incompletos')
def step_impl(context):
    # Asume que los datos están en un DataTable
    for row in context.table:
        nombre = row['nombre']
        imagen = row['imagen']
        contacto = row['contacto']
        numero = row['número']
        descripcion = row['descripción']

        # Abre el modal de agregar soporte
        context.driver.find_element(By.ID, 'add-support-btn').click()

        # Rellena el formulario
        context.driver.find_element(By.ID, 'name').send_keys(nombre)
        context.driver.find_element(By.ID, 'image').send_keys(imagen)
        context.driver.find_element(By.ID, 'contact').send_keys(contacto)
        context.driver.find_element(By.ID, 'phone').send_keys(numero)
        context.driver.find_element(By.ID, 'description').send_keys(descripcion)
        screenshot_path = take_screenshot(context, 'intentar_agregar_soporte_incompleto')

    add_screenshot_to_pdf(context.pdf, screenshot_path, "Intentar agregar soporte con campos incompletos")


@then('debería ver un mensaje de error indicando campos obligatorios')
def step_impl(context):
    # Verifica que el mensaje de error esté presente
    context.driver.find_element(By.XPATH, "//button[text()='Agregar']").click()

    screenshot_path = take_screenshot(context, 'mensaje_error_campos_obligatorios')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificar mensaje de error por campos obligatorios")

    context.driver.find_element(By.CLASS_NAME, "close").click()

@then('el soporte "{nombre}" no debería estar en la lista')
def step_impl(context, nombre):
    screenshot_path = take_screenshot(context, 'verificar_soporte_no_existente')
    add_screenshot_to_pdf(context.pdf, screenshot_path,
                          "Verificar que el soporte con datos incompletos no está en la lista")
    context.driver.quit()

# ---------------------------------------------------------------------------------

@given('Abrir navegador de gestión de soporte para eliminar y cancelar eliminacio')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/gestionsoporte/index.html')
    screenshot_path = take_screenshot(context, 'abrir_navegador_gestion_soporte')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador de gestión de soporte")

@when('agrego un soporte con los siguientes datos para eliminar y cancelar eliminacion')
def step_impl(context):
    # Asume que los datos están en un DataTable
    for row in context.table:
        nombre = row['nombre']
        imagen = row['imagen']
        contacto = row['contacto']
        numero = row['número']
        descripcion = row['descripción']

        # Abre el modal de agregar soporte
        context.driver.find_element(By.ID, 'add-support-btn').click()

        # Rellena el formulario
        context.driver.find_element(By.ID, 'name').send_keys(nombre)
        context.driver.find_element(By.ID, 'image').send_keys(imagen)
        context.driver.find_element(By.ID, 'contact').send_keys(contacto)
        context.driver.find_element(By.ID, 'phone').send_keys(numero)
        context.driver.find_element(By.ID, 'description').send_keys(descripcion)

        # Envía el formulario
        context.driver.find_element(By.XPATH, "//button[text()='Agregar']").click()
        screenshot_path = take_screenshot(context, 'soporte_agregado')
        add_screenshot_to_pdf(context.pdf, screenshot_path, f"Soporte agregado: {nombre}")


@then('el soporte "{nombre}" debería estar en la lista para eliminar')
def step_impl(context, nombre):
    # Verifica que el soporte esté en la lista
    support_list = context.driver.find_elements(By.XPATH, "//h3")
    found = False
    for support in support_list:
        if nombre in support.text:
            found = True
            break
    assert found, f"El soporte '{nombre}' no está en la lista."

    screenshot_path = take_screenshot(context, 'verificar_soporte_en_lista')
    add_screenshot_to_pdf(context.pdf, screenshot_path, f"Verificar que el soporte '{nombre}' está en la lista")


@when('eliminar soporte creado')
def step_impl(context):
    # Encuentra y presiona el botón de eliminar del soporte específico
    delete_buttons = context.driver.find_elements(By.CLASS_NAME, 'delete-btn')
    delete_buttons[0].click()  # Asumiendo que queremos eliminar el primer soporte para simplificación

    # Presiona el botón de confirmar eliminación en el modal
    confirm_delete_button = context.driver.find_element(By.ID, 'confirm-delete-btn')
    screenshot_path = take_screenshot(context, 'confirmar_eliminacion')
    confirm_delete_button.click()
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Confirmar eliminación del soporte")


@then('verificar que el soporte ha sido eliminado')
def step_impl(context):
    # Espera a que el soporte sea eliminado
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element((By.XPATH, "//h3[text()='Soporte 1']"))
    )

    # Verifica que el soporte ya no esté en la lista
    support_list = context.driver.find_elements(By.XPATH, "//h3")
    for support in support_list:
        assert "Soporte 1" not in support.text, "El soporte 'Soporte 1' aún está en la lista."

    screenshot_path = take_screenshot(context, 'verificar_soporte_eliminado')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificar que el soporte ha sido eliminado")
    context.driver.quit()

#

@given('Abrir navegador de gestión de soporte para eliminar')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/gestionsoporte/index.html')
    screenshot_path = take_screenshot(context, 'abrir_navegador_gestion_soporte')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador de gestión de soporte")


@when('agrego un soporte con los siguientes datos para eliminar')
def step_impl(context):
    for row in context.table:
        nombre = row['nombre']
        imagen = row['imagen']
        contacto = row['contacto']
        numero = row['número']
        descripcion = row['descripción']

        # Abre el modal de agregar soporte
        context.driver.find_element(By.ID, 'add-support-btn').click()

        # Rellena el formulario
        context.driver.find_element(By.ID, 'name').send_keys(nombre)
        context.driver.find_element(By.ID, 'image').send_keys(imagen)
        context.driver.find_element(By.ID, 'contact').send_keys(contacto)
        context.driver.find_element(By.ID, 'phone').send_keys(numero)
        context.driver.find_element(By.ID, 'description').send_keys(descripcion)

        # Envía el formulario
        context.driver.find_element(By.XPATH, "//button[text()='Agregar']").click()
        screenshot_path = take_screenshot(context, 'soporte_agregado')
        add_screenshot_to_pdf(context.pdf, screenshot_path, f"Soporte agregado: {nombre}")


@then('el soporte "{nombre}" debería estar en la lista para eliminar y cancelar la eliminacion')
def step_impl(context, nombre):
    support_list = context.driver.find_elements(By.XPATH, "//h3")
    found = False
    for support in support_list:
        if nombre in support.text:
            found = True
            break
    assert found, f"El soporte '{nombre}' no está en la lista."

    screenshot_path = take_screenshot(context, 'verificar_soporte_en_lista')
    add_screenshot_to_pdf(context.pdf, screenshot_path, f"Verificar que el soporte '{nombre}' está en la lista")


@when('intento eliminar soporte pero cancelo la eliminación')
def step_impl(context):
    # Encuentra y presiona el botón de eliminar del soporte específico
    delete_buttons = context.driver.find_elements(By.CLASS_NAME, 'delete-btn')
    delete_buttons[0].click()  # Asumiendo que queremos eliminar el primer soporte para simplificación

    # Presiona el botón de cancelar en el modal de eliminación
    cancel_delete_button = context.driver.find_element(By.ID, 'cancel-delete-btnn') #cancel-delete-btn
    screenshot_path = take_screenshot(context, 'cancelar_eliminacion')
    cancel_delete_button.click()
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Cancelar eliminación del soporte")


@then('verificar que el soporte aún está en la lista después de cancelar')
def step_impl(context):
    support_list = context.driver.find_elements(By.XPATH, "//h3")
    found = False
    for support in support_list:
        if "Soporte 1" in support.text:
            found = True
            break
    assert found, "El soporte 'Soporte 1' no está en la lista después de cancelar la eliminación."

    screenshot_path = take_screenshot(context, 'verificar_soporte_aun_en_lista')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Verificar que el soporte aún está en la lista")
    context.driver.quit()
