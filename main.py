import weaviate

from indexer import encode_img

def main():
    client = weaviate.connect_to_local()
    query_img_path = './images-to-test-search/zebra_test.jpeg'

    try:
        image_collection = client.collections.get("Images")

        response = image_collection.query.near_image(
            near_image=encode_img(query_img_path),
            limit=1,
            return_properties=['filename']
        )
        print('\n Most similar image: -- ')
        most_similar_image = response.objects[0]
        print(f" --- {most_similar_image.properties['filename']} --- is the most similar image.")
    finally:
        client.close()

if __name__ == "__main__":
    main()