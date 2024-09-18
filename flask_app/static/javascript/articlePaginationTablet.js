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
                <p class="article-container-information-text">${article.previewText.substring(0, 200)}${article.previewText.length > 200 ? '...' : ''}</p>
            </div>
        `;
        articleList.appendChild(articleItem);
    });

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

});



