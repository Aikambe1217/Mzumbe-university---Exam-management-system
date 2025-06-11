document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            // Simple validation
            if (!username || !password) {
                alert('Please enter both username and password');
                return;
            }
            
            // In a real application, you would send this data to the server for authentication
            // For this demo, we'll just redirect to the dashboard
            window.location.href = 'dashboard.html';
        });
    }
});