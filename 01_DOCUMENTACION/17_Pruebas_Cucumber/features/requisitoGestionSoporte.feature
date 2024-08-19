Feature: Gestión de Soporte

  Scenario: Agregar soporte y verificar su existencia
    Given Abrir navegador de gestión de soporte
    When agrego un soporte con los siguientes datos
      | nombre     | imagen        | contacto | número    | descripción         |
      | Soporte 1  | imagen1.jpg   | email1   | 123456789 | Descripción 1       |
    Then el soporte "Soporte 1" debería estar en la lista

  Scenario: Agregar soporte con campos incompletos y validar errores
    Given Abrir navegador de gestión de soporte con campos incompletos y validar errores
    When intento agregar un soporte con los siguientes datos incompletos
      | nombre     | imagen        | contacto | número    | descripción         |
      | Soporte 1  |               | email1   |           | Descripción 1       |
    Then debería ver un mensaje de error indicando campos obligatorios
    And el soporte "Soporte 1" no debería estar en la lista

  Scenario: Agregar soporte y verificar su existencia y eliminarlo
  Given Abrir navegador de gestión de soporte para eliminar
  When agrego un soporte con los siguientes datos para eliminar
    | nombre     | imagen        | contacto | número    | descripción         |
    | Soporte 1  | imagen1.jpg   | email1   | 123456789 | Descripción 1       |
  Then el soporte "Soporte 1" debería estar en la lista para eliminar
  When eliminar soporte creado
  Then verificar que el soporte ha sido eliminado

    #Agregar y cancelar eliminacion (F)
  Scenario: Agregar soporte, intentar eliminarlo, y cancelar la eliminación
  Given Abrir navegador de gestión de soporte para eliminar y cancelar eliminacion
  When agrego un soporte con los siguientes datos para eliminar y cancelar eliminacion
    | nombre     | imagen        | contacto | número    | descripción         |
    | Soporte 1  | imagen1.jpg   | email1   | 123456789 | Descripción 1       |
  Then el soporte "Soporte 1" debería estar en la lista para eliminar y cancelar la eliminacion
  When intento eliminar soporte pero cancelo la eliminación
  Then verificar que el soporte aún está en la lista después de cancelar

  #Ingresar a la pagina con url fallido