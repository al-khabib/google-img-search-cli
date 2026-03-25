# save images in a format easy to query

# Collection - like a table in a relational database

import weaviate
import os
from weaviate.classes.config import Property, DataType
from weaviate.collections.classes.config import Configure


def main():
    client = weaviate.connect_to_local()

    # create Images collection
    try:
        client.collections.create(
            name="Images",
            properties=[
                Property(name='filename', data_type=DataType.TEXT),
                Property(name='image', data_type=DataType.BLOB)       
            ],
            #    tell the model which property to convert to vector
            vector_config=Configure.Vectors.img2vec_neural(image_fields=['image'])
        )

        # get the images collection
        img_collection = client.collections.get("Images")

        image_folder = './images-to-index'

        # look through the images in the image folder 
        for filename in os.listdir(image_folder):
            # get image path
            image_path = os.path.join(image_folder, filename)

            # insert this image into the collection
            img_collection.data.insert(
                {
                    'filename': filename,
                    'image': image_path # image_path is just a text, we need to encode the actual image data as a blob first
                }
            )

    except Exception as e:
        print(f"Collection already exists: {e}")    