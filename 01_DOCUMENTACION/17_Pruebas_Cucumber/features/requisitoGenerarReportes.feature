Feature: Generación de reportes

  Scenario: Generar reporte en PDF
    Given el usuario está en la página de pagos
    When el usuario hace clic en el botón "Generar PDF"
    Then el reporte en pdf se debió haber generado
      #Generar reporte de pagos sin datos
   Scenario: No generar reporte en PDF cuando no hay datos
  Given el usuario está en la página de pagos con la tabla vacía
  When el usuario hace clic en el botón "Generar PDF" con datos vacíos
  Then el reporte en pdf no se debe generar si la tabla está vacía

