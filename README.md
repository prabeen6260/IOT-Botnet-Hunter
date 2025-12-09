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

