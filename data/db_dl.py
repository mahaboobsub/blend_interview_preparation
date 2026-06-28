# db_dl.py - COMPREHENSIVE Deep Learning & Computer Vision
# Covers: Neural Network fundamentals, CNN, RNN/LSTM, Transformers, ViT, VGG16, Autoencoders/GANs

DL_QUESTIONS = []

def add(sub, q, a, is_coding=False, code_python=""):
    DL_QUESTIONS.append({
        "category": "dl_cv",
        "subcategory": sub,
        "question": q,
        "answer": a.strip(),
        "is_coding": is_coding,
        "code_sql": "",
        "code_java": "",
        "code_python": code_python.strip()
    })

# ═══════════════════════════════════════════════════════════════
# NEURAL NETWORK FUNDAMENTALS (15)
# ═══════════════════════════════════════════════════════════════

add("NN Fundamentals", "Compare MLP, CNN, and RNN architectures.", """
* **MLP (Multi-Layer Perceptron)**: Fully connected feedforward network. Every neuron connects to all neurons in next layer. Use for tabular data. Universal Approximation Theorem.
* **CNN (Convolutional Neural Network)**: Uses convolutional filters for local pattern detection, pooling layers for dimensionality reduction, weight sharing to reduce parameters. Use for images, spatial data.
* **RNN (Recurrent Neural Network)**: Feeds output back into itself, maintaining hidden state across time steps. Use for sequential data, time-series, text.
""")

add("NN Fundamentals", "Why were LSTMs and GRUs developed? Structural differences.", """
* **Problem**: Vanilla RNNs suffer from vanishing gradient — gradients shrink to zero over long sequences, preventing learning of long-range dependencies.
* **LSTM (Long Short-Term Memory)**: Introduces cell state + 3 gates:
  - Forget gate (fₜ): Decides what to discard from cell state.
  - Input gate (iₜ): Decides what new info to store.
  - Output gate (oₜ): Decides what to output.
* **GRU (Gated Recurrent Unit)**: Simplified LSTM with 2 gates:
  - Update gate (zₜ): Combines forget + input gates.
  - Reset gate (rₜ): Controls how much past info to discard.
* **GRU**: Fewer parameters, faster training. LSTM: Better for very long sequences.
""")

add("NN Fundamentals", "Explain activation functions: ReLU, GELU, Sigmoid, Softmax.", """
Activation functions introduce non-linearity:
* **ReLU**: f(x) = max(0, x). Fast, avoids vanishing gradient. Problem: dying ReLU (negative inputs always output 0).
* **Leaky ReLU**: f(x) = x if x>0, αx otherwise. Fixes dying ReLU.
* **GELU**: f(x) = x·Φ(x). Smooth, probabilistic activation. Preferred in Transformers because it provides better gradient flow near zero.
* **Sigmoid**: f(x) = 1/(1+e⁻ˣ). Outputs [0,1]. Used for binary output. Problem: vanishing gradient at extremes.
* **Tanh**: f(x) = (eˣ-e⁻ˣ)/(eˣ+e⁻ˣ). Outputs [-1,1]. Zero-centered. Used in LSTM gates.
* **Softmax**: Normalizes logits to probability distribution summing to 1. Used for multi-class classification output layer.
""")

add("NN Fundamentals", "Explain SGD vs Adam optimizer. When to use which?", """
* **SGD (Stochastic Gradient Descent)**: Updates weights using gradient of single/mini-batch. Simple but slow, can get stuck in local minima.
  - With momentum: Accelerates in consistent gradient direction.
* **Adam (Adaptive Moment Estimation)**: Combines momentum (1st moment: mean of gradients) and RMSprop (2nd moment: uncentered variance). Adaptive learning rates per parameter.
  - Default choice for most deep learning tasks.
  - Converges faster than SGD.
* **When to use SGD**: When you want better generalization (SGD + momentum often generalizes better than Adam for CNNs on vision tasks).
* **When to use Adam**: Default for NLP, Transformers, quick prototyping, tasks where convergence speed matters.
""")

