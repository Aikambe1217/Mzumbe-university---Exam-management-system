document.addEventListener('DOMContentLoaded', function() {
    // Report generation functionality
    const generateReportBtn = document.getElementById('generateReportBtn');
    const printReportBtn = document.getElementById('printReportBtn');
    const exportReportBtn = document.getElementById('exportReportBtn');
    
    if (generateReportBtn) {
        generateReportBtn.addEventListener('click', function() {
            const reportType = document.getElementById('reportType').value;
            const startDate = document.getElementById('startDate').value;
            const endDate = document.getElementById('endDate').value;
            
            // In a real application, you would fetch the report data from the server
            alert(`Generating ${reportType} report for date range: ${startDate} to ${endDate}`);
            
            // Update report date
            const reportDateElement = document.getElementById('reportDate');
            if (reportDateElement) {
                const today = new Date();
                const options = { year: 'numeric', month: 'long', day: 'numeric' };
                reportDateElement.textContent = today.toLocaleDateString('en-US', options);
            }
            
            // Update report title
            const reportTitleElement = document.querySelector('.report-title h2');
            if (reportTitleElement) {
                let title = '';
                switch (reportType) {
                    case 'submissions':
                        title = 'Submissions Report';
                        break;
                    case 'collections':
                        title = 'Collections Report';
                        break;
                    case 'marked':
                        title = 'Marked Materials Report';
                        break;
                    case 'pending':
                        title = 'Pending Returns Report';
                        break;
                    case 'overdue':
                        title = 'Overdue Returns Report';
                        break;
                    case 'summary':
                        title = 'Summary Report';
                        break;
                    default:
                        title = 'Examination Materials Report';
                }
                reportTitleElement.textContent = title;
            }
        });
    }
    
    if (printReportBtn) {
        printReportBtn.addEventListener('click', function() {
            // In a real application, you would format the report for printing
            window.print();
        });
    }
    
    if (exportReportBtn) {
        exportReportBtn.addEventListener('click', function() {
            const reportType = document.getElementById('reportType').value;
            
            // In a real application, you would generate and download the report file
            alert(`Exporting ${reportType} report as PDF`);
        });
    }
});