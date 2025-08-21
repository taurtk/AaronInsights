document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('idea-form');
    const loading = document.getElementById('loading');
    const container = document.getElementById('ideas-container');
    const exampleButtons = document.querySelectorAll('.example-button');

    // Handle form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const prompt = document.getElementById('prompt').value;
        if (prompt) {
            generateIdeas(prompt);
        }
    });

    // Handle example button clicks
    exampleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const topic = this.textContent.replace(/[^\w\s]/gi, '').trim();
            document.getElementById('prompt').value = topic;
            generateIdeas(topic);
        });
    });

    function generateIdeas(prompt) {
        loading.style.display = 'block';
        container.innerHTML = '';

        const formData = new FormData();
        formData.append('prompt', prompt);

        fetch('/generate_ideas', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loading.style.display = 'none';
            if (data.success) {
                displayIdeas(data.clusters);
            } else {
                container.innerHTML = `<div class="error">Error: ${data.error}</div>`;
            }
        })
        .catch(error => {
            loading.style.display = 'none';
            container.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        });
    }

    function displayIdeas(clusters) {
        let html = '';
        
        Object.keys(clusters).forEach(cluster => {
            html += `<div class="ideas-header"><h2>🎯 ${cluster.charAt(0).toUpperCase() + cluster.slice(1)}</h2></div>`;
            
            clusters[cluster].forEach((idea, index) => {
                html += `
                <div class="idea-card">
                    <h3 style="color: #2d3748; margin-bottom: 1rem;">💡 Idea ${index + 1}</h3>
                    <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 1.5rem;">${idea.idea}</p>
                    
                    <div class="metric-grid">
                        <div class="metric-card">
                            <h4 style="color: #667eea; margin: 0;">⭐ ${idea.novelty || 8}/10</h4>
                            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #718096;">Novelty</p>
                        </div>
                        <div class="metric-card">
                            <h4 style="color: #38a169; margin: 0;">🎯 ${idea.uniqueness || 7}/10</h4>
                            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #718096;">Uniqueness</p>
                        </div>
                        <div class="metric-card">
                            <h4 style="color: #f56565; margin: 0;">💰 ${idea.business_value || 9}/10</h4>
                            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #718096;">Business Value</p>
                        </div>
                    </div>
                    
                    ${idea.differentiator ? `<p><strong>🎯 Key Differentiator:</strong> ${idea.differentiator}</p>` : ''}
                    
                    ${idea.validation ? `
                    <div class="validation-section">
                        <h4 style="color: #c2410c; margin-bottom: 0.5rem;">✅ Validation Framework</h4>
                        <p><strong>Target Users:</strong> ${idea.validation.target_users || 'TBD'}</p>
                        <p><strong>Entry Barrier:</strong> ${(idea.validation.entry_barrier || 'medium').charAt(0).toUpperCase() + (idea.validation.entry_barrier || 'medium').slice(1)}</p>
                        <p><strong>Monetization:</strong> ${idea.validation.monetization || 'TBD'}</p>
                        <p><strong>Key Risks:</strong> ${idea.validation.risks || 'Market competition'}</p>
                    </div>
                    ` : ''}
                    
                    ${idea.market_analysis ? `
                    <div class="market-section">
                        <h4 style="color: #1e40af; margin-bottom: 0.5rem;">📊 Market Intelligence</h4>
                        <p><strong>Total Addressable Market:</strong> ${idea.market_analysis.tam || 'Analyzing...'}</p>
                        <p><strong>Growth Rate:</strong> ${idea.market_analysis.cagr || 'Calculating...'}</p>
                        <p style="font-size: 0.9rem; color: #64748b;"><em>Source: ${idea.market_analysis.source || 'Market Research 2024'}</em></p>
                    </div>
                    ` : ''}
                    
                    ${idea.justification ? `<p><strong>💭 Analysis:</strong> ${idea.justification}</p>` : ''}
                </div>
                `;
            });
        });
        
        container.innerHTML = html;
    }
});