# save images in a format easy to query

# Collection - like a table in a relational database

import weaviate
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
    except Exception as e:
        print(f"Collection already exists: {e}")    