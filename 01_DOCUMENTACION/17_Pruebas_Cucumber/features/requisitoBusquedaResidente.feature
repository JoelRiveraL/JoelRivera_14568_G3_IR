# Created by joela at 8/4/2024
Feature: Busqueda informacion Residente

  Scenario: Visualizar datos en tabla general
    Given Abrir navegador busqueda de residentes
    Then verificar tabla de existencia de resumen general residentes

  Scenario: Buscar datos de un residente
    Given Abrir navegador busqueda de residente especifico
    When ingresar datos de busqueda del residente cedula
    Then verificar tabla de datos del residente especifico

  Scenario: Buscar datos de un residente por nombre
    Given Abrir navegador busqueda de residente por nombre especifico
    When ingresar datos de busqueda del residente por nombre
    Then verificar tabla de datos del residente especifico por nombre

  Scenario: Buscar datos de un residente datos erroneos
    Given Abrir navegador busqueda de residente especifico datos erroneos
    When ingresar datos de busqueda del residente cedula datos erroneos
    Then verificar mensaje de error datos erroneos