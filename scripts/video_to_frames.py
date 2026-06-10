"""Extract every frame from every video in `--video-dir` into per-video JPG folders.

For each video file `foo.mp4` in `--video-dir`, frames are saved as
`<output-dir>/foo/<frame_index>.jpg`.
"""

import argparse
import os

import cv2


def extract_frames(video_dir, output_dir):
    for video in os.listdir(video_dir):
        video_path = os.path.join(video_dir, video)
        if not os.path.isfile(video_path):
            continue

        stem, _ = os.path.splitext(video)
        out_subdir = os.path.join(output_dir, stem)
        os.makedirs(out_subdir, exist_ok=True)

        capture = cv2.VideoCapture(video_path)
        i = 0
        try:
            while capture.isOpened():
                ok, frame = capture.read()
                if not ok:
                    break
                cv2.imwrite(os.path.join(out_subdir, f"{i}.jpg"), frame)
                i += 1
        finally:
            capture.release()

    cv2.destroyAllWindows()


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--video-dir",
        default=os.environ.get("VIDEO_DIR"),
        help="Directory containing video files. Env: VIDEO_DIR.",
    )
    parser.add_argument(
        "--output-dir",
        default=os.environ.get("OUTPUT_DIR"),
        help="Directory to write per-video frame folders. Env: OUTPUT_DIR.",
    )
    args = parser.parse_args()
    if not args.video_dir or not args.output_dir:
        parser.error("Both --video-dir and --output-dir are required.")
    return args


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    extract_frames(args.video_dir, args.output_dir)


if __name__ == "__main__":
    main()
