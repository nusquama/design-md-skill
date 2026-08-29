#!/usr/bin/env python3
"""Quantize an image's dominant colors (k-means) for Branch B."""
import sys, json
try:
    from PIL import Image
    import numpy as np
    from sklearn.cluster import KMeans
except ImportError:
    print(json.dumps({"error": "pillow + scikit-learn required"}))
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: quantize_palette.py <image> [--k 12] [--no-crop]")
        sys.exit(1)
    path = sys.argv[1]
    k = 12
    if "--k" in sys.argv:
        k = int(sys.argv[sys.argv.index("--k") + 1])
    img = Image.open(path).convert("RGB")
    img = img.resize((150, 150))
    pixels = np.array(img).reshape(-1, 3)
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(pixels)
    centers = km.cluster_centers_.astype(int)
    print(json.dumps(["#%02x%02x%02x" % tuple(c) for c in centers], indent=2))

if __name__ == "__main__":
    main()
