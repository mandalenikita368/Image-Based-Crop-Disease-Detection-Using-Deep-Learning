import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
import numpy as np
import os
import json


class PlantDiseaseModel:
    def __init__(self, model_path="plant_disease_model.h5", class_names_path="class_names_from_training.json"):
        self.model = None
        self.model_path = model_path
        self.class_names_path = class_names_path
        self.img_height = 224
        self.img_width = 224

        # ✅ Load class names dynamically from JSON (created by save_class_names.py)
        if os.path.exists(self.class_names_path):
            with open(self.class_names_path, "r") as f:
                self.class_names = json.load(f)
            print(f"✅ Loaded {len(self.class_names)} class names from {self.class_names_path}")
        else:
            raise FileNotFoundError(
                f"❌ Missing {self.class_names_path}. Please run save_class_names.py first to generate it."
            )

        self.num_classes = len(self.class_names)

    def build_model(self):
        """Build CNN model using transfer learning with MobileNetV2"""
        base_model = MobileNetV2(
            input_shape=(self.img_height, self.img_width, 3),
            include_top=False,
            weights='imagenet'
        )
        base_model.trainable = False

        inputs = keras.Input(shape=(self.img_height, self.img_width, 3))
        x = keras.applications.mobilenet_v2.preprocess_input(inputs)
        x = base_model(x, training=False)
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dropout(0.3)(x)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.4)(x)
        x = layers.Dense(128, activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.3)(x)
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)

        model = keras.Model(inputs, outputs)
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

        self.model = model
        return model

    def load_model(self):
        """Load trained model from disk"""
        if os.path.exists(self.model_path):
            self.model = keras.models.load_model(self.model_path)
            print(f"✅ Loaded model from {self.model_path}")
            return True
        print("⚠️ Model file not found. You need to train it first.")
        return False

    def initialize_model(self):
        """Alias for backward compatibility with older app.py"""
        self.load_model()

    def preprocess_image(self, image):
        """Preprocess image for model input"""
        image = image.resize((self.img_width, self.img_height))
        image_array = np.array(image)

        if image_array.shape[-1] == 4:
            image_array = image_array[:, :, :3]

        image_array = image_array.astype(np.float32) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        return image_array

    def predict(self, image):
        """Predict disease from image"""
        if self.model is None:
            if not self.load_model():
                raise ValueError("❌ Model not loaded. Train or load the model first.")

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
            'top_3_predictions': top_3_predictions,
            'all_predictions': predictions[0].tolist()
        }
