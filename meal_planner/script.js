document.addEventListener('DOMContentLoaded', function() {
    const saveButton = document.getElementById('saveButton');
    const clearButton = document.getElementById('clearButton');
    const mealTable = document.getElementById('mealTable');
    const textareas = mealTable.getElementsByTagName('textarea');

    const mealIds = [];
    for (let i = 0; i < textareas.length; i++) {
        if (textareas[i].id) {
            mealIds.push(textareas[i].id);
        }
    }

    // Function to load saved meals from localStorage
    function loadMeals() {
        const savedMeals = localStorage.getItem('mealPlan');
        if (savedMeals) {
            const meals = JSON.parse(savedMeals);
            mealIds.forEach(id => {
                const textarea = document.getElementById(id);
                if (textarea && meals[id]) {
                    textarea.value = meals[id];
                }
            });
        }
        console.log('Meals loaded.');
    }

    // Function to save meals to localStorage
    function saveMeals() {
        const currentMeals = {};
        let hasData = false;
        mealIds.forEach(id => {
            const textarea = document.getElementById(id);
            if (textarea) {
                currentMeals[id] = textarea.value.trim();
                if (textarea.value.trim() !== '') {
                    hasData = true;
                }
            }
        });

        if (hasData) {
            localStorage.setItem('mealPlan', JSON.stringify(currentMeals));
            alert('¡Plan de comidas guardado!');
            console.log('Meals saved.');
        } else {
            localStorage.removeItem('mealPlan'); // Remove if all fields are empty
            alert('No hay datos para guardar. El plan guardado (si existe) ha sido limpiado.');
            console.log('No data to save. Cleared saved plan if it existed.');
        }
    }

    // Function to clear all meal inputs and localStorage
    function clearMeals() {
        if (confirm('¿Estás seguro de que quieres limpiar todo el plan? Esta acción no se puede deshacer.')) {
            mealIds.forEach(id => {
                const textarea = document.getElementById(id);
                if (textarea) {
                    textarea.value = '';
                }
            });
            localStorage.removeItem('mealPlan');
            alert('Plan de comidas limpiado.');
            console.log('Meals cleared.');
        }
    }

    // Add event listeners
    if (saveButton) {
        saveButton.addEventListener('click', saveMeals);
    }
    if (clearButton) {
        clearButton.addEventListener('click', clearMeals);
    }

    // Load meals when the page loads
    loadMeals();
});
