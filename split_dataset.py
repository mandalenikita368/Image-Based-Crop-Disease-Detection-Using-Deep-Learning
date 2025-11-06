import os
import shutil
import random

# 🔹 Source: jahan tera PlantVillage dataset pada hai
SOURCE_DIR = r"C:\Users\nikit\Downloads\archive\PlantVillage"

# 🔹 Destination: jahan tu apna app chala raha hai
DEST_DIR = r"C:\Users\nikit\Downloads\ExpenseFlow\ExpenseFlow\dataset"

TRAIN_RATIO = 0.9  # 90% training, 10% validation

# Create train/valid folders
train_dir = os.path.join(DEST_DIR, "train")
valid_dir = os.path.join(DEST_DIR, "valid")
os.makedirs(train_dir, exist_ok=True)
os.makedirs(valid_dir, exist_ok=True)

# Get all class folders
classes = [d for d in os.listdir(SOURCE_DIR) if os.path.isdir(os.path.join(SOURCE_DIR, d))]
print(f"Found {len(classes)} classes")

for cls in classes:
    src_folder = os.path.join(SOURCE_DIR, cls)
    train_folder = os.path.join(train_dir, cls)
    valid_folder = os.path.join(valid_dir, cls)

    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(valid_folder, exist_ok=True)

    images = [f for f in os.listdir(src_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    random.shuffle(images)

    split_idx = int(len(images) * TRAIN_RATIO)
    train_imgs = images[:split_idx]
    valid_imgs = images[split_idx:]

    for img in train_imgs:
        shutil.copy(os.path.join(src_folder, img), os.path.join(train_folder, img))

    for img in valid_imgs:
        shutil.copy(os.path.join(src_folder, img), os.path.join(valid_folder, img))

    print(f"{cls}: {len(train_imgs)} train, {len(valid_imgs)} valid")

print("✅ Dataset successfully split into train/valid folders!")
