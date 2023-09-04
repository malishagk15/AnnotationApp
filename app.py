import os
import cv2
import csv
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['FRAME_FOLDER'] = 'frames'
app.config['CSV_FOLDER'] = 'csv'  # New folder for CSV files
app.config['VIDEO_FILE'] = ''
app.config['FRAME_NAMES'] = []

@app.route('/')
def index():
    return render_template('index.html', frame_names=app.config['FRAME_NAMES'])

@app.route('/upload', methods=['POST'])
def upload():
    if 'video_file' not in request.files:
        return redirect(request.url)
    
    video_file = request.files['video_file']

    if video_file.filename == '':
        return redirect(request.url)

    if video_file:
        app.config['VIDEO_FILE'] = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
        video_file.save(app.config['VIDEO_FILE'])
        
        # Create a folder with the video file's name to store CSV files
        video_name = os.path.splitext(os.path.basename(app.config['VIDEO_FILE']))[0]
        csv_folder = os.path.join(app.config['CSV_FOLDER'], video_name)
        os.makedirs(csv_folder, exist_ok=True)
        app.config['CSV_FILE'] = os.path.join(csv_folder, 'labels.csv')

        # Extract frame names from the video
        app.config['FRAME_NAMES'] = extract_frames(app.config['VIDEO_FILE'])

        # Create an empty CSV file if it doesn't exist
        if not os.path.exists(app.config['CSV_FILE']):
            with open(app.config['CSV_FILE'], mode='w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['VideoName', 'FrameName', 'Label'])

        return redirect(url_for('index'))

def extract_frames(video_path):
    frame_folder = app.config['FRAME_FOLDER']
    os.makedirs(frame_folder, exist_ok=True)
    
    frame_names = []
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_name = f"frame_{frame_count}.jpg"
        frame_names.append(frame_name)
        
        frame_path = os.path.join(frame_folder, frame_name)
        cv2.imwrite(frame_path, frame)
        frame_count += 1
    
    cap.release()
    return frame_names

@app.route('/get_frame', methods=['GET'])
def get_frame():
    frame_name = request.args.get('frame_name', default='', type=str)
    frame_path = os.path.join(app.config['FRAME_FOLDER'], frame_name)

    if os.path.exists(frame_path):
        return send_file(frame_path, mimetype='image/jpeg')
    else:
        return '', 404

@app.route('/label', methods=['POST'])
def label():
    frame_index = int(request.form['frame_index'])
    frame_name = app.config['FRAME_NAMES'][frame_index]
    label = request.form['frame_label']
    video_name = os.path.basename(app.config['VIDEO_FILE'])

    # Check if the frame_name already exists in the CSV file
    with open(app.config['CSV_FILE'], mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        data = list(csv_reader)

    frame_name_exists = False
    for row in data:
        if len(row) >= 2 and row[1] == frame_name:  # Check if row has at least 2 elements
            row[2] = label  # Update the label in the existing row
            frame_name_exists = True
            break

    # If frame_name doesn't exist, add a new row
    if not frame_name_exists:
        data.append([video_name, frame_name, label])

    # Write the updated data back to the CSV file
    with open(app.config['CSV_FILE'], mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)

    return redirect(url_for('index'))

@app.route('/download_csv')
def download_csv():
    return send_file(app.config['CSV_FILE'], as_attachment=True)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['FRAME_FOLDER'], exist_ok=True)
    app.run(debug=True)