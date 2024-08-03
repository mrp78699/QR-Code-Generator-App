from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import qrcode
import os

app = Flask(__name__)

def get_new_filename(file_path):
    
    if not os.path.isfile(file_path):
        return file_path
    
    base, extension = os.path.splitext(file_path)
    counter = 1

    while os.path.isfile(f"{base}{counter}{extension}"):
        counter += 1
    
    return f"{base}{counter}{extension}"

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        text = request.form['text']
        bar_color = request.form['bar_color']
        bac_color = request.form['bac_color']
        in_file_path = "outputs/qrcode.png"
        new_file_path = get_new_filename(in_file_path)

        qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
        )

        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color=bar_color, back_color=bac_color)
        img.save(new_file_path)

        return redirect(url_for('index', filename=os.path.basename(new_file_path)))
    
    filename = request.args.get('filename')
    return render_template('index.html', filename=filename)

@app.route('/outputs/<filename>')
def download_file(filename):
    return send_from_directory('outputs', filename)

if __name__ == '__main__':
    os.makedirs('outputs', exist_ok=True)
    app.run(debug=True)
