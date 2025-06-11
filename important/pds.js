   
        document.addEventListener('DOMContentLoaded', function() {
            // Print button functionality
            const printBtn = document.querySelector('.print-btn');
            if (printBtn) {
                printBtn.addEventListener('click', function() {
                    window.print();
                });
            }

            // Download button functionality
            const downloadBtn = document.querySelector('.download-btn');
            if (downloadBtn) {
                downloadBtn.addEventListener('click', function() {
                    // Create a clone of the report content for download
                    const reportContent = document.querySelector('.report-card').cloneNode(true);
                    
                    // Create a new document with necessary styling
                    const html = `
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8">
                        <title>General Report</title>
                        <style>
                            ${Array.from(document.styleSheets)
                                .map(sheet => {
                                    try {
                                        return Array.from(sheet.cssRules)
                                            .map(rule => rule.cssText)
                                            .join('\n');
                                    } catch (e) {
                                        console.log('Cannot access stylesheet rules');
                                        return '';
                                    }
                                })
                                .join('\n')}
                        </style>
                        <script src="https://cdn.jsdelivr.net/npm/chart.js"><\/script>
                    </head>
                    <body>
                        ${reportContent.outerHTML}
                        <script>
                            ${document.querySelector('.report-charts script').textContent}
                        <\/script>
                    </body>
                    </html>`;

                    // Create a blob and download link
                    const blob = new Blob([html], { type: 'text/html' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'general_report.html';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                });
            }

            // Share button functionality
            const shareBtn = document.querySelector('.share-btn');
            if (shareBtn) {
                shareBtn.addEventListener('click', function() {
                    // Check if Web Share API is supported
                    if (navigator.share) {
                        navigator.share({
                            title: document.getElementById('reportTitle').textContent,
                            text: 'Check out this report',
                            url: window.location.href,
                        })
                        .catch(error => {
                            console.log('Error sharing:', error);
                            fallbackShare();
                        });
                    } else {
                        fallbackShare();
                    }
                });
            }

            // Fallback share function (copy URL to clipboard)
            function fallbackShare() {
                // Create a temporary input element
                const input = document.createElement('input');
                input.value = window.location.href;
                document.body.appendChild(input);
                input.select();
                document.execCommand('copy');
                document.body.removeChild(input);
                
                // Show a notification
                alert('Report URL copied to clipboard!');
            }
        });
    