add("NN Fundamentals", "What is backpropagation? How does it work?", """
Backpropagation computes gradients of the loss function w.r.t. each weight using the chain rule, enabling gradient descent to update weights.
* **Forward pass**: Compute predictions layer by layer.
* **Loss computation**: Compare predictions to ground truth.
* **Backward pass**: Propagate error gradients from output to input, computing ∂L/∂w for each weight.
* **Weight update**: w = w - α × ∂L/∂w (gradient descent).
* **Chain rule**: For deep networks, gradients multiply through layers: ∂L/∂w₁ = ∂L/∂a₃ × ∂a₃/∂a₂ × ∂a₂/∂w₁.
* **Vanishing gradient**: If derivatives < 1 at each layer, gradients shrink exponentially. Solved by ReLU, skip connections, LSTM gates.
""")

add("NN Fundamentals", "What is batch normalization? Why is it used?", """
Batch normalization normalizes the inputs of each layer to have zero mean and unit variance within each mini-batch.
* **How it works**: For each feature in a layer: x̂ = (x - μ_batch)/√(σ²_batch + ε), then scale and shift: y = γx̂ + β (learnable parameters).
* **Benefits**:
  1. Stabilizes training (reduces internal covariate shift).
  2. Allows higher learning rates → faster convergence.
  3. Acts as mild regularization.
  4. Reduces sensitivity to weight initialization.
* **Layer Normalization**: Normalizes across features (not batch). Used in Transformers because batch size may vary.
""")

add("NN Fundamentals", "What is dropout? How does it prevent overfitting?", """
Dropout randomly sets a fraction (p) of neurons to zero during training.
* **How it works**: At each training step, each neuron has probability p of being "dropped." At inference, all neurons are active but outputs are scaled by (1-p).
* **Why it works**: Forces the network to learn redundant representations. No neuron can rely on specific other neurons → more robust features.
* **Typical rates**: p = 0.2-0.5 for hidden layers.
* **Alternatives**: DropConnect (drops weights), Spatial Dropout (drops entire feature maps for CNNs).
""")

add("NN Fundamentals", "What is transfer learning? When and how to use it?", """
Transfer learning uses a model pre-trained on a large dataset as the starting point for a new task.
* **How to use**:
  1. **Feature extraction**: Freeze pre-trained layers, replace only the final classification head. Train only the new head on your data.
  2. **Fine-tuning**: Unfreeze some/all pre-trained layers and train with a small learning rate. Updates pre-trained weights for domain adaptation.
* **When to use**: Limited labeled data, similar domain to pre-training data.
* **Common pre-trained models**: ResNet, VGG16 (vision), BERT, GPT (NLP), CLIP (vision+language).
""")

# ═══════════════════════════════════════════════════════════════
# TRANSFORMERS & ATTENTION (10)
# ═══════════════════════════════════════════════════════════════

add("Transformers", "Describe the core Transformer architecture.", """
The Transformer (Vaswani et al., 2017) eliminates recurrence, using Self-Attention for parallel processing.
* **Components**:
  1. **Input Embedding + Positional Encoding**: Tokens → vectors + position info.
  2. **Multi-Head Self-Attention**: Learns contextual relationships between ALL tokens simultaneously.
  3. **Add & Norm**: Residual connections + Layer Normalization for stable gradient flow.
  4. **Feed-Forward Network**: Two linear layers with activation, applied per position.
* **Encoder**: Bidirectional attention (sees all tokens). Used for understanding.
* **Decoder**: Causal (masked) attention (sees only past tokens). Used for generation.
""")

add("Transformers", "Explain the Self-Attention mechanism mathematically.", """
Self-Attention computes a weighted representation of all tokens based on their relevance to each other:
1. Create Query (Q), Key (K), Value (V) from input: Q = XW_Q, K = XW_K, V = XW_V.
2. Compute attention scores: Scores = QK^T (dot product of every query with every key).
3. Scale: Scores / √d_k (prevents vanishing gradients in softmax).
4. Apply softmax: Weights = softmax(Scores/√d_k) → attention probabilities.
5. Weighted output: Output = Weights × V.
* **Multi-Head**: Run h parallel attention heads with different projection matrices, concatenate outputs. Allows model to attend to different aspects simultaneously.
""")

