import instaloader
import json
import os
import shutil
import glob
from datetime import datetime
from itertools import takewhile, dropwhile, islice

# --- CONFIGURATION ---
TARGET_USERNAME = "injeffsbelly"  # The account to scrape
ROOT_OUTPUT_FOLDER = "output" # Main folder
IMAGES_FOLDER = "images"                # Subfolder for JPGs
JSON_FOLDER = "json"                    # Subfolder for JSONs
OUTPUT_FILENAME = "posts.json"
TEMP_FOLDER = "temp" # A temporary holding area
# ---------------------

final_img_path = os.path.join(ROOT_OUTPUT_FOLDER, IMAGES_FOLDER)
final_json_path = os.path.join(ROOT_OUTPUT_FOLDER, JSON_FOLDER)
output_file_path = os.path.join(final_json_path, OUTPUT_FILENAME)
temp_path = TEMP_FOLDER

for p in [final_img_path, final_json_path, temp_path]:
    os.makedirs(p, exist_ok=True)

# 2. Configure Instaloader
L = instaloader.Instaloader(
    download_pictures=True,
    download_videos=False, 
    download_video_thumbnails=False,
    download_geotags=False, 
    download_comments=False, 
    save_metadata=False,
    compress_json=False
)

# L.login("YOUR_USER", "YOUR_PASS") # Recommended

print(f"Starting reliable archive for: {TARGET_USERNAME}")
posts = islice(instaloader.Profile.from_username(L.context, TARGET_USERNAME).get_posts(), 50)

# SINCE = datetime(2025, 9, 1)
# UNTIL = datetime(2025, 12, 6)

# for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):

all_posts_data = []
for post in posts:
    # A. Clean the temp folder to ensure it's empty
    for file in os.listdir(temp_path):
        os.remove(os.path.join(temp_path, file))

    # B. Download into the TEMP folder    
    try:
        did_download = L.download_post(post, target=temp_path)
    except Exception as e:
        print(f"[!] Error downloading {post.shortcode}: {e}")
        continue
    
    # C. Find the downloaded image file(s) in the temp folder
    downloaded_files = glob.glob(os.path.join(temp_path, "*"))
    
    # Filter for media files only (ignore potential leftover metadata if settings changed)
    image_files = [f for f in downloaded_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    # If list is empty (meaning it was a video post), SKIP IT.
    if not image_files:
        continue

    saved_paths = []

    # D. Loop through ALL files found (Handling Sidecars)
    saved_paths = []
    for index, source_file in enumerate(sorted(image_files)):
        # 1. Get extension (.jpg)
        extension = os.path.splitext(source_file)[1]
        
        # 2. Generate unique name: Shortcode_1.jpg, Shortcode_2.jpg...
        new_filename = f"{post.shortcode}_{index + 1}{extension}"
        destination_path = os.path.join(final_img_path, new_filename)
        
        # 3. Move file
        shutil.move(source_file, destination_path)
        
        # 4. Add to list
        relative_path = os.path.join(final_img_path, new_filename)
        saved_paths.append(os.path.join("instascraper", relative_path))


    # E. Create JSON with the VERIFIED path
    # Get location data
    location = (None, None)
    if post.location:
        location = (post.location.lat, post.location.lng)

    post_data = {
        "post_url": f"https://www.instagram.com/p/{post.shortcode}/",
        "local_image_paths": saved_paths,
        "date": str(post.date_local),
        "caption": post.caption if post.caption else "", # The main text
        "location": {
            "lat": location[0],
            "lon": location[1],
        }
    }

    all_posts_data.append(post_data)

    # 8. Save the Master JSON File immediately (Overwrites with new data included)
    # This prevents data loss if the script crashes halfway through
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(all_posts_data, f, indent=4, ensure_ascii=False)

if os.path.exists(temp_path):
    shutil.rmtree(temp_path)
    print("[-] Temp folder cleaned up.")