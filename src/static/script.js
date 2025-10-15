document.addEventListener("DOMContentLoaded", () => {
    const portfolioItemsContainer = document.getElementById("portfolio-items");
    const statusMessage = document.createElement("p");

    const setStatus = (message, cssClass = "") => {
        statusMessage.textContent = message;
        statusMessage.className = cssClass;
        if (!portfolioItemsContainer.contains(statusMessage)) {
            portfolioItemsContainer.appendChild(statusMessage);
        }
    };

    const clearStatus = () => {
        if (portfolioItemsContainer.contains(statusMessage)) {
            portfolioItemsContainer.removeChild(statusMessage);
        }
    };

    const createMediaElement = (item) => {
        const mediaType = (item.type || "").toLowerCase();
        const mediaSrc = item.src;
        if (!mediaSrc) {
            const fallback = document.createElement("p");
            fallback.textContent = "Missing media source.";
            fallback.className = "error-message";
            return fallback;
        }

        if (mediaType === "image") {
            const img = document.createElement("img");
            img.src = mediaSrc;
            img.alt = item.title || "Portfolio image";
            img.addEventListener("click", () => openModal(mediaSrc, "image"));
            return img;
        }
        if (mediaType === "video") {
            const video = document.createElement("video");
            video.src = mediaSrc;
            video.controls = true;
            video.addEventListener("click", () => openModal(mediaSrc, "video"));
            return video;
        }
        const fallback = document.createElement("p");
        fallback.textContent = "Unsupported media type.";
        fallback.className = "error-message";
        return fallback;
    };

    const renderPortfolioItems = (items) => {
        portfolioItemsContainer.innerHTML = "";
        if (!Array.isArray(items) || items.length === 0) {
            setStatus("No portfolio items found.", "loading");
            return;
        }

        clearStatus();
        items.forEach((item) => {
            const itemDiv = document.createElement("div");
            itemDiv.classList.add("portfolio-item");

            const title = document.createElement("h3");
            title.textContent = item.title || "Untitled";

            const category = document.createElement("p");
            category.textContent = `Category: ${item.category || "Uncategorized"}`;

            const description = document.createElement("p");
            description.textContent = item.description || "";

            itemDiv.appendChild(title);
            itemDiv.appendChild(category);
            itemDiv.appendChild(createMediaElement(item));
            if (description.textContent) {
                itemDiv.appendChild(description);
            }

            portfolioItemsContainer.appendChild(itemDiv);
        });
    };

    const loadPortfolioItems = async () => {
        setStatus("Loading portfolio…", "loading");
        try {
            const response = await fetch("/api/portfolio");
            if (!response.ok) {
                throw new Error(`Request failed with status ${response.status}`);
            }
            const data = await response.json();
            renderPortfolioItems(data.portfolio);
        } catch (error) {
            console.error("Error loading portfolio items:", error);
            setStatus("Failed to load portfolio items.", "error-message");
        }
    };

    loadPortfolioItems();
});

// Modal helpers

defineModalHandlers();

function defineModalHandlers() {
    const modal = document.getElementById("myModal");
    const modalImg = document.getElementById("img01");
    const modalVid = document.getElementById("vid01");
    const source = modalVid ? modalVid.querySelector("source") : null;
    const closeElement = document.getElementsByClassName("close")[0];

    if (!modal || !modalImg || !modalVid || !closeElement) {
        return;
    }

    window.openModal = (src, type) => {
        modal.style.display = "flex";
        if (type === "image") {
            modalImg.src = src;
            modalImg.style.display = "block";
            modalVid.style.display = "none";
            modalVid.pause();
            modalVid.currentTime = 0;
        } else if (type === "video") {
            modalVid.pause();
            modalVid.currentTime = 0;
            modalVid.removeAttribute("src");
            if (source) {
                source.src = src;
            }
            modalVid.src = src;
            modalVid.load();
            modalVid.play();
            modalVid.style.display = "block";
            modalImg.style.display = "none";
        }
    };

    const closeModal = () => {
        modal.style.display = "none";
        modalVid.pause();
        modalVid.currentTime = 0;
    };

    closeElement.addEventListener("click", closeModal);

    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            closeModal();
        }
    });
}
