/**
 * Mock Analytics Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // Default Data
    let trendData = { "Jun 14": 412, "Jun 15": 380, "Jun 16": 450, "Jun 17": 510, "Jun 18": 490, "Jun 19": 605, "Jun 20": 580 };
    let typeData = { 
        "Helmet Non-Compliance": 45, 
        "Red-Light": 25, 
        "Triple Riding": 18, 
        "Stop-Line": 15, 
        "Wrong-Side": 12, 
        "Illegal Parking": 20, 
        "Speeding": 10 
    };
    let camData = { "CAM-N-01": 340, "CAM-S-04": 290, "CAM-E-05": 210, "CAM-W-12": 150, "CAM-N-08": 90 };
    let statusData = { "OPEN": 15, "APPROVED": 65, "REJECTED": 15, "ESCALATED": 5 };

    // Function to render all charts
    const renderAllCharts = () => {
        if(typeof renderViolationTrendChart === 'function') {
            renderViolationTrendChart("trendChart", trendData);
            renderViolationTypeChart("typeChart", typeData);
            renderCameraChart("cameraChart", camData);
            renderStatusChart("statusChart", statusData);
        } else {
            console.error("charts.js not loaded or functions not found.");
        }
    };

    // Initial render
    setTimeout(renderAllCharts, 100);

    // Mock Interactivity (Filter Changes)
    const filters = ['filterType', 'filterCam', 'filterReviewer'];
    
    const randomizeData = () => {
        // Randomize trend
        const keys = Object.keys(trendData);
        keys.forEach(k => trendData[k] = Math.floor(Math.random() * 400) + 100);
        
        // Randomize types
        typeData["Helmet Non-Compliance"] = Math.floor(Math.random() * 50) + 20;
        typeData["Red-Light"] = Math.floor(Math.random() * 30) + 10;
        typeData["Triple Riding"] = Math.floor(Math.random() * 25) + 5;
        typeData["Stop-Line"] = Math.floor(Math.random() * 20) + 5;
        typeData["Wrong-Side"] = Math.floor(Math.random() * 15) + 2;
        typeData["Illegal Parking"] = Math.floor(Math.random() * 30) + 10;
        typeData["Speeding"] = Math.floor(Math.random() * 20) + 5;
        
        // Randomize Cameras
        camData["CAM-N-01"] = Math.floor(Math.random() * 300) + 100;
        camData["CAM-S-04"] = Math.floor(Math.random() * 200) + 50;
        
        // Randomize Status
        statusData["APPROVED"] = Math.floor(Math.random() * 60) + 40;
        statusData["OPEN"] = Math.floor(Math.random() * 20) + 5;

        // Randomize KPIs
        document.getElementById('kpiTotal').innerText = (Math.floor(Math.random() * 5000) + 5000).toLocaleString();
        document.getElementById('kpiPending').innerText = (Math.random() * 10 + 2).toFixed(1) + "%";
        document.getElementById('kpiAuto').innerText = (Math.random() * 30 + 50).toFixed(1) + "%";
        
        // Randomize Insight
        const insights = [
            "<strong>CAM-South-04</strong> saw a 15% spike in helmet violations during evening hours.",
            "<strong>Speeding</strong> incidents have dropped 8% across all zones compared to last period.",
            "<strong>R. Vargas</strong> has an exceptional turnaround time averaging 1m 45s this week.",
            "<strong>ANPR failures</strong> increased slightly at CAM-East-05 due to adverse weather conditions."
        ];
        document.getElementById('dynamicInsight').innerHTML = insights[Math.floor(Math.random() * insights.length)];

        renderAllCharts();
    };

    filters.forEach(id => {
        const el = document.getElementById(id);
        if(el) {
            el.addEventListener('change', () => {
                // Show loading state temporarily on KPIs
                document.getElementById('kpiTotal').innerText = "...";
                document.getElementById('kpiPending').innerText = "...";
                
                setTimeout(randomizeData, 400);
            });
        }
    });

    // Time Toggle Interactivity
    const toggles = document.querySelectorAll('.chart-toggles .btn-text');
    toggles.forEach(toggle => {
        toggle.addEventListener('click', (e) => {
            toggles.forEach(t => t.classList.remove('active'));
            e.target.classList.add('active');
            
            let txt = e.target.innerText;
            if(txt === '7D') {
                trendData = { "Jun 14": 412, "Jun 15": 380, "Jun 16": 450, "Jun 17": 510, "Jun 18": 490, "Jun 19": 605, "Jun 20": 580 };
            } else if(txt === '30D') {
                trendData = { "Week 1": 2100, "Week 2": 2400, "Week 3": 2150, "Week 4": 2800 };
            } else if(txt === '90D') {
                trendData = { "April": 8400, "May": 9100, "June": 11200 };
            }
            if(typeof renderViolationTrendChart === 'function') {
                renderViolationTrendChart("trendChart", trendData);
            }
        });
    });

    // Export Interactivity
    const btnExport = document.getElementById('btnExportReport');
    if(btnExport) {
        btnExport.addEventListener('click', () => {
            // Re-use toast logic from main app or create a simple one
            let container = document.getElementById('toastContainer');
            if (!container) {
                container = document.createElement('div');
                container.id = 'toastContainer';
                container.className = 'toast-container';
                document.body.appendChild(container);
            }

            const toast = document.createElement('div');
            toast.className = 'toast show';
            toast.innerText = "Exporting Analytics Report as PDF...";
            container.appendChild(toast);

            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => toast.remove(), 300);
            }, 3000);
        });
    }

});
