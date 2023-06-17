import csv
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import os
import glob
import numpy as np

def create_model():
    model = keras.Sequential([
        keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 4)),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Conv2D(128, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model

def extract_data_from_csv(file_path):
    data = []
    targets = []
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header row if present
        for row in reader:
            image_dir = r"{}".format(row[6])  # Assuming the image path is in the fifth column
            image_dir = os.path.join(image_dir, r"*.png")
            image_paths = glob.glob(image_dir)
            for image_path in image_paths:
                image = Image.open(image_path)
                image = image.resize((224, 224))
                image_array = keras.utils.img_to_array(image)
                image_array /= 255.0
                # sex = row[1]  # Assuming the sex label is in the second column
                # age = int(row[2])  # Assuming the age label is in the third column
                # breed = row[3]  # Assuming the breed label is in the fourth column
                # color = row[4]  # Assuming the color label is in the fifth column
                weight = int(row[5])  # Assuming the weight label is in the seventh column
                #labels = [sex, age, breed, color, weight]
                data.append((image_array, weight))
    return data

# Example usage

csv_file_path = '.\cowData.csv'
data = extract_data_from_csv(csv_file_path)

#Split the data into training and validation sets
train_data = data[:int(len(data)*0.8)]
#train_targets = targets[:int(len(targets)*0.8)]
val_data = data[int(len(data)*0.8):]
#val_targets = targets[int(len(targets)*0.8):]

# Create the model
model = create_model()

# Train the model
batch_size = 32
epochs = 10

train_dataset = tf.data.Dataset.from_generator(lambda: train_data,
                                               output_types=(tf.float32, tf.int32),
                                               output_shapes=((224, 224, 4), ()))

train_dataset = train_dataset.shuffle(buffer_size=len(train_data))
train_dataset = train_dataset.batch(batch_size)

val_dataset = tf.data.Dataset.from_generator(lambda: val_data,
                                             output_types=(tf.float32, tf.int32),
                                             output_shapes=((224, 224, 4), ()))
val_dataset = val_dataset.batch(batch_size)

model.fit(train_dataset, epochs=epochs, validation_data=val_dataset)