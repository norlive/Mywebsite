document.addEventListener('DOMContentLoaded', () => {
    const adminIdInput = document.getElementById('admin-id');
    const loginForm = document.getElementById('login-form');
    const loginMessage = document.getElementById('login-message');
    const adminPanel = document.getElementById('admin-panel');
    const addItemForm = document.getElementById('add-item-form');
    const portfolioAdminList = document.getElementById('portfolio-admin-list');

    let currentAdminId = null;

    // Function to load portfolio items for admin view
    const loadAdminPortfolioItems = async () => {
        try {
            const response = await fetch('/api/portfolio');
            const data = await response.json();
            portfolioAdminList.innerHTML = '';
            
            if (data.portfolio && data.portfolio.length > 0) {
                data.portfolio.forEach(item => {
                    const listItem = document.createElement('li');
                    listItem.innerHTML = `
                        <span>${item.title} (${item.category}) - ${item.type}</span>
                        <button onclick="deleteItem('${item.id}')">Delete</button>
                    `;
                    portfolioAdminList.appendChild(listItem);
                });
            } else {
                portfolioAdminList.innerHTML = '<li>No items found.</li>';
            }
        } catch (error) {
            console.error('Error loading admin portfolio items:', error);
            portfolioAdminList.innerHTML = '<li>Failed to load items.</li>';
        }
    };

    // Admin Login
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        try {
            const response = await fetch('/api/admin/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    admin_id: adminIdInput.value
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                currentAdminId = adminIdInput.value;
                loginMessage.textContent = '';
                document.getElementById('login-section').style.display = 'none';
                adminPanel.style.display = 'block';
                loadAdminPortfolioItems();
            } else {
                loginMessage.textContent = result.message || 'Invalid Admin ID';
            }
        } catch (error) {
            console.error('Login error:', error);
            loginMessage.textContent = 'Login failed. Please try again.';
        }
    });

    // Add new portfolio item
    addItemForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const title = document.getElementById("item-title").value;
        const src = document.getElementById("item-src").value;
        const type = document.getElementById("item-type").value;
        const category = document.getElementById("item-category").value;
        const description = document.getElementById("item-description").value;

        if (!src) {
            alert("Please enter a URL for the item.");
            return;
        }

        const newItem = {
            admin_id: currentAdminId,
            title: title,
            src: src,
            type: type,
            category: category,
            description: description
        };

        try {
            const response = await fetch("/api/portfolio", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    admin_id: currentAdminId,
                    items: [newItem] // Send as a list for consistency with backend
                })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                alert("Item added successfully!");
                addItemForm.reset();
                loadAdminPortfolioItems();
            } else {
                alert("Failed to add item: " + (result.error || "Unknown error"));
            }
        } catch (error) {
            console.error("Error adding item:", error);
            alert("Failed to add item. Please try again.");
        }
    });

    // Delete portfolio item (global function)
    window.deleteItem = async (itemId) => {
        if (confirm(`Are you sure you want to delete item ${itemId}?`)) {
            try {
                const response = await fetch(`/api/portfolio/${itemId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        admin_id: currentAdminId
                    })
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    alert('Item deleted successfully!');
                    loadAdminPortfolioItems();
                } else {
                    alert('Failed to delete item: ' + (result.error || 'Unknown error'));
                }
            } catch (error) {
                console.error('Error deleting item:', error);
                alert('Failed to delete item. Please try again.');
            }
        }
    };
});

