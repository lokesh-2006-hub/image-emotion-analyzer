let imageFile = null;

function handleFileChange(input) {
    const analyzeButton = document.getElementById('analyzeButton');
    const uploadedImage = document.getElementById('uploadedImage');
    const file = input.files[0];
    imageFile = file;

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            uploadedImage.src = e.target.result;
            uploadedImage.style.display = 'block';
            analyzeButton.disabled = false;
        }
        reader.readAsDataURL(file);
    } else {
        uploadedImage.style.display = 'none';
        analyzeButton.disabled = true;
    }
}

async function analyzeImage() {
    const captionOutput = document.getElementById('captionOutput');
    const sentimentOutput = document.getElementById('sentimentOutput');
    const emotionOutput = document.getElementById('emotionOutput');
    const reasonOutput = document.getElementById('reasonOutput');

    if (!imageFile) {
        alert('Please select an image first!');
        return;
    }

    captionOutput.textContent = "Analyzing...";
    sentimentOutput.textContent = "";
    emotionOutput.textContent = "";
    reasonOutput.textContent = "";

    const formData = new FormData();
    formData.append('image', imageFile);

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        if (response.ok) {
            captionOutput.textContent = data.caption;
            sentimentOutput.textContent = data.sentiment;
            emotionOutput.textContent = data.emotion;
            reasonOutput.textContent = data.reason;
        } else {
            captionOutput.textContent = "Error analyzing image.";
        }
    } catch (error) {
        console.error('Error:', error);
        captionOutput.textContent = "Error analyzing image.";
    }
}
