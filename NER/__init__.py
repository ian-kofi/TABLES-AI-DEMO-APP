# NER/__init__.py
from gliner import GLiNER

# Define the model globally
model = None

def load_model():
    global model
    if model is None:
        print("Loading model for the first time...")
        model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")
        model.eval()
    else:
        print("Model already loaded.")