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