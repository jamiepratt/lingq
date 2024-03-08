document.addEventListener('DOMContentLoaded', function() {
    // Function to create the popup
    function createPopup(text, target) {
        const popup = document.createElement('div');
        popup.classList.add('popup');
        popup.textContent = text;
        document.body.appendChild(popup);

        // Position the popup above the target element
        const rect = target.getBoundingClientRect();
        popup.style.left = `${rect.left}px`;
        popup.style.top = `${rect.top - popup.offsetHeight - 5}px`; // Adjust 5px for spacing
        popup.style.display = 'block';
    }

    // Function to remove the popup
    function removePopup() {
        const popup = document.querySelector('.popup');
        if (popup) {
            popup.remove();
        }
    }

    // Attach event listeners to elements with data-tooltip
    const elements = document.querySelectorAll('[data-tooltip]');
    elements.forEach(el => {
        el.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            createPopup(tooltipText, this);
        });

        el.addEventListener('mouseleave', function() {
            removePopup();
        });
    });
});
