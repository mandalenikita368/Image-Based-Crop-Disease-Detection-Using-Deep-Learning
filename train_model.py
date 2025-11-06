import os
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# ✅ Configuration
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 10  # pehle test ke liye 10 epochs, baad me 25-30 kar sakta hai
DATA_DIR = "dataset/train"
VAL_DIR = "dataset/valid"
MODEL_PATH = "plant_disease_model.h5"

# ✅ Check folders
if not os.path.exists(DATA_DIR) or not os.path.exists(VAL_DIR):
    raise FileNotFoundError("❌ Dataset folders not found! Make sure dataset/train and dataset/valid exist.")

# ✅ Data generators
train_gen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True
).flow_from_directory(
    DATA_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

val_gen = ImageDataGenerator(rescale=1./255).flow_from_directory(
    VAL_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

num_classes = len(train_gen.class_indices)
print(f"✅ Found {num_classes} disease categories.")

# ✅ Model definition
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))
for layer in base_model.layers:
    layer.trainable = False  # Freeze base model

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.4)(x)
preds = Dense(num_classes, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=preds)

model.compile(optimizer=Adam(1e-3), loss="categorical_crossentropy", metrics=["accuracy"])

# ✅ Callbacks
callbacks = [
    ModelCheckpoint(MODEL_PATH, monitor="val_accuracy", save_best_only=True),
    EarlyStopping(monitor="val_accuracy", patience=3, restore_best_weights=True)
]

# ✅ Train the model
print("🚀 Starting training...")
history = model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS, callbacks=callbacks)

print(f"✅ Training complete! Model saved as {MODEL_PATH}")
