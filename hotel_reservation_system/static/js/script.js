document.addEventListener("DOMContentLoaded", function() {
    // Select the form element
    const form = document.querySelector("form");

    // Check if the form element exists
    if (form) {
        form.addEventListener("submit", function(event) {
            const requiredFields = form.querySelectorAll("input[required]");
            let formIsValid = true;
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    formIsValid = false;
                    alert("Please fill all required fields.");
                    field.focus();
                }
            });

            if (!formIsValid) {
                event.preventDefault(); // Prevent form submission
            }
        });
    } else {
        console.error("Form element not found.");
    }
});
