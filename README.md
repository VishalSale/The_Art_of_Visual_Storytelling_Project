# The-Art-of-Visual-Storytelling_Apr_2024/Vishal Sale

### Object Detection and Story Generation with OpenAI

This project utilizes object detection techniques and natural language generation to create stories based on detected objects in images. The process involves detecting objects in images, generating sentences describing the objects, and crafting compelling stories using AI-powered text generation.

#### Setup Instructions

1. **Clone the Repository:**
   Clone the GitHub repository to your local machine.

   ```bash
   git clone https://github.com/VishalSale/The_Art_of_Visual_Storytelling_Project.git
   ```

2. **Install Dependencies:**
   Navigate to the project directory and install the required Python dependencies.

   ```bash
   cd your-repo
   pip install -r requirements.txt
   ```

3. **Set Up OpenAI API Key:**
   Obtain an API key from OpenAI and set it as an environment variable in a `.env` file. Rename the `.env.example` file to `.env` and replace `API_KEY` with your actual API key.

4. **Run the Code:**
   Execute the Python script `main.py` to detect objects in images and generate stories.

   ```bash
   python main.py
   ```

5. **Provide Image Inputs:**
   When prompted, choose whether to provide local images or image URLs. Enter the path or URL for each image you want to process.

6. **View Output:**
   The script will display detected objects in each image, along with the generated sentences describing them. Additionally, it will craft a story based on the detected objects and their surroundings.

7. **Using a Different Model for Object Detection:**
   If you want to use a different model or your own model for object detection, you can easily do so. First, import the necessary modules:

   ```python
   from transformers import DetrFeatureExtractor, DetrForObjectDetection
   ```

   Then, initialize the feature extractor and model, and initialize the object detector with them instead of the default one. For example, if you want to use ResNet-101 as your backbone:

   ```python
   # Initialize another model and feature extractor
   feature_extractor = DetrFeatureExtractor.from_pretrained('facebook/detr-resnet-101')
   model = DetrForObjectDetection.from_pretrained('facebook/detr-resnet-101')

   # Initialize the object detection pipeline
   object_detector = pipeline("object-detection", model=model, feature_extractor=feature_extractor)
   ```

#### Notes

- Make sure you have a stable internet connection to download images from URLs.
- Ensure that the images you provide are clear and contain recognizable objects for accurate detection.
- Adjust the temperature and maximum tokens parameters in the script for different storytelling outputs.

Follow these steps to execute the code and explore the fascinating world of object detection and storytelling with AI!
