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
    body { margin: 0; background: #111; color: #fff; font-family: sans-serif; display: flex; flex-direction: column; }
    .thumbs { display: flex; overflow-x: auto; gap: 10px; padding: 20px; background: #222; }
    .thumbs img { height: 100px; cursor: pointer; border-radius: 6px; transition: transform 0.2s; }
    .thumbs img:hover { transform: scale(1.05); }

    .viewer { display: flex; flex: 1; padding: 20px; gap: 20px; align-items: flex-start; }
    .viewer img { max-height: 500px; border-radius: 8px; background: #333; }
    .desc { max-width: 400px; font-size: 16px; line-height: 1.5; }

    .gallery::-webkit-scrollbar { height: 8px; }
    .gallery::-webkit-scrollbar-thumb { background: #444; border-radius: 4px; }
  </style>
</head>
<body>
  <h1 style="text-align:center;">Kenji Gallery</h1>

  <div class="thumbs" id="thumbs">\n"""
    for img in images:
        html += f'    <img src="{IMAGE_FOLDER}/{img}" alt="{img}" onclick="showImage(\'{IMAGE_FOLDER}/{img}\', \'{img}\')">\n'
    html += """  </div>

  <div class="viewer">
    <img id="mainImage" src="" alt="Selected Image">
    <div class="desc" id="description">Click an image to see its description.</div>
  </div>

  <script>
    function showImage(src, desc) {
      document.getElementById("mainImage").src = src;
      document.getElementById("description").textContent = desc;
    }
  </script>
</body>
</html>"""
    return html

if __name__ == "__main__":
    images = get_sorted_images()
    html = generate_html(images)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {OUTPUT_FILE} with {len(images)} images.")
