from flask import Flask, render_template, request
from PIL import Image
import numpy as np 
from sklearn.cluster import KMeans

app = Flask(__name__)

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

@app.route('/', methods=['GET', 'POST'])
def index():
    colors = []

    if request.method == 'POST':
        file = request.files["image"]
        image = Image.open(file).convert('RGB')

        # Resize image
        image = image.resize((200, 200))

        pixels = np.array(image)
        pixels = pixels.reshape(-1, 3)

        # KMeans clustering
        kmeans = KMeans(n_clusters=10, n_init=10)
        kmeans.fit(pixels)

        count = np.bincount(kmeans.labels_)
        centers = kmeans.cluster_centers_.astype(int)

        # Sort colors by frequency
        sorted_colors = sorted(
            zip(count, centers),
            reverse=True,
            key=lambda x: x[0]
        )

        for count, rgb in sorted_colors:
            colors.append({
                "hex":rgb_to_hex(tuple(rgb)),
                "rgb":tuple(rgb),
                "percent": round((count / len(pixels)) * 100, 2)
            })
        
    return render_template('index.html', colors=colors)

if __name__ == '__main__':
    app.run(debug=True)


