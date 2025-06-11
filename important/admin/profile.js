document.addEventListener('DOMContentLoaded', function() {
    // Tab switching functionality
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Add active class to clicked button
            button.classList.add('active');

            // Show corresponding content
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Personal Information Edit Functionality
    const editPersonalInfoBtn = document.getElementById('edit-personal-info');
    const savePersonalInfoBtn = document.getElementById('save-personal-info');
    const cancelPersonalInfoBtn = document.getElementById('cancel-personal-info');
    const personalInfoForm = document.getElementById('personal-info-form');
    const formActions = document.querySelector('.form-actions');
    const personalInfoInputs = personalInfoForm.querySelectorAll('input');
    let originalValues = {};

    editPersonalInfoBtn.addEventListener('click', () => {
        // Store original values
        personalInfoInputs.forEach(input => {
            originalValues[input.id] = input.value;
            input.disabled = false;
        });

        // Show save and cancel buttons
        formActions.style.display = 'flex';
        editPersonalInfoBtn.style.display = 'none';
    });

    savePersonalInfoBtn.addEventListener('click', () => {
        // Here you would typically send the data to the server
        // For now, we'll just simulate a successful save
        
        // Show success message
        showNotification('Personal information updated successfully!', 'success');
        
        // Disable inputs and hide buttons
        personalInfoInputs.forEach(input => {
            input.disabled = true;
        });
        
        formActions.style.display = 'none';
        editPersonalInfoBtn.style.display = 'block';
    });

    cancelPersonalInfoBtn.addEventListener('click', () => {
        // Restore original values
        personalInfoInputs.forEach(input => {
            input.value = originalValues[input.id];
            input.disabled = true;
        });
        
        // Hide save and cancel buttons
        formActions.style.display = 'none';
        editPersonalInfoBtn.style.display = 'block';
    });

    // Password Change Functionality
    const changePasswordBtn = document.getElementById('change-password');
    const currentPasswordInput = document.getElementById('current-password');
    const newPasswordInput = document.getElementById('new-password');
    const confirmPasswordInput = document.getElementById('confirm-password');

    changePasswordBtn.addEventListener('click', () => {
        // Basic validation
        if (!currentPasswordInput.value) {
            showNotification('Please enter your current password.', 'error');
            return;
        }

        if (!newPasswordInput.value) {
            showNotification('Please enter a new password.', 'error');
            return;
        }

        if (newPasswordInput.value !== confirmPasswordInput.value) {
            showNotification('New passwords do not match.', 'error');
            return;
        }

        // Here you would typically send the data to the server
        // For now, we'll just simulate a successful password change
        
        // Show success message
        showNotification('Password changed successfully!', 'success');
        
        // Clear form
        currentPasswordInput.value = '';
        newPasswordInput.value = '';
        confirmPasswordInput.value = '';
    });

    // Notification Preferences Functionality
    const saveNotificationsBtn = document.getElementById('save-notifications');
    
    saveNotificationsBtn.addEventListener('click', () => {
        // Here you would typically send the data to the server
        // For now, we'll just simulate a successful save
        
        // Show success message
        showNotification('Notification preferences saved!', 'success');
    });

    // Activity Log Filtering
    const filterButtons = document.querySelectorAll('.filter-content a');
    const activityItems = document.querySelectorAll('.activity-item');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            
            const filter = button.getAttribute('data-filter');
            
            activityItems.forEach(item => {
                if (filter === 'all') {
                    item.style.display = 'flex';
                } else {
                    if (item.querySelector(`.activity-icon.${filter}`)) {
                        item.style.display = 'flex';
                    } else {
                        item.style.display = 'none';
                    }
                }
            });
        });
    });

    // Profile Picture Upload
    const avatarUpload = document.getElementById('avatar-upload');
    const profileAvatar = document.querySelector('.profile-avatar img');
    
    avatarUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        
        if (file) {
            const reader = new FileReader();
            
            reader.onload = function(event) {
                profileAvatar.src = event.target.result;
                showNotification('Profile picture updated!', 'success');
            };
            
            reader.readAsDataURL(file);
        }
    });

    // Notification function
    function showNotification(message, type) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="notification-icon">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            </div>
            <div class="notification-message">${message}</div>
            <button class="notification-close"><i class="fas fa-times"></i></button>
        `;
        
        // Add to DOM
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        // Add close button functionality
        const closeButton = notification.querySelector('.notification-close');
        closeButton.addEventListener('click', () => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        });
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 5000);
    }

    // Dropdown functionality
    const userDropdown = document.querySelector('.user-profile .dropdown');
    
    userDropdown.addEventListener('click', (e) => {
        const dropdownContent = userDropdown.querySelector('.dropdown-content');
        dropdownContent.classList.toggle('show');
        e.stopPropagation();
    });
    
    document.addEventListener('click', () => {
        const dropdownContent = document.querySelector('.dropdown-content');
        if (dropdownContent.classList.contains('show')) {
            dropdownContent.classList.remove('show');
        }
    });

    // Filter dropdown functionality
    const filterDropdown = document.querySelector('.filter-dropdown');
    
    if (filterDropdown) {
        const filterBtn = filterDropdown.querySelector('.filter-btn');
        const filterContent = filterDropdown.querySelector('.filter-content');
        
        filterBtn.addEventListener('click', (e) => {
            filterContent.classList.toggle('show');
            e.stopPropagation();
        });
        
        document.addEventListener('click', () => {
            if (filterContent.classList.contains('show')) {
                filterContent.classList.remove('show');
            }
        });
    }

    // Pagination functionality
    const paginationButtons = document.querySelectorAll('.pagination-btn');
    
    paginationButtons.forEach(button => {
        button.addEventListener('click', () => {
            paginationButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Here you would typically load the corresponding page of activities
            // For now, we'll just simulate a page change
            if (!button.classList.contains('next')) {
                showNotification(`Navigated to page ${button.textContent}`, 'success');
            } else {
                showNotification('Navigated to next page', 'success');
            }
        });
    });
});