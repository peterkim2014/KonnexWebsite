document.addEventListener("DOMContentLoaded", function() {
    const contactLink = document.querySelector(".contact");
    const dropdownContent = document.querySelector(".dropdown-content");

    // Show dropdown content on touchstart (tap) event
    contactLink.addEventListener("touchstart", function() {
        dropdownContent.style.display = "block";
    });

    // Hide dropdown content on touchend (release) event
    contactLink.addEventListener("touchstart", function(event) {
        // Check if the touch event target is outside the bounds of the contact link or dropdown content
        if (!contactLink.contains(event.target) && !dropdownContent.contains(event.target)) {
            dropdownContent.style.display = "none";
        }
    });

    dropdownContent.addEventListener("touchstart", function(event) {
        // Check if the touch event target is outside the bounds of the contact link or dropdown content
        if (!contactLink.contains(event.target) && !dropdownContent.contains(event.target)) {
            dropdownContent.style.display = "none";
        }
    });
});