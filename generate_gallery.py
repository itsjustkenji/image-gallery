import os

IMAGE_FOLDER = "images"
OUTPUT_FILE = "index.html"

def extract_number(filename):
    name, ext = os.path.splitext(filename)
    if " TRANS" in name:
        try:
            return int(name.split(" TRANS")[0])
        except ValueError:
            return None
    return None

def get_sorted_images():
    files = os.listdir(IMAGE_FOLDER)
    images = [f for f in files if f.lower().endswith(('.jpg', '.png'))]
    numbered = [(extract_number(f), f) for f in images]
    return [f for num, f in sorted(numbered) if num is not None]

def generate_html(images):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Kenji Gallery</title>
  <style>
    body { margin: 0; background: #111; color: #fff; font-family: sans-serif; }
    .gallery { display: flex; overflow-x: auto; gap: 10px; padding: 20px; scroll-snap-type: x mandatory; }
    .gallery img { height: 300px; scroll-snap-align: start; border-radius: 8px; object-fit: cover; background: #222; }
    .gallery::-webkit-scrollbar { height: 8px; }
    .gallery::-webkit-scrollbar-thumb { background: #444; border-radius: 4px; }
  </style>
</head>
<body>
  <h1 style="text-align:center;">Kenji Gallery</h1>
  <div class="gallery">\n"""
    for img in images:
        html += f'    <img src="{IMAGE_FOLDER}/{img}" alt="{img}">\n'
    html += "  </div>\n</body>\n</html>"
    return html

if __name__ == "__main__":
    images = get_sorted_images()
    html = generate_html(images)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {OUTPUT_FILE} with {len(images)} images.")
