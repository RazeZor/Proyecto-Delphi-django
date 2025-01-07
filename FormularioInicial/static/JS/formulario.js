document.addEventListener('DOMContentLoaded', function() {
    let currentStep = 1;
    const form = document.getElementById('multiStepForm');
    const steps = document.querySelectorAll('.step-content');
    const progressSteps = document.querySelectorAll('.step');
    const nextBtn = document.getElementById('nextBtn');
    const prevBtn = document.getElementById('prevBtn');
    const totalSteps = steps.length;

    function showStep(stepNumber) {
        steps.forEach(step => step.classList.remove('active'));
        progressSteps.forEach((step, index) => {
            if (index < stepNumber - 1) {
                step.classList.add('complete');
            } else if (index === stepNumber - 1) {
                step.classList.add('active');
                step.classList.remove('complete');
            } else {
                step.classList.remove('active', 'complete');
            }
        });
        
        document.querySelector(`[data-step="${stepNumber}"]`).classList.add('active');
        
        if (stepNumber === 1) {
            prevBtn.style.display = 'none';
        } else {
            prevBtn.style.display = 'block';
        }
        
        if (stepNumber === totalSteps) {
            nextBtn.textContent = 'Enviar';
        } else {
            nextBtn.textContent = 'Siguiente';
        }
    }

    nextBtn.addEventListener('click', function() {
        if (currentStep < totalSteps) {
            currentStep++;
            showStep(currentStep);
        } else {
            // Aquí puedes manejar el envío del formulario
            alert('Formulario enviado!');
        }
    });

    prevBtn.addEventListener('click', function() {
        if (currentStep > 1) {
            currentStep--;
            showStep(currentStep);
        }
    });

    // Inicializar el formulario
    showStep(1);
});