import os

content = """

add("Projects", "In your Fashion Recommendation System, how exactly did you extract features from images, and why did you use a pre-trained CNN?", \"\"\"
* **Feature Extraction Process**:
  1. **Preprocessing**: Images were loaded and resized to the required input size of the model (e.g., 224x224 for VGG16/ResNet). They were then converted to arrays and preprocessed (e.g., zero-centering color channels) using the model's specific preprocessing function (`preprocess_input`).
  2. **Model Architecture**: I loaded a pre-trained CNN (like VGG16 or ResNet50) excluding the top classification layers (`include_top=False`). 
  3. **Pooling**: I applied Global Average Pooling (or Global Max Pooling) to the final convolutional feature map to flatten it into a 1D vector (e.g., a 2048-d or 4096-d vector).
  4. **Normalization**: The extracted feature vector was normalized (e.g., L2 normalization) so that the scale of the features wouldn't affect the similarity calculations.
* **Why Pre-trained (Transfer Learning)**: 
  - Training a deep CNN from scratch requires a massive dataset (millions of images) and significant compute power. 
  - Pre-trained models (trained on ImageNet) have already learned excellent hierarchical visual features (edges, textures, shapes, object parts) that generalize perfectly to clothing and fashion items.
\"\"\")

add("Projects", "How did you measure the similarity between the input image and the dataset images in your fashion recommender?", \"\"\"
* **Cosine Similarity**: I used Cosine Similarity to compare the feature vector of the input image against the feature vectors of all images in the database.
* **Why Cosine?**: Cosine similarity measures the cosine of the angle between two vectors in a multi-dimensional space. It is highly effective for high-dimensional feature vectors because it cares about the *direction* (the pattern of features) rather than the *magnitude* (overall intensity). 
* **Process**: 
  1. The input image is converted into a normalized feature vector.
  2. The dot product is calculated between the input vector and all database vectors.
  3. The database images are sorted in descending order of their similarity scores (where 1 is identical and 0 is completely orthogonal).
  4. The top N images are returned as recommendations.
* **Alternatives**: Euclidean distance (L2 distance) could also be used, but Cosine is generally preferred for normalized deep learning embeddings as it handles the high-dimensional space more robustly.
\"\"\")

add("Projects", "If you wanted to scale or improve the accuracy of your fashion recommendation system, what techniques would you apply?", \"\"\"
* **Accuracy Improvements**:
  1. **Fine-tuning**: Unfreeze the last few convolutional blocks of the pre-trained model and train it on the fashion dataset using a Triplet Loss or Contrastive Loss function to explicitly teach the model what 'similar' clothing looks like.
  2. **Object Detection / Segmentation**: Use YOLO or Mask R-CNN to detect and crop just the clothing item (ignoring the background, model's face, or text), passing only the cropped clothing to the feature extractor.
  3. **Multi-modal embeddings**: Combine the image features with text features (clothing description, brand, color text) using a model like CLIP.
* **Scaling Improvements**:
  1. **Vector Database**: Instead of doing a linear scan using basic Cosine Similarity, I would use a Vector Database like Qdrant, Pinecone, or FAISS (Facebook AI Similarity Search) which uses Approximate Nearest Neighbor (ANN) algorithms (like HNSW) to reduce search time.
  2. **Caching**: Cache frequent search queries using Redis.
\"\"\")
"""

with open('data/db_projects.py', 'a', encoding='utf-8') as f:
    f.write(content)
