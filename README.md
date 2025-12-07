Hacksmith v6.0
Group: SecureStack
Tool: Geol0c4t

Geol0c4t ("Geolocate") is an OSINT tool for building a geographic visualisation of the locations of a person's social media posts.

1. The user must input a social media account name (currently only supports Instagram)
2. Geol0c4t will collate all social media posts that contain images.
3. Geol0c4t will attempt to determine each post's location through various image geolocation techniques (neural-network, EXIF metadata, reverse image search, etc)
4. Finally, Geol0c4t renders a geographic visualisation of the post locations on an interactive world map. The user can filter posts based on keyword search and timeline slider.

# Set up
Two virtual environments are required
python3.12 (geoclip_venv)
- torch
- geoclip

python3.14 (venv)
- instaloader
- argparse
- folium

run main.py on venv

# Project structure
Geol0c4t/
├── instascraper/           # Python module that scrapes social media posts
├──── output/
├────── json/                   # caches data on each social media post
├────── images/                 # caches social media post images downloaded by the tool
├── geovisualise/           # Python module that renders the geographic visualisation

# JSON schema
At each step, our tool works with a JSON file storing data of the person's social media posts. Each post is an object with the following fields:
- Post URL
- Image filepath(s) (photos are cached inside `.\scraped_images`)
- Post caption
- Datetime of post
- Location (determined via various image geolocation techniques)

Example:
[
    {
        "post_url": "https://www.instagram.com/p/ABC123xyz/",
        "local_image_paths": [
            ".\\scraped_images\\post1_img1.jpg",
            ".\\scraped_images\\post1_img2.jpg"
        ],
        "caption": "This is my first post.",
        "date": "2024-01-15 14:32:10",
        "location": {
            "lat": 40.712776,
            "lon": -74.005974
        }
    },
    {
        "post_url": "https://www.instagram.com/p/XYZ789abc/",
        "local_image_paths": [
            ".\\scraped_images\\post2_img1.jpg"
        ],
        "caption": "The food was delicious",
        "date": "2024-02-03 09:12:45",
        "location": {
            "lat": 34.052235,
            "lon": -118.243683
        }
    }
]