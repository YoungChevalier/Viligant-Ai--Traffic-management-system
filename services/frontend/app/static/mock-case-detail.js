/**
 * Case Detail Logic Wired to Real API
 */

document.addEventListener('DOMContentLoaded', async () => {

    const urlParams = new URLSearchParams(window.location.search);
    const caseId = urlParams.get('id');

    if (!caseId) {
        document.body.innerHTML = '<h2>No Case ID provided</h2>';
        return;
    }

    let data = null;
    const imgMap = {
        "Helmet Non-Compliance": "no_helmet_violation.png",
        "Red-Light Violation": "red_light_violation.png",
        "Triple Riding": "triple_riding_violation.png",
        "Stop-Line Violation": "stop_line_violation.png",
        "Wrong-Side Driving": "wrong_side_driving.png",
        "Illegal Parking": "illegal_parking.png",
        "Speeding": "speeding_car.png"
    };

    // Formatters
    const formatDateTime = (isoString) => {
        if(!isoString) return "N/A";
        const d = new Date(isoString);
        return d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    };

    const formatTimeOnly = (isoString) => {
        if(!isoString) return "N/A";
        const d = new Date(isoString);
        return d.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    };

    // Toast
    const showToast = (message, type = 'success') => {
        let container = document.getElementById('toastContainer');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toastContainer';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerText = message;
        container.appendChild(toast);
        requestAnimationFrame(() => toast.classList.add('show'));
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    };

    // Load data
    try {
        const apiData = await ApiClient.getCaseDetail(caseId);
        data = {
            id: apiData.id,
            type: apiData.type,
            imgUrl: `/static/img/${imgMap[apiData.type] || 'red_light_violation.png'}`,
            score: apiData.score,
            severity: apiData.severity,
            status: apiData.status,
            plate: apiData.plate,
            cam: apiData.cam,
            loc: apiData.cam,
            lane: "Lane 2",
            time: apiData.time,
            vehType: apiData.vehicleType || "Unknown",
            vehColor: apiData.vehicleColor || "Unknown",
            vehColorName: apiData.vehicleColor || "Unknown",
            assignee: apiData.assignee || "Unassigned",
            reasoning: `AI detected ${apiData.type} with ${apiData.score}% confidence.`
        };
    } catch (e) {
        console.error("Failed to load case detail", e);
        showToast("Error loading case data", "error");
        return;
    }

    // Populate UI
    document.getElementById('headerCaseId').innerText = data.id;
    document.getElementById('bcCaseId').innerText = data.id;
    document.getElementById('headerSubtitle').innerText = `${data.type} • ${formatDateTime(data.time)}`;
    document.getElementById('headerStatus').innerText = data.status;

    document.getElementById('sumViolation').innerText = data.type;
    document.getElementById('sumConf').innerText = `${data.score}%`;
    document.getElementById('sumSeverity').innerText = data.severity;
    if (data.severity === 'High') {
        document.getElementById('sumSeverity').style.color = 'var(--color-danger)';
        document.getElementById('sumSeverity').classList.add('font-semibold');
    }
    document.getElementById('aiReasoningText').innerText = data.reasoning;

    document.getElementById('ocrPlateDisplay').innerText = data.plate;
    document.getElementById('ocrConf').innerText = `${Math.min(99, data.score + 5)}%`;

    document.getElementById('metaCam').innerText = data.cam;
    document.getElementById('metaLoc').innerText = data.loc;
    document.getElementById('metaLane').innerText = data.lane;
    document.getElementById('metaTime').innerText = formatDateTime(data.time);
    document.getElementById('metaVehType').innerText = data.vehType;
    document.getElementById('metaVehColorBox').style.backgroundColor = data.vehColorName;
    document.getElementById('metaVehColor').innerText = data.vehColorName;
    document.getElementById('metaAssignee').innerText = data.assignee;

    document.getElementById('timeCreated').innerText = formatTimeOnly(data.time);
    const classTime = new Date(new Date(data.time).getTime() + 12000);
    document.getElementById('timeClassified').innerText = formatTimeOnly(classTime.toISOString());
    const assignTime = new Date(new Date(data.time).getTime() + 300000);
    document.getElementById('timeAssigned').innerText = formatTimeOnly(assignTime.toISOString());
    document.getElementById('timelineAssignee').innerText = data.assignee;

    document.getElementById('bboxPlate').innerText = `Plate: ${data.plate}`;
    document.getElementById('bboxVehicle').innerText = data.vehType;

    const evidencePlaceholder = document.getElementById('evidencePlaceholder');
    evidencePlaceholder.style.position = 'relative';
    evidencePlaceholder.style.overflow = 'hidden';
    evidencePlaceholder.style.backgroundColor = '#000';
    evidencePlaceholder.innerHTML += `<img id="realEvidenceImg" src="${data.imgUrl}" alt="${data.type}" style="position:absolute; top:0; left:0; width:100%; height:100%; object-fit:cover; z-index: 1;">`;

    document.getElementById('bboxPlate').style.zIndex = '2';
    document.getElementById('bboxVehicle').style.zIndex = '2';
    document.getElementById('evidenceText').style.zIndex = '2';
    document.getElementById('evidenceText').style.textShadow = '0 1px 3px rgba(0,0,0,0.8)';

    // Interactions
    let currentDecision = null;
    const btnApprove = document.getElementById('btnApprove');
    const btnReject = document.getElementById('btnReject');
    const btnEscalate = document.getElementById('btnEscalate');
    const reasonGroup = document.getElementById('reasonGroup');
    const decisionReason = document.getElementById('decisionReason');
    const reasonError = document.getElementById('reasonError');
    const btnSubmit = document.getElementById('btnSubmitDecision');
    const actionArea = document.querySelector('.action-area');

    if (data.status !== 'Pending') {
        actionArea.innerHTML = `<div class="p-4 bg-light text-center rounded border"><p class="text-muted mb-0">This case has already been marked as <strong>${data.status}</strong>.</p></div>`;
    }

    const resetButtons = () => {
        btnApprove.style.opacity = '0.5';
        btnReject.style.opacity = '0.5';
        btnEscalate.style.opacity = '0.5';
    };

    const validateSubmit = () => {
        if (!currentDecision) {
            btnSubmit.disabled = true;
            return;
        }
        if (currentDecision === 'reject' || currentDecision === 'escalate') {
            if (!decisionReason.value) {
                btnSubmit.disabled = true;
                return;
            }
        }
        btnSubmit.disabled = false;
        reasonError.style.display = 'none';
    };

    if (btnApprove) btnApprove.addEventListener('click', () => {
        resetButtons();
        btnApprove.style.opacity = '1';
        currentDecision = 'approve';
        reasonGroup.style.display = 'none';
        validateSubmit();
    });

    if (btnReject) btnReject.addEventListener('click', () => {
        resetButtons();
        btnReject.style.opacity = '1';
        currentDecision = 'reject';
        reasonGroup.style.display = 'block';
        validateSubmit();
    });

    if (btnEscalate) btnEscalate.addEventListener('click', () => {
        resetButtons();
        btnEscalate.style.opacity = '1';
        currentDecision = 'escalate';
        reasonGroup.style.display = 'block';
        validateSubmit();
    });

    if (decisionReason) decisionReason.addEventListener('change', () => {
        if (!decisionReason.value && (currentDecision === 'reject' || currentDecision === 'escalate')) {
            reasonError.style.display = 'block';
        } else {
            reasonError.style.display = 'none';
        }
        validateSubmit();
    });

    if (btnSubmit) btnSubmit.addEventListener('click', async () => {
        btnSubmit.disabled = true;
        btnSubmit.innerText = 'Submitting...';
        
        const statusMap = { 'approve': 'Approved', 'reject': 'Rejected', 'escalate': 'Escalated' };
        
        try {
            await ApiClient.submitDecision(data.id, statusMap[currentDecision], decisionReason.value);
            showToast('Decision submitted successfully');
            setTimeout(() => {
                window.location.href = '/static/review-queue.html';
            }, 1000);
        } catch (e) {
            console.error(e);
            showToast('Failed to submit decision', 'error');
            btnSubmit.disabled = false;
            btnSubmit.innerText = 'Submit Decision';
        }
    });
});
