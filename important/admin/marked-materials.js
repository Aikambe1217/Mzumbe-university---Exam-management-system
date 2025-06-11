document.addEventListener('DOMContentLoaded', function() {
    // Modal functionality
    const modal = document.getElementById('markedMaterialModal');
    const newMarkedMaterialBtn = document.getElementById('newMarkedMaterialBtn');
    const closeBtn = document.querySelector('.close-btn');
    const cancelBtn = document.getElementById('cancelBtn');
    const markedMaterialForm = document.getElementById('markedMaterialForm');
    
    // Open modal
    if (newMarkedMaterialBtn) {
        newMarkedMaterialBtn.addEventListener('click', function() {
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
    if (markedMaterialForm) {
        markedMaterialForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(markedMaterialForm);
            const markedMaterialData = {};
            
            for (const [key, value] of formData.entries()) {
                markedMaterialData[key] = value;
            }
            
            // In a real application, you would send this data to the server
            console.log('Marked Material Data:', markedMaterialData);
            
            // For demo purposes, show success message and close modal
            alert('Marked material recorded successfully!');
            modal.style.display = 'none';
            
            // Optionally, reset the form
            markedMaterialForm.reset();
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
                
                alert(`Viewing details for marked material ${id}`);
                // In a real application, you would open a details modal or navigate to a details page
            });
        });
    }
    
    if (editButtons.length > 0) {
        editButtons.forEach(button => {
            button.addEventListener('click', function() {
                const row = this.closest('tr');
                const id = row.querySelector('td:first-child').textContent;
                
                alert(`Editing marked material ${id}`);
                // In a real application, you would populate the form with existing data and open the modal
            });
        });
    }
    
    if (deleteButtons.length > 0) {
        deleteButtons.forEach(button => {
            button.addEventListener('click', function() {
                const row = this.closest('tr');
                const id = row.querySelector('td:first-child').textContent;
                
                if (confirm(`Are you sure you want to delete marked material ${id}?`)) {
                    // In a real application, you would send a delete request to the server
                    alert(`Marked material ${id} deleted successfully!`);
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