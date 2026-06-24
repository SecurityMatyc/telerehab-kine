// Inicializar Flatpickr en todos los inputs de tipo fecha
document.addEventListener('DOMContentLoaded', function() {
    // Buscar inputs con name que contenga "fecha" o "date"
    const dateInputs = document.querySelectorAll('input[name*="fecha"], input[name*="date"]');
    
    dateInputs.forEach(input => {
        flatpickr(input, {
            locale: 'es',
            dateFormat: 'Y-m-d',        // FORMATO PARA DJANGO
            altInput: true,
            altFormat: 'd/m/Y',         // SOLO VISUAL
            allowInput: true,
            disableMobile: true,
            theme: 'dark',
            placeholder: 'Selecciona una fecha',
            position: 'auto',
            // FORZAR el formato correcto
            onChange: function(selectedDates, dateStr, instance) {
                // dateStr viene en formato Y-m-d por el dateFormat
                instance.input.value = dateStr;
            },
            // Al cerrar el calendario, asegurar el formato
            onClose: function(selectedDates, dateStr, instance) {
                if (dateStr) {
                    instance.input.value = dateStr;
                }
            }
        });
    });
});