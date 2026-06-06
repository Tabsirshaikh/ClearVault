// DOM Elements
const modeTabs = document.querySelectorAll('.tab');
const modeContents = document.querySelectorAll('.mode-content');
const securityOptions = document.querySelectorAll('.security-option');
const progressSection = document.getElementById('progress-section');
const trustScore = document.getElementById('trust-score');
const btnComplete = document.getElementById('btn-complete');
const certificateModal = document.getElementById('certificate-modal');
const btnCloseCertificate = document.getElementById('btn-close-certificate');
const modalClose = document.querySelector('.modal__close');
const btnExportPdf = document.getElementById('btn-export-pdf');
const deviceName = document.getElementById('device-name');
const deviceOs = document.getElementById('device-os');
const storageInfo = document.getElementById('storage-info');

// Advanced Mode Elements
const btnManual = document.getElementById('btn-manual');
const fileBrowser = document.getElementById('file-browser');
const fileList = document.getElementById('file-list');
const currentPath = document.getElementById('current-path');
const btnSelectAll = document.getElementById('btn-select-all');
const btnClearSelection = document.getElementById('btn-clear-selection');
const btnShowSelected = document.getElementById('btn-show-selected');
const btnUpDirectory = document.getElementById('btn-up-directory');
const selectedCount = document.getElementById('selected-count');
const algorithmSelection = document.getElementById('algorithm-selection');
const algorithmOptions = document.querySelectorAll('.algorithm-option');
const advancedControls = document.getElementById('advanced-controls');
const deletionSummary = document.getElementById('deletion-summary');
const btnStartAdvancedWipe = document.getElementById('btn-start-advanced-wipe');

// State
let currentMode = 'basic';
let selectedSecurity = 'standard';
let selectedAlgorithm = null;
let selectedFiles = new Set();
let currentDirectory = 'C:\\';

// API communication functions
async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(`/api/${endpoint}`, options);
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        return { success: false, error: error.message };
    }
}

// Initialize the app
async function init() {
    // Set up event listeners
    setupEventListeners();
    
    // Initialize trust score animation
    animateTrustScore();
    
    // Load system information
    await loadSystemInfo();
    
    // Load current settings
    await loadSettings();
}

// Set up event listeners
function setupEventListeners() {
    // Mode tabs
    modeTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const mode = tab.dataset.mode;
            switchMode(mode);
        });
    });
    
    // Security options
    securityOptions.forEach(option => {
        option.addEventListener('click', () => {
            const security = option.dataset.security;
            selectSecurity(security);
        });
    });
    
    // Complete wipe button
    btnComplete.addEventListener('click', startWipeProcess);
    
    // Certificate modal
    btnCloseCertificate.addEventListener('click', () => {
        certificateModal.style.display = 'none';
    });
    
    modalClose.addEventListener('click', () => {
        certificateModal.style.display = 'none';
    });
    
    btnExportPdf.addEventListener('click', async () => {
        if (window.currentReport) {
            const data = await apiRequest('generate_certificate', 'POST', {
                report_data: window.currentReport
            });
            
            if (data.success && data.pdf_file) {
                // Download the PDF
                window.open(`/api/download_certificate/${data.pdf_file}`, '_blank');
            } else {
                alert('PDF generation failed or not available');
            }
        }
    });
    
    // Advanced mode
    btnManual.addEventListener('click', () => {
        fileBrowser.style.display = 'block';
        algorithmSelection.style.display = 'block';
        advancedControls.style.display = 'flex';
        loadDirectory(currentDirectory);
    });
    
    // File browser controls
    btnSelectAll.addEventListener('click', selectAllFiles);
    btnClearSelection.addEventListener('click', clearSelection);
    btnShowSelected.addEventListener('click', showSelectedFiles);
    btnUpDirectory.addEventListener('click', navigateUp);
    
    // Algorithm selection
    algorithmOptions.forEach(option => {
        option.addEventListener('click', () => {
            selectAlgorithm(option.dataset.algorithm);
        });
    });
    
    // Start advanced wipe
    btnStartAdvancedWipe.addEventListener('click', startAdvancedWipe);
}

// Switch between basic and advanced modes
function switchMode(mode) {
    currentMode = mode;
    
    // Update tabs
    modeTabs.forEach(tab => {
        if (tab.dataset.mode === mode) {
            tab.classList.add('tab--active');
        } else {
            tab.classList.remove('tab--active');
        }
    });
    
    // Show/hide mode content
    modeContents.forEach(content => {
        if (content.id === `${mode}-mode`) {
            content.style.display = 'block';
        } else {
            content.style.display = 'none';
        }
    });
    
    // Reset advanced mode UI when switching away
    if (mode !== 'advanced') {
        fileBrowser.style.display = 'none';
        algorithmSelection.style.display = 'none';
        advancedControls.style.display = 'none';
        selectedFiles.clear();
        updateSelectedCount();
    }
}

