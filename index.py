from flask import Flask, request, send_file, jsonify
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)

PORT = int(os.environ.get('REMBG_PORT', 5050))

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'removebg-microservice',
        'model': 'u2net'
    })

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    try:
        # Check if image file is in request
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided. Use "image" field in multipart form.'
            }), 400

        file = request.files['image']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400

        # Read image from request
        input_image = Image.open(file.stream)
        
        # Remove background using rembg
        output_image = remove(input_image)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return send_file(
            img_byte_arr,
            mimetype='image/png',
            as_attachment=False,
            download_name='removed_bg.png'
        )

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print(f"RemoveBG Microservice starting on port {PORT}")
    print(f"Health: http://localhost:{PORT}/health")
    print(f"Remove BG: POST http://localhost:{PORT}/remove-bg")
    app.run(host='0.0.0.0', port=PORT, debug=False)
