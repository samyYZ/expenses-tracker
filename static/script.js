// Function to calculate remaining balance and check warnings
document.addEventListener('DOMContentLoaded', function () {
    const flashMessage = document.querySelector('.flash-message');
    if (flashMessage) {
        setTimeout(() => {
            flashMessage.remove();
        }, 3000); // Removes the flash message after 3 seconds
    }
});

