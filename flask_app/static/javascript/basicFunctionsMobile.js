document.addEventListener("DOMContentLoaded", function() {
    const contactLink = document.querySelector(".contact");
    const dropdownContent = document.querySelector(".dropdown-content");

    // Show dropdown content on touchstart (tap) event
    contactLink.addEventListener("touchstart", function() {
        dropdownContent.style.display = "block";
    });

    // Hide dropdown content when touching outside the box or "Contact us" again
    document.addEventListener("touchend", function(event) {
        // Check if the touch event target is outside the bounds of the contact link or dropdown content
        if (!contactLink.contains(event.target) && !dropdownContent.contains(event.target)) {
            dropdownContent.style.display = "none";
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    // Get all anchor links with href starting with '#'
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    // Add event listener to each anchor link
    anchorLinks.forEach(function(link) {
        link.addEventListener("click", function(event) {
            event.preventDefault(); // Prevent default behavior of anchor links
            
            // Get the target section ID from the href attribute
            const targetId = this.getAttribute("href").substring(1);
            const targetSection = document.getElementById(targetId);
            
            // Calculate the distance to scroll
            const offsetTop = targetSection.offsetTop;
            
            // Calculate the scroll position to reach
            const scrollPosition = offsetTop - window.pageYOffset;
            
            // Perform smooth scroll animation
            smoothScroll(scrollPosition, 500); // Adjust the second parameter for the duration of the animation (in milliseconds)
        });
    });
});

// Function to perform smooth scroll animation
function smoothScroll(scrollAmount, duration) {
    const startingY = window.pageYOffset;
    const diff = scrollAmount;
    let start;

    // Animation function
    window.requestAnimationFrame(function step(timestamp) {
        if (!start) start = timestamp;
        const time = timestamp - start;

        // Calculate new position
        const percentage = Math.min(time / duration, 1);
        window.scrollTo(0, startingY + diff * percentage);

        // Continue animation until duration is reached
        if (time < duration) {
            window.requestAnimationFrame(step);
        }
    });
}


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