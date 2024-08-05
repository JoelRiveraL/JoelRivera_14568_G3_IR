# Created by joela at 8/4/2024
Feature: Ingreso de datos Residente

  Scenario: Ingresos de datos exitoso
    Given Abrir navegador de ingreso de residentes
    When proporicionar datos validos en el formulario
    Then verificar mensaje de confirmacion de ingreso

  Scenario: Ingreso de cedula repetida
    Given Abrir navegador de ingreso de residentes con cedula repetida
    When proporicionar datos validos en el formulario con cedula repetida
    Then verificar mensaje de confirmacion de ingreso con cedula repetida

  Scenario: Ingreso de cedula no valida
    Given Abrir navegador de ingreso de residentes con cedula no valida
    When proporicionar datos validos en el formulario con cedula no valida
    Then verificar mensaje de confirmacion de ingreso con cedula no valida

  Scenario: Falta de datos a la hora de ingresar
    Given Abrir navegador de ingreso de residentes con datos incompletos
    When proporicionar datos validos en el formulario con datos incompletos
    Then verificar mensaje de confirmacion de ingreso con datos incompletos
