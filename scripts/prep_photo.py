"""
Prepare a portrait photo for clean ASCII conversion:
  1. Segment the subject cleanly using OpenCV GrabCut + morphological cleanup
  2. Boost LOCAL contrast (CLAHE) so the face gains crisp definition, highlights, and shadows
  3. Composite onto pure white (255) so the background maps cleanly to spaces in the ASCII ramp

Output: source-prepped.png (grayscale), consumed by make_ascii_svg.py.
"""
import os
import sys
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.jpg")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

def prep_photo():
    img = cv2.imread(INP)
    if img is None:
        print(f"Error: could not read {INP}", file=sys.stderr)
        sys.exit(1)
        
    h, w = img.shape[:2]
    mask = np.zeros((h, w), np.uint8)

    # Base background everywhere
    mask[:, :] = cv2.GC_BGD

    # Central body & face region marked as probable foreground
    mask[int(h*0.22):int(h*0.96), int(w*0.20):int(w*0.80)] = cv2.GC_PR_FGD

    # Definite foreground on core face, eyes, nose, lips, beard
    mask[int(h*0.28):int(h*0.75), int(w*0.32):int(w*0.62)] = cv2.GC_FGD

    # Definite background for the brick pillar & right side background
    mask[0:int(h*0.60), int(w*0.65):w] = cv2.GC_BGD
    mask[int(h*0.60):h, int(w*0.64):w] = cv2.GC_BGD

    # Definite background for top ceiling & left background
    mask[0:int(h*0.22), :] = cv2.GC_BGD
    mask[int(h*0.65):h, 0:int(w*0.30)] = cv2.GC_BGD
    mask[0:int(h*0.65), 0:int(w*0.22)] = cv2.GC_BGD

    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    cv2.grabCut(img, mask, None, bgdModel, fgdModel, 8, cv2.GC_INIT_WITH_MASK)
    mask2 = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 1, 0).astype('uint8')

    # Morphological clean up
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernel)

    # Keep only the largest connected component (Sandesh's head & neck)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask2)
    if num_labels > 1:
        largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        mask2 = np.where(labels == largest_label, 1, 0).astype('uint8')

    # Additional manual cleanup for any lingering right-side brick artifacts
    mask2[int(h*0.60):, int(w*0.61):] = 0
    mask2[int(h*0.68):, :int(w*0.32)] = 0

    # Local contrast enhancement with CLAHE
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.6, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    gray = cv2.convertScaleAbs(gray, alpha=1.05, beta=18)

    # Feather edges with Gaussian blur
    mask_f = mask2.astype(np.float32)
    mask_f = cv2.GaussianBlur(mask_f, (9, 9), 1.8)

    # Vignette/gradient fade on neck bottom so it fades gracefully
    fade_start = int(h * 0.88)
    fade_len = h - fade_start
    if fade_len > 0:
        for y in range(fade_start, h):
            factor = (h - y) / float(fade_len)
            mask_f[y, :] *= factor

    # Composite onto pure white (255)
    out = gray.astype(np.float32) * mask_f + 255.0 * (1.0 - mask_f)
    out = np.clip(out, 0, 255).astype(np.uint8)

    cv2.imwrite(OUT, out)
    print(f"wrote {OUT} {out.shape}")

if __name__ == "__main__":
    prep_photo()
