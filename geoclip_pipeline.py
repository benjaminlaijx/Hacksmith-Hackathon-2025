import json
import torch
import os
from pathlib import Path
from PIL import Image
from geoclip.model import GeoCLIP

# 1. Load GeoCLIP model
model = GeoCLIP(from_pretrained=True)

# Get the directory of instascraper output
instascraper_dir = Path("instascraper/output")

# 2. Build a reference dataset of GPS embeddings
# Example: known locations with lat/lon
reference_coords = [
    {"lat": 40.712776, "lon": -74.005974},   # New York
    {"lat": 34.052235, "lon": -118.243683},  # Los Angeles
    {"lat": 51.507351, "lon": -0.127758},    # London
]

def predict_latlon(image_path, top_k=1):
    """
    Use GeoCLIP to predict GPS coordinates from an image.
    """
    # The image_path comes as "output/images/filename.jpg"
    # We need to prepend "instascraper/" to make it "instascraper/output/images/filename.jpg"
    if isinstance(image_path, str):
        if image_path.startswith("output/"):
            full_path = Path("instascraper") / image_path
        elif image_path.startswith("instascraper/"):
            full_path = Path(image_path)
        else:
            full_path = Path(image_path)
    else:
        full_path = Path(image_path)
    
    if not full_path.exists():
        raise FileNotFoundError(f"Image not found: {full_path}")
    
    top_pred_gps, top_pred_prob = model.predict(str(full_path), top_k=top_k)
    
    # Return the top prediction
    lat, lon = top_pred_gps[0].tolist()
    return {"lat": float(lat), "lon": float(lon)}

def process_json(json_path, output_path="output.json"):
    """
    Fill missing lat/lon in JSON using GeoCLIP predictions.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        if entry.get("location") is None or (isinstance(entry.get("location"), dict) and entry["location"].get("lat") is None):
            # Get image paths
            image_paths = entry.get("local_image_paths")
            if image_paths:
                try:
                    prediction = predict_latlon(image_paths[0])
                    entry["location"] = prediction
                    print(f"[OK] Predicted location for {entry['post_url']}: {prediction}")
                except Exception as e:
                    print(f"[ERROR] Error processing {entry['post_url']}: {str(e)}")
                    # Keep location as is if prediction fails
                    if entry.get("location") is None:
                        entry["location"] = {"lat": None, "lon": None}

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nUpdated JSON saved to {output_path}")

if __name__ == "__main__":
    # Use the posts.json from instascraper output
    posts_json = "instascraper/output/json/posts.json"
    output_json = "output.json"
    
    process_json(posts_json, output_json)






