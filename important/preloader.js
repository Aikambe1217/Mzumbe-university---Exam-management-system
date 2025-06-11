// Updated preloader script that removes the session variable after showing
document.addEventListener('DOMContentLoaded', function() {
    // Get preloader elements
    const preloader = document.getElementById('mzumbePreloader');
    const progressBar = document.getElementById('preloaderProgressBar');
    const percentageText = document.getElementById('preloaderPercentage');
    
    // If elements don't exist, exit early
    if (!preloader || !progressBar || !percentageText) {
      console.error('Preloader elements not found');
      return;
    }
    
    // Make sure preloader is visible
    preloader.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    
    // Set fixed duration for preloader (5 seconds)
    const duration = 5000; // 5 seconds
    const startTime = Date.now();
    let progress = 0;
    
    // Function to update progress
    function updateProgress() {
      // Calculate elapsed time
      const elapsed = Date.now() - startTime;
      
      // Calculate progress percentage (0-100)
      progress = Math.min((elapsed / duration) * 100, 100);
      
      // Update progress bar width
      progressBar.style.width = progress + '%';
      
      // Update percentage text
      percentageText.textContent = Math.floor(progress) + '%';
      
      // If not complete, continue updating
      if (progress < 100) {
        requestAnimationFrame(updateProgress);
      } else {
        // When complete, hide preloader after a short delay
        setTimeout(hidePreloader, 300);
      }
    }
    
    // Function to hide preloader
    function hidePreloader() {
      preloader.style.opacity = '0';
      
      // After transition completes, remove from DOM
      setTimeout(function() {
        preloader.style.display = 'none';
        document.body.style.overflow = 'auto';
        
        // Remove the session variable by making an AJAX request
        fetch('/clear-preloader-session/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCsrfToken(),
            'Content-Type': 'application/json'
          }
        });
      }, 500);
    }
    
    // Helper function to get CSRF token
    function getCsrfToken() {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
          return value;
        }
      }
      return '';
    }
    
    // Start updating progress
    requestAnimationFrame(updateProgress);
  });