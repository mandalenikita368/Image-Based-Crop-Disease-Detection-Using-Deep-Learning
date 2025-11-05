import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

class PlantDiseaseModel:
    def __init__(self):
        self.model = None
        self.class_names = [
            'Tomato___Bacterial_spot',
            'Tomato___Early_blight',
            'Tomato___Late_blight',
            'Tomato___Leaf_Mold',
            'Tomato___Septoria_leaf_spot',
            'Tomato___Spider_mites Two-spotted_spider_mite',
            'Tomato___Target_Spot',
            'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
            'Tomato___Tomato_mosaic_virus',
            'Tomato___healthy',
            'Potato___Early_blight',
            'Potato___Late_blight',
            'Potato___healthy',
            'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
            'Corn_(maize)___Common_rust',
            'Corn_(maize)___Northern_Leaf_Blight',
            'Corn_(maize)___healthy'
        ]
        self.num_classes = len(self.class_names)
        self.img_height = 224
        self.img_width = 224
        
    def build_model(self):
        """Build CNN model architecture based on PlantVillage approach"""
        model = keras.Sequential([
            layers.Input(shape=(self.img_height, self.img_width, 3)),
            
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.2),
            
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.2),
            
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.3),
            
            layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.3),
            
            layers.Conv2D(512, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.4),
            
            layers.Flatten(),
            layers.Dense(512, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.4),
            
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def initialize_weights(self):
        """Initialize model with random weights (simulating pre-trained model)"""
        if self.model is None:
            self.build_model()
        
        dummy_input = np.random.rand(1, self.img_height, self.img_width, 3).astype(np.float32)
        _ = self.model.predict(dummy_input, verbose=0)
        
    def preprocess_image(self, image):
        """Preprocess image for model input"""
        image = image.resize((self.img_width, self.img_height))
        image_array = np.array(image)
        
        if image_array.shape[-1] == 4:
            image_array = image_array[:, :, :3]
        
        image_array = image_array / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
    
    def predict(self, image):
        """Predict disease from image"""
        if self.model is None:
            self.initialize_weights()
        
        processed_image = self.preprocess_image(image)
        predictions = self.model.predict(processed_image, verbose=0)
        
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        predicted_class = self.class_names[predicted_class_idx]
        
        top_3_indices = np.argsort(predictions[0])[-3:][::-1]
        top_3_predictions = [
            {
                'class': self.class_names[idx],
                'confidence': float(predictions[0][idx])
            }
            for idx in top_3_indices
        ]
        
        return {
            'predicted_class': predicted_class,
            'confidence': confidence,
            'top_3_predictions': top_3_predictions
        }
