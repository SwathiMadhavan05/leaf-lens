LeafLens is a Streamlit-based plant leaf health analysis app that classifies uploaded leaf images as healthy or diseased and returns treatment-oriented guidance. The project combines classical digital image processing, handcrafted feature extraction, and a pre-trained machine learning classifier for fast browser-based diagnosis.

Overview
The application accepts a leaf image, standardizes it, extracts visual features, runs a trained classifier, and combines that prediction with rule-based lesion analysis to produce:

Healthy vs diseased decision
Confidence score
Green area, lesion area, and spot count metrics
Disease pattern label
Recommended treatment suggestions
The repository also includes the experimentation notebook used during model development and several saved model artifacts from intermediate training stages.

Features
Streamlit web interface with login, landing screen, upload flow, and result cards
OpenCV-based preprocessing and lesion analysis
Hybrid prediction logic:
joblib ML model probability
rule-based visual disease scoring
Confidence-aware output for user trust
Treatment guidance for common visible patterns such as:
powdery mildew
rust or fungal leaf spots
chlorosis or stress pattern
blight or necrotic spot pattern
Deployable on Streamlit Community Cloud
Project Structure
LeafLens/
├── app.py
├── requirements.txt
├── README.md
├── DIP_Plantdisease.ipynb
├── leaf_health_model.joblib
├── plant_*.npz
└── data/
    ├── healthy/
    └── diseased/
Important files
app.py
Main Streamlit application and inference pipeline.

requirements.txt
Pinned Python dependencies for local execution and deployment.

DIP_Plantdisease.ipynb
Experimental notebook for feature engineering, model training, and validation.

leaf_health_model.joblib
Primary classifier used by the Streamlit app.

plant_*.npz
Intermediate and alternate saved model artifacts from development.

data/healthy, data/diseased
Sample image folders used for dataset organization and testing.

How It Works
1. Image input
The user uploads a leaf image through the Streamlit UI. The image is loaded in RGB format using Pillow and converted into a NumPy array.

2. Preprocessing
The app standardizes the image using OpenCV:

resize to fixed dimensions
convert to grayscale and HSV
compute leaf masks from saturation and brightness thresholds
clean masks with morphology
isolate the main leaf using connected components
3. Feature extraction
The ML feature extractor computes:

HSV statistics
RGB channel statistics
green, yellow, brown, white, and dark pixel ratios
edge density with Canny
gradient magnitude features with Sobel
grayscale histogram variance, peak, and entropy
4. Diagnosis logic
LeafLens uses a hybrid approach:

If leaf_health_model.joblib is available, the app predicts disease probability using predict_proba.
In parallel, the app computes visual lesion ratios and spot counts directly from the image.
A final decision is made by combining model confidence with rule-based disease heuristics.
5. Output
The app returns:

healthy or diseased status
confidence percentage
disease type pattern
treatment recommendations
key visual metrics for explanation
Model Development
The model development process is documented in DIP_Plantdisease.ipynb.

That notebook includes:

dataset preparation and train/test splitting
feature extraction experiments
classical ML model comparisons
custom 32-feature DIP pipeline experiments
saved .npz model variants
Streamlit prototype exploration
Models explored during development include:

Random Forest
SVM with RBF kernel
KNN
custom ensemble-style experimental predictors
Installation
Prerequisites
Python 3.10 or later recommended
pip
Local setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Run the app
streamlit run app.py
After startup, open the local Streamlit URL shown in the terminal.

Demo Login
The current app includes hardcoded demo credentials in app.py (line 411):

Username: farmer01
Password: leaf123
Username: agriadmin
Password: crop456
These are suitable only for demo purposes and should be replaced before any real multi-user deployment.

Dependencies
Key packages used in this project:

streamlit
opencv-python-headless
numpy
scikit-learn
scikit-image
joblib
pillow
matplotlib
seaborn
The dependency list is pinned in requirements.txt for reproducible deployment.

Deployment Notes
The project is designed for Streamlit Community Cloud deployment.

Important deployment detail:

use opencv-python-headless rather than opencv-python to avoid cloud runtime issues with cv2
Typical deployment flow:

Push the repository to GitHub
Connect the repo in Streamlit Community Cloud
Set app.py as the entry point
Let Streamlit install dependencies from requirements.txt
Limitations
The current app is tuned for healthy vs diseased screening and visible disease-pattern guidance rather than lab-grade diagnosis.
Login is static and demo-only.
Dataset size in the repository is limited and may not cover all crops, environments, or disease stages.
Several .npz models are experimental artifacts and not all are used by the deployed app.
Future Improvements
Expand dataset diversity across crops and disease stages
Replace demo login with secure authentication
Add multiclass disease classification
Add severity estimation
Improve model monitoring and evaluation reporting
Add mobile-friendly capture and multilingual support
Acknowledgments
LeafLens was built as a plant disease detection project combining digital image processing, classical machine learning, and Streamlit deployment for accessible agricultural decision support.
