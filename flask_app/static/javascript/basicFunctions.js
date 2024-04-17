// JavaScript for dropdown functionality
document.addEventListener("DOMContentLoaded", function() {
    const contactLink = document.querySelector(".contact");
    const dropdownContent = document.querySelector(".dropdown-content");

    // Show dropdown content on mouseover
    contactLink.addEventListener("mouseover", function() {
        dropdownContent.style.display = "block";
    });

    // Hide dropdown content on mouseout of both the "Contact us" link and the dropdown content
    contactLink.addEventListener("mouseout", function(event) {
        // Check if the mouse is outside the bounds of the contact link or dropdown content
        if (!contactLink.contains(event.relatedTarget) && !dropdownContent.contains(event.relatedTarget)) {
            dropdownContent.style.display = "none";
        }
    });

    dropdownContent.addEventListener("mouseout", function(event) {
        // Check if the mouse is outside the bounds of the contact link or dropdown content
        if (!contactLink.contains(event.relatedTarget) && !dropdownContent.contains(event.relatedTarget)) {
            dropdownContent.style.display = "none";
        }
    });
});