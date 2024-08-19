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


@given('el usuario está en la página de pagos')
def step_impl(context):
    ensure_pdf_initialized(context)
    setup_browser(context)
    context.driver.get('http://localhost/tablasresidentesypagos/index.html')
    screenshot_path = take_screenshot(context, 'abrir_navegador')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")


@when('el usuario hace clic en el botón "Generar PDF"')
def step_impl(context):
    # Encuentra y presiona el botón de generar reporte en PDF
    generate_report_button = context.driver.find_element(By.ID, 'generatePDF')
    generate_report_button.click()

    screenshot_path = take_screenshot(context, 'presionar_boton_generar_reporte')
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Presionar botón de generar reporte")


@then('el reporte en pdf se debió haber generado')
def step_impl(context):
    time.sleep(5)  # Espera para que el archivo se descargue completamente
    pdf_path = r'C:\Users\joela\Downloads\reporte_pagos.pdf'

    if not os.path.exists(pdf_path):
        raise AssertionError("El archivo PDF no se encontró en la ubicación esperada.")

    context.driver.get('file:///' + pdf_path.replace('\\', '/'))  # Abrir el archivo PDF en el navegador
    time.sleep(5)
    screenshot_path = take_screenshot(context, 'reporte_de_pagos_generado')
    time.sleep(5)
    add_screenshot_to_pdf(context.pdf, screenshot_path, "Reporte de pagos generado")

    context.driver.quit()
    #--------------------------------------------------------------------------------------

    @given('el usuario está en la página de pagos con la tabla vacía')
    def step_impl(context):
        ensure_pdf_initialized(context)
        setup_browser(context)
        context.driver.get('http://localhost/tablasresidentesypagos/index.html')
        screenshot_path = take_screenshot(context, 'abrir_navegador')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Abrir navegador")

        # Buscar un valor que no exista para dejar la tabla vacía
        search_input = context.driver.find_element(By.ID, 'search-payments')
        search_input.send_keys('w')  # Asumimos que 'w' no coincide con ningún registro

        # Tomar captura de pantalla de la tabla vacía
        time.sleep(1)  # Dar tiempo para que la búsqueda filtre los resultados
        screenshot_path = take_screenshot(context, 'tabla_vacia')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Tabla de pagos vacía")

    @when('el usuario hace clic en el botón "Generar PDF" con datos vacíos')
    def step_impl(context):
        # Encuentra y presiona el botón de generar reporte en PDF
        generate_report_button = context.driver.find_element(By.ID, 'generatePDF')
        generate_report_button.click()

        screenshot_path = take_screenshot(context, 'presionar_boton_generar_reporte')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "Presionar botón de generar reporte")

    @then('el reporte en pdf no se debe generar si la tabla está vacía')
    def step_impl(context):
        time.sleep(5)  # Espera para asegurarse de que el archivo debería haberse generado si fuera el caso
        pdf_path = r'C:\Users\joela\Downloads\reporte_pagos.pdf'

        if os.path.exists(pdf_path):
            raise AssertionError("El archivo PDF se generó aunque no debería haberse generado.")

        screenshot_path = take_screenshot(context, 'sin_reporte_de_pagos_generado')
        add_screenshot_to_pdf(context.pdf, screenshot_path, "No se generó reporte de pagos cuando la tabla está vacía")

        context.driver.quit()