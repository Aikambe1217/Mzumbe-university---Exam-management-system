document.addEventListener('DOMContentLoaded', function() {
    // Settings tabs functionality
    const tabLinks = document.querySelectorAll('.settings-nav li');
    const tabContents = document.querySelectorAll('.settings-tab');
    
    if (tabLinks.length > 0) {
        tabLinks.forEach(link => {
            link.addEventListener('click', function() {
                // Remove active class from all tabs
                tabLinks.forEach(tab => tab.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Add active class to clicked tab
                this.classList.add('active');
                
                // Show corresponding content
                const tabId = this.getAttribute('data-tab');
                const tabContent = document.getElementById(tabId);
                if (tabContent) {
                    tabContent.classList.add('active');
                }
            });
        });
    }
    
    // Form submissions
    const generalSettingsForm = document.getElementById('generalSettingsForm');
    const notificationSettingsForm = document.getElementById('notificationSettingsForm');
    const securitySettingsForm = document.getElementById('securitySettingsForm');
    
    if (generalSettingsForm) {
        generalSettingsForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(generalSettingsForm);
            const generalSettings = {};
            
            for (const [key, value] of formData.entries()) {
                generalSettings[key] = value;
            }
            
            // In a real application, you would send this data to the server
            console.log('General Settings:', generalSettings);
            
            // For demo purposes, show success message
            alert('General settings saved successfully!');
        });
    }
    
    if (notificationSettingsForm) {
        notificationSettingsForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(notificationSettingsForm);
            const notificationSettings = {};
            
            for (const [key, value] of formData.entries()) {
                notificationSettings[key] = value;
            }
            
            // Handle checkboxes that are not checked (they don't get included in FormData)
            const checkboxes = notificationSettingsForm.querySelectorAll('input[type="checkbox"]');
            checkboxes.forEach(checkbox => {
                if (!formData.has(checkbox.name)) {
                    notificationSettings[checkbox.name] = 'off';
                }
            });
            
            // In a real application, you would send this data to the server
            console.log('Notification Settings:', notificationSettings);
            
            // For demo purposes, show success message
            alert('Notification settings saved successfully!');
        });
    }
    
    if (securitySettingsForm) {
        securitySettingsForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(securitySettingsForm);
            const securitySettings = {};
            
            for (const [key, value] of formData.entries()) {
                securitySettings[key] = value;
            }
            
            // In a real application, you would send this data to the server
            console.log('Security Settings:', securitySettings);
            
            // For demo purposes, show success message
            alert('Security settings saved successfully!');
        });
    }
    
    // Backup and restore functionality
    const backupNowBtn = document.getElementById('backupNowBtn');
    const restoreBtn = document.getElementById('restoreBtn');
    
    if (backupNowBtn) {
        backupNowBtn.addEventListener('click', function() {
            // In a real application, you would trigger a backup process
            alert('Backup process started. This may take a few minutes.');
            
            // Simulate backup completion after 2 seconds
            setTimeout(function() {
                alert('Backup completed successfully!');
            }, 2000);
        });
    }
    
    if (restoreBtn) {
        restoreBtn.addEventListener('click', function() {
            const backupFile = document.getElementById('backupFile').value;
            
            if (!backupFile) {
                alert('Please select a backup file to restore.');
                return;
            }
            
            if (confirm('Are you sure you want to restore from the selected backup? This will replace all current data.')) {
                // In a real application, you would trigger a restore process
                alert('Restore process started. This may take a few minutes.');
                
                // Simulate restore completion after 3 seconds
                setTimeout(function() {
                    alert('Restore completed successfully!');
                }, 3000);
            }
        });
    }
    
    // System maintenance functionality
    const clearCacheBtn = document.getElementById('clearCacheBtn');
    const optimizeDbBtn = document.getElementById('optimizeDbBtn');
    
    if (clearCacheBtn) {
        clearCacheBtn.addEventListener('click', function() {
            // In a real application, you would trigger a cache clearing process
            alert('Clearing system cache. This may take a moment.');
            
            // Simulate completion after 1 second
            setTimeout(function() {
                alert('Cache cleared successfully!');
            }, 1000);
        });
    }
    
    if (optimizeDbBtn) {
        optimizeDbBtn.addEventListener('click', function() {
            // In a real application, you would trigger a database optimization process
            alert('Optimizing database. This may take a few minutes.');
            
            // Simulate completion after 2 seconds
            setTimeout(function() {
                alert('Database optimized successfully!');
            }, 2000);
        });
    }
});