from flask import Flask, request, jsonify
from PIL import Image
import io
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

app = Flask(__name__)

# Load BLIP model for image captioning
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

def analyze_caption(caption):
    """Simple rules to generate sentiment, emotion, and reason based on caption."""
    caption_lower = caption.lower()

    if any(word in caption_lower for word in ["smile", "happy", "bright"]):
        sentiment = "Positive"
        emotion = "Happiness"
    elif any(word in caption_lower for word in ["sad", "dark", "lonely", "cry"]):
        sentiment = "Negative"
        emotion = "Sadness"
    elif any(word in caption_lower for word in ["fight", "shield", "battle", "ready", "determination"]):
        sentiment = "Neutral"
        emotion = "Determination"
    else:
        sentiment = "Neutral"
        emotion = "Neutrality"

    reason = f"The image shows {caption}. This suggests a feeling of {emotion.lower()} because of the elements present."

    return sentiment, emotion, reason

from flask import render_template

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({'error': 'No image selected'}), 400

    try:
        image_bytes = image_file.read()

        # Step 1: Generate caption
        caption = generate_caption(image_bytes)

        # Step 2: Analyze caption
        sentiment, emotion, reason = analyze_caption(caption)

        return jsonify({
            'sentiment': sentiment,
            'emotion': emotion,
            'reason': reason,
            'caption': caption
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
