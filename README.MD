# RemoveBG Microservice

A simple and efficient Flask-based microservice for removing image backgrounds using the `rembg` library with the U2-Net model.

## Requirements

- Python 3.8+
- Flask >= 3.0.0
- rembg >= 2.0.69
- Pillow >= 10.0.0
- onnxruntime >= 1.18.0

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ItzApipAjalah/Py-RemoveBackground.git
cd removebg
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Start the Server

```bash
python index.py
```

By default, the server runs on port `5050`. You can customize this using the `REMBG_PORT` environment variable:

```bash
# Windows
set REMBG_PORT=8080
python index.py

# Linux/macOS
REMBG_PORT=8080 python index.py
```

## API Endpoints

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "service": "removebg-microservice",
  "model": "u2net"
}
```

---

### Remove Background

```http
POST /remove-bg
Content-Type: multipart/form-data
```

**Request Body:**
| Field   | Type | Description                |
|---------|------|----------------------------|
| `image` | File | The image file to process  |

**Success Response:**
- **Content-Type:** `image/png`
- **Body:** The processed image with transparent background

**Error Response:**
```json
{
  "success": false,
  "error": "Error message here"
}
```

---

## Example Usage

### Using cURL

```bash
curl -X POST -F "image=@/path/to/your/image.jpg" \
  http://localhost:5050/remove-bg \
  --output result.png
```

### Using Python Requests

```python
import requests

url = "http://localhost:5050/remove-bg"
files = {"image": open("input.jpg", "rb")}

response = requests.post(url, files=files)

if response.status_code == 200:
    with open("output.png", "wb") as f:
        f.write(response.content)
    print("Background removed successfully!")
else:
    print(f"Error: {response.json()}")
```

### Using JavaScript (Fetch API)

```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);

fetch('http://localhost:5050/remove-bg', {
  method: 'POST',
  body: formData
})
.then(response => response.blob())
.then(blob => {
  const url = URL.createObjectURL(blob);
  // Use the processed image URL
})
.catch(error => console.error('Error:', error));
```

## Project Structure

```
removebg/
├── index.py           # Main Flask application
├── requirements.txt   # Python dependencies
├── README.md          # Documentation
├── .gitignore         # Git ignore rules
└── venv/              # Virtual environment (not tracked)
```

## Notes

- The first request may take longer as the model needs to be loaded into memory
- Large images may require more processing time
- Output format is always PNG with transparent background
- Ensure you have sufficient RAM for processing large images (recommended: 4GB+)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Made using Flask and rembg**