add("Transformers", "Why does Self-Attention have O(N²) complexity? How to mitigate?", """
* **Cause**: The QK^T matrix multiplication produces an N×N attention matrix for sequence length N. Both compute and memory scale quadratically.
* **Implications**: Processing long contexts (128K+ tokens) becomes extremely expensive.
* **Mitigations**:
  1. **FlashAttention**: Optimizes GPU memory access (SRAM vs HBM) without changing the math.
  2. **Sliding Window Attention** (Mistral, Longformer): Each token only attends to local neighbors.
  3. **Linear Attention**: Approximates attention with kernel functions, achieving O(N) complexity.
  4. **State Space Models** (Mamba, S4): Replace attention with recurrence-like mechanism. O(N) scaling.
  5. **KV-Cache**: At inference, caches computed K,V matrices to avoid recomputation.
""")

add("Transformers", "Compare Encoder-Only (BERT), Decoder-Only (GPT), and Encoder-Decoder (T5).", """
* **Encoder-Only (BERT)**:
  - Bidirectional self-attention (sees full context).
  - Pre-trained with Masked Language Modeling (MLM) + Next Sentence Prediction.
  - Use: Classification, NER, sentiment analysis, embeddings.
* **Decoder-Only (GPT)**:
  - Causal (left-to-right) masked attention.
  - Pre-trained with next-token prediction.
  - Use: Text generation, chat, code generation, reasoning.
* **Encoder-Decoder (T5, BART)**:
  - Encoder processes input, decoder generates output with cross-attention.
  - Use: Translation, summarization, question answering.
""")

add("Transformers", "What are positional encodings? Sinusoidal vs RoPE.", """
Since Transformers process all tokens in parallel (no recurrence), they need positional information.
* **Sinusoidal Positional Encoding**: Fixed sin/cos waves of varying frequencies added to embeddings. Provides absolute position.
  - PE(pos, 2i) = sin(pos/10000^(2i/d))
  - PE(pos, 2i+1) = cos(pos/10000^(2i/d))
* **RoPE (Rotary Position Embedding)**: Multiplies Q and K vectors by rotation matrices encoding relative position. Encodes relative distance between tokens.
  - Advantage: Better generalization to longer sequences than seen during training.
  - Used in: LLaMA, Mistral, GPT-NeoX.
""")

# ═══════════════════════════════════════════════════════════════
# CNN & COMPUTER VISION (10)
# ═══════════════════════════════════════════════════════════════

add("CNN & Vision", "Explain the architecture of a CNN. What are convolutions, pooling, and stride?", """
A CNN processes spatial data through layers:
* **Convolutional Layer**: Slides learnable filters (kernels) across input, computing dot products. Detects local patterns (edges, textures). Parameters: filter size, stride, padding.
* **Stride**: Step size of the filter. Stride 1 = slides by 1 pixel. Stride 2 = halves spatial dimensions.
* **Padding**: Adding zeros around input edges. 'Same' padding preserves dimensions. 'Valid' = no padding.
* **Pooling Layer**: Downsamples feature maps. Max pooling (takes max value in window), Average pooling. Reduces computation and provides translation invariance.
* **Fully Connected Layer**: Flattened features → classification.
* **Output size**: (W - F + 2P)/S + 1, where W=input, F=filter, P=padding, S=stride.
""")

add("CNN & Vision", "Explain ResNet architecture and skip connections.", """
* **Problem**: Very deep networks (>20 layers) suffer from degradation — accuracy drops as depth increases, not due to overfitting but due to optimization difficulty.
* **Skip/Residual Connections**: Instead of learning H(x), the network learns the residual F(x) = H(x) - x, then computes H(x) = F(x) + x.
  - The identity shortcut allows gradients to flow directly through skip connections during backpropagation.
  - Enables training of extremely deep networks (ResNet-152).
* **Residual Block**: Input x → Conv → BN → ReLU → Conv → BN → Add x → ReLU.
* **Impact**: Solved degradation problem. Foundation for most modern vision architectures.
""")

add("CNN & Vision", "What is VGG16? Explain its architecture and use in feature extraction.", """
VGG16 is a 16-layer deep CNN developed by the Visual Geometry Group at Oxford (2014).
* **Architecture**: 13 conv layers + 3 FC layers. Uses only 3×3 convolution filters throughout.
  - Input: 224×224×3 RGB image.
  - 5 blocks of conv layers with increasing filters: 64 → 128 → 256 → 512 → 512.
  - Max pooling 2×2 after each block.
  - 3 FC layers: 4096 → 4096 → 1000 (ImageNet classes).
  - Total parameters: ~138 million.
* **For transfer learning**: Remove FC layers, use conv blocks as feature extractor. Add custom classifier head for your task.
* **Used in**: Fashion recommendation systems, image similarity, style transfer, medical imaging.
""")

