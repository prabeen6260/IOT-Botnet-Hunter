🛡️ IoT Botnet Hunter: Universal Network Detection System

This project is a sophisticated Intrusion Detection System (IDS) that uses Machine Learning to detect malicious network traffic from compromised IoT devices (like webcams and doorbells).

It addresses the real-world threat posed by botnets such as Mirai and Bashlite, which leverage insecure IoT devices to launch large-scale Distributed Denial of Service (DDoS) attacks.

🚀 Key Achievements

Universal Model: A Random Forest Classifier trained on heterogeneous data (traffic from multiple distinct device types) to create a robust model that avoids false positives across different hardware architectures.

Behavioral Detection: Uses 115 statistical features (Mean, Variance, Jitter, and Volume) over Damped Time Windows, allowing the model to detect attacks based on behavioral patterns, not just IP addresses.

Multi-Class Classification: The system distinguishes between benign traffic and four distinct attack behaviors:

Mirai Flood (High-Volume)

Bashlite Flood (High-Volume)

Reconnaissance Scan (Low-Volume, Stealthy)

SOC Dashboard: Built with Streamlit and Plotly, providing real-time visualization of the network pulse, confidence scores, and threat classification for immediate security analysis.

💻 Technical Stack

Language: Python

ML Libraries: scikit-learn (Random Forest), joblib

Data Analysis: pandas, numpy

Visualization: Streamlit, Plotly

⚙️ How to Run Locally

Prerequisites

Python 3.8+

A local copy of the N-BaIoT dataset (for training).

Setup

Clone this repository and install dependencies:

git clone [https://github.com/YOUR_USERNAME/iot-botnet-hunter.git](https://github.com/YOUR_USERNAME/iot-botnet-hunter.git)
cd iot-botnet-hunter
pip install -r requirements.txt


Prepare Data: Create the required directory structure (data/Doorbell/, etc.) and place the necessary sampled CSV files inside (e.g., the first 200 rows of benign_traffic.csv and the attack files).

Train & Save the Model:

python train_universal.py


Launch the Dashboard:

streamlit run app.py


The application will launch in your browser. Use the "Auto-Pilot (Live)" mode to see the system monitor a mixed traffic stream.
