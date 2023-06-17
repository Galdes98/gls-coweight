import csv
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import os
import glob

def extract_data_from_csv(file_path):
    data = []
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header row if present
        for row in reader:
            image_dir = r"{}".format(row[4])  # Assuming the image path is in the fifth column
            #print(r"{}".format(row[4]))
            image_dir = os.path.join(image_dir, r"*.png")
            image_paths = glob.glob(image_dir)
            #print(image_dir)
            for image_path in image_paths:
                print(image_path)
                image = Image.open(image_path)
                # Resize the image to match the input size of the model
                image = image.resize((224, 224))
                # Convert the image to a numpy array
                image_array = keras.preprocessing.image.img_to_array(image)
                # Normalize the image
                image_array /= 255.0
                label = int(row[1])  # Assuming the label is in the second column
                data.append((image_array, label))
    return data

# Example usage
csv_file_path = '.\cowData.csv'
data = extract_data_from_csv(csv_file_path)