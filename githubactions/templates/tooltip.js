
document.addEventListener('DOMContentLoaded', function() {
    // Function to create the popup
    function createPopup(text, target) {
        const popup = document.createElement('div');
        popup.classList.add('popup');
        popup.innerHTML = text;
        document.body.appendChild(popup);

        // Position the popup above the target element
        const rect = target.getBoundingClientRect();

        // Adjust the position to account for scrolling
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        popup.style.left = `${rect.left}px`;
        popup.style.top = `${rect.bottom + scrollTop - popup.offsetHeight + 5}px`;
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
    const tt_elements = document.querySelectorAll('[data-tooltip]');
    tt_elements.forEach(el => {
        el.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            createPopup(tooltipText, this);
        });

        el.addEventListener('mouseleave', function() {
            removePopup();
        });
    });
    // Attach event listeners to elements with data-is-key
    const key_elements = document.querySelectorAll('[data-is-key]');
    key_elements.forEach(el => {
        el.addEventListener('mouseenter', function() {
            const tooltipText = "{{key_html}}";
            createPopup(tooltipText, this);
        });

        el.addEventListener('mouseleave', function() {
            removePopup();
        });
    });
});