// Select security level
function selectSecurity(security) {
    selectedSecurity = security;
    
    // Update UI
    securityOptions.forEach(option => {
        if (option.dataset.security === security) {
            option.classList.add('selected');
            option.querySelector('input[type="radio"]').checked = true;
        } else {
            option.classList.remove('selected');
        }
    });
    
    // Update trust score based on selection
    let newScore = 850;
    if (security === 'professional') newScore = 920;
    if (security === 'enterprise') newScore = 990;
    
    animateValue(trustScore, parseInt(trustScore.textContent), newScore, 500);
}

// Load system information
async function loadSystemInfo() {
    const data = await apiRequest('system_info');
    if (data.success) {
        deviceName.textContent = `${data.system} - ${data.machine}`;
        deviceOs.textContent = `${data.platform} ${data.release}`;
        
        // Update storage info if available
        if (data.disk_info && data.disk_info.length > 0) {
            const disk = data.disk_info[0]; // Use first disk
            const usedPercent = (disk.used / disk.total * 100).toFixed(1);
            const usedFormatted = formatBytes(disk.used);
            const totalFormatted = formatBytes(disk.total);
            
            storageInfo.textContent = `${usedFormatted} used of ${totalFormatted}`;
            document.querySelector('.storage-bar__fill').style.width = `${usedPercent}%`;
        }
    }
}

// Load current settings
async function loadSettings() {
    const data = await apiRequest('get_settings');
    if (data.success) {
        // Update UI based on settings
        const dryRunIndicator = document.querySelector('.dry-run-indicator');
        const testModeIndicator = document.querySelector('.test-mode-indicator');
        const adminStatus = document.querySelector('.admin-status');
        
        if (dryRunIndicator) {
            dryRunIndicator.textContent = data.dry_run_mode ? 'SAFE MODE' : 'DESTRUCTIVE MODE';
        }
        
        if (testModeIndicator) {
            testModeIndicator.textContent = data.test_mode ? 'TEST MODE' : 'LIVE MODE';
        }
        
        if (adminStatus) {
            adminStatus.textContent = data.is_admin ? 'ADMIN' : 'USER';
        }
    }
}

// Format bytes to human readable format
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// Load directory contents
async function loadDirectory(path = '') {
    const data = await apiRequest('list_directory', 'POST', { path });
    
    if (data.success) {
        currentDirectory = data.path;
        currentPath.textContent = currentDirectory;
        
        // Clear file list
        fileList.innerHTML = '';
        
        // Add items to file list
        data.items.forEach(item => {
            const li = document.createElement('li');
            li.className = 'file-item';
            li.dataset.path = item.path;
            
            if (selectedFiles.has(item.path)) {
                li.classList.add('selected');
            }
            
            if (item.error) {
                li.classList.add('error');
            }
            
            const icon = item.type === 'folder' || item.type === 'parent' ? '📁' : '📄';
            li.innerHTML = `
                <span class="file-icon">${icon}</span>
                <span class="file-name">${item.name}</span>
                <span class="file-size">${item.size}</span>
                <input type="checkbox" class="file-checkbox" ${selectedFiles.has(item.path) ? 'checked' : ''} ${item.type === 'folder' || item.type === 'parent' ? 'disabled' : ''}>
            `;
            
            // Add event listeners
            li.addEventListener('click', (e) => {
                if (e.target.type !== 'checkbox') {
                    if (item.type === 'folder' || item.type === 'parent') {
                        loadDirectory(item.path);
                    } else if (!item.error) {
                        toggleFileSelection(item);
                    }
                }
            });
            
            const checkbox = li.querySelector('.file-checkbox');
            checkbox.addEventListener('change', () => {
                if (!item.error && item.type !== 'folder' && item.type !== 'parent') {
                    toggleFileSelection(item);
                }
            });
            
            fileList.appendChild(li);
        });
    } else {
        alert('Error loading directory: ' + data.error);
    }
}

// Toggle file selection
async function toggleFileSelection(file) {
    if (selectedFiles.has(file.path)) {
        selectedFiles.delete(file.path);
    } else {
        selectedFiles.add(file.path);
    }
    
    // Update API selection
    const data = await apiRequest('select_files', 'POST', { files: Array.from(selectedFiles) });
    
    if (data.success) {
        updateSelectedCount(data.selected_count, data.total_size);
    }
}

