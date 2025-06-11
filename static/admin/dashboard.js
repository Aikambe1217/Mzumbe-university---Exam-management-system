document.addEventListener('DOMContentLoaded', function() {
    // Initialize notifications dropdown
    const notificationsIcon = document.querySelector('.notifications');
    if (notificationsIcon) {
        notificationsIcon.addEventListener('click', function() {
            // Toggle notifications panel (would be implemented in a real application)
            alert('Notifications panel would open here');
        });
    }
    
    // Initialize user dropdown
    const userInfo = document.querySelector('.user-info');
    if (userInfo) {
        userInfo.addEventListener('click', function(e) {
            const dropdown = this.querySelector('.dropdown-menu');
            if (dropdown && e.target !== dropdown && !dropdown.contains(e.target)) {
                dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
            }
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!userInfo.contains(e.target)) {
                const dropdown = userInfo.querySelector('.dropdown-menu');
                if (dropdown) {
                    dropdown.style.display = 'none';
                }
            }
        });
    }
    
    // Initialize remind buttons
    const remindButtons = document.querySelectorAll('.btn-action');
    if (remindButtons.length > 0) {
        remindButtons.forEach(button => {
            button.addEventListener('click', function() {
                const row = this.closest('tr');
                const lecturer = row.querySelector('td:nth-child(2)').textContent;
                const course = row.querySelector('td:nth-child(1)').textContent;
                
                alert(`Reminder sent to ${lecturer} for ${course}`);
            });
        });
    }
});