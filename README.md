Hacksmith v6.0
Group: SecureStack
Tool: Geol0c4t

Geol0c4t ("Geolocate") is an automated OSINT tool for building a geographic visualisation of the locations of a person's social media images.

1. The user must input a target person's social media account(s) (supported social media platforms: IG, Facebook, etc)
2. The tool will collate all their social media posts that contain images, storing each post as a JSON object.
3. The tool will then attempt to determine the location of each post through various image geolocation techniques (neural-network, EXIF metadata, reverse image search, etc)
4. Finally, the tool will output a geographic visualisation of the locations of the person's posts. The user can check each location and view the post made there.

# Development
```
# Activate virtual environment (requires a virtual environment setup).
.venv/scripts/activate

# Install required dependencies.
pip install -r requirements.txt

# Save required dependencies (if any new ones are added).
pip freeze > requirements.txt
```

# Project structure
Geol0c4t/
├── instascraper/           # Python module that scrapes social media posts
├──── output/
├──────json/                    # caches data on each social media post
├──────images/                  # caches social media post images downloaded by the tool
├── geovisualise/           # Python module that renders the geographic visualisation

# JSON schema
At each step, our tool works with a JSON file storing data of the person's social media posts. Each post is an object with the following fields:
- Post URL
- Photo filepath(s) (photos are cached inside `.\scraped_images`)
- Geolocation (determined via various image geolocation techniques)
- Datetime of post

Example:
{
    "post_url": f"https://www.instagram.com/p/{post.shortcode}/",
    "local_image_path": full_image_path,
    "date": str(post.date_local),
    "location": {
        "lat": post.location.lat,
        "lon": post.location.lng,
    }
}