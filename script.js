let globalNicData = []; // This will hold all your CSV rows

const nicSections = [
    { id: 'A', title: 'Agriculture, Forestry and Fishing' },
    { id: 'B', title: 'Mining and Quarrying' },
    { id: 'C', title: 'Manufacturing' },
    // ... add the rest of the 21 sections here
];

// 1. Load the CSV as soon as the page opens
window.onload = () => {
    loadCSV();
    renderCategoryGrid();
};

function loadCSV() {
    Papa.parse("/static/latest_nic_dataset.csv", {
        download: true,
        header: true,
        complete: function(results) {
            globalNicData = results.data;
            console.log("CSV Loaded successfully:", globalNicData.length, "rows found.");
        }
    });
}

function renderCategoryGrid() {
    const categoryGrid = document.getElementById('categoryGrid');
    nicSections.forEach(cat => {
        const card = document.createElement('div');
        card.className = 'category-card';
        card.innerHTML = `<span>Section ${cat.id}</span><p>${cat.title}</p>`;
        
        card.onclick = () => {
            document.querySelectorAll('.category-card').forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            displayFilteredCodes(cat.id, cat.title);
        };
        categoryGrid.appendChild(card);
    });
}

// 2. Filter the global data based on the Section ID (A, B, C, etc.)
function displayFilteredCodes(sectionId, sectionTitle) {
    const codesList = document.getElementById('codesList');
    const selectedTitle = document.getElementById('selectedCategoryTitle');
    
    selectedTitle.innerText = `Section ${sectionId}: ${sectionTitle}`;
    
    // Filter the CSV data
    const filtered = globalNicData.filter(row => row.Section === sectionId);

    if (filtered.length > 0) {
        codesList.innerHTML = filtered.map(item => `
            <div class="code-item">
                <b>${item.Code}</b> ${item.Description}
            </div>
        `).join('');
    } else {
        codesList.innerHTML = '<p class="placeholder-text">No codes found for this section in the CSV.</p>';
    }
}