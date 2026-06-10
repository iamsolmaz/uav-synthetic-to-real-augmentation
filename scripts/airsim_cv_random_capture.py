"""Generate Scene + Segmentation images from an Unreal Engine map via AirSim CV mode.

Setup:
  In AirSim `settings.json`, enable Computer Vision mode:
    https://github.com/Microsoft/AirSim/blob/main/docs/image_apis.md#computer-vision-mode

For each iteration the script:
  1. Samples a random offset around the player start (exponential XY, uniform Z).
  2. Aims the CV camera at the origin with a small random rotational offset.
  3. Captures one Scene PNG and one Segmentation PNG per pose.

Note: segmentation colors can take a moment to stabilize on first run. If the
colors suddenly change, delete the initial images and rerun.
"""

import argparse
import math
import os
import pprint
import random
import tempfile
import time

import airsim
import numpy as np
from tqdm import tqdm


def cart2sph(x, y, z):
    """Return (r, elevation, azimuth) for a point looking at the origin."""
    x2y2 = x ** 2 + y ** 2
    r = math.sqrt(x2y2 + z ** 2)
    elev = math.atan2(z, math.sqrt(x2y2))
    az = math.atan2(y, x)
    return r, elev, az


def sample_pose(rng):
    x = (2 + np.random.exponential(5)) * [-1, 1][rng.randrange(2)]
    y = (2 + np.random.exponential(5)) * [-1, 1][rng.randrange(2)]
    z = rng.uniform(-10, 10)
    return x, y, z


def capture(client, output_dir, num_images):
    pp = pprint.PrettyPrinter(indent=4)
    rng = random.Random()

    for i in tqdm(range(num_images)):
        x, y, z = sample_pose(rng)
        distance = 2 * math.sqrt(x ** 2 + y ** 2 + z ** 2)

        _, pitch, yaw = cart2sph(x, y, z)
        pitch += math.radians(rng.uniform(-15, 15))
        yaw += math.radians(rng.uniform(-15, 15))
        roll = math.radians(rng.uniform(-5, 5))

        client.simSetVehiclePose(
            airsim.Pose(
                airsim.Vector3r(x, y, z),
                airsim.to_quaternion(pitch, roll, yaw + math.pi),
            ),
            True,
        )

        time.sleep(0.2)  # let the scene render

        responses = client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene),
            airsim.ImageRequest("0", airsim.ImageType.Segmentation),
        ])

        for j, response in enumerate(responses):
            filename = os.path.join(output_dir, f"{i}_{j}")
            if response.pixels_as_float:
                print(f"Type {response.image_type}, size {len(response.image_data_float)}, "
                      f"pos {pprint.pformat(response.camera_position)}")
                airsim.write_pfm(os.path.normpath(filename + ".pfm"), airsim.get_pfm_array(response))
            else:
                print(f"Type {response.image_type}, size {len(response.image_data_uint8)}, "
                      f"pos {pprint.pformat(response.camera_position)}")
                airsim.write_file(
                    os.path.normpath(filename + f"_{distance}.png"),
                    response.image_data_uint8,
                )

        pp.pprint(client.simGetVehiclePose())


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        default=os.environ.get("OUTPUT_DIR") or os.path.join(tempfile.gettempdir(), "airsim_cv_mode"),
        help="Directory to save captured images. Env: OUTPUT_DIR. "
             "Default: <tempdir>/airsim_cv_mode.",
    )
    parser.add_argument(
        "--num-images",
        type=int,
        default=500,
        help="Number of poses to capture (default: 500).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    print(f"Saving images to {args.output_dir}")

    client = airsim.VehicleClient()
    client.confirmConnection()

    capture(client, args.output_dir, args.num_images)


if __name__ == "__main__":
    main()
