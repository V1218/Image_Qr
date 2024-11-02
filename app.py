from flask import Flask, render_template_string, request
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    # Inline HTML and CSS for the frontend
    html_code = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Enhanced QR Code Generator</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: Arial, sans-serif;
                background: url('static/pixelcut-export (1).png') no-repeat center center fixed;
                background-size: cover;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                color: #333;
            }
            .container {
                background-color: rgba(255, 255, 255, 0.85);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
                width: 600px;
                height: 500px;
                text-align: center;
                border: 2px solid #ccc; /* Add this line to create a border */
            }
            h1 {
                font-size: 24px;
                color: #333;
                margin-bottom: 20px;
            }
            form {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            input[type="text"] {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
                width: 100%;
            }
            .color-input {
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .color-picker-label {
                font-size: 16px;
            }
            .color-picker {
                width: 50px;
                height: 30px;
                border: 1px solid #ddd;
                border-radius: 5px;
                cursor: pointer;
            }
            button {
                padding: 10px;
                border: none;
                border-radius: 5px;
                background-color: #4CAF50;
                color: #fff;
                font-size: 16px;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            .back-btn, .download-btn {
                display: inline-block;
                margin-top: 15px;
                padding: 10px;
                border-radius: 5px;
            }
            .back-btn {
                background-color: #f44336;
                color: #fff;
                margin-left: 10px; /* Space between buttons */
            }
            .back-btn:hover {
                background-color: #d32f2f;
            }
            .download-btn {
                display: none;
                background-color: #007BFF;
                color: white;
            }
            .download-btn:hover {
                background-color: #0056b3;
            }
            #qr-code {
                margin-top: 20px;
            }
            img {
                max-width: 200px;
                height: auto;
                margin-top: 15px;
                border-radius: 5px;
            }
        </style>
        <script>
            let qrCodeDataUrl = '';

            async function generateQRCode(event) {
                event.preventDefault();
                const data = document.querySelector('input[name="data"]').value;
                const fgColor = document.querySelector('input[name="fg_color"]').value;
                const bgColor = document.querySelector('input[name="bg_color"]').value;

                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ data: data, fg_color: fgColor, bg_color: bgColor })
                });

                if (response.ok) {
                    qrCodeDataUrl = await response.text();
                    document.getElementById('qr-code').innerHTML = `<img src="${qrCodeDataUrl}" alt="QR Code">`;
                    document.querySelector('.download-btn').style.display = 'inline-block';
                } else {
                    alert('Error generating QR Code. Please try again.');
                }
            }

            function downloadQRCode() {
                const link = document.createElement('a');
                link.href = qrCodeDataUrl;
                link.download = 'qr_code.png';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }

            function resetForm() {
                document.querySelector('form').reset();
                document.getElementById('qr-code').innerHTML = '';
                document.querySelector('.download-btn').style.display = 'none';
            }
        </script>
    </head>
    <body>
        <div class="container">
            <h1>QR Code Generator</h1>
            <form onsubmit="generateQRCode(event)">
                <input type="text" name="data" placeholder="Enter text or URL" required>

                <!-- QR Code Color Picker -->
                <div class="color-input">
                    <label for="fg_color" class="color-picker-label">QR Code Color:</label>
                    <input type="color" name="fg_color" value="#000000" class="color-picker">
                </div>

                <!-- Background Color Picker -->
                <div class="color-input">
                    <label for="bg_color" class="color-picker-label">Background Color:</label>
                    <input type="color" name="bg_color" value="#ffffff" class="color-picker">
                </div>

                <button type="submit">Generate QR Code</button>
            </form>
            <div id="qr-code"></div>
            <button class="download-btn" onclick="downloadQRCode()">Download QR Code</button>
            <button class="back-btn" onclick="resetForm()">Back</button>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_code)

@app.route('/generate', methods=['POST'])
def generate_qr():
    data = request.json['data']
    fg_color = request.json.get('fg_color', 'black')
    bg_color = request.json.get('bg_color', 'white')
    
    qr = qrcode.QRCode(version=None, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=fg_color, back_color=bg_color)
    img_stream = BytesIO()
    img.save(img_stream, format='PNG')
    img_stream.seek(0)
    
    qr_code_data_url = base64.b64encode(img_stream.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{qr_code_data_url}"

if __name__ == "__main__":
    app.run(debug=True)