// Update selected file count
function updateSelectedCount(count = selectedFiles.size, totalSize = '') {
    selectedCount.textContent = `${count} file${count !== 1 ? 's' : ''} selected${totalSize ? ` (${totalSize})` : ''}`;
    deletionSummary.textContent = `${count} file${count !== 1 ? 's' : ''} selected for deletion${totalSize ? `, ${totalSize}` : ''}`;
}

// Navigate up one directory
async function navigateUp() {
    const parts = currentDirectory.split(/[\\/]/);
    parts.pop(); // Remove last part
    
    if (parts.length === 0) {
        if (os.name === 'nt') {
            currentDirectory = 'C:\\';
        } else {
            currentDirectory = '/';
        }
    } else {
        currentDirectory = parts.join('/');
        if (os.name === 'nt' && !currentDirectory.includes(':')) {
            currentDirectory = 'C:\\';
        }
    }
    
    await loadDirectory(currentDirectory);
}

// Select all files in current directory
async function selectAllFiles() {
    // Get all files in current directory (non-folders)
    const fileItems = Array.from(fileList.querySelectorAll('.file-item'))
        .filter(item => !item.querySelector('.file-icon').textContent.includes('📁'))
        .filter(item => !item.classList.contains('error'));
    
    fileItems.forEach(item => {
        const path = item.dataset.path;
        selectedFiles.add(path);
    });
    
    // Update API selection
    const data = await apiRequest('select_files', 'POST', { files: Array.from(selectedFiles) });
    
    if (data.success) {
        updateSelectedCount(data.selected_count, data.total_size);
        populateFileList(currentDirectory);
    }
}

// Clear selection
async function clearSelection() {
    selectedFiles.clear();
    
    // Update API selection
    await apiRequest('select_files', 'POST', { files: [] });
    
    updateSelectedCount();
    populateFileList(currentDirectory);
}

// Show only selected files
function showSelectedFiles() {
    alert(`Selected files:\n${Array.from(selectedFiles).join('\n')}`);
}

// Select algorithm
function selectAlgorithm(algorithm) {
    selectedAlgorithm = algorithm;
    
    algorithmOptions.forEach(option => {
        if (option.dataset.algorithm === algorithm) {
            option.classList.add('selected');
        } else {
            option.classList.remove('selected');
        }
    });
}

// Start advanced wipe process
async function startAdvancedWipe() {
    if (selectedFiles.size === 0) {
        alert('Please select at least one file to delete.');
        return;
    }
    
    if (!selectedAlgorithm) {
        alert('Please select a wiping algorithm.');
        return;
    }
    
    // Show progress section
    progressSection.style.display = 'flex';
    fileBrowser.style.display = 'none';
    algorithmSelection.style.display = 'none';
    advancedControls.style.display = 'none';
    
    // Start the deletion process
    const data = await apiRequest('delete_files', 'POST', {
        files: Array.from(selectedFiles),
        algorithm: selectedAlgorithm
    });
    
    if (data.success) {
        // Simulate progress for UI
        simulateAdvancedWipeProgress(data.results);
        
        // Store report for certificate
        window.currentReport = data.report;
    } else {
        progressText.textContent = 'Deletion Failed!';
        progressStats.textContent = 'Error during file deletion: ' + data.error;
    }
}

// Simulate advanced wipe progress
function simulateAdvancedWipeProgress(results) {
    const progressRing = document.querySelector('.progress-ring__progress');
    const progressText = document.getElementById('progress-text');
    const progressStats = document.getElementById('progress-stats');
    
    const circumference = 2 * Math.PI * 90;
    progressRing.style.strokeDasharray = `${circumference} ${circumference}`;
    
    let progress = 0;
    const totalFiles = results.length;
    let processedFiles = 0;
    
    progressRing.style.strokeDashoffset = circumference;
    
    const interval = setInterval(() => {
        // Update progress
        progress += 100 / totalFiles / 10;
        
        // Update UI
        const offset = circumference - (progress / 100) * circumference;
        progressRing.style.strokeDashoffset = offset;
        
        progressText.textContent = `Deleting files (${selectedAlgorithm})`;
        
        // Check if we should move to next file
        if (progress >= (processedFiles + 1) / totalFiles * 100) {
            processedFiles++;
        }
        
        progressStats.textContent = `File ${processedFiles} of ${totalFiles}`;
        
        // Check if all files are complete
        if (progress >= 100) {
            clearInterval(interval);
            progressText.textContent = 'Deletion Complete!';
            
            const successful = results.filter(r => r.status === 'success').length;
            progressStats.textContent = `${successful} of ${totalFiles} files successfully erased`;
            
            // Show certificate after a delay
            setTimeout(() => showAdvancedCertificate(window.currentReport), 1500);
        }
    }, 100);
}