add("CNN & Vision", "Explain U-Net architecture and its use in image segmentation.", """
* **Architecture**: Symmetric encoder-decoder with skip connections.
  - **Encoder (Contracting path)**: Conv + Pool blocks. Captures what is in the image.
  - **Decoder (Expanding path)**: UpConv + Conv blocks. Localizes where things are.
  - **Skip connections**: Copy features from encoder to corresponding decoder level. Preserves fine spatial details lost during downsampling.
* **Use case**: Pixel-level semantic segmentation. Originally designed for biomedical image segmentation.
* **Why skip connections matter**: Without them, the decoder would have to reconstruct spatial details from a compressed bottleneck. Skip connections directly provide high-resolution features for precise boundary delineation.
""")

add("CNN & Vision", "What is Vision Transformer (ViT)? How does it compare to CNNs?", """
* **ViT Architecture**:
  1. Split image into fixed-size patches (e.g., 16×16).
  2. Flatten patches and linearly project into embeddings (like word tokens).
  3. Add positional embeddings.
  4. Feed through standard Transformer Encoder blocks.
  5. Classification via MLP head on [CLS] token.
* **ViT vs CNN**:
  - **Inductive bias**: CNNs have locality and translation equivariance built in. ViT must learn spatial relationships from scratch.
  - **Data requirements**: ViT needs massive datasets (JFT-300M) to outperform CNNs. On small datasets, CNNs win.
  - **Global context**: ViT captures long-range dependencies from layer 1 (global self-attention). CNNs only get global context after many layers.
""")

# ═══════════════════════════════════════════════════════════════
# GENERATIVE MODELS (5)
# ═══════════════════════════════════════════════════════════════

add("Generative Models", "Compare Autoencoders, VAEs, and GANs.", """
* **Autoencoder**: Encoder → latent code z → Decoder. Learns compressed representation. Use: denoising, anomaly detection, dimensionality reduction.
* **VAE (Variational Autoencoder)**: Probabilistic — encoder outputs μ and σ of a distribution. Samples z ~ N(μ, σ²). Uses reparameterization trick for backprop. Loss = reconstruction + KL divergence. Use: generating new samples.
* **GAN (Generative Adversarial Network)**: Two networks compete:
  - Generator: Creates fake data from random noise.
  - Discriminator: Distinguishes real from fake.
  - Training: Adversarial min-max game until Generator fools Discriminator.
  Use: High-quality image synthesis (StyleGAN, DALL-E predecessor).
""")

add("Generative Models", "What is Fine-Tuning vs Prompt Engineering? When to use which?", """
* **Prompt Engineering**: Designing input prompts to guide LLM behavior. No model training needed.
  - Techniques: Zero-shot, few-shot, Chain-of-Thought, system prompts.
  - Pros: Instant, zero cost, no ML expertise needed.
  - Use: General tasks, prototyping, format-controlled outputs.
* **Fine-Tuning**: Training a pre-trained model on custom data, updating weights.
  - Methods: Full fine-tuning, LoRA (Low-Rank Adaptation), QLoRA.
  - Pros: Higher consistency, domain specialization, reduces prompt length.
  - Use: Brand voice, domain-specific language, strict output formats, reducing inference cost.
* **Decision**: Start with prompt engineering. Fine-tune when prompt engineering fails to meet quality requirements.
""")

add("Generative Models", "What are diffusion models? How do they generate images?", """
Diffusion models generate data by learning to reverse a gradual noising process.
* **Forward process**: Gradually add Gaussian noise to clean data over T steps until it becomes pure noise.
* **Reverse process (learned)**: Train a neural network (typically a U-Net) to predict and remove noise at each step, going from pure noise → clean image.
* **Training**: Minimize MSE between predicted and actual noise at each step.
* **Inference**: Start from random noise, iteratively denoise T steps.
* **Examples**: Stable Diffusion, DALL-E 2, Midjourney.
* **Advantages over GANs**: More stable training (no mode collapse), better diversity, easier to control.
""")
