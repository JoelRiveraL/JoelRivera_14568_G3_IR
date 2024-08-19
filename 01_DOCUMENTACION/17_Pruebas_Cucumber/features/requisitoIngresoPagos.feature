# Created by joela at 8/4/2024
Feature: Ingreso de pagos del Residente

  Scenario: Verificar residente y registrar pago exitoso
    Given Abrir navegador de ingreso de pagos
    When proporcionar datos válidos en la búsqueda del residente
    Then verificar mensaje de existencia del residente
    When ingresar datos de pago
    Then verificar mensaje de confirmación de pago

  Scenario: Verificar residente con nombre, cedula y registrar pago exitoso
    Given Abrir navegador de ingreso de pagos con nombre
    When proporcionar datos válidos en la búsqueda  con nombre del residente
    Then verificar tabla de existencia del residente
    When proporcionar datos válidos en la búsqueda  con cedula del residente
    Then verificar mensaje de existencia del residente despues de buscar por nombre
    When ingresar datos de pago despues de buscar por nombre
    Then verificar mensaje de confirmación de pago despues de buscar por nombre

  Scenario: Verificar residente con nombre incorrecto y registrar pago exitoso
    Given Abrir navegador de ingreso de pagos con nombre incorrecto
    When proporcionar datos válidos en la búsqueda  con nombre incorrecto del residente
    Then verificar mensaje de nombre incorrecto

  Scenario: Verificar residente y registrar pago incorrecto
    Given Abrir navegador de ingreso de pagos incorrecto
    When proporcionar datos válidos en la búsqueda del residente y pagos incorrecto
    Then verificar mensaje de existencia del residente de pago incorrecto
    When ingresar datos de pago incorrecto
    Then verificar mensaje de pago incorrecto

  Scenario: No se encuentra el apartado de ingreso de pagos
    Given Abrir navegador con direccion de ingreso de pagos incorrecta
    Then Comprobar pagina de error 404 del ingreso de pagos
