// Select all <i> tags with the class "icon-updating"
const icons = document.querySelectorAll('.icon-updating i');

// Define a regular expression pattern to match class names like "bi-google", "bi-instagram", etc.
const pattern = /^bi-(google|instagram|facebook|youtube)$/;

// Iterate through each <i> tag
icons.forEach(icon => {
    // Get the class list of the icon
    const classList = icon.classList;

    // Iterate through each class in the classList
    for (let i = 0; i < classList.length; i++) {
        // Check if the class matches the pattern
        if (pattern.test(classList[i])) {
            // Apply styles based on the matched class name
            switch (classList[i]) {
                case 'bi-google':
                    icon.style.color = '#dd4b39';
                    break;
                case 'bi-instagram':
                    icon.style.color = '#ac2bac';
                    break;
                case 'bi-facebook':
                    icon.style.color = '#3b5998';
                    break;
                case 'bi-youtube':
                    icon.style.color = '#ed302f';
                    break;
                // Add more cases for other icons if needed
            }
            // Exit the loop once a matching class is found
        }
    }
});
