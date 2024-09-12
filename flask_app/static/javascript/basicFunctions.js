// Function called when reCAPTCHA is successfully completed
function onRecaptchaSuccess(token) {
    document.getElementById('submit-button').disabled = false; // Enable the button
}
// Function called when reCAPTCHA expires
function onRecaptchaExpired() {
    document.getElementById('submit-button').disabled = true; // Disable the button
}
// Function called when there is an error with reCAPTCHA
function onRecaptchaError() {
    document.getElementById('submit-button').disabled = true; // Disable the button
}
// Disable the button initially
document.getElementById('submit-button').disabled = true;

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
document.addEventListener("DOMContentLoaded", function () {
    const transactionFeatures = document.querySelectorAll('.key-transaction-feature');
    const featuresContainer = document.querySelector('.key-transaction-features');
    const descriptionContainer = document.getElementById('transaction-description');
    const descriptionText = document.getElementById('description-text');
    const featureStepsContainer = document.getElementById('feature-steps'); // Container to display feature steps
    const header = document.querySelector('.purpose-text-container h4');
    const banner = document.querySelector('.purpose-banner');

    // Get the back button image URL from the data attribute
    const backBtnImageUrl = banner.getAttribute('data-back-btn-url');
    const oneIconUrl = banner.getAttribute('data-one-icon-url');
    const twoIconUrl = banner.getAttribute('data-two-icon-url');
    const threeIconUrl = banner.getAttribute('data-three-icon-url');
    const fourIconUrl = banner.getAttribute('data-four-icon-url');

    // Create a new container div for button and title
    const headerFlexContainer = document.createElement('div');
    headerFlexContainer.classList.add('header-flex-container');
    
    // Move the h4 into this container
    header.parentNode.insertBefore(headerFlexContainer, header);
    headerFlexContainer.appendChild(header);

    // Create a new back button dynamically (as an image)
    const backBtn = document.createElement('img');
    backBtn.id = 'back-btn';
    backBtn.src = backBtnImageUrl;
    backBtn.alt = 'Go Back';
    backBtn.style.display = 'none';
    backBtn.classList.add('back-btn-style');
    headerFlexContainer.insertBefore(backBtn, header);

    const descriptions = {
        retail: "Retail transactions allow effortless checkout using cryptocurrency, enabling you to pay for goods and services just as easily as using a credit card.",
        "peer-to-peer": "Peer-to-peer transactions facilitate instant and seamless crypto transfers between users, ensuring a secure and fast connection.",
        group: "Group transactions make it easy to handle payments for multiple users in a single transaction, ideal for collaborative purchases or shared expenses."
    };

    // Store the original h4 text
    const originalHeaderText = header.textContent;

    // Function to add the steps for each feature
    function addFeatureSteps(featureType) {
        // Clear any previous steps
        featureStepsContainer.innerHTML = '';

        if (featureType === 'retail') {
            const step1 = document.createElement('div');
            step1.innerHTML = `<img class="feature-steps-img" src="${oneIconUrl}" alt="Step 1"> <h5 class="feature-step-text">Choose Crypto</h5>`;

            const step2 = document.createElement('div');
            step2.innerHTML = `<img class="feature-steps-img" src="${twoIconUrl}" alt="Step 2"> <h5 class="feature-step-text">Tap on Payment Processor</h5>`;

            const step3 = document.createElement('div');
            step3.innerHTML = `<img class="feature-steps-img" src="${threeIconUrl}" alt="Step 3"> <h5 class="feature-step-text">Confirm Transaction</h5>`;

            featureStepsContainer.appendChild(step1);
            featureStepsContainer.appendChild(step2);
            featureStepsContainer.appendChild(step3);
        }
        if (featureType === 'peer-to-peer') {
            const step1 = document.createElement('div');
            step1.innerHTML = `<img class="feature-steps-img" src="${oneIconUrl}" alt="Step 1"> <h5 class="feature-step-text">Select a Friend</h5>`;

            const step2 = document.createElement('div');
            step2.innerHTML = `<img class="feature-steps-img" src="${twoIconUrl}" alt="Step 2"> <h5 class="feature-step-text">Type Amount</h5>`;

            const step3 = document.createElement('div');
            step3.innerHTML = `<img class="feature-steps-img" src="${threeIconUrl}" alt="Step 3"> <h5 class="feature-step-text">Confirm Transaction</h5>`;

            featureStepsContainer.appendChild(step1);
            featureStepsContainer.appendChild(step2);
            featureStepsContainer.appendChild(step3);
        }
        if (featureType === 'group') {
            const step1 = document.createElement('div');
            step1.innerHTML = `<img class="feature-steps-img" src="${oneIconUrl}" alt="Step 1"> <h5 class="feature-step-text">Choose from Group List</h5>`;

            const step2 = document.createElement('div');
            step2.innerHTML = `<img class="feature-steps-img" src="${twoIconUrl}" alt="Step 2"> <h5 class="feature-step-text">Select Payment Method</h5>`;

            const step3 = document.createElement('div');
            step3.innerHTML = `<img class="feature-steps-img" src="${threeIconUrl}" alt="Step 3"> <h5 class="feature-step-text">Confirm Transaction</h5>`;

            featureStepsContainer.appendChild(step1);
            featureStepsContainer.appendChild(step2);
            featureStepsContainer.appendChild(step3);
        }
        // You can add similar steps for 'peer-to-peer' and 'group' features here
    }

    transactionFeatures.forEach((feature) => {
        feature.addEventListener('click', () => {
            const featureType = feature.getAttribute('data-feature');
            const featureTitle = feature.querySelector('h2').textContent;

            // Replace h4 with h2 content and display the back button
            header.textContent = featureTitle;
            backBtn.style.display = 'inline-block'; // Show the back button (as an image)

            // Add animation class for the header swap
            header.classList.add('swap-animation');

            // Add the steps to the #feature-steps container
            addFeatureSteps(featureType);

            // Fade out the features container
            featuresContainer.classList.add('fade-out-feature');

            // Wait for fade-out to complete, then hide the features container and show the description
            setTimeout(() => {
                featuresContainer.classList.add('hidden');
                featuresContainer.classList.remove('fade-out-feature'); // Reset fade-out class
                descriptionText.textContent = descriptions[featureType];

                // Fade in the description container
                descriptionContainer.classList.add('fade-in-feature');
                descriptionContainer.classList.add('visible');

                // Remove fade-in after it completes
                setTimeout(() => {
                    descriptionContainer.classList.remove('fade-in-feature');
                    header.classList.remove('swap-animation'); // Reset animation class
                }, 300); // Match to CSS transition duration
            }, 300); // Match to CSS transition duration
        });
    });

    backBtn.addEventListener('click', () => {
        // Restore the original h4 content and hide the back button
        header.textContent = originalHeaderText;
        backBtn.style.display = 'none'; // Hide the back button
        header.classList.add('swap-animation'); // Apply the swap animation

        // Fade out the description container
        descriptionContainer.classList.add('fade-out-feature');

        // Wait for fade-out to complete, then hide the description container and show the features container
        setTimeout(() => {
            descriptionContainer.classList.remove('visible');
            descriptionContainer.classList.remove('fade-out-feature'); // Reset fade-out class

            // Fade in the features container
            featuresContainer.classList.remove('hidden');
            featuresContainer.classList.add('fade-in-feature');

            // Remove fade-in after it completes
            setTimeout(() => {
                featuresContainer.classList.remove('fade-in-feature');
                header.classList.remove('swap-animation'); // Reset animation class
            }, 300); // Match to CSS transition duration
        }, 300); // Match to CSS transition duration
    });
});






