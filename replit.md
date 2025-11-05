# AI Plant Disease Detector

## Overview

This is a web-based plant disease detection application that uses deep learning to identify diseases in crop leaves. The system leverages transfer learning with MobileNetV2 (pre-trained on ImageNet) and a custom classification head to detect 17 different plant conditions across three crop types: Tomato (10 disease classes + healthy), Corn/Maize (4 disease classes + healthy), and Potato (3 disease classes + healthy).

The application provides real-time disease predictions with confidence scores, displays top-3 alternative diagnoses, and offers comprehensive disease information including symptoms, treatment recommendations, prevention measures, and pathogen details.

**Current Status:** The application uses synthetic training data for demonstration purposes. For production deployment, it requires training with the PlantVillage dataset (~54,000 images).

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework:** Streamlit-based web interface
- **Layout:** Wide layout with two-column design for image upload and results display
- **Caching Strategy:** Uses `@st.cache_resource` decorator for model loading to prevent reloading on every interaction
- **Image Handling:** PIL (Python Imaging Library) for image processing and display
- **User Feedback:** Warning messages for demo mode and low confidence predictions

### Backend Architecture
- **Deep Learning Framework:** TensorFlow/Keras
- **Model Architecture:** 
  - Base: MobileNetV2 (frozen, ImageNet weights)
  - Input shape: 224x224x3
  - Custom classification head on top of base model
  - Output: 17-class softmax classification
- **Preprocessing:** MobileNetV2-specific preprocessing pipeline
- **Model Persistence:** HDF5 format (.h5 file) for trained model storage
- **Class Management:** Hardcoded list of 17 class names mapping to disease categories

### Data Architecture
- **Disease Information Storage:** Python dictionary-based disease database in `disease_info.py`
- **Database Schema:** Each disease entry contains:
  - Disease name
  - Crop type
  - Pathogen information
  - Symptoms (list)
  - Treatment recommendations (list)
  - Prevention measures (list)
- **No persistent database:** All disease information is stored in-memory as static data

### Key Design Patterns
- **Transfer Learning:** Leverages pre-trained MobileNetV2 to reduce training requirements and improve accuracy with limited data
- **Frozen Base Model:** Base model layers are set to non-trainable to preserve ImageNet features and only train the classification head
- **Resource Caching:** Model loaded once and cached to optimize performance across multiple predictions
- **Separation of Concerns:** 
  - `model.py`: Model architecture and prediction logic
  - `disease_info.py`: Disease knowledge base
  - `app.py`: User interface and interaction flow

### Trade-offs and Rationale
- **MobileNetV2 vs. Other Architectures:** Chosen for its balance of accuracy and computational efficiency, making it suitable for web deployment with limited resources
- **Streamlit vs. Flask/Django:** Streamlit selected for rapid prototyping and simplified UI development without frontend frameworks
- **In-memory Database vs. SQL/NoSQL:** Disease information is static and small enough to keep in-memory, avoiding database overhead
- **Synthetic Data Limitation:** Current implementation uses synthetic data as a proof-of-concept, with clear documentation that production requires real PlantVillage dataset training

## External Dependencies

### Machine Learning & Scientific Computing
- **TensorFlow/Keras:** Deep learning framework for model building, training, and inference
- **NumPy:** Numerical operations and array manipulations for image data

### Web Framework
- **Streamlit:** Web application framework providing the user interface

### Image Processing
- **PIL (Pillow):** Image loading, manipulation, and display

### Training Data Source (Production)
- **PlantVillage Dataset:** Kaggle dataset with ~54,000 labeled images of healthy and diseased crop leaves
  - URL: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
  - Required for production model training
  - Not currently integrated (using synthetic data instead)

### Pre-trained Models
- **MobileNetV2 (ImageNet):** Transfer learning base model with ImageNet weights, automatically downloaded by Keras

### File System Dependencies
- **Model Storage:** Local file system for saving/loading trained model (`plant_disease_model.h5`)
- **No cloud storage integration:** All assets stored locally