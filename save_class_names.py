import json, os
from tensorflow.keras.preprocessing.image import ImageDataGenerator

DATA_DIR = r"C:\Users\nikit\Downloads\ExpenseFlow\ExpenseFlow\dataset\train"
datagen = ImageDataGenerator(rescale=1./255)
gen = datagen.flow_from_directory(DATA_DIR, target_size=(224,224), batch_size=1, class_mode='categorical', shuffle=False)

# 🔹 Save class index mapping
with open("train_class_indices.json", "w") as f:
    json.dump(gen.class_indices, f, indent=2)
print("✅ Saved train_class_indices.json")

# 🔹 Create list in correct order
idx_to_name = [None] * len(gen.class_indices)
for name, idx in gen.class_indices.items():
    idx_to_name[idx] = name

with open("class_names_from_training.json", "w") as f:
    json.dump(idx_to_name, f, indent=2)
print("✅ Saved class_names_from_training.json")
