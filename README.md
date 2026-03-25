# Google Image Search CLI

A terminal-based reverse image search engine that demonstrates how modern image search works under the hood — using vector embeddings and a vector database instead of metadata or keyword matching.

Built as a learning project to explore **vector databases**, **neural image embeddings**, and **semantic similarity search**.

---

## How It Works

1. **Indexing:** Each image is converted into a 2048-dimensional vector using a ResNet50 CNN (via `img2vec-neural`), then stored in Weaviate alongside its filename and raw bytes.
2. **Searching:** A query image goes through the same vectorization pipeline. Weaviate performs a nearest-neighbor search in the embedding space and returns the most visually similar image.

```
Query Image → ResNet50 Encoder → 2048-D Vector → Weaviate near_image Search → Similar Image
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Vector Database | [Weaviate](https://weaviate.io/) v1.30.0 |
| Image Vectorizer | img2vec-neural (ResNet50) |
| Python Client | weaviate-client v4.20.4 |
| Containerization | Docker & Docker Compose |
| Runtime | Python 3.11 |

---

## Project Structure

```
google-img-search-cli/
├── docker-compose.yml          # Weaviate + img2vec-neural services
├── indexer.py                  # Indexes images into the vector database
├── main.py                     # Queries the database for similar images
├── images-to-index/            # Images to be indexed
│   ├── eagle.jpeg
│   ├── panda.jpeg
│   ├── tiger.jpeg
│   └── zebra.jpeg
└── images-to-test-search/      # Query images for similarity search
    └── zebra_test.jpeg
```

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- Python 3.11+

---

## Setup & Usage

### 1. Start the vector database

```bash
docker-compose up -d
```

This starts two services:
- **Weaviate** on `localhost:8080` — the vector database
- **img2vec-neural** — the ResNet50 inference server used for vectorization

Wait ~10 seconds for both services to be ready.

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install weaviate-client
```

### 3. Index your images

Place images inside the `images-to-index/` directory, then run:

```bash
python indexer.py
```

Output:
```
Total images indexed: 4
```

Each image is encoded as base64, vectorized by the ResNet50 model, and stored in a Weaviate collection named `Images`.

### 4. Search for similar images

Place a query image at `images-to-test-search/zebra_test.jpeg`, then run:

```bash
python main.py
```

Output:
```
Most similar image: zebra.jpeg
```

### 5. Tear down

```bash
docker-compose down
```

---

## Weaviate Collection Schema

**Collection:** `Images`

| Property | Type | Description |
|----------|------|-------------|
| `filename` | TEXT | Original filename of the image |
| `image` | BLOB | Base64-encoded image data |

Vectorization is applied to the `image` field using the `img2vec-neural` module, producing 2048-dimensional ResNet50 feature vectors.

---

## Docker Services

```yaml
Weaviate:
  port: 8080 (HTTP), 50051 (gRPC)
  vectorizer: img2vec-neural
  auth: anonymous (no credentials required)

img2vec-neural:
  model: ResNet50
  compute: CPU (CUDA disabled)
```

---

## Key Concepts Demonstrated

- **Vector embeddings** — representing images as points in high-dimensional space where semantic similarity maps to geometric proximity
- **Nearest-neighbor search** — finding the closest vector to a query without scanning every record
- **Multimodal vectorization** — using a CNN to extract visual features for search
- **Weaviate `near_image` queries** — searching a vector database using an image as the query

---

## Limitations

- Image paths and the query image are hardcoded in the scripts — modify them directly to use different files
- Only the top-1 result is returned by default
- Vectorization runs on CPU; large datasets will be slow
- No authentication configured (suitable for local development only)
