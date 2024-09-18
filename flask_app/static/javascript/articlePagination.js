// Function to get article data from the hidden element
function getArticlesData() {
    const articleDataElement = document.getElementById('article-data');
    return JSON.parse(articleDataElement.textContent || articleDataElement.innerText);
}

// Constants
const articlesPerPage = 6;
let currentPage = 1;

// Get the articles data
const articles = getArticlesData();

// Function to display the articles for the current page
function displayArticles(page) {
    const articleList = document.getElementById('article-list');
    articleList.innerHTML = '';

    // Calculate start and end indexes for the current page
    const start = (page - 1) * articlesPerPage;
    const end = start + articlesPerPage;

    const articlesToDisplay = articles.slice(start, end);
    
    // Iterate through the articles to display and add them to the DOM
    articlesToDisplay.forEach(article => {
        const articleItem = document.createElement('li');
        articleItem.classList.add('article-container');

        articleItem.innerHTML = `
            <a href="/articles?article_id=${article.id}">
                ${article.title}
            </a>
            <div class="article-container-information">
                <div class="article-container-information-image">
                    <img class="previewArticleImage" src="/static/uploads/${article.thumbnail}" alt="${article.title}">
                </div>
                <p>${article.previewText.substring(0, 100)}${article.previewText.length > 100 ? '...' : ''}</p>
            </div>
        `;
        articleList.appendChild(articleItem);
    });
    adjustVignetteBackgroundHeight();

    window.scrollTo({
        top: 0,
        behavior: 'smooth' // Adds a smooth scrolling effect
    });
}

// Function to create pagination controls
function createPaginationControls() {
    const paginationControls = document.getElementById('pagination-controls');
    const totalPages = Math.ceil(articles.length / articlesPerPage);
    
    // Clear current pagination
    paginationControls.innerHTML = '';
    
    // Create buttons for each page
    for (let i = 1; i <= totalPages; i++) {
        const pageButton = document.createElement('button');
        pageButton.innerText = i;
        pageButton.classList.add('page-button');
        if (i === currentPage) {
            pageButton.classList.add('active');
        }
        
        // Add click event to switch pages
        pageButton.addEventListener('click', () => {
            currentPage = i;
            displayArticles(currentPage);
            createPaginationControls();
        });
        
        paginationControls.appendChild(pageButton);
    }
}

// Initialize the article list and pagination controls
document.addEventListener('DOMContentLoaded', () => {
    displayArticles(currentPage);
    createPaginationControls();
    // Adjust vignette height once articles are displayed
    adjustVignetteBackgroundHeight();

    // Attach resize listener
    window.addEventListener('resize', adjustVignetteBackgroundHeight);
});



// Function to dynamically adjust the height of the vignette background
function adjustVignetteBackgroundHeight() {
    console.log("Running adjustVignetteBackgroundHeight");

    // Select the relevant elements
    const articleMainContainer = document.querySelector('.article-main-container');
    const vignetteBackground = document.querySelector('.vignette-background-articles');

    // Check if elements exist and log them for debugging
    if (!articleMainContainer) {
        console.error("article-main-container not found");
        return; // Exit if the element is not found
    } else {
        console.log("article-main-container found:", articleMainContainer);
    }

    if (!vignetteBackground) {
        console.error("vignette-background-articles not found");
        return; // Exit if the element is not found
    } else {
        console.log("vignette-background-articles found:", vignetteBackground);
    }

    // Get the height of the article-main-container
    const articleMainContainerHeight = articleMainContainer.offsetHeight;

    // Log the container height for debugging
    console.log("Article Main Container Height:", articleMainContainerHeight);

    // Calculate 80% of the article-main-container height for the vignette
    const vignetteHeight = articleMainContainerHeight * 0.8;

    // Log the calculated vignette height
    console.log("Calculated Vignette Height:", vignetteHeight);

    // Set the min-height of the vignette background and apply a visible background color for debugging
    vignetteBackground.style.minHeight = `${vignetteHeight}px`;
    // Log the final min-height of the vignette background
    console.log("Vignette Background Min-Height Set:", vignetteBackground.style.minHeight);
}