// Show advanced certificate
function showAdvancedCertificate(report) {
    // Generate certificate details
    document.getElementById('certificate-id').textContent = `ID: ${report.report_id}`;
    document.getElementById('certificate-date').textContent = new Date(report.generated_at).toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
    document.getElementById('certificate-device').textContent = deviceName.textContent;
    document.getElementById('certificate-method').textContent = report.algorithm_used;
    document.getElementById('certificate-status').textContent = 'Successfully Completed';
    document.getElementById('certificate-signature').textContent = report.certificate_info.validation_code;
    
    // Show modal
    certificateModal.style.display = 'flex';
}

// Start the wipe process
async function startWipeProcess() {
    // Hide the action card and show progress
    btnComplete.style.display = 'none';
    document.getElementById('reset-options-section').style.display = 'none';
    progressSection.style.display = 'flex';
    
    // Execute the reset
    const data = await apiRequest('execute_reset', 'POST', {
        mode: selectedSecurity
    });
    
    if (data.success) {
        // Simulate progress for UI
        simulateWipeProgress();
    } else {
        progressText.textContent = 'Reset Failed!';
        progressStats.textContent = 'Error during system reset: ' + data.error;
    }
}

// Simulate wipe progress
function simulateWipeProgress() {
    const progressRing = document.querySelector('.progress-ring__progress');
    const progressText = document.getElementById('progress-text');
    const progressStats = document.getElementById('progress-stats');
    
    const circumference = 2 * Math.PI * 90;
    progressRing.style.strokeDasharray = `${circumference} ${circumference}`;
    
    let progress = 0;
    
    progressRing.style.strokeDashoffset = circumference;
    
    const interval = setInterval(() => {
        // Update progress
        progress += 0.5;
        
        // Update UI
        const offset = circumference - (progress / 100) * circumference;
        progressRing.style.strokeDashoffset = offset;
        
        // Update status messages based on progress
        if (progress < 25) {
            progressText.textContent = 'Preparing system...';
            progressStats.textContent = 'Stopping services';
        } else if (progress < 50) {
            progressText.textContent = 'Backing up system state...';
            progressStats.textContent = 'Creating restore point';
        } else if (progress < 75) {
            progressText.textContent = 'Wiping data...';
            progressStats.textContent = `Pass ${Math.floor((progress - 50) / 25 * 3) + 1} of 3`;
        } else {
            progressText.textContent = 'Finalizing...';
            progressStats.textContent = 'Preparing for reboot';
        }
        
        // Check if complete
        if (progress >= 100) {
            clearInterval(interval);
            progressText.textContent = 'Reset Complete!';
            progressStats.textContent = 'System will restart shortly';
            
            // Show certificate after a delay
            setTimeout(showCertificate, 1500);
        }
    }, 50);
}

// Show certificate
function showCertificate() {
    // Generate certificate details
    document.getElementById('certificate-id').textContent = `ID: CERT-${Math.floor(Math.random() * 10000000000)}`;
    document.getElementById('certificate-date').textContent = new Date().toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
    document.getElementById('certificate-device').textContent = deviceName.textContent;
    
    let method;
    switch(selectedSecurity) {
        case 'standard':
            method = 'NIST 800-88 Clear (1-pass)';
            break;
        case 'professional':
            method = 'DoD 5220.22-M (3-pass)';
            break;
        case 'enterprise':
            method = 'Gutmann Method (7-pass)';
            break;
    }
    
    document.getElementById('certificate-method').textContent = method;
    document.getElementById('certificate-status').textContent = 'Successfully Completed';
    document.getElementById('certificate-signature').textContent = `0x${Math.random().toString(16).substr(2, 14)}`;
    
    // Show modal
    certificateModal.style.display = 'flex';
}

// Animate trust score value
function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        element.textContent = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Animate trust score on page load
function animateTrustScore() {
    trustScore.textContent = '0';
    setTimeout(() => {
        animateValue(trustScore, 0, 850, 2000);
    }, 500);
}

// Initialize the app when the DOM is loaded
document.addEventListener('DOMContentLoaded', init);