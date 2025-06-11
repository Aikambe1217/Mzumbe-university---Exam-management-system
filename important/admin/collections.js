document.addEventListener('DOMContentLoaded', function() {
    // Modal functionality
    const modal = document.getElementById('collectionModal');
    const newCollectionBtn = document.getElementById('newCollectionBtn');
    const closeBtn = document.querySelector('.close-btn');
    const cancelBtn = document.getElementById('cancelBtn');
    const collectionForm = document.getElementById('collectionForm');
    
    // Open modal
    if (newCollectionBtn) {
        newCollectionBtn.addEventListener('click', function() {
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
    if (collectionForm) {
        collectionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(collectionForm);
            const collectionData = {};
            
            for (const [key, value] of formData.entries()) {
                collectionData[key] = value;
            }
            
            // In a real application, you would send this data to the server
            console.log('Collection Data:', collectionData);
            
            // For demo purposes, show success message and close modal
            alert('Collection recorded successfully!');
            modal.style.display = 'none';
            
            // Optionally, reset the form
            collectionForm.reset();
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
                
                alert(`Viewing details for collection ${id}`);
                // In a real application, you would open a details modal or navigate to a details page
            });
        });
    }
    
    if (editButtons.length > 0) {
        editButtons.forEach(button => {
            button.addEventListener('click', function() {
                const row = this.closest('tr');
                const id = row.querySelector('td:first-child').textContent;
                
                alert(`Editing collection ${id}`);
                // In a real application, you would populate the form with existing data and open the modal
            });
        });
    }
    
    if (deleteButtons.length > 0) {
        deleteButtons.forEach(button => {
            button.addEventListener('click', function() {
                const row = this.closest('tr');
                const id = row.querySelector('td:first-child').textContent;
                
                if (confirm(`Are you sure you want to delete collection ${id}?`)) {
                    // In a real application, you would send a delete request to the server
                    alert(`Collection ${id} deleted successfully!`);
                    row.remove();
                }
            });
        });
    }
    
    // Filter functionality
    const filterButton = document.querySelector('.btn-filter');
    
    if (filterButton) {
        filterButton.addEventListener('click', function() {
            const courseFilter = document.getElementById('courseFilter').value;
            const lecturerFilter = document.getElementById('lecturerFilter').value;
            const startDate = document.getElementById('startDate').value;
            const endDate = document.getElementById('endDate').value;
            const statusFilter = document.getElementById('statusFilter').value;
            
            // In a real application, you would filter the data based on these values
            alert(`Filtering with: Course=${courseFilter}, Lecturer=${lecturerFilter}, Date Range=${startDate} to ${endDate}, Status=${statusFilter}`);
        });
    }
});