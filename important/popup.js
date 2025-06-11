
                    // Get elements
                    const viewAllButton = document.getElementById('viewAllButton');
                    const activityPopup = document.getElementById('activityPopup');
                    const closePopup = document.getElementById('closePopup');
                    
                    
                    // Show popup when "View All" is clicked
                    viewAllButton.addEventListener('click', function(e) {
                        e.preventDefault();
                        activityPopup.style.display = 'flex';
                        document.body.style.overflow = 'hidden'; // Prevent scrolling when popup is open
                    });
                    
                    // Close popup when X is clicked
                    closePopup.addEventListener('click', function() {
                        activityPopup.style.display = 'none';
                        document.body.style.overflow = ''; // Restore scrolling
                    });
                    
                    // Close popup when clicking outside the content
                    activityPopup.addEventListener('click', function(e) {
                        if (e.target === activityPopup) {
                            activityPopup.style.display = 'none';
                            document.body.style.overflow = ''; // Restore scrolling
                        }
                    });
                    
                    // Close popup when ESC key is pressed
                    document.addEventListener('keydown', function(e) {
                        if (e.key === 'Escape' && activityPopup.style.display === 'flex') {
                            activityPopup.style.display = 'none';
                            document.body.style.overflow = ''; // Restore scrolling
                        }
                    });

                //   notification
                document.addEventListener("DOMContentLoaded", function () {
                    const viewNotification = document.getElementById('viewNotification');
                    const notificationPopup = document.getElementById('notificationPopup');
                    const closenotification = document.getElementById('closenotification');
                
                    if (viewNotification && notificationPopup && closenotification) {
                        viewNotification.addEventListener('click', function (e) {
                            e.preventDefault();
                            notificationPopup.style.display = 'flex';
                            document.body.style.overflow = 'hidden';
                        });
                
                        closenotification.addEventListener('click', function () {
                            notificationPopup.style.display = 'none';
                            document.body.style.overflow = '';
                        });
                
                        notificationPopup.addEventListener('click', function (e) {
                            if (e.target === notificationPopup) {
                                notificationPopup.style.display = 'none';
                                document.body.style.overflow = '';
                            }
                        });
                
                        document.addEventListener('keydown', function (e) {
                            if (e.key === 'Escape' && notificationPopup.style.display === 'flex') {
                                notificationPopup.style.display = 'none';
                                document.body.style.overflow = '';
                            }
                        });
                    }
                });
                