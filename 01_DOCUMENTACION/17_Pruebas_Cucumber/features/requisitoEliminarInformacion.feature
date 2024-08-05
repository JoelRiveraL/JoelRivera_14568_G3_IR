# Created by joela at 8/4/2024
Feature: Eliminar informacion del residente

  Scenario: Eliminar informacion del residente correctamente
    Given Abrir navegador para eliminar informacion
    When seleccionar filas a eliminar
    Then presionar boton de eliminar
    When revisar los datos que se van a eliminar
    Then revisar informacion eliminada en la tabla

  Scenario: Eliminar informacion del residente sin seleccionar
    Given Abrir navegador para eliminar informacion sin seleccionar
    When seleccionar filas a eliminar sin seleccionar
    Then presionar boton de eliminar sin seleccionar
    When revisar los datos que se van a eliminar sin seleccionar
    Then revisar informacion no eliminada en la tabla