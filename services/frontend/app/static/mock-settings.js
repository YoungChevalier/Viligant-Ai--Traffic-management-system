/**
 * Mock Settings Logic
 */

document.addEventListener('DOMContentLoaded', () => {

    // Store initial values to support "Reset to Defaults" and diff detection
    const initialStates = new Map();

    const getElementValue = (el) => {
        if(el.type === 'checkbox') return el.checked;
        return el.value;
    };

    const setElementValue = (el, val) => {
        if(el.type === 'checkbox') el.checked = val;
        else el.value = val;
    };

    // Initialize map
    const initMap = () => {
        document.querySelectorAll('.settings-section').forEach(section => {
            const inputs = section.querySelectorAll('.mock-setting');
            inputs.forEach(input => {
                initialStates.set(input, getElementValue(input));
            });
        });
    };

        const saveBtn = section.querySelector('.btn-save');
        const resetBtn = section.querySelector('.btn-reset');

        // Watch for changes to enable Save button
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                let hasChanges = false;
                inputs.forEach(inp => {
                    if(getElementValue(inp) !== initialStates.get(inp)) {
                        hasChanges = true;
                    }
                });
                
                if(saveBtn) {
                    saveBtn.disabled = !hasChanges;
                }
            });
            // Also handle 'change' for selects and checkboxes
            input.addEventListener('change', () => {
                let hasChanges = false;
                inputs.forEach(inp => {
                    if(getElementValue(inp) !== initialStates.get(inp)) {
                        hasChanges = true;
                    }
                });
                
                if(saveBtn) {
                    saveBtn.disabled = !hasChanges;
                }
            });
        });

        // Save Action
        if(saveBtn) {
            saveBtn.addEventListener('click', () => {
                // Update initial states to new values
                inputs.forEach(input => {
                    initialStates.set(input, getElementValue(input));
                });
                saveBtn.disabled = true;
                
                // Show success toast
                const sectionName = section.querySelector('.settings-section-title').innerText;
                if(window.showToast) {
                    window.showToast(`${sectionName} saved successfully.`, 'success');
                }
            });
        }

        // Reset Action
        if(resetBtn) {
            resetBtn.addEventListener('click', () => {
                inputs.forEach(input => {
                    setElementValue(input, initialStates.get(input));
                });
                if(saveBtn) saveBtn.disabled = true;
                if(window.showToast) {
                    window.showToast(`Reset to defaults.`, 'info');
                }
            });
        }
    });

    // Toast Utility (fallback if not in app.js)
    window.showToast = window.showToast || ((message, type = 'success') => {
        let container = document.getElementById('toastContainer');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toastContainer';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = 'toast show';
        if(type === 'error' || type === 'danger') toast.style.borderLeftColor = 'var(--color-danger)';
        if(type === 'warning') toast.style.borderLeftColor = 'var(--color-warning)';
        if(type === 'info') toast.style.borderLeftColor = 'var(--color-primary)';
        toast.innerText = message;
        
        container.appendChild(toast);

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    });

    // Boot
    const boot = async () => {
        try {
            const settings = await ApiClient.getSettings();
            settings.forEach(s => {
                const el = document.getElementById(s.key);
                if (el) {
                    if (s.value === "true") setElementValue(el, true);
                    else if (s.value === "false") setElementValue(el, false);
                    else setElementValue(el, s.value);
                }
            });
            initMap();
        } catch (e) {
            console.error("Failed to load settings", e);
            initMap(); // fallback
        }
    };
    boot();

});
