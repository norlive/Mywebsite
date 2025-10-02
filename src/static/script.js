document.addEventListener('DOMContentLoaded', () => {
    const portfolioItemsContainer = document.getElementById('portfolio-items');

    // Function to load portfolio items from API
    const loadPortfolioItems = async () => {
        try {
            const response = await fetch('/api/portfolio');
            const data = await response.json();

            portfolioItemsContainer.innerHTML = ''; // Clear existing items

            if (data.portfolio && data.portfolio.length > 0) {
                data.portfolio.forEach(item => {
                    const itemDiv = document.createElement('div');
                    itemDiv.classList.add('portfolio-item');

                    let mediaElement;
                    if (item.type === 'image') {
                        mediaElement = `<img src="${item.src}" alt="${item.title}" onclick="openModal('${item.src}', 'image')">`;
                    } else if (item.type === 'video') {
                        mediaElement = `<video controls src="${item.src}" onclick="openModal('${item.src}', 'video')"></video>`;
                    }

                    itemDiv.innerHTML = `
                        <h3>${item.title}</h3>
                        <p>Category: ${item.category}</p>
                        ${mediaElement}
                        <p>${item.description}</p>
                    `;
                    portfolioItemsContainer.appendChild(itemDiv);
                });
            } else {
                portfolioItemsContainer.innerHTML = '<p>No portfolio items found.</p>';
            }
        } catch (error) {
            console.error('Error loading portfolio items:', error);
            portfolioItemsContainer.innerHTML = '<p>Failed to load portfolio items.</p>';
        }
    };

    loadPortfolioItems();
});




// Get the modal
const modal = document.getElementById("myModal");

// Get the image and video elements inside the modal
const modalImg = document.getElementById("img01");
const modalVid = document.getElementById("vid01");
const modalContentContainer = document.getElementById("modal-content-container");

// Get the <span> element that closes the modal
const span = document.getElementsByClassName("close")[0];

// Function to open the modal
window.openModal = (src, type) => {
    modal.style.display = "flex"; // Use flex to center content
    if (type === "image") {
        modalImg.src = src;
        modalImg.style.display = "block";
        modalVid.style.display = "none";
        modalImg.classList.add("image-content");
        modalVid.classList.remove("video-content");
    } else if (type === "video") {
        modalVid.src = src;
        modalVid.style.display = "block";
        modalImg.style.display = "none";
        modalVid.classList.add("video-content");
        modalImg.classList.remove("image-content");
        modalVid.load(); // Load the video to ensure it plays
        modalVid.play(); // Autoplay video
    }
}

// When the user clicks on <span> (x), close the modal
span.onclick = () => {
    modal.style.display = "none";
    modalVid.pause(); // Pause video when closing modal
    modalVid.currentTime = 0; // Reset video to start
}

// When the user clicks anywhere outside of the modal content, close it
window.onclick = (event) => {
    if (event.target == modal) {
        modal.style.display = "none";
        modalVid.pause(); // Pause video when closing modal
        modalVid.currentTime = 0; // Reset video to start
    }
}


