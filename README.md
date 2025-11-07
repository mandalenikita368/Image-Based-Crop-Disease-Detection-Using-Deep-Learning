# 🌱 AI Plant Disease Detector

A complete deep learning–based web application for detecting **crop diseases** using **Convolutional Neural Networks (CNNs)** and **Transfer Learning (MobileNetV2)**.

---

## 🧠 Overview

This project identifies plant diseases from leaf images and provides detailed insights on symptoms, treatment, and prevention.  
The model has been trained using the **PlantVillage dataset** with 17 total classes across 3 major crops:

- 🍅 **Tomato** → 10 disease classes + healthy  
- 🌽 **Corn (Maize)** → 4 disease classes + healthy  
- 🥔 **Potato** → 3 disease classes + healthy  

**🧩 Total Classes:** 17  

---

## ✨ Features

### 🌾 AI-Powered Disease Detection
- Upload any crop leaf image (Tomato, Potato, or Corn)
- Get real-time predictions with confidence levels
- Displays top-3 probable diseases

### 🧬 Transfer Learning (MobileNetV2)
- Fine-tuned CNN for plant disease classification  
- Lightweight and fast inference

### 📋 Detailed Disease Insights
For every prediction, users get:
- **Crop name**
- **Pathogen information**
- **Symptoms**
- **Treatment recommendations**
- **Prevention measures**

### ⚙️ Additional Features
- Real-time Streamlit web interface  
- Automatic image preprocessing  
- Dynamic disease database  
- Error handling and low-confidence warnings  
- Fully responsive UI  

---

## 🏗️ Project Architecture


---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | Streamlit |
| **Backend** | Python 3.12 |
| **Deep Learning** | TensorFlow / Keras (MobileNetV2) |
| **Database** | SQLite (via SQLAlchemy) |
| **Environment** | Conda / Virtualenv |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/mandalenikita368/Image-Based-Crop-Disease-Detection-Using-Deep-Learning.git
cd Image-Based-Crop-Disease-Detection-Using-Deep-Learning
python -m venv venv
venv\Scripts\activate  # (on Windows)
# or
source venv/bin/activate  # (on macOS/Linux)
pip install -r requirements.txt
streamlit run app.py
