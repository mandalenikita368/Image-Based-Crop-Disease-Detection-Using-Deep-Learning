# 🌱 AI Plant Disease Detector

A complete web application for detecting plant diseases in crops using Deep Learning CNN with transfer learning.

## Overview

This application uses a Convolutional Neural Network (CNN) with transfer learning from MobileNetV2 to detect diseases in:
- 🍅 **Tomato** (10 disease classes + healthy)
- 🌽 **Corn/Maize** (4 disease classes + healthy) 
- 🥔 **Potato** (3 disease classes + healthy)

**Total Classes:** 17 plant conditions across 3 crop types

## Features

### ✨ Current Implementation
- **Image Upload Interface** - Drag-and-drop or browse for crop leaf images
- **Transfer Learning Model** - MobileNetV2 (ImageNet pre-trained) + custom classification head
- **Real-time Predictions** - Instant disease detection with confidence scores
- **Top-3 Predictions** - View alternative diagnoses with probabilities
- **Comprehensive Disease Database** - Detailed information on:
  - Symptoms
  - Treatment recommendations
  - Prevention measures
  - Pathogen information
- **Responsive UI** - Works on desktop, tablet, and mobile browsers
- **Error Handling** - Robust error management and user feedback
- **Low Confidence Warnings** - Alerts users when predictions are uncertain

### 🚀 Architecture
```
User Upload Image → Preprocessing → MobileNetV2 (frozen) → 
Custom Classification Head → Softmax → Disease Prediction + Confidence
```

## Current Status

⚠️ **Important:** This application currently uses **synthetic training data** for demonstration purposes. 

For production deployment with accurate disease detection, you need to:

1. **Download PlantVillage Dataset**
   - Dataset: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
   - Contains ~54,000 images of healthy and diseased crop leaves
   
2. **Train the Model**
   - Replace `train_with_synthetic_data()` in `model.py`
   - Implement data loading from PlantVillage directory structure
   - Train for 20-50 epochs with data augmentation
   - Achieve 90%+ validation accuracy
   
3. **Save & Deploy Trained Weights**
   - Save model to `plant_disease_model.h5`
   - Application will automatically load on startup

## Installation & Setup

### Prerequisites
- Python 3.11+
- TensorFlow 2.20+
- Streamlit
- 2GB+ RAM recommended

### Quick Start

1. **Install Dependencies**
   ```bash
   # Dependencies are already installed in this Replit environment
   # For local setup:
   pip install streamlit tensorflow pillow numpy pandas matplotlib
   ```

2. **Run the Application**
   ```bash
   streamlit run app.py --server.port 5000
   ```

3. **Access the App**
   - Open browser to `http://localhost:5000`
   - Upload a crop leaf image
   - Click "Analyze Image"
   - View results and disease information

## File Structure

```
.
├── app.py                  # Main Streamlit application
├── model.py                # CNN model architecture & training
├── disease_info.py         # Disease database with treatment info
├── README.md               # This file
└── plant_disease_model.h5  # Saved model (auto-generated)
```

## Supported Disease Classes

### Tomato (10 classes)
- Bacterial Spot
- Early Blight
- Late Blight
- Leaf Mold
- Septoria Leaf Spot
- Spider Mites (Two-spotted spider mite)
- Target Spot
- Tomato Yellow Leaf Curl Virus
- Tomato Mosaic Virus
- Healthy

### Potato (3 classes)
- Early Blight
- Late Blight
- Healthy

### Corn/Maize (4 classes)
- Cercospora Leaf Spot (Gray Leaf Spot)
- Common Rust
- Northern Leaf Blight
- Healthy

## Training with PlantVillage Dataset

### Step 1: Download Dataset
```python
# Download from Kaggle or use PlantVillage directly
# Expected structure:
# PlantVillage/
#   ├── Tomato___Bacterial_spot/
#   ├── Tomato___Early_blight/
#   └── ...
```

### Step 2: Update model.py
```python
def train_with_plantvillage_data(self, data_dir):
    """Train model with actual PlantVillage dataset"""
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    
    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        validation_split=0.2
    )
    
    train_generator = datagen.flow_from_directory(
        data_dir,
        target_size=(self.img_height, self.img_width),
        batch_size=32,
        class_mode='categorical',
        subset='training'
    )
    
    val_generator = datagen.flow_from_directory(
        data_dir,
        target_size=(self.img_height, self.img_width),
        batch_size=32,
        class_mode='categorical',
        subset='validation'
    )
    
    self.model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=30
    )
    
    self.save_model()
```

### Step 3: Train
```python
from model import PlantDiseaseModel

model = PlantDiseaseModel()
model.build_model()
model.train_with_plantvillage_data('path/to/PlantVillage/')
```

## Technology Stack

- **Frontend:** Streamlit (Python web framework)
- **Deep Learning:** TensorFlow 2.20 + Keras
- **Base Model:** MobileNetV2 (ImageNet pre-trained)
- **Image Processing:** Pillow (PIL), NumPy
- **Data Handling:** Pandas, NumPy

## Performance

### Expected Metrics (with PlantVillage Training)
- Validation Accuracy: 90-95%
- Inference Time: < 1 second per image
- Model Size: ~15MB

### Current Demo Metrics
- Uses synthetic data for demonstration
- Shows UI/UX flow and architecture
- Requires PlantVillage training for accurate predictions

## Usage Tips

### For Best Results
1. **Image Quality**
   - Use clear, well-lit images
   - Focus on the affected leaf area
   - Avoid blurry or dark images
   - Ensure leaf fills most of the frame

2. **Supported Formats**
   - JPG, JPEG, PNG
   - RGB or RGBA images
   - Any resolution (auto-resized to 224x224)

3. **Interpretation**
   - Check confidence scores
   - Review top-3 predictions
   - Consult experts for severe cases
   - Use prevention measures proactively

## Future Enhancements

- [ ] Train on actual PlantVillage dataset
- [ ] Add more crop types (pepper, grape, apple, etc.)
- [ ] Implement batch image processing
- [ ] Add user accounts and detection history
- [ ] Integrate weather data for context-aware recommendations
- [ ] Mobile app version (Progressive Web App)
- [ ] Export detection reports
- [ ] Multi-language support

## Disclaimer

This application is designed as an educational tool and demonstration of AI-powered plant disease detection. For production agricultural use:
- Train the model on actual PlantVillage dataset
- Validate predictions with agricultural experts
- Use as a supplementary tool, not sole diagnostic method
- Consider local growing conditions and variations

## License

Educational and demonstration purposes.

## Contact & Support

For questions about implementing this with actual PlantVillage data or deploying for production use, consult with agricultural AI specialists and agronomists.

---

**Built with** ❤️ **using Streamlit, TensorFlow, and Deep Learning**
