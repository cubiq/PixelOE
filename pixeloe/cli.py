import os
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("input_img", type=str)
    parser.add_argument("--output_img", "-O", type=str, default=None)
    parser.add_argument(
        "--mode",
        "-M",
        type=str,
        default="contrast",
        choices=["center", "contrast", "k-centroid", "bicubic", "nearest"],
    )
    parser.add_argument("--target_size", "-S", type=int, default=256)
    parser.add_argument("--patch_size", "-P", type=int, default=6)
    parser.add_argument("--thickness", "-T", type=int, default=1)
    parser.add_argument("--no_color_matching", action="store_true")
    parser.add_argument("--contrast", type=float, default=1.0)
    parser.add_argument("--saturation", type=float, default=1.0)
    parser.add_argument("--colors", type=int, default=None)
    parser.add_argument("--no_upscale", action="store_true")
    parser.add_argument("--no_downscale", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    import numpy as np
    import cv2
    from PIL import Image

    from . import pixelize

    img = Image.open(args.input_img)
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = pixelize(
        img,
        args.mode,
        args.target_size,
        args.patch_size,
        args.thickness,
        not args.no_color_matching,
        args.contrast,
        args.saturation,
        args.colors,
        args.no_upscale,
        args.no_downscale,
    )
    if args.output_img is None:
        args.output_img = os.path.join(
            os.path.dirname(args.input_img),
            f"output_{os.path.basename(args.input_img)}",
        )
        print(f"Output image: {args.output_img}")
    data = cv2.imencode(os.path.splitext(args.output_img)[1], img)[1].tobytes()
    with open(args.output_img, "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
