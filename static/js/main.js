// Main JavaScript file for Term Sheet Validation application

document.addEventListener('DOMContentLoaded', function() {
    // File upload handling
    initializeFileUpload();
    
    // Form submission handling
    setupFormSubmission();
    
    // Validation rule form handling
    setupValidationRuleForm();
    
    // Dashboard interactions
    setupDashboardInteractions();
});

/**
 * Initialize file upload functionality with drag and drop
 */
function initializeFileUpload() {
    const dropZone = document.querySelector('.drop-zone');
    const fileInput = document.getElementById('document-file');
    
    if (!dropZone || !fileInput) return;
    
    // Handle file selection
    fileInput.addEventListener('change', function() {
        if (fileInput.files.length > 0) {
            const fileName = fileInput.files[0].name;
            document.querySelector('.file-name').textContent = fileName;
            document.querySelector('.selected-file').classList.remove('d-none');
            document.querySelector('.drop-zone-prompt').classList.add('d-none');
        }
    });
    
    // Handle drag and drop
    ['dragover', 'dragenter'].forEach(eventName => {
        dropZone.addEventListener(eventName, function(e) {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });
    });
    
    ['dragleave', 'dragend', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, function(e) {
            e.preventDefault();
            dropZone.classList.remove('dragover');
        });
    });
    
    // Handle file drop
    dropZone.addEventListener('drop', function(e) {
        e.preventDefault();
        
        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            const fileName = fileInput.files[0].name;
            document.querySelector('.file-name').textContent = fileName;
            document.querySelector('.selected-file').classList.remove('d-none');
            document.querySelector('.drop-zone-prompt').classList.add('d-none');
        }
    });
    
    // Handle click to select file
    dropZone.addEventListener('click', function() {
        fileInput.click();
    });
}

/**
 * Setup form submission with loading spinner
 */
function setupFormSubmission() {
    const uploadForm = document.getElementById('upload-form');
    const spinner = document.querySelector('.spinner-overlay');
    
    if (!uploadForm || !spinner) return;
    
    uploadForm.addEventListener('submit', function() {
        // Validate form
        const fileInput = document.getElementById('document-file');
        if (!fileInput || !fileInput.files.length) {
            alert('Please select a file to upload');
            return false;
        }
        
        // Show loading spinner
        spinner.style.visibility = 'visible';
        
        // Form is valid, allow submission
        return true;
    });
}

/**
 * Setup validation rule form
 */
function setupValidationRuleForm() {
    const ruleTypeSelect = document.getElementById('rule-type');
    const ruleValueField = document.getElementById('rule-value');
    const ruleValueLabel = document.querySelector('label[for="rule-value"]');
    
    if (!ruleTypeSelect || !ruleValueField || !ruleValueLabel) return;
    
    ruleTypeSelect.addEventListener('change', function() {
        const selectedRule = ruleTypeSelect.value;
        
        // Change the label and placeholder based on rule type
        switch (selectedRule) {
            case 'required':
                ruleValueLabel.textContent = 'Value (true/false):';
                ruleValueField.placeholder = 'true';
                break;
            case 'date_format':
                ruleValueLabel.textContent = 'Date Format:';
                ruleValueField.placeholder = '%Y-%m-%d';
                break;
            case 'range':
                ruleValueLabel.textContent = 'Range (min,max):';
                ruleValueField.placeholder = '0,100';
                break;
            case 'regex':
                ruleValueLabel.textContent = 'Regular Expression:';
                ruleValueField.placeholder = '^[A-Za-z0-9]+$';
                break;
            case 'date_after':
                ruleValueLabel.textContent = 'Reference Field:';
                ruleValueField.placeholder = 'effective_date';
                break;
            default:
                ruleValueLabel.textContent = 'Rule Value:';
                ruleValueField.placeholder = '';
        }
    });
}

/**
 * Setup dashboard interactions
 */
function setupDashboardInteractions() {
    const documentCards = document.querySelectorAll('.dashboard-card');
    
    if (!documentCards.length) return;
    
    // Add click event to document cards
    documentCards.forEach(card => {
        card.addEventListener('click', function() {
            const documentId = this.dataset.documentId;
            if (documentId) {
                window.location.href = `/document/${documentId}`;
            }
        });
    });
}

/**
 * Toggle visibility of extracted data sections
 */
function toggleDataSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.classList.toggle('d-none');
    }
}

/**
 * Handle file removal from upload form
 */
function removeSelectedFile() {
    const fileInput = document.getElementById('document-file');
    fileInput.value = '';
    document.querySelector('.file-name').textContent = '';
    document.querySelector('.selected-file').classList.add('d-none');
    document.querySelector('.drop-zone-prompt').classList.remove('d-none');
}
