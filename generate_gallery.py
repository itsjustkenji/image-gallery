import os

IMAGE_FOLDER = "images"
DESCRIPTION_FILE = "descriptions.txt"
CHANGES_FILE = "changes.txt"
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

def load_stats():
    transactions = "N/A"
    money = "N/A"
    if os.path.exists(CHANGES_FILE):
        with open(CHANGES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "Total Transactions Done:" in line:
                    transactions = line.split("Total Transactions Done:")[1].strip()
                elif "Total Money Sold:" in line:
                    money = line.split("Total Money Sold:")[1].strip()
    return transactions, money

def get_base_name(filename):
    return os.path.splitext(filename)[0]

def generate_html(images, descriptions, transactions, money):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Kenji Proof Gallery</title>
  <style>
    body {{
      margin: 0;
      font-family: sans-serif;
      color: #fff;
      display: flex;
      flex-direction: column;
      align-items: center;
      position: relative;
      z-index: 1;
      background: #111;
    }}
    #bgVideo {{
      position: fixed;
      top: 0; left: 0;
      width: 100vw;
      height: 100vh;
      object-fit: cover;
      z-index: -1;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      padding: 20px;
      max-width: 1000px;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 20px;
      box-shadow: 0 0 10px rgba(0,0,0,0.3);
    }}
    .grid img {{
      width: 100%;
      height: auto;
      cursor: pointer;
      border-radius: 12px;
      transition: transform 0.2s;
    }}
    .grid img:hover {{
      transform: scale(1.03);
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; }}
      to {{ opacity: 1; }}
    }}

    .overlay {{
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 100%;
      background: rgba(0, 0, 0, 0.6);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 999;
      animation: fadeIn 0.3s ease forwards;
    }}
    .overlay-box {{
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: flex-start;
      gap: 30px;
      padding: 30px;
      background: #222;
      border-radius: 30px;
      box-shadow: 0 0 20px rgba(0,0,0,0.5);
      max-width: fit-content;
      max-height: fit-content;
    }}
    .overlay-box img {{
      max-height: 70vh;
      max-width: 40vw;
      border-radius: 20px;
    }}
    .desc-wrap {{
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      justify-content: center;
    }}
    .desc {{
      font-size: 16px;
      line-height: 1.5;
      margin: 40px 0 20px 0;
      max-width: 400px;
    }}
    .back-btn {{
      background: #444;
      color: #fff;
      border: none;
      padding: 8px 16px;
      border-radius: 12px;
      cursor: pointer;
      align-self: flex-start;
    }}
    .back-btn:hover {{
      background: #666;
    }}
    .stats {{
      margin-bottom: 30px;
      font-size: 24px;
      line-height: 1.6;
      text-align: center;
    }}
  </style>
</head>
<body>
  <video autoplay muted loop id="bgVideo">
    <source src="background.mp4" type="video/mp4">
  </video>

  <h1>Kenji / itsjustkenji's<br>Proof Of Success</h1>
  <div class="stats">
    <strong>Total Transactions Done:</strong> {transactions}<br>
    <strong>Total Money Sold:</strong> {money}
  </div>

  <div class="grid">\n"""
    for img in images:
        base = get_base_name(img)
        desc = descriptions.get(base, "No description available.")
        html += f'    <img src="{IMAGE_FOLDER}/{img}" alt="" onclick="showOverlay(\'{IMAGE_FOLDER}/{img}\', `{desc}`)">\n'
    html += """  </div>

  <div class="overlay" id="overlay">
    <div class="overlay-box">
      <img id="overlayImage" src="" alt="">
      <div class="desc-wrap">
        <div class="desc" id="overlayDesc">Description</div>
        <button class="back-btn" onclick="closeOverlay()">Back</button>
      </div>
    </div>
  </div>

  <script>
    function showOverlay(src, desc) {
      const overlay = document.getElementById("overlay");
      document.getElementById("overlayImage").src = src;
      document.getElementById("overlayDesc").textContent = desc;
      overlay.style.display = "flex";
      overlay.style.animation = "none";
      void overlay.offsetWidth;
      overlay.style.animation = "fadeIn 0.3s ease forwards";
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
    transactions, money = load_stats()
    html = generate_html(images, descriptions, transactions, money)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Generated index.html with stats from changes.txt and fixed video background.")
