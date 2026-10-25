/**
 * ============================================================================
 * Prakriti: Nature & Belief Explorer - Main Client Script
 * ============================================================================
 * Handles:
 * 1. Mobile menu toggle
 * 2. Real-time client-side search & filtering on Browse page
 * 3. Tab switching in Admin dashboard
 * 4. Dismissible alerts & smooth interactions
 * ============================================================================
 */

document.addEventListener("DOMContentLoaded", function () {
  // --------------------------------------------------------------------------
  // 1. Mobile Navigation Toggle
  // --------------------------------------------------------------------------
  const mobileToggle = document.querySelector(".mobile-toggle");
  const navMenu = document.querySelector(".nav-menu");

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener("click", function () {
      navMenu.classList.toggle("open");
      const isExpanded = navMenu.classList.contains("open");
      mobileToggle.setAttribute("aria-expanded", isExpanded);
    });
  }

  // --------------------------------------------------------------------------
  // 2. Client-side Live Filter on Browse Page
  // --------------------------------------------------------------------------
  const searchInput = document.getElementById("browseSearchInput");
  const categoryPills = document.querySelectorAll(".filter-pill");
  const festivalSelect = document.getElementById("festivalFilterSelect");
  const elementCards = document.querySelectorAll(".browse-element-card");
  const resultsCounter = document.getElementById("resultsCounter");
  const noResultsBox = document.getElementById("noResultsMessage");

  let activeCategory = "All";
  let activeFestivalId = "";

  function filterElements() {
    const query = searchInput ? searchInput.value.toLowerCase().trim() : "";
    let visibleCount = 0;

    elementCards.forEach((card) => {
      const name = (card.dataset.name || "").toLowerCase();
      const category = card.dataset.category || "";
      const description = (card.dataset.description || "").toLowerCase();
      const festivals = (card.dataset.festivals || "").toLowerCase();
      const festivalId = card.dataset.festivalId || "";

      // Match category
      const matchesCategory =
        activeCategory === "All" || category === activeCategory;

      // Match festival dropdown
      const matchesFestival =
        !activeFestivalId ||
        festivalId === activeFestivalId ||
        festivals.includes(activeFestivalId.toLowerCase());

      // Match search query across name, description, category
      const matchesSearch =
        !query ||
        name.includes(query) ||
        description.includes(query) ||
        category.toLowerCase().includes(query) ||
        festivals.includes(query);

      if (matchesCategory && matchesFestival && matchesSearch) {
        card.style.display = "flex";
        visibleCount++;
      } else {
        card.style.display = "none";
      }
    });

    // Update results counter
    if (resultsCounter) {
      resultsCounter.textContent = `Showing ${visibleCount} nature element${
        visibleCount === 1 ? "" : "s"
      }`;
    }

    // Toggle No Results placeholder
    if (noResultsBox) {
      noResultsBox.style.display = visibleCount === 0 ? "block" : "none";
    }
  }

  // Attach search input listener
  if (searchInput) {
    searchInput.addEventListener("input", filterElements);
  }

  // Attach category pills listeners
  if (categoryPills.length > 0) {
    categoryPills.forEach((pill) => {
      pill.addEventListener("click", function () {
        categoryPills.forEach((p) => p.classList.remove("active"));
        this.classList.add("active");
        activeCategory = this.dataset.category || "All";
        filterElements();
      });
    });
  }

  // Attach festival dropdown listener
  if (festivalSelect) {
    festivalSelect.addEventListener("change", function () {
      activeFestivalId = this.value;
      filterElements();
    });
  }

  // --------------------------------------------------------------------------
  // 3. Admin Dashboard Tabs
  // --------------------------------------------------------------------------
  const tabButtons = document.querySelectorAll(".admin-tab-btn");
  const tabSections = document.querySelectorAll(".admin-tab-content");

  if (tabButtons.length > 0 && tabSections.length > 0) {
    tabButtons.forEach((btn) => {
      btn.addEventListener("click", function () {
        const targetTab = this.dataset.tab;

        // Activate button
        tabButtons.forEach((b) => b.classList.remove("active"));
        this.classList.add("active");

        // Show target section
        tabSections.forEach((section) => {
          if (section.id === targetTab) {
            section.style.display = "block";
          } else {
            section.style.display = "none";
          }
        });
      });
    });
  }

  // --------------------------------------------------------------------------
  // 4. Auto-dismiss Flash Alerts
  // --------------------------------------------------------------------------
  const alerts = document.querySelectorAll(".alert");
  if (alerts.length > 0) {
    setTimeout(() => {
      alerts.forEach((alert) => {
        alert.style.transition = "opacity 0.5s ease";
        alert.style.opacity = "0";
        setTimeout(() => alert.remove(), 500);
      });
    }, 4500);
  }
});
