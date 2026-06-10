"""Recursively convert every PNG under `--input-dir` to a JPG in `--output-dir`."""

import argparse
import os
from pathlib import Path

from PIL import Image


def convert(input_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    for src in input_dir.glob("**/*.png"):
        dst = output_dir / (src.stem + ".jpg")
        with Image.open(src) as im:
            im.convert("RGB").save(dst, "JPEG")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        default=os.environ.get("INPUT_DIR"),
        help="Directory of PNG images (recursive). Env: INPUT_DIR.",
    )
    parser.add_argument(
        "--output-dir",
        default=os.environ.get("OUTPUT_DIR"),
        help="Directory for JPG output. Env: OUTPUT_DIR.",
    )
    args = parser.parse_args()
    if not args.input_dir or not args.output_dir:
        parser.error("Both --input-dir and --output-dir are required.")
    return args


def main():
    args = parse_args()
    convert(Path(args.input_dir), Path(args.output_dir))


if __name__ == "__main__":
    main()
