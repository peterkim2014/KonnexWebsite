

document.addEventListener("DOMContentLoaded", function() {
    var myScreenOrientation = window.screen.orientation;
    // alert(`The orientation of the screen is: ${myScreenOrientation.type}`);

    window.screen.orientation.addEventListener("change", () => {
        // alert(`The orientation of the screen is: ${myScreenOrientation.type}`);
    });
});

// JavaScript to trigger animations when scrolling
document.addEventListener("DOMContentLoaded", function() {
    const faders = document.querySelectorAll('.fade-in');

    const appearOptions = {
        threshold: 0,
        rootMargin: "0px 0px -10px 0px"
    };

    const appearOnScroll = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (!entry.isIntersecting) {
                return;
            } else {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, appearOptions);

    faders.forEach(fader => {
        appearOnScroll.observe(fader);
    });
});
// JavaScript to trigger animations on scroll (repeated animation)
document.addEventListener("DOMContentLoaded", function() {
    const sections = document.querySelectorAll('.fade-slide-up');

    const options = {
        threshold: 0.005,  // Trigger when 20% of the element is visible
        rootMargin: "0px 0px -10px 0px"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');  // Add the animation class when visible
            } else {
                entry.target.classList.remove('visible');  // Remove the class when it's no longer visible
            }
        });
    }, options);

    sections.forEach(section => {
        observer.observe(section);  // Observe each section
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const articleContainers = document.querySelectorAll('.article-container-information');

    articleContainers.forEach(container => {
        const articleBody = container.querySelector('p');
        const parser = new DOMParser();
        const doc = parser.parseFromString(articleBody.innerHTML, 'text/html');
        
        // Extract only <p> tags, ignoring headers
        const paragraphs = doc.querySelectorAll('p');
        let paragraphText = '';
        paragraphs.forEach(p => {
            paragraphText += p.outerHTML; // Keep the outerHTML to retain <p> tags
        });

        // Set the filtered content back to the article's paragraph element
        articleBody.innerHTML = paragraphText;
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const contactLink = document.querySelector(".contact");
    const dropdownContent = document.querySelector(".dropdown-content");
    contactLink.classList.remove("route-selected");

    // Show dropdown content on touchstart (tap) event
    contactLink.addEventListener("touchstart", function() {
        dropdownContent.style.display = "block";
        contactLink.classList.remove("route-selected");
    });

    // Hide dropdown content when touching outside the box or "Contact us" again
    document.addEventListener("touchend", function(event) {
        // Check if the touch event target is outside the bounds of the contact link or dropdown content
        if (!contactLink.contains(event.target) && !dropdownContent.contains(event.target)) {
            dropdownContent.style.display = "none";
            contactLink.classList.remove("route-selected");
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
            const offsetTop = targetSection.offsetTop - 75;
            
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

// Function to handle scroll-to-top button click
document.getElementById("scrollToTopBtn").addEventListener("touchstart", function() {
    scrollAnimation();
});

// Function to scroll back to the top of the page with smooth animation
function scrollAnimation() {
    var currentScroll = document.documentElement.scrollTop || document.body.scrollTop;

    if (currentScroll > 0) {
        // Calculate scroll speed (quadratic function for a smooth transition)
        var scrollSpeed = Math.sqrt(currentScroll);

        // Scroll the page up by a certain amount with smooth behavior
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }
}

// Function to show/hide scroll-to-top button based on scroll position
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    var scrollToTopBtn = document.getElementById("scrollToTopBtn");

    if (document.body.scrollTop > 1000 || document.documentElement.scrollTop > 1000) {
        scrollToTopBtn.style.display = "block";
    } else {
        scrollToTopBtn.style.display = "none";
    }
}



// Function to scroll back to the top of the page when button is clicked
function scrollToTop() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE, and Opera
}


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

// Add click event listeners to all route links
var routeLinks = document.querySelectorAll(".route");
routeLinks.forEach(function(link) {
    link.addEventListener("click", addBottomBorder);
});


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










function onRecaptchaSuccess(token) {
    document.getElementById('submit-button').disabled = false; 
}
function onRecaptchaExpired() {
    document.getElementById('submit-button').disabled = true;
}
function onRecaptchaError() {
    document.getElementById('submit-button').disabled = true;
}
document.getElementById('submit-button').disabled = true;