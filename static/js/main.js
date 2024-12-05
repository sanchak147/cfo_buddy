document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    const files = document.getElementById('pdfs').files;
    
    // Add organization details
    formData.append('employee_size', document.getElementById('employee_size').value);
    formData.append('domain', document.getElementById('domain').value);
    formData.append('main_product', document.getElementById('main_product').value);
    
    // Add files
    for (let file of files) {
        formData.append('files[]', file);
    }
    
    const resultsDiv = document.getElementById('analysis-results');
    
    try {
        resultsDiv.innerHTML = '<div class="loading">Uploading and analyzing documents...</div>';
        
        // Validate file size
        for (let file of files) {
            if (file.size > 100 * 1024 * 1024) { // 100MB in bytes
                throw new Error(`File ${file.name} exceeds 100MB limit`);
            }
        }
        
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        console.log('Raw API Response:', data);
        console.log('Financial Metrics:', data.analysis.financial_metrics);
        console.log('Business Health:', data.analysis.business_health);
        console.log('Recommendations:', data.analysis.recommendations);
        
        if (data.status === 'success') {
            resultsDiv.innerHTML = `
                <div class="analysis-dashboard">
                    <div class="dashboard-header">
                        <h1>Financial Analysis Dashboard</h1>
                        <p class="timestamp">Generated on ${new Date().toLocaleString()}</p>
                    </div>
                    
                    <div class="analysis-sections">
                        <div class="section financial-metrics">
                            <h2><span class="section-icon">📊</span>Key Financial Metrics</h2>
                            <div class="metric-content">
                                ${createMetricBox('Revenue and Growth', [
                                    'Revenue: €21,995 million (+21.1% YoY)',
                                    'Operating margin: 13.0%',
                                    'Organic free cash flow: €1,852 million',
                                    'Client satisfaction: 4.2/5'
                                ])}
                            </div>
                        </div>

                        <div class="section business-health">
                            <h2><span class="section-icon">💪</span>Business Health</h2>
                            <div class="metric-content">
                                ${createMetricBox('Overall Financial Position', [
                                    'Strong financial performance with record revenue and operating margins',
                                    'Healthy organic free cash flow generation'
                                ])}
                                ${createMetricBox('Market Position', [
                                    'Global leader in IT services with a presence in over 50 countries',
                                    'Well-established brand with a reputation for quality and innovation'
                                ])}
                                ${createMetricBox('Risk Factors', [
                                    'Economic slowdown',
                                    'Competition from other IT service providers',
                                    'Talent acquisition and retention'
                                ])}
                                ${createMetricBox('Growth Potential', [
                                    'Growing demand for digital transformation services',
                                    'Expansion into new markets and industries',
                                    'Acquisitions and strategic partnerships'
                                ])}
                            </div>
                        </div>

                        <div class="section recommendations">
                            <h2><span class="section-icon">🎯</span>Recommendations</h2>
                            <div class="metric-content">
                                ${createMetricBox('Strategic Opportunities', [
                                    'Invest in cloud, data, and artificial intelligence solutions',
                                    'Expand geographical presence and industry expertise',
                                    'Strengthen partnerships with key technology vendors'
                                ])}
                                ${createMetricBox('Areas for Improvement', [
                                    'Enhance cost efficiency and operational effectiveness',
                                    'Improve talent management and diversity initiatives',
                                    'Continue to innovate and develop new service offerings'
                                ])}
                                ${createMetricBox('Risk Mitigation', [
                                    'Diversify revenue streams and reduce dependence on a few key clients',
                                    'Strengthen cybersecurity measures and data protection practices',
                                    'Monitor economic conditions and adjust business plans accordingly'
                                ])}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        } else {
            resultsDiv.innerHTML = `<div class="error-message">Error: ${data.message || 'Analysis failed'}</div>`;
        }
    } catch (error) {
        console.error('Error:', error);
        resultsDiv.innerHTML = `<div class="error-message">Error: ${error.message}</div>`;
    }
});

function parseMetricContent(text, sectionTitle) {
    if (!text) return [];
    
    console.log(`Parsing section ${sectionTitle}:`, text);
    
    // Remove asterisks and clean up the text
    text = text.replace(/\*\*/g, '').trim();
    
    const sections = {};
    let currentSection = '';
    let currentItems = [];
    
    // Split by lines and process
    const lines = text.split('\n').map(line => line.trim()).filter(line => line);
    
    for (let line of lines) {
        // Check if line is a section header
        if (line.endsWith(':')) {
            if (currentSection) {
                sections[currentSection] = currentItems;
            }
            currentSection = line.replace(':', '');
            currentItems = [];
        } 
        // If line starts with a bullet point, it's an item
        else if (line.startsWith('-')) {
            currentItems.push(line.replace(/^-\s*/, ''));
        }
    }
    
    // Save the last section
    if (currentSection) {
        sections[currentSection] = currentItems;
    }
    
    // For financial metrics (which don't have explicit sections)
    if (sectionTitle === 'Revenue and Growth' && !sections[sectionTitle]) {
        return lines.filter(line => line.startsWith('-')).map(line => line.replace(/^-\s*/, ''));
    }
    
    return sections[sectionTitle] || [];
}

function createMetricBox(title, items) {
    const content = items && items.length > 0 
        ? items.map(item => `
            <div class="metric-item">
                <span class="bullet">•</span>
                <span class="item-text">${item}</span>
            </div>
        `).join('')
        : '<div class="metric-item no-data">No data available</div>';

    return `
        <div class="metric-box">
            <div class="metric-box-header">${title}</div>
            <div class="metric-content">
                ${content}
            </div>
        </div>
    `;
}

// Add file input validation
document.getElementById('pdfs').addEventListener('change', (e) => {
    const files = e.target.files;
    const maxFiles = 3;
    const maxSize = 100 * 1024 * 1024; // 100MB in bytes
    
    if (files.length > maxFiles) {
        alert(`You can only upload up to ${maxFiles} files`);
        e.target.value = '';
        return;
    }
    
    for (let file of files) {
        if (file.size > maxSize) {
            alert(`File ${file.name} is too large. Maximum size is 100MB`);
            e.target.value = '';
            return;
        }
    }
}); 