Feature: Generación de reportes

  Scenario: Generar reporte en PDF
    Given el usuario está en la página de pagos
    When el usuario hace clic en el botón "Generar PDF"
    Then el reporte en pdf se debió haber generado
