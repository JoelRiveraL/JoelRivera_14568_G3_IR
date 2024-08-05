# Created by joela at 7/23/2024
Feature: login funcionalidad para la aplicacion UrbTreasurySystem

  Scenario: Validar nombre de usuario y contraseña de administrador
    Given abrir navegador
    When proporcionando un nombre de usuario y contraseña válidos
    Then Verificando pagina


  Scenario: Validar nombre de usuario y contraseña de residente
    Given abrir navegador residente
    When proporcionando un nombre de usuario y contraseña válidos residente
    Then Verificando pagina residente

  Scenario: Validar nombre de usuario y contraseña incorrectos usuario
    Given abrir navegador incorrecto usuario
    When proporcionando un nombre de usuario incorrecto y contraseña
    Then Verificando pagina incorrecto usuario

  Scenario: Validar nombre de usuario y contraseña incorrectos contraseña
    Given abrir navegador incorrecto password
    When proporcionando un nombre de incorrecto y contraseña incorrecta
    Then Verificando pagina incorrecto contraseña

  Scenario: Validar nombre de usuario y contraseña incorrectos
    Given abrir navegador contraseña y usuario incorrectos
    When proporcionando un nombre de incorrecto y contraseña incorrectos
    Then Verificando pagina incorrecto contraseña y usuario


