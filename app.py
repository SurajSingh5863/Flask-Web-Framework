from flask import Flask, request, render_template
import base64
import io
from PIL import Image, ImageDraw

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    data = request.json
    frame_data = data.get('frame', None)
    
    if frame_data:
        # Decode the base64 frame data
        frame_bytes = base64.b64decode(frame_data.split(',')[1])
        
        # Create a PIL Image object from the frame bytes
        image = Image.open(io.BytesIO(frame_bytes))
        
        # Draw a rectangle on the image
        draw = ImageDraw.Draw(image)
        rectangle_coords = (50, 50, 200, 200)  # (x1, y1, x2, y2)
        draw.rectangle(rectangle_coords, outline='red', width=2)
        
        # Convert the image back to bytes
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        processed_frame_data = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return {'message': 'Frame received and processed!', 'processed_frame': processed_frame_data}
    else:
        return {'message': 'No frame data received.'}, 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=5000)

