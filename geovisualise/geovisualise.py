'''
1. Parse the JSON file for social media posts and their locations
2. Render a world map that the user can scroll and interact with, displaying the location of each post.
3. The user can click on each location to see the post made there (renders the page of its URL).

uses Folium
'''

import json
import folium
from folium import plugins
import webbrowser
import os
import base64
from datetime import datetime

def load_posts(json_file):
    """Load posts from JSON file"""
    with open(json_file, 'r', encoding="utf-8") as f:
        return json.load(f)

def image_to_base64(image_path):
    """Convert image to base64 for embedding"""
    try:
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        print(f"  Error converting image {image_path}: {e}")
        return None

def parse_date(date_str):
    """Parse date string to datetime object"""
    try:
        return datetime.fromisoformat(date_str)
    except:
        return None

def create_map(posts, output_file='social_media_map.html'):
    """Create an interactive map with all post locations"""
    
    # Sort posts by date
    posts_with_dates = []
    for post in posts:
        dt = parse_date(post.get('date', ''))
        if dt:
            posts_with_dates.append((dt, post))
    
    posts_with_dates.sort(key=lambda x: x[0])
    
    if not posts_with_dates:
        print("No valid dates found in posts!")
        return None
    
    # Get date range
    min_date = posts_with_dates[0][0]
    max_date = posts_with_dates[-1][0]
    
    # Calculate center point
    avg_lat = sum(post['location']['lat'] for _, post in posts_with_dates) / len(posts_with_dates)
    avg_lon = sum(post['location']['lon'] for _, post in posts_with_dates) / len(posts_with_dates)
    
    # Create base map
    m = folium.Map(
        location=[avg_lat, avg_lon],
        zoom_start=4,
        tiles='OpenStreetMap'
    )
    
    # Add fullscreen button
    plugins.Fullscreen().add_to(m)
    
    print("Creating map with timeline slider...")
    
    # Prepare marker data for JavaScript
    markers_data = []
    
    for i, (dt, post) in enumerate(posts_with_dates, 1):
        lat = post['location']['lat']
        lon = post['location']['lon']
        post_url = post.get('post_url', '')
        post_caption = post.get('caption', '')
        post_date = post.get('date', '')
        
        print(f"Processing post {i}/{len(posts_with_dates)}")
        
        # Create image gallery from local images
        images_html = ""
        for img_path in post['local_image_paths'][:3]:
            img_base64 = image_to_base64(img_path)
            if img_base64:
                images_html += f'''
                <img src="data:image/jpeg;base64,{img_base64}" 
                     style="width: 100%; margin: 5px 0; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                '''
        
        # Format caption
        caption_display = post_caption.replace('\n', '<br>').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;') if post_caption else ''
        
        # Create popup HTML
        popup_html = f"""
        <div style="width: 400px; max-height: 600px; overflow-y: auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
            <div style="background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); 
                        padding: 15px; color: white;">
                <h3 style="margin: 0; font-size: 18px; font-weight: 600;">Post #{i}</h3>
                <p style="margin: 5px 0 0 0; font-size: 13px; opacity: 0.9;">📅 {post_date}</p>
            </div>
            <div style="padding: 0; background: white;">
                <div style="background: #fafafa; padding: 10px;">
                    {images_html}
                </div>
                <div style="padding: 15px;">
                    {f'<p style="margin: 0 0 12px 0; font-size: 14px; line-height: 1.5; color: #262626;">{caption_display}</p>' if caption_display else ''}
                    <p style="margin: 5px 0; font-size: 12px; color: #8e8e8e;">🌍 {lat}, {lon}</p>
                    {f'<a href="{post_url}" target="_blank" style="display: block; margin-top: 12px; background: #0095f6; color: white; padding: 10px; text-align: center; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 14px;">View Full Post on Instagram →</a>' if post_url else ''}
                </div>
            </div>
        </div>
        """
        
        # Add marker to map with unique ID
        marker_id = f"marker_{i}"
        marker = folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=440),
            tooltip=f"📸 Post #{i} - {post_date}",
            icon=folium.Icon(color='red', icon='camera', prefix='fa')
        )
        
        # Add custom div_id to marker
        marker._name = marker_id
        marker.add_to(m)
        
        # Store marker data for timeline control
        markers_data.append({
            'timestamp': int(dt.timestamp() * 1000),
            'date': post_date,
            'id': marker_id,
            'caption': post_caption.lower() if post_caption else ''
        })
    
    # Save map
    m.save(output_file)
    
    # Add timeline slider controls
    min_timestamp = int(min_date.timestamp() * 1000)
    max_timestamp = int(max_date.timestamp() * 1000)
    
    timeline_html = f"""
    <style>
        #timeline-container {{
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: white;
            padding: 12px 16px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.25);
            z-index: 400;
            width: 280px;
            font-family: Arial, sans-serif;
        }}
        .slider-container {{
            margin: 8px 0;
        }}
        .slider-label {{
            font-size: 11px;
            font-weight: 600;
            color: #333;
            margin-bottom: 3px;
        }}
        .slider-value {{
            font-size: 10px;
            color: #666;
            margin-left: 6px;
        }}
        input[type="range"] {{
            width: 100%;
            height: 4px;
            border-radius: 2px;
            background: #ddd;
            outline: none;
            -webkit-appearance: none;
        }}
        input[type="range"]::-webkit-slider-thumb {{
            -webkit-appearance: none;
            appearance: none;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: #E1306C;
            cursor: pointer;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }}
        input[type="range"]::-moz-range-thumb {{
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: #E1306C;
            cursor: pointer;
            border: none;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }}
        #stats {{
            text-align: center;
            margin-top: 8px;
            font-size: 10px;
            color: #666;
        }}
        .timeline-title {{
            font-size: 12px;
            font-weight: 600;
            color: #E1306C;
            margin-bottom: 8px;
            text-align: center;
        }}
        #keyword-search {{
            width: 100%;
            padding: 6px 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 11px;
            box-sizing: border-box;
            margin-bottom: 8px;
        }}
        #keyword-search:focus {{
            outline: none;
            border-color: #E1306C;
        }}
        .search-label {{
            font-size: 11px;
            font-weight: 600;
            color: #333;
            margin-bottom: 3px;
        }}
    </style>
    
    <div id="timeline-container">
        <div class="timeline-title">🔍 Filters</div>
        
        <div style="margin-bottom: 10px;">
            <div class="search-label">Keyword Search</div>
            <input type="text" id="keyword-search" placeholder="Search captions...">
        </div>
        
        <div class="slider-container">
            <div class="slider-label">Start: <span class="slider-value" id="start-date-value"></span></div>
            <input type="range" id="start-slider" min="{min_timestamp}" max="{max_timestamp}" value="{min_timestamp}">
        </div>
        <div class="slider-container">
            <div class="slider-label">End: <span class="slider-value" id="end-date-value"></span></div>
            <input type="range" id="end-slider" min="{min_timestamp}" max="{max_timestamp}" value="{max_timestamp}">
        </div>
        <div id="stats"></div>
    </div>
    
    <script>
        const markersData = {json.dumps(markers_data)};
        
        const startSlider = document.getElementById('start-slider');
        const endSlider = document.getElementById('end-slider');
        const startDateValue = document.getElementById('start-date-value');
        const endDateValue = document.getElementById('end-date-value');
        const keywordSearch = document.getElementById('keyword-search');
        const stats = document.getElementById('stats');
        
        function formatDate(timestamp) {{
            const date = new Date(timestamp);
            return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {{hour: '2-digit', minute:'2-digit'}});
        }}
        
        function updateMarkers() {{
            const startTime = parseInt(startSlider.value);
            const endTime = parseInt(endSlider.value);
            const keyword = keywordSearch.value.toLowerCase().trim();
            
            // Ensure start is always before end
            if (startTime > endTime) {{
                startSlider.value = endTime;
                return;
            }}
            
            startDateValue.textContent = formatDate(startTime);
            endDateValue.textContent = formatDate(endTime);
            
            let visibleCount = 0;
            
            // Get all leaflet panes that contain markers
            const markerPane = document.querySelector('.leaflet-marker-pane');
            if (!markerPane) {{
                console.error('Marker pane not found');
                return;
            }}
            
            const allMarkers = Array.from(markerPane.children);
            console.log('Total markers found:', allMarkers.length);
            
            markersData.forEach((data, index) => {{
                if (allMarkers[index]) {{
                    // Check time range
                    const inTimeRange = data.timestamp >= startTime && data.timestamp <= endTime;
                    
                    // Check keyword match (if keyword is provided)
                    const matchesKeyword = !keyword || data.caption.includes(keyword);
                    
                    if (inTimeRange && matchesKeyword) {{
                        allMarkers[index].style.display = '';
                        visibleCount++;
                    }} else {{
                        allMarkers[index].style.display = 'none';
                    }}
                }}
            }});
            
            stats.textContent = `Showing ${{visibleCount}} of ${{markersData.length}} posts`;
        }}
        
        startSlider.addEventListener('input', updateMarkers);
        endSlider.addEventListener('input', updateMarkers);
        keywordSearch.addEventListener('input', updateMarkers);
        
        // Wait for map to fully load
        setTimeout(() => {{
            updateMarkers();
        }}, 500);
    </script>
    """
    
    # Insert timeline controls into HTML
    with open(output_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    html_content = html_content.replace('</body>', f'{timeline_html}</body>')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Map with timeline slider saved to {output_file}")
    return output_file

def main():
    json_file = 'output.json'
    
    try:
        posts = load_posts(json_file)
        print(f"Loaded {len(posts)} posts")
        
        output_file = create_map(posts)
        
        if output_file:
            webbrowser.open('file://' + os.path.realpath(output_file))
        
    except FileNotFoundError:
        print(f"Error: {json_file} not found!")
    except json.JSONDecodeError:
        print(f"Error: {json_file} is not valid JSON!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()