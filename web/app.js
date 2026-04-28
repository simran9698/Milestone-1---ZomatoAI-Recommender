document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/locations');
        const locations = await response.json();
        const select = document.getElementById('location');
        select.innerHTML = '<option value="" disabled selected>Select a location</option>';
        locations.forEach(loc => {
            const option = document.createElement('option');
            option.value = loc;
            option.textContent = loc;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Failed to load locations:', error);
    }
});

document.getElementById('recommendation-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const location = document.getElementById('location').value;
    const cuisine = document.getElementById('cuisine').value || null;
    const min_rating = parseFloat(document.getElementById('min_rating').value);
    const max_budget = parseFloat(document.getElementById('max_budget').value);
    const extra_preferences = document.getElementById('extra_preferences').value || null;
    
    const resultsContainer = document.getElementById('results');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('span');
    
    btnText.textContent = 'Finding Places...';
    submitBtn.disabled = true;
    resultsContainer.innerHTML = '';
    
    try {
        const response = await fetch('/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                location,
                cuisine,
                min_rating,
                max_budget,
                extra_preferences
            })
        });
        
        const data = await response.json();
        
        if (data.reason_code !== 'SUCCESS') {
            resultsContainer.innerHTML = `<div class="info-message">
                <i data-lucide="info" style="width: 48px; height: 48px; margin-bottom: 1rem; color: var(--primary)"></i>
                <h3>No recommendations found</h3>
                <p>Reason: ${data.reason_code.replace(/_/g, ' ')}</p>
            </div>`;
        } else {
            let html = '';
            data.results.forEach((restaurant, index) => {
                html += `
                    <div class="restaurant-card" style="animation-delay: ${index * 0.1}s">
                        <div class="card-header">
                            <div class="card-title">
                                <h3>${restaurant.name}</h3>
                                <p>${restaurant.cuisines.join(', ')}</p>
                            </div>
                            <div class="rating-badge">
                                <i data-lucide="star" style="width: 14px; height: 14px; fill: currentColor"></i>
                                ${restaurant.rating.toFixed(1)}
                            </div>
                        </div>
                        <div class="card-stats">
                            <div class="stat">
                                <i data-lucide="map-pin"></i>
                                <span>${restaurant.location}</span>
                            </div>
                            <div class="stat">
                                <i data-lucide="banknote"></i>
                                <span>₹${restaurant.cost_for_two} for two</span>
                            </div>
                            <div class="stat">
                                <i data-lucide="users"></i>
                                <span>${restaurant.votes} votes</span>
                            </div>
                        </div>
                        <div class="explanation">
                            <strong>AI Analysis</strong>
                            ${restaurant.explanation}
                        </div>
                    </div>
                `;
            });
            resultsContainer.innerHTML = html;
        }
        // Refresh icons
        if (window.lucide) {
            window.lucide.createIcons();
        }
    } catch (error) {
        resultsContainer.innerHTML = `<div class="error-message">
            <i data-lucide="alert-circle" style="width: 48px; height: 48px; margin-bottom: 1rem; color: var(--accent)"></i>
            <h3>Connection Error</h3>
            <p>${error.message}</p>
        </div>`;
        if (window.lucide) window.lucide.createIcons();
    } finally {
        btnText.textContent = 'Find Places';
        submitBtn.disabled = false;
    }
});
