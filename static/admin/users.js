document.addEventListener('DOMContentLoaded', function() {
    // Modal functionality
    const modal = document.getElementById('userModal');
    const newUserBtn = document.getElementById('newUserBtn');
    const closeBtn = document.querySelector('.close-btn');
    const cancelBtn = document.getElementById('cancelBtn');
    const userForm = document.getElementById('userForm');
    
    // Open modal
    if (newUserBtn) {
        newUserBtn.addEventListener('click', function() {
            // Reset form and set title for new user
            if (userForm) userForm.reset();
            const modalTitle = modal.querySelector('.modal-header h2');
            if (modalTitle) modalTitle.textContent = 'Add New User';
            
            modal.style.display = 'flex';
        });
    }
    
    // Close modal
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    // Form submission
    if (userForm) {
        userForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(userForm);
            const userData = {};
            
            for (const [key, value] of formData.entries()) {
                userData[key] = value;
            }
            
            // In a real application, you would send this data to the server
            console.log('User Data:', userData);
            
            // For demo purposes, show success message and close modal
            alert('User saved successfully!');
            modal.style.display = 'none';
            
            // Optionally, reset the form
            userForm.reset();
        });
    }
    
    // Action buttons functionality
    const viewButtons = document.querySelectorAll('.btn-icon[title="View Details"]');
    const editButtons = document.querySelectorAll('.btn-icon[title="Edit"]');
    const deleteButtons = document.querySelectorAll('.btn-icon[title="Delete"]');
    
    if (viewButtons.length > 0) {
        viewButtons.forEach(button => {
            button.addEventListener('click', function() {
                const row = this.closest('tr');
                const id = row.querySelector('td:first-child').textContent;
                const name = row.querySelector('td:nth-child(2)').textContent;
                
                alert(`Viewing details for user ${name} (${id})`);
                // In a real application, you would open a details modal or navigate to a details page
            });
        });
    }
    
    if (editButtons.length > 0) {
        editButtons.forEach(button => {
            button.addEventListener('click', function() {
                const row = this.closest('tr');
                const id = row.querySelector('td:first-child').textContent;
                const name = row.querySelector('td:nth-child(2)').textContent;
                
                // Set modal title for editing
                const modalTitle = modal.querySelector('.modal-header h2');
                if (modalTitle) modalTitle.textContent = `Edit User: ${name}`;
                
                // In a real application, you would populate the form with existing data
                alert(`Editing user ${name} (${id})`);
                
                // Open the modal
                modal.style.display = 'flex';
            });
        });
    }
    
    if (deleteButtons.length > 0) {
        deleteButtons.forEach(button => {
            button.addEventListener('click', function() {
                const row = this.closest('tr');
                const id = row.querySelector('td:first-child').textContent;
                const name = row.querySelector('td:nth-child(2)').textContent;
                
                if (confirm(`Are you sure you want to delete user ${name} (${id})?`)) {
                    // In a real application, you would send a delete request to the server
                    alert(`User ${name} (${id}) deleted successfully!`);
                    row.remove();
                }
            });
        });
    }
    
    // Filter functionality
    const filterButton = document.querySelector('.btn-filter');
    
    if (filterButton) {
        filterButton.addEventListener('click', function() {
            const roleFilter = document.getElementById('roleFilter').value;
            const statusFilter = document.getElementById('statusFilter').value;
            
            // In a real application, you would filter the data based on these values
            alert(`Filtering with: Role=${roleFilter}, Status=${statusFilter}`);
        });
    }
});