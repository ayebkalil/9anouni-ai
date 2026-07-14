import os
import sys
from PIL import Image
import pytesseract
from pytesseract import Output

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)
sys.stdout.reconfigure(encoding='utf-8')

image_path = os.path.join(project_root, "data", "processed", "prod-run-finance_law_2026-12280f7c", "p0002-col-left.png")

if not os.path.exists(image_path):
    print("Could not find a test image. Adjust path.")
    sys.exit(1)

img = Image.open(image_path)
data = pytesseract.image_to_data(img, lang="ara", output_type=Output.DICT)

# Reconstruct
lines = []
current_line_words = []
current_line_id = None
confidences = []

for i in range(len(data['text'])):
    word = data['text'][i].strip()
    conf = data['conf'][i]
    
    line_id = (data['block_num'][i], data['par_num'][i], data['line_num'][i])
    
    if line_id != current_line_id:
        if current_line_words:
            lines.append(" ".join(current_line_words))
            current_line_words = []
        current_line_id = line_id
        
    if word and conf != -1:
        current_line_words.append(word)
        try:
            confidences.append(float(conf))
        except ValueError:
            pass

if current_line_words:
    lines.append(" ".join(current_line_words))
    
text = "\n".join(lines)
print("--- RECONSTRUCTED TEXT ---")
print(text[:300])

print("\n--- ORIGINAL TEXT ---")
orig_text = pytesseract.image_to_string(img, lang="ara")
print(orig_text[:300])
