# Created by joela at 8/4/2024
Feature: Editar informacion de residente

  Scenario: Editar informacion con datos correctos
    Given Abrir navegador editar informacion
    When seleccionar filas a editar
    Then presionar boton de editar
    When editar informacion con datos correctos
    Then revisar informacion editada en la tabla

  Scenario: Editar informacion con datos incorrectos
    Given Abrir navegador editar informacion incorrecta
    When seleccionar filas a editar informacion incorrecta
    Then presionar boton de editar informacion incorrecta
    When editar informacion con datos incorrecta
    Then revisar informacion incorrecta editada en la tabla

  Scenario: Editar informacion sin datos
    Given Abrir navegador editar sin datos
    When No seleccionar filas a editar informacion
    Then presionar boton de editar sin datos
    When editar informacion sin datos
    Then revisar informacion no editada en la tabla

  Scenario: Editar informacion Monto menor a veinte
    Given Abrir navegador editar informacion monto
    When seleccionar filas a editar el monto
    Then presionar boton de editar informacion
    When editar informacion de monto con valores menores a veinte
    Then revisar informacion no editada en la tabla y mensaje de error

  Scenario: Editar informacion campos vacios
    Given Abrir navegador editar informacion campos vacios
    When seleccionar filas a editar con campos vacios
    Then presionar boton a editar con campos vacios
    When editar informacion dejando los campos vacios
    Then verificar mensaje de error por campos vacios
    When cerrar ventaja emergente de editar informacion
    Then revisar informacion no editada con campos vacios
