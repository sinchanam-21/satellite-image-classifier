document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const previewSection = document.getElementById('previewSection');
    const uploadSection = document.getElementById('uploadSection');
    const imagePreview = document.getElementById('imagePreview');
    const removeBtn = document.getElementById('removeBtn');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultSection = document.getElementById('resultSection');
    const btnLoader = document.getElementById('btnLoader');
    const btnText = analyzeBtn.querySelector('.btn-text');

    // Drag and Drop
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--primary)';
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.style.borderColor = 'var(--glass-border)';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        const files = e.dataTransfer.files;
        if (files.length) handleFile(files[0]);
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) handleFile(e.target.files[0]);
    });

    let currentFile = null;

    function handleFile(file) {
        if (!file.type.startsWith('image/')) return;
        currentFile = file;

        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            dropZone.classList.add('hidden');
            previewSection.classList.remove('hidden');
            resultSection.classList.add('hidden');
        };
        reader.readAsDataURL(file);
    }

    removeBtn.addEventListener('click', () => {
        dropZone.classList.remove('hidden');
        previewSection.classList.add('hidden');
        resultSection.classList.add('hidden');
        fileInput.value = '';
        currentFile = null;
    });

    analyzeBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        let formData = new FormData();
        formData.append('file', currentFile);

        // Show loading
        btnLoader.classList.remove('hidden');
        btnText.textContent = 'Scanning...';
        analyzeBtn.disabled = true;

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.error) {
                alert(result.error);
            } else {
                showResults(result);
            }
        } catch (error) {
            console.error(error);
            alert('Analysis failed. Please ensure the model is trained.');
        } finally {
            btnLoader.classList.add('hidden');
            btnText.textContent = 'Analyze Terrain';
            analyzeBtn.disabled = false;
        }
    });

    function showResults(data) {
        resultSection.classList.remove('hidden');
        document.getElementById('predictionClass').textContent = data.class;
        document.getElementById('confidenceValue').textContent = `${(data.confidence * 100).toFixed(1)}% Confidence`;

        const barsContainer = document.getElementById('probabilityBars');
        barsContainer.innerHTML = '';

        Object.entries(data.probabilities).forEach(([className, prob]) => {
            const percentage = (prob * 100).toFixed(1);
            const item = document.createElement('div');
            item.className = 'prob-item';
            item.innerHTML = `
                <div class="prob-info">
                    <span>${className}</span>
                    <span>${percentage}%</span>
                </div>
                <div class="progress-bg">
                    <div class="progress-fill" style="width: 0%; background: ${getColor(className)}"></div>
                </div>
            `;
            barsContainer.appendChild(item);

            // Animate width
            setTimeout(() => {
                item.querySelector('.progress-fill').style.width = `${percentage}%`;
            }, 100);
        });

        // Scroll to results
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }

    function getColor(className) {
        const colors = {
            'cloudy': 'var(--accent-cloudy)',
            'desert': 'var(--accent-desert)',
            'green_area': 'var(--accent-green)',
            'water': 'var(--accent-water)'
        };
        return colors[className] || 'var(--primary)';
    }
});
