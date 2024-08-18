document.addEventListener('DOMContentLoaded', function() {
    // Create and append the star field container
    const numStars = 100; // Number of stars to generate
    const starField = document.createElement('div');
    starField.className = 'star-field'; // Add a class for styling
    document.body.appendChild(starField);

    // Create a document fragment to batch append stars
    const fragment = document.createDocumentFragment();

    // Generate stars
    for (let i = 0; i < numStars; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.top = `${Math.random() * 100}vh`;
        star.style.left = `${Math.random() * 100}vw`;
        star.style.opacity = Math.random();
        fragment.appendChild(star);
    }

    // Append all stars at once
    starField.appendChild(fragment);

    // Ensure the star field container covers the entire viewport
    const starFieldStyle = document.createElement('style');
    starFieldStyle.textContent = `
        .star-field {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            pointer-events: none;
            z-index: -1; /* Ensure stars are behind other content */
        }
    `;
    document.head.appendChild(starFieldStyle);
});
