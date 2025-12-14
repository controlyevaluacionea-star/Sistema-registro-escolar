# Plan: Sistema de Registro de Pagos Escolares

## Objetivo
Crear un sistema completo de registro de pagos para administración escolar con soporte para mensualidades, inscripciones, pagos extraordinarios, múltiples métodos de pago y monedas, además de reportes de cierre diario y anual.

---

## Fase 1: Estructura de Datos y Registro Básico de Pagos ✅
- [x] Crear modelo de datos para estudiantes, pagos, conceptos de pago (mensualidades 1-12, inscripción, extraordinarios)
- [x] Implementar formulario de registro de nuevo pago con selección de estudiante y concepto
- [x] Agregar campos para método de pago (efectivo, pago móvil, transferencia) y moneda (BS efectivo, USD efectivo, otras divisas, BS digital)
- [x] Crear tabla de historial de pagos registrados con información completa
- [x] Implementar validación de datos y manejo de errores en el registro

---

## Fase 2: Gestión de Estudiantes y Conceptos de Pago ✅
- [x] Crear interfaz para registro y gestión de estudiantes (nombre, grado, sección, representante)
- [x] Implementar sistema de búsqueda y filtrado de estudiantes
- [x] Agregar funcionalidad para editar y eliminar pagos registrados
- [x] Crear vista de estado de cuenta por estudiante mostrando pagos realizados y pendientes
- [x] Implementar sistema de configuración de montos para cada concepto de pago

---

## Fase 3: Sistema de Reportes y Dashboard ✅
- [x] Crear dashboard principal con resumen de pagos del día actual
- [x] Implementar reporte de cierre del día con desglose por método de pago y moneda
- [x] Agregar reporte de recaudación total anual con gráficos y estadísticas
- [x] Crear filtros de reportes por rango de fechas, método de pago y moneda
- [x] Implementar exportación de reportes a formato imprimible

---

## Fase 4: Verificación UI ✅
- [x] Verificar formulario de registro de pagos funciona correctamente
- [x] Validar que los reportes muestran datos precisos
- [x] Comprobar que el dashboard presenta la información correctamente
- [x] Verificar navegación entre diferentes secciones del sistema

---

## Fase 5: Sistema de Cédulas y Búsqueda Avanzada ✅
- [x] Agregar campos de cédula al modelo de estudiante (cédula del estudiante y del representante)
- [x] Modificar formulario de estudiantes para incluir cédulas con validación
- [x] Implementar búsqueda de estudiantes por cédula (estudiante o representante)
- [x] Actualizar la interfaz de búsqueda en el registro de pagos para buscar por cédula
- [x] Agregar validación de formato de cédula venezolana

---

## Fase 6: Sistema de Tasas de Cambio y Conversión Automática
- [ ] Instalar librería currency_rate_bcv para obtener tasa del BCV
- [ ] Crear página de configuración del sistema con tasa de cambio
- [ ] Implementar obtención automática de tasa BCV del día
- [ ] Permitir override manual de la tasa por el administrador
- [ ] Modificar sistema de conceptos para trabajar en USD como base
- [ ] Implementar conversión automática USD a Bs según método de pago seleccionado

---

## Fase 7: Pagos Extraordinarios y Restricciones
- [ ] Crear sistema de configuración de pagos extraordinarios
- [ ] Permitir definir pagos extraordinarios para toda la escuela
- [ ] Implementar asignación de pagos extraordinarios por grado específico
- [ ] Agregar asignación de pagos extraordinarios por sección específica
- [ ] Modificar formulario de pagos para mostrar solo mensualidades por defecto
- [ ] Agregar opción para activar pagos extraordinarios en el formulario

---

## Fase 8: Generación de Facturas
- [ ] Diseñar formato de factura con información completa del pago
- [ ] Implementar generación automática de factura al registrar pago
- [ ] Agregar numeración consecutiva de facturas
- [ ] Incluir información de la escuela, estudiante, conceptos y totales
- [ ] Implementar vista previa e impresión de facturas
- [ ] Agregar repositorio de facturas generadas para consulta posterior