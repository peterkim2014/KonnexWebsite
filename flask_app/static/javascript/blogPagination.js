// Function to get blog data from the hidden element
function getBlogsData() {
    const blogDataElement = document.getElementById('blog-data');
    return JSON.parse(blogDataElement.textContent || blogDataElement.innerText);
}

// Constants
const blogsPerPage = 8;
let currentPage = 1;

// Get the blogs data
const blogs = getBlogsData();

// Function to display the blogs for the current page
function displayBlogs(page) {
    const blogList = document.getElementById('blog-list');
    blogList.innerHTML = '';

    // Calculate start and end indexes for the current page
    const start = (page - 1) * blogsPerPage;
    const end = start + blogsPerPage;

    const blogsToDisplay = blogs.slice(start, end);
    
    // Iterate through the blogs to display and add them to the DOM
    blogsToDisplay.forEach(blog => {
        const blogItem = document.createElement('li');
        blogItem.classList.add('blog-container');

        blogItem.innerHTML = `
            <a href="/blogs?blog_id=${blog.id}">
                ${blog.title}
            </a>
            <div class="blog-container-information">
                <div class="blog-container-information-image">
                    <img class="previewBlogImage" src="/static/uploads/${blog.thumbnail}" alt="${blog.title}">
                </div>
                <p>${blog.body.substring(0, 200)}${blog.body.length > 200 ? '...' : ''}</p>
            </div>
        `;
        blogList.appendChild(blogItem);
    });
}

// Function to create pagination controls
function createPaginationControls() {
    const paginationControls = document.getElementById('pagination-controls');
    const totalPages = Math.ceil(blogs.length / blogsPerPage);
    
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
            displayBlogs(currentPage);
            createPaginationControls();
        });
        
        paginationControls.appendChild(pageButton);
    }
}

// Initialize the blog list and pagination controls
document.addEventListener('DOMContentLoaded', () => {
    displayBlogs(currentPage);
    createPaginationControls();
});
