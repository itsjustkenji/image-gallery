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
    .viewer {
      display: none;
      flex-direction: row;
      gap: 20px;
      padding: 20px;
      max-width: 1000px;
      align-items: flex-start;
    }
    .viewer img {
      max-width: 400px;
      border-radius: 8px;
    }
    .desc {
      max-width: 500px;
      font-size: 16px;
      line-height: 1.5;
    }
    .back-btn {
      margin-top: 10px;
      background: #333;
      color: #fff;
      border: none;
      padding: 8px 16px;
      border-radius: 4px;
      cursor: pointer;
    }
    .back-btn:hover {
      background: #555;
    }
  </style>
</head>
<body>
  <h1>Kenji Gallery</h1>

  <div class="grid" id="grid">\n"""
    for img in images:
        html += f'    <img src="{IMAGE_FOLDER}/{img}" alt="{img}" onclick="showImage(\'{IMAGE_FOLDER}/{img}\', \'{img}\')">\n'
    html += """  </div>

  <div class="viewer" id="viewer">
    <img id="mainImage" src="" alt="Selected">
    <div class="desc">
      <div id="description">Click a photo to see its description.</div>
      <button class="back-btn" onclick="goBack()">Back to Grid</button>
    </div>
  </div>

  <script>
    function showImage(src, desc) {
      document.getElementById("mainImage").src = src;
      document.getElementById("description").textContent = desc;
      document.getElementById("viewer").style.display = "flex";
      document.getElementById("grid").style.display = "none";
      window.scrollTo({ top: 0, behavior: "smooth" });
    }

    function goBack() {
      document.getElementById("viewer").style.display = "none";
      document.getElementById("grid").style.display = "grid";
      window.scrollTo({ top: 0, behavior: "smooth" });
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
    print(f"✅ Generated {OUTPUT_FILE} with {len(images)} images.")
