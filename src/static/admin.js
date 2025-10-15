document.addEventListener("DOMContentLoaded", () => {
    const adminIdInput = document.getElementById("admin-id");
    const loginForm = document.getElementById("login-form");
    const loginMessage = document.getElementById("login-message");
    const adminPanel = document.getElementById("admin-panel");
    const loginSection = document.getElementById("login-section");
    const addItemForm = document.getElementById("add-item-form");
    const portfolioAdminList = document.getElementById("portfolio-admin-list");
    const itemSrcInput = document.getElementById("item-src");
    const itemFileInput = document.getElementById("item-file");
    const itemTypeSelect = document.getElementById("item-type");
    const uploadStatus = document.getElementById("upload-status");

    let currentAdminId = null;

    const setLoginMessage = (message) => {
        loginMessage.textContent = message || "";
    };

    const setUploadStatus = (message, statusClass = "") => {
        if (!uploadStatus) {
            return;
        }
        const classes = ["upload-status"];
        if (statusClass) {
            classes.push(statusClass);
        }
        uploadStatus.className = classes.join(" ");
        uploadStatus.textContent = message || "";
    };

    const resetUploadState = () => {
        if (itemFileInput) {
            itemFileInput.value = "";
        }
        setUploadStatus("");
    };

    const clearPortfolioList = () => {
        while (portfolioAdminList.firstChild) {
            portfolioAdminList.removeChild(portfolioAdminList.firstChild);
        }
    };

    const setPortfolioListStatus = (message) => {
        clearPortfolioList();
        const statusItem = document.createElement("li");
        statusItem.textContent = message;
        portfolioAdminList.appendChild(statusItem);
    };

    const renderAdminPortfolioItems = (items) => {
        clearPortfolioList();
        if (!Array.isArray(items) || items.length === 0) {
            setPortfolioListStatus("No items found.");
            return;
        }

        items.forEach((item) => {
            const listItem = document.createElement("li");

            const info = document.createElement("span");
            const displayTitle = item.title || "Untitled";
            const displayCategory = item.category || "Uncategorized";
            const displayType = item.type || "unknown";
            info.textContent = `${displayTitle} (${displayCategory}) - ${displayType}`;

            const deleteButton = document.createElement("button");
            deleteButton.type = "button";
            deleteButton.textContent = "Delete";
            deleteButton.addEventListener("click", () => handleDeleteItem(item.id));

            listItem.appendChild(info);
            listItem.appendChild(deleteButton);
            portfolioAdminList.appendChild(listItem);
        });
    };

    const loadAdminPortfolioItems = async () => {
        setPortfolioListStatus("Loading items...");
        try {
            const response = await fetch("/api/portfolio");
            if (!response.ok) {
                throw new Error(`Request failed with status ${response.status}`);
            }
            const data = await response.json();
            renderAdminPortfolioItems(data.portfolio);
        } catch (error) {
            console.error("Error loading admin portfolio items:", error);
            setPortfolioListStatus("Failed to load items.");
        }
    };

    const handleFileUpload = async (file) => {
        if (!file) {
            return;
        }

        if (!currentAdminId) {
            alert("Please login before uploading files.");
            resetUploadState();
            return;
        }

        setUploadStatus(`Uploading ${file.name}...`);

        const formData = new FormData();
        formData.append("admin_id", currentAdminId);
        formData.append("file", file);

        try {
            const response = await fetch("/api/portfolio/upload", {
                method: "POST",
                body: formData,
            });

            const result = await response.json();
            if (!response.ok) {
                throw new Error(result.error || "Upload failed");
            }

            if (itemSrcInput) {
                itemSrcInput.value = result.src || "";
            }
            if (itemTypeSelect && result.type) {
                const normalizedType = result.type.toLowerCase();
                if (["image", "video"].includes(normalizedType)) {
                    itemTypeSelect.value = normalizedType;
                }
            }

            setUploadStatus(`Uploaded ${file.name}`, "success");
        } catch (error) {
            console.error("Upload error:", error);
            setUploadStatus(error.message || "Upload failed.", "error");
            if (itemFileInput) {
                itemFileInput.value = "";
            }
        }
    };

    if (itemFileInput) {
        itemFileInput.disabled = true;
        itemFileInput.addEventListener("change", async () => {
            const [file] = itemFileInput.files || [];
            if (!file) {
                resetUploadState();
                return;
            }
            await handleFileUpload(file);
        });
    }

    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const adminId = (adminIdInput.value || "").trim();
        if (!adminId) {
            setLoginMessage("Please enter an Admin ID.");
            return;
        }

        try {
            const response = await fetch("/api/admin/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ admin_id: adminId }),
            });

            const result = await response.json();
            if (response.ok && result.success) {
                currentAdminId = adminId;
                setLoginMessage("");
                loginSection.style.display = "none";
                adminPanel.style.display = "block";
                if (itemFileInput) {
                    itemFileInput.disabled = false;
                }
                await loadAdminPortfolioItems();
            } else {
                setLoginMessage(result.message || "Invalid Admin ID");
            }
        } catch (error) {
            console.error("Login error:", error);
            setLoginMessage("Login failed. Please try again.");
        }
    });

    addItemForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        if (!currentAdminId) {
            alert("Please login before adding items.");
            return;
        }

        const title = document.getElementById("item-title").value.trim();
        const src = itemSrcInput ? itemSrcInput.value.trim() : "";
        const type = itemTypeSelect ? itemTypeSelect.value : "";
        const category = document.getElementById("item-category").value.trim();
        const description = document.getElementById("item-description").value.trim();

        if (!title || !src || !category || !type) {
            alert("Please fill in all required fields.");
            return;
        }

        const payload = {
            admin_id: currentAdminId,
            items: [
                {
                    title,
                    src,
                    type,
                    category,
                    description,
                },
            ],
        };

        try {
            const response = await fetch("/api/portfolio", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            });

            const result = await response.json();
            if (response.ok) {
                alert("Item added successfully!");
                addItemForm.reset();
                resetUploadState();
                if (itemSrcInput) {
                    itemSrcInput.value = "";
                }
                await loadAdminPortfolioItems();
            } else {
                alert(`Failed to add item: ${result.error || "Unknown error"}`);
            }
        } catch (error) {
            console.error("Error adding item:", error);
            alert("Failed to add item. Please try again.");
        }
    });

    const handleDeleteItem = async (itemId) => {
        if (!currentAdminId) {
            alert("Please login before deleting items.");
            return;
        }
        if (!confirm(`Are you sure you want to delete item ${itemId}?`)) {
            return;
        }

        try {
            const response = await fetch(`/api/portfolio/${itemId}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ admin_id: currentAdminId }),
            });

            const result = await response.json();
            if (response.ok) {
                alert("Item deleted successfully!");
                await loadAdminPortfolioItems();
            } else {
                alert(`Failed to delete item: ${result.error || "Unknown error"}`);
            }
        } catch (error) {
            console.error("Error deleting item:", error);
            alert("Failed to delete item. Please try again.");
        }
    };
});
