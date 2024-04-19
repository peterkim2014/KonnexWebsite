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

document.addEventListener("DOMContentLoaded", function() {
    const fileUploadInput = document.getElementById("file-upload");
    const documentNameElement = document.getElementById("document-name");
    const documentSizeElement = document.getElementById("document-size");

    fileUploadInput.addEventListener("change", function() {
        // Check if a file is selected
        if (this.files.length > 0) {
            const file = this.files[0];
            const fileName = file.name;
            const fileSize = getFileSize(file.size);

            // Update document name and size elements
            documentNameElement.textContent = fileName;
            documentSizeElement.textContent = fileSize;
        } else {
            // Reset document name and size elements if no file is selected
            documentNameElement.textContent = "";
            documentSizeElement.textContent = "";
        }
    });

    // Function to convert file size to human-readable format
    function getFileSize(sizeInBytes) {
        const units = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        let size = sizeInBytes;
        let unitIndex = 0;

        while (size >= 1024 && unitIndex < units.length - 1) {
            size /= 1024;
            unitIndex++;
        }

        return size.toFixed(2) + ' ' + units[unitIndex];
    }
});