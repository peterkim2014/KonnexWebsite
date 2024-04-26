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



// Add click event listeners to all route links
var routeLinks = document.querySelectorAll(".route");
routeLinks.forEach(function(link) {
    link.addEventListener("mouseover", addBottomBorder);
});
routeLinks.forEach(function(link) {
    link.addEventListener("mouseleave", removeBottomBorder);
});
// Function to add bottom border to the selected route
function addBottomBorder() {
    // Remove "route-selected" class from all route links
    var routeLinks = document.querySelectorAll(".route");
    routeLinks.forEach(function(link) {
        link.classList.remove("route-selected");
    });

    // Add "route-selected" class to the clicked link, except for "Contact us"
    if (!this.classList.contains("contact")) {
        this.classList.add("route-selected");
    }
}
// Function to add bottom border to the selected route
function removeBottomBorder() {
    // Remove "route-selected" class from all route links
    var routeLinks = document.querySelectorAll(".route");
    routeLinks.forEach(function(link) {
        link.classList.remove("route-selected");
    });
}


document.addEventListener("DOMContentLoaded", function() {
    const images = document.querySelectorAll("img[data-src]");
    const options = {
        root: null,
        rootMargin: "0px",
        threshold: 0.1
    };

    const lazyLoad = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute("data-src");
                observer.unobserve(img);
            }
        });
    };

    const observer = new IntersectionObserver(lazyLoad, options);
    images.forEach(image => observer.observe(image));
});

// Get all img elements in the document
const imgElements = document.querySelectorAll('img');

// Loop through each img element and add the loading="lazy" attribute
imgElements.forEach(img => {
    img.setAttribute('loading', 'lazy');
});




// Attach event listener to the form submission
// document.getElementById('join-form-function').addEventListener('submit', handleFormSubmit);

// Function to handle form submission
function handleFormSubmit(event) {
    event.preventDefault(); // Prevent default form submission behavior

    // Retrieve form data
    const formData = event.target;
    console.log("Form data: ", formData)


    fetch('http://localhost:5000/mailchimp', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error signaling Mailchimp API:', error);
    });
}


// Attach event listener to the form submission
// document.getElementById('submit-join').addEventListener('submit', handleFormSubmitJoin);

// Function to handle form submission
function handleFormSubmitJoin(event) {
    event.preventDefault(); // Prevent default form submission behavior

    // Retrieve form data
    const formData = event.target;
    console.log("Form data: ", formData)


    fetch('http://localhost:5000/joinTeamEmail', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error signaling Mailchimp API:', error);
    });
}


// Attach event listener to the form submission
// document.getElementById('contactFormEmail').addEventListener('submit', handleFormSubmitContact);

// Function to handle form submission
function handleFormSubmitContact(event) {
    event.preventDefault(); // Prevent default form submission behavior

    // Retrieve form data
    const formData = event.target;
    console.log("Form data: ", formData)


    fetch('http://localhost:5000/contactUsEmail', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error signaling Mailchimp API:', error);
    });
}