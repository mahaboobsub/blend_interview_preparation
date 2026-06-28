// app.js - Study Hub Client Application

document.addEventListener("DOMContentLoaded", () => {
    // 1. Core State
    let state = {
        questions: window.QUESTIONS_DATA || [],
        categories: {
            "sql_db": "SQL, DB Design & DBMS Deep Concepts",
            "dsa": "Data Structures & Algorithms (DSA)",
            "ml_stats": "Machine Learning & Statistics",
            "dl_cv": "Deep Learning & Computer Vision",
            "genai_rag": "Generative AI, RAG & Agents",
            "fullstack": "Fullstack Development (JS/Python/REST)",
            "devops_projects": "DevOps, System Design & Projects"
        },
        currentCategory: null, // null means show welcome dashboard
        searchQuery: "",
        flashcardMode: false,
        reviewedIds: JSON.parse(localStorage.getItem("reviewed_questions")) || []
    };

    // 2. DOM Elements Cache
    const dom = {
        categoryList: document.getElementById("category-list"),
        cardsContainer: document.getElementById("cards-container"),
        searchInput: document.getElementById("search-input"),
        progressPercent: document.getElementById("progress-percent"),
        progressFill: document.getElementById("progress-fill"),
        progressFraction: document.getElementById("progress-fraction"),
        currentTitle: document.getElementById("current-category-title"),
        toggleFlashcardBtn: document.getElementById("toggle-flashcard-mode"),
        resetProgressBtn: document.getElementById("reset-progress"),
        welcomeDashboard: document.getElementById("welcome-dashboard"),
        statSql: document.getElementById("stat-sql"),
        statDsa: document.getElementById("stat-dsa"),
        statMl: document.getElementById("stat-ml"),
        statGenai: document.getElementById("stat-genai")
    };

    // 3. Init Function
    function init() {
        calculateStats();
        renderCategoryMenu();
        updateProgressBar();
        setupEventListeners();
        renderDashboard();
    }

    // 4. Calculate dashboard statistics
    function calculateStats() {
        const counts = { sql_db: 0, dsa: 0, ml_stats: 0, dl_cv: 0, genai_rag: 0 };
        state.questions.forEach(q => {
            if (counts[q.category] !== undefined) {
                counts[q.category]++;
            }
        });
        
        if (dom.statSql) dom.statSql.textContent = counts.sql_db;
        if (dom.statDsa) dom.statDsa.textContent = counts.dsa;
        if (dom.statMl) dom.statMl.textContent = counts.ml_stats + counts.dl_cv;
        if (dom.statGenai) dom.statGenai.textContent = counts.genai_rag;
    }

    // 5. Render sidebar categories with status counts
    function renderCategoryMenu() {
        dom.categoryList.innerHTML = "";
        
        // Add Dashboard link
        const dashLi = document.createElement("li");
        dashLi.className = `category-item ${state.currentCategory === null ? "active" : ""}`;
        dashLi.innerHTML = `
            <span class="category-title"><i class="fa-solid fa-gauge" style="margin-right: 8px;"></i>Dashboard</span>
        `;
        dashLi.addEventListener("click", () => {
            state.currentCategory = null;
            state.searchQuery = "";
            dom.searchInput.value = "";
            renderCategoryMenu();
            renderDashboard();
        });
        dom.categoryList.appendChild(dashLi);

        // Add each topic category
        Object.entries(state.categories).forEach(([key, title]) => {
            const catQuestions = state.questions.filter(q => q.category === key);
            const completedCount = catQuestions.filter(q => state.reviewedIds.includes(q.id)).length;
            
            const li = document.createElement("li");
            li.className = `category-item ${state.currentCategory === key ? "active" : ""}`;
            li.innerHTML = `
                <span class="category-title">${title}</span>
                <span class="category-badge">${completedCount}/${catQuestions.length}</span>
            `;
            
            li.addEventListener("click", () => {
                state.currentCategory = key;
                state.searchQuery = "";
                dom.searchInput.value = "";
                renderCategoryMenu();
                renderCards();
            });
            dom.categoryList.appendChild(li);
        });
    }

    // 6. Update progress bars
    function updateProgressBar() {
        const total = state.questions.length;
        const completed = state.reviewedIds.filter(id => state.questions.some(q => q.id === id)).length;
        const percent = total > 0 ? Math.round((completed / total) * 100) : 0;
        
        dom.progressPercent.textContent = `${percent}%`;
        dom.progressFill.style.width = `${percent}%`;
        dom.progressFraction.textContent = `${completed}/${total} Completed`;
    }

    // 7. Render Dashboard
    function renderDashboard() {
        dom.welcomeDashboard.style.display = "flex";
        dom.currentTitle.textContent = "Study Dashboard";
        
        // Remove existing question cards
        const cards = dom.cardsContainer.querySelectorAll(".qa-grid");
        cards.forEach(c => c.remove());
    }

    // 8. Render Q&A cards
    function renderCards() {
        dom.welcomeDashboard.style.display = "none";
        
        // Remove existing cards
        const existing = dom.cardsContainer.querySelectorAll(".qa-grid");
        existing.forEach(c => c.remove());

        let listToRender = [];
        if (state.searchQuery) {
            dom.currentTitle.textContent = `Search Results: "${state.searchQuery}"`;
            const query = state.searchQuery.toLowerCase();
            listToRender = state.questions.filter(q => 
                q.question.toLowerCase().includes(query) || 
                q.answer.toLowerCase().includes(query)
            );
        } else {
            dom.currentTitle.textContent = state.categories[state.currentCategory];
            listToRender = state.questions.filter(q => q.category === state.currentCategory);
        }

        if (listToRender.length === 0) {
            const noResults = document.createElement("div");
            noResults.className = "qa-grid quick-start";
            noResults.innerHTML = `<h3>No questions found matching the selection</h3>`;
            dom.cardsContainer.appendChild(noResults);
            return;
        }

        const grid = document.createElement("div");
        grid.className = "qa-grid";

        listToRender.forEach(q => {
            const isReviewed = state.reviewedIds.includes(q.id);
            const card = document.createElement("div");
            card.className = `qa-card category-${q.category} ${isReviewed ? "reviewed" : ""} ${state.flashcardMode ? "flashcard-hidden" : ""}`;
            card.dataset.id = q.id;

            // Generate metadata badges
            let badgesHtml = `<span class="qa-badge">${q.subcategory}</span>`;
            if (q.is_coding) badgesHtml += `<span class="qa-badge" style="background: rgba(139, 92, 246, 0.1); color: var(--accent-purple);">Coding</span>`;

            // Coding panel HTML (SQL / Java / Python tabs)
            let codeSectionHtml = "";
            if (q.is_coding) {
                let tabsHtml = "";
                let codeBlocksHtml = "";

                if (q.code_sql) {
                    tabsHtml += `<button class="code-tab active" data-lang="sql">SQL Query</button>`;
                    codeBlocksHtml += `
                        <div class="code-block active" data-lang="sql">
                            <button class="btn-copy"><i class="fa-regular fa-copy"></i> Copy</button>
                            <pre><code>${escapeHtml(q.code_sql)}</code></pre>
                        </div>
                    `;
                }
                if (q.code_java) {
                    const isActive = !q.code_sql;
                    tabsHtml += `<button class="code-tab ${isActive ? "active" : ""}" data-lang="java">Java</button>`;
                    codeBlocksHtml += `
                        <div class="code-block ${isActive ? "active" : ""}" data-lang="java">
                            <button class="btn-copy"><i class="fa-regular fa-copy"></i> Copy</button>
                            <pre><code>${escapeHtml(q.code_java)}</code></pre>
                        </div>
                    `;
                }
                if (q.code_python) {
                    const isActive = !q.code_sql && !q.code_java;
                    tabsHtml += `<button class="code-tab ${isActive ? "active" : ""}" data-lang="python">Python</button>`;
                    codeBlocksHtml += `
                        <div class="code-block ${isActive ? "active" : ""}" data-lang="python">
                            <button class="btn-copy"><i class="fa-regular fa-copy"></i> Copy</button>
                            <pre><code>${escapeHtml(q.code_python)}</code></pre>
                        </div>
                    `;
                }

                codeSectionHtml = `
                    <div class="qa-code-section">
                        <div class="code-tabs">${tabsHtml}</div>
                        ${codeBlocksHtml}
                    </div>
                `;
            }

            // Convert simple markdown tags in answer (bullets & strong)
            const formattedAnswer = q.answer
                .replace(/\n\* (.*)/g, '\n<ul><li>$1</li></ul>')
                .replace(/<\/ul>\n<ul>/g, '')
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

            card.innerHTML = `
                <div class="qa-header">
                    <div class="qa-title-wrapper">
                        <div class="qa-meta">${badgesHtml}</div>
                        <h2 class="qa-question">${escapeHtml(q.question)}</h2>
                    </div>
                    <label class="reviewed-toggle">
                        <input type="checkbox" ${isReviewed ? "checked" : ""}>
                        <i class="${isReviewed ? "fa-solid fa-circle-check" : "fa-regular fa-circle"}"></i>
                        <span>Reviewed</span>
                    </label>
                </div>
                
                <button class="flashcard-reveal-btn">Reveal Explanation</button>
                
                <div class="qa-answer">${formattedAnswer}</div>
                ${codeSectionHtml}
            `;

            // Bind Event Listeners on Card
            bindCardEvents(card, q);
            grid.appendChild(card);
        });

        dom.cardsContainer.appendChild(grid);
    }

    // 9. Card Interaction handlers
    function bindCardEvents(card, questionData) {
        // Checked Box
        const checkbox = card.querySelector(".reviewed-toggle input");
        const checkIcon = card.querySelector(".reviewed-toggle i");
        
        checkbox.addEventListener("change", (e) => {
            const checked = e.target.checked;
            if (checked) {
                if (!state.reviewedIds.includes(questionData.id)) {
                    state.reviewedIds.push(questionData.id);
                }
                card.classList.add("reviewed");
                checkIcon.className = "fa-solid fa-circle-check";
            } else {
                state.reviewedIds = state.reviewedIds.filter(id => id !== questionData.id);
                card.classList.remove("reviewed");
                checkIcon.className = "fa-regular fa-circle";
            }
            
            localStorage.setItem("reviewed_questions", JSON.stringify(state.reviewedIds));
            updateProgressBar();
            renderCategoryMenu();
        });

        // Flashcard Reveal
        const revealBtn = card.querySelector(".flashcard-reveal-btn");
        revealBtn.addEventListener("click", () => {
            card.classList.remove("flashcard-hidden");
        });

        // Code tab swapping
        const tabs = card.querySelectorAll(".code-tab");
        const blocks = card.querySelectorAll(".code-block");
        
        tabs.forEach(tab => {
            tab.addEventListener("click", () => {
                const lang = tab.dataset.lang;
                tabs.forEach(t => t.classList.remove("active"));
                blocks.forEach(b => b.classList.remove("active"));
                
                tab.classList.add("active");
                card.querySelector(`.code-block[data-lang="${lang}"]`).classList.add("active");
            });
        });

        // Clipboard Copy
        const copyBtns = card.querySelectorAll(".btn-copy");
        copyBtns.forEach(btn => {
            btn.addEventListener("click", () => {
                const code = btn.nextElementSibling.querySelector("code").textContent;
                navigator.clipboard.writeText(code).then(() => {
                    btn.innerHTML = `<i class="fa-solid fa-check"></i> Copied!`;
                    btn.style.color = "var(--accent-green)";
                    setTimeout(() => {
                        btn.innerHTML = `<i class="fa-regular fa-copy"></i> Copy`;
                        btn.style.color = "var(--text-secondary)";
                    }, 2000);
                });
            });
        });
    }

    // 10. Global Event listeners setup
    function setupEventListeners() {
        // Toggle Flashcard Mode
        dom.toggleFlashcardBtn.addEventListener("click", () => {
            state.flashcardMode = !state.flashcardMode;
            dom.toggleFlashcardBtn.classList.toggle("btn-primary");
            dom.toggleFlashcardBtn.classList.toggle("btn-secondary");
            
            const cards = document.querySelectorAll(".qa-card");
            cards.forEach(card => {
                if (state.flashcardMode) {
                    card.classList.add("flashcard-hidden");
                } else {
                    card.classList.remove("flashcard-hidden");
                }
            });
        });

        // Reset progress
        dom.resetProgressBtn.addEventListener("click", () => {
            if (confirm("Are you sure you want to reset all progress tracking? This cannot be undone.")) {
                state.reviewedIds = [];
                localStorage.removeItem("reviewed_questions");
                init();
                if (state.currentCategory !== null) {
                    renderCards();
                }
            }
        });

        // Search inputs
        let debounceTimer;
        dom.searchInput.addEventListener("input", (e) => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                const value = e.target.value.trim();
                state.searchQuery = value;
                if (value) {
                    state.currentCategory = null;
                    renderCategoryMenu();
                    renderCards();
                } else {
                    state.currentCategory = null;
                    renderCategoryMenu();
                    renderDashboard();
                }
            }, 300);
        });
    }

    // Utility escape html
    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }

    // Start App
    init();
});
