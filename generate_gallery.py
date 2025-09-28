import os

IMAGE_FOLDER = "images"
DESCRIPTION_FILE = "descriptions.txt"
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

def load_descriptions():
    desc_map = {}
    if os.path.exists(DESCRIPTION_FILE):
        with open(DESCRIPTION_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "|" in line:
                    key, desc = line.strip().split("|", 1)
                    desc_map[key.strip()] = desc.strip()
    return desc_map

def get_base_name(filename):
    return os.path.splitext(filename)[0]  # removes .jpg/.png

def generate_html(images, descriptions):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Kenji Gallery</title>
  <style>
    body {
      margin: 0;
      font-family: sans-serif;
      background: #111;
      color: #fff;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      padding: 20px;
      max-width: 1000px;
    }
    .grid img {
      width: 100%;
      height: auto;
      cursor: pointer;
      border-radius: 6px;
      transition: transform 0.2s;
    }
    .grid img:hover {
      transform: scale(1.03);
    }

    .overlay {
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 100%;
      background: rgba(0,0,0,0.95);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 999;
    }
    .overlay-content {
      display: flex;
      gap: 30px;
      padding: 30px;
      max-width: 1000px;
      width: 90%;
      align-items: flex-start;
    }
    .overlay img {
      max-height: 80vh;
      border-radius: 8px;
    }
    .desc {
      max-width: 400px;
      font-size: 16px;
      line-height: 1.5;
    }
    .close-btn {
      position: absolute;
      top: 20px;
      right: 30px;
      background: #333;
      color: #fff;
      border: none;
      padding: 8px 16px;
      border-radius: 4px;
      cursor: pointer;
    }
    .close-btn:hover {
      background: #555;
    }
  </style>
</head>
<body>
  <h1>Kenji Gallery</h1>

  <div class="grid">\n"""
    for img in images:
        base = get_base_name(img)
        desc = descriptions.get(base, "No description available.")
        html += f'    <img src="{IMAGE_FOLDER}/{img}" alt="" onclick="showOverlay(\'{IMAGE_FOLDER}/{img}\', `{desc}`)">\n'
    html += """  </div>

  <div class="overlay" id="overlay">
    <div class="overlay-content">
      <img id="overlayImage" src="" alt="">
      <div class="desc" id="overlayDesc">Description</div>
    </div>
    <button class="close-btn" onclick="closeOverlay()">Close</button>
  </div>

  <script>
    function showOverlay(src, desc) {
      document.getElementById("overlayImage").src = src;
      document.getElementById("overlayDesc").textContent = desc;
      document.getElementById("overlay").style.display = "flex";
    }

    function closeOverlay() {
      document.getElementById("overlay").style.display = "none";
    }
  </script>
</body>
</html>"""
    return html

if __name__ == "__main__":
    images = get_sorted_images()
    descriptions = load_descriptions()
    html = generate_html(images, descriptions)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Generated {OUTPUT_FILE} with {len(images)} images and overlay layout.")