// Function to initialize fade-in and fade-slide-up animations
function initializeAnimations() {
    // Initialize fade-in animations
    const faders = document.querySelectorAll('.fade-in');
    const appearOptions = {
        threshold: 0,
        rootMargin: "0px 0px -25px 0px"
    };

    const appearOnScroll = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // Stop observing after it's visible
            }
        });
    }, appearOptions);

    faders.forEach(fader => {
        appearOnScroll.observe(fader);
    });

    // Initialize fade-slide-up animations
    const sliders = document.querySelectorAll('.fade-slide-up');
    const slideOptions = {
        threshold: 0.05,
        rootMargin: "0px 0px -25px 0px"
    };

    const slideObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            } else {
                entry.target.classList.remove('visible');
            }
        });
    }, slideOptions);

    sliders.forEach(slider => {
        slideObserver.observe(slider);
    });
}

// Initialize animations when the DOM is loaded
document.addEventListener("DOMContentLoaded", function() {
    initializeAnimations();
});

// For Single Page Applications or dynamic content loading
if (window.history.pushState) {
    // Listen for navigation events and reinitialize animations
    window.addEventListener('popstate', function() {
        initializeAnimations();
    });

    // If using a framework or router (like React or Vue), listen to routing changes
    document.addEventListener('page:change', function() {
        initializeAnimations();
    });
}

// MutationObserver to detect content changes (if content is loaded dynamically)
const observerConfig = { childList: true, subtree: true };
const domObserver = new MutationObserver((mutationsList, observer) => {
    for (const mutation of mutationsList) {
        if (mutation.type === 'childList') {
            initializeAnimations(); // Reinitialize animations when new elements are added
        }
    }
});

// Start observing the body for changes
domObserver.observe(document.body, observerConfig);


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



