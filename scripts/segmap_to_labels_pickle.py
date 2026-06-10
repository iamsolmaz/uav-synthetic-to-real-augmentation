"""Build per-pixel class labels and bounding boxes from segmentation PNGs.

For every segmentation image in `--input-dir` (filenames like `<idx>_1_<dist>.png`),
the script:
  - maps each RGBA pixel to a class id via the COLOR_TO_CLASS / CLASS_TO_ID tables;
  - finds the bounding box of the drone class;
  - copies the matching raw image (`<idx>_0_<dist>.png`) into `--output-dir`,
    renamed to encode the bbox: `<idx>_<x_min>_<y_min>_<w>_<h>_<dist>.png`;
  - dumps `[class_id_to_name_key, {index: flat_pixel_labels}]` to
    `<output-dir>/segLabels.pickle`.

Adjust COLOR_TO_CLASS to match the segmentation palette in your scene.
"""

import argparse
import os
import pickle

from PIL import Image
from tqdm import tqdm


# RGBA -> class name. Adjust to match your AirSim segmentation palette.
COLOR_TO_CLASS = {
    (232, 250, 80, 255): "foliage",
    (249, 79, 73, 255): "sky",
    (187, 70, 156, 255): "ground",
    (42, 7, 136, 255): "drone",
    # Stray mislabeled pixel observed once in ~20k images; safe to fold into background.
    (202, 97, 155, 255): "error",
}

CLASS_TO_ID = {
    "foliage": 0,
    "sky": 1,
    "ground": 2,
    "drone": 3,
    "error": 0,
}

ID_TO_CLASS = {
    0: "foliage",
    1: "sky",
    2: "ground",
    3: "plane",
}

DRONE_ID = CLASS_TO_ID["drone"]


def get_labels(img, output, index):
    """Append the flattened class-id list for `img` to `output[index]`; return bbox."""
    width, height = img.size
    pixels = list(img.getdata())

    pixel_vals = []
    x_min, y_min = width, height
    x_max, y_max = 0, 0

    for pixel_idx, pixel in enumerate(pixels):
        class_id = CLASS_TO_ID[COLOR_TO_CLASS[pixel]]
        pixel_vals.append(class_id)
        if class_id == DRONE_ID:
            y = pixel_idx // width
            x = pixel_idx % width
            if y < y_min:
                y_min = y
            if y > y_max:
                y_max = y
            if x < x_min:
                x_min = x
            if x > x_max:
                x_max = x

    output[index] = pixel_vals
    return output, x_min, x_max, y_min, y_max


def process_directory(input_dir, output_dir):
    """Process one input dir; write renamed raws + segLabels.pickle into output_dir."""
    output = {}

    for filename in tqdm(os.listdir(input_dir), desc=os.path.basename(input_dir) or input_dir):
        parts = filename.split("_")
        if len(parts) < 3 or parts[1] != "1":
            continue

        index = int(parts[0])
        distance = parts[2][:-4]  # strip ".png"
        seg_path = os.path.join(input_dir, filename)
        if not os.path.isfile(seg_path):
            continue

        raw_parts = parts.copy()
        raw_parts[1] = "0"
        raw_path = os.path.join(input_dir, "_".join(raw_parts))

        with Image.open(seg_path) as img:
            output, x_min, x_max, y_min, y_max = get_labels(img, output, index)

        w = max(0, x_max - x_min)
        h = max(0, y_max - y_min)

        with Image.open(raw_path) as raw_im:
            out_name = f"{index}_{x_min}_{y_min}_{w}_{h}_{distance}.png"
            raw_im.save(os.path.join(output_dir, out_name))

    write_out = [ID_TO_CLASS, output]
    with open(os.path.join(output_dir, "segLabels.pickle"), "wb") as outfile:
        pickle.dump(write_out, outfile, -1)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        default=os.environ.get("INPUT_DIR"),
        help="Directory containing segmentation + raw image pairs. Env: INPUT_DIR.",
    )
    parser.add_argument(
        "--output-dir",
        default=os.environ.get("OUTPUT_DIR"),
        help="Directory for renamed raw images + segLabels.pickle. Env: OUTPUT_DIR.",
    )
    args = parser.parse_args()
    if not args.input_dir or not args.output_dir:
        parser.error("Both --input-dir and --output-dir are required.")
    return args


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    process_directory(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
