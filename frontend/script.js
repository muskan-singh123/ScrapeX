document.addEventListener('DOMContentLoaded', () => {
    const scrapeBtn = document.getElementById('scrapeBtn');
    const queryInput = document.getElementById('queryInput');
    const priceInput = document.getElementById('priceInput');
    const resultsContainer = document.getElementById('results');
    const loadingDiv = document.getElementById('loading');

    scrapeBtn.addEventListener('click', async () => {
        const query = queryInput.value.trim();
        const price = priceInput.value.trim();

        if (!query || !price) {
            alert('Please enter both a query and a budget.');
            return;
        }

        // UI State: Loading
        resultsContainer.innerHTML = '';
        loadingDiv.classList.remove('hidden');
        scrapeBtn.disabled = true;
        scrapeBtn.style.opacity = '0.7';

        try {
            // Build URL with query params
            const response = await fetch(`/scrape/flipkart?query=${encodeURIComponent(query)}&budget=${encodeURIComponent(price)}`);
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            renderResults(data.products);

        } catch (error) {
            console.error('Error:', error);
            resultsContainer.innerHTML = `<div class="glass-panel" style="grid-column: 1/-1; text-align: center; color: #ef4444;">
                <i class="fa-solid fa-circle-exclamation" style="font-size: 2rem; margin-bottom: 1rem;"></i>
                <p>Failed to fetch results. Please try again.</p>
            </div>`;
        } finally {
            // UI State: Ready
            loadingDiv.classList.add('hidden');
            scrapeBtn.disabled = false;
            scrapeBtn.style.opacity = '1';
        }
    });

    function renderResults(products) {
        if (!products || products.length === 0) {
            resultsContainer.innerHTML = `<div class="glass-panel" style="grid-column: 1/-1; text-align: center;">
                <p>No products found matching your criteria.</p>
            </div>`;
            return;
        }

        resultsContainer.innerHTML = products.map((product, index) => `
            <div class="product-card" style="animation-delay: ${index * 0.05}s">
                <div class="card-content">
                    <h3 class="product-name" title="${product.Product_name}">${product.Product_name || 'No Name'}</h3>
                    <div class="product-price">${product.Prices || 'N/A'}</div>
                    
                    <div class="product-meta">
                        <span><i class="fa-solid fa-star" style="color: #fbbf24;"></i> ${getRating(product.Reviews)}</span>
                    </div>

                    <p class="product-details">${formatDescription(product.Description)}</p>
                    
                    <a href="${formatLink(product.Links)}" target="_blank" class="view-btn">
                        View on Flipkart <i class="fa-solid fa-external-link-alt"></i>
                    </a>
                </div>
            </div>
        `).join('');
    }

    function formatLink(link) {
        if (!link) return '#';
        if (link.startsWith('http')) return link;
        return `https://www.flipkart.com${link}`;
    }

    function getRating(reviewsText) {
        // Simple extraction if reviews contains rating, otherwise random placeholder provided by design or N/A
        if (!reviewsText) return 'N/A';
        // Usually reviews might look like "4.5 stars" or "3,000 Ratings"
        // Let's just return truncated text
        return reviewsText.split(' ')[0] || 'N/A'; 
    }

    function formatDescription(desc) {
        if (!desc) return '';
        // Often creates a long string, maybe split by |
        return desc; 
    }
});
