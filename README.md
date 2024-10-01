# AnnotationApp

AnnotationApp is a web-based image annotation tool specifically designed for creating annotations compatible with YOLO models. This tool simplifies the process of labeling objects in images, generating annotations in YOLO format for model training.

## Features
- Web-based interface for easy image annotation.
- Supports bounding box annotations.
- Saves annotations in YOLO format.
- Built with Python and Flask for a simple, responsive user experience.

## Prerequisites
- Python 3.10.9
- Conda (optional but recommended for creating isolated environments)
- Flask
- YOLO-compatible images for annotation.

## Installation

Follow these steps to set up and run the project on your local machine.

### 1. Clone the Repository
```
git clone https://github.com/malishagk15/AnnotationApp.git
```

### 2. Navigate to the Project Directory
```
cd your_repository
```

### 3. Create a Python Environment (using Conda)
If you haven't installed Conda, you can download it from [Anaconda](https://www.anaconda.com/products/distribution).

Create an environment with Python 3.10.9:
```
conda create -n myenv python=3.10.9
```

### 4. Activate the Environment
```
conda activate myenv
```

### 5. Install Dependencies
Make sure all required Python packages are installed:
```
pip install -r requirements.txt
```

### 6. Run the Flask App
Once the setup is complete, you can run the app:
```
python app.py
```

### 7. Access the Application
Open your browser and navigate to `http://127.0.0.1:5000` to start annotating images.

## Usage
1. Upload an image using the web interface.
2. Annotate the objects using the provided tools.
3. Save the annotations in YOLO format, ready for use in model training.

## Contributing
Feel free to fork the repository and submit pull requests if you would like to contribute. Any feedback or feature requests are welcome.
