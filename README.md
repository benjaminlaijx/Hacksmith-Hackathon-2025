Hacksmith v6.0
Group: SecureStack
Tool: Geol0c4t

Geol0c4t ("Geolocate") is an automated OSINT tool for building a geolocational visualisation of a person's wehereabouts based on images pulled from social media.

1. The user must input a target person's social media account(s).
2. The tool will pull photos of the target from their accounts. (The user can optionally input photos of the target they already have.)
3. The tool will then attempt to geolocate each photo using various techniques (neural-network, EXIF metadata, reverse image search, etc)
4. Finally, the tool will output a heatmap visualisation of the person's known locations.

# Development
```
# Activate virtual environment (requires a virtual environment setup).
.venv/scripts/activate

# Install required dependencies.
pip install -r requirements.txt

# Save required dependencies (if any new ones are added).
pip freeze > requirements.txt
```