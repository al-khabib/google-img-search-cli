# save images in a format easy to query

# Collection - like a table in a relational database

import weaviate
import os
import base64
from weaviate.classes.config import Property, DataType
from weaviate.collections.classes.config import Configure


def encode_img(image_path: str):
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8') # encode the image data as a base64 string

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
                    'image': encode_img(image_path) # image_path is just a text, we need to encode the actual image data as a blob first
                }
            )

        print(f"Indexed {img_collection.aggregate.over_all(total_count=True).total_count} images")    

    finally:
        # client has to be closed after use in vector db all the time, 
        client.close()

if __name__ == "__main__":
    main()