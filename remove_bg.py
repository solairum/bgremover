"""
bgremover engine: remove the background from an image.

Command line usage:
    python remove_bg.py photo.jpg
    python remove_bg.py photo.jpg --model birefnet-general-lite    (more accurate)
    python remove_bg.py photo.jpg --single-subject                 (keep only the largest object)

The result is saved as photo_nobg.png next to the original image,
with a transparent background.
"""

import argparse
from pathlib import Path

import numpy as np             # array computations (an image is an array of pixels)
from PIL import Image          # Pillow: open and save images
from rembg import new_session, remove  # rembg: AI background removal
from scipy import ndimage      # image analysis tools (installed with rembg)

# Allowed models. All of them use permissive licenses (MIT or Apache 2.0),
# so they are compatible with an open-source project. "bria-rmbg" is
# deliberately left out because its license forbids commercial use.
MODELS = {
    "isnet-general-use": "Good balance, fast (~170 MB). Default.",
    "birefnet-general-lite": "Sharper edges, needs several GB of RAM (~220 MB).",
    "birefnet-general": "Most accurate, very demanding (~1 GB download).",
    "u2net": "Older and lighter model (~170 MB).",
}
DEFAULT_MODEL = "isnet-general-use"

# Model cache: a dictionary {model name: loaded model}.
# Loading a model takes several seconds. With this cache it only happens
# once; the following images reuse the model already in memory.
_sessions = {}


def get_session(model_name: str):
    """Return the requested model, loading it only the first time."""
    if model_name not in _sessions:
        _sessions[model_name] = new_session(model_name)
    return _sessions[model_name]


def keep_largest_object(result: Image.Image) -> Image.Image:
    """Make transparent everything that is not the largest cut-out object.

    Useful when the model keeps several things (a subject plus some text,
    a logo...) while you only want the main subject.
    """
    # The alpha channel tells how visible each pixel is
    # (0 = transparent, 255 = opaque). We get it as an array.
    alpha = np.array(result.getchannel("A"))

    # label() numbers each "island" of visible pixels that touch each other:
    # the main subject becomes island 1, each letter of a text another island, etc.
    labels, count = ndimage.label(alpha > 0)
    if count <= 1:
        return result  # only one object: nothing to remove

    # Count the pixels of each island (island 0 is the background, ignore it)
    # and keep the number of the largest one.
    sizes = np.bincount(labels.ravel())
    sizes[0] = 0
    largest = sizes.argmax()

    # Every pixel outside the largest island becomes transparent.
    alpha[labels != largest] = 0
    result.putalpha(Image.fromarray(alpha))
    return result


def remove_background(
    image: Image.Image,
    model_name: str = DEFAULT_MODEL,
    single_subject: bool = False,
) -> Image.Image:
    """The engine: takes an image, returns the image without its background.

    This function knows nothing about files or the terminal, which is what
    lets both the command line and the web interface use it.
    """
    # convert("RGB") handles unusual images (grayscale, PNG with transparency...)
    # so the model always receives the same format.
    image = image.convert("RGB")

    # post_process_mask=True cleans up the mask: it removes "half-kept"
    # areas and smooths the edges.
    result = remove(image, session=get_session(model_name), post_process_mask=True)

    if single_subject:
        result = keep_largest_object(result)

    return result


def process_file(
    input_path: Path,
    model_name: str = DEFAULT_MODEL,
    single_subject: bool = False,
) -> Path:
    """File version: open the image, remove the background, save the result."""
    result = remove_background(Image.open(input_path), model_name, single_subject)

    # Always save as PNG, because JPG does not support transparency.
    output_path = input_path.with_name(input_path.stem + "_nobg.png")
    result.save(output_path)
    return output_path


def main():
    # argparse reads the command line arguments for us and generates
    # the help automatically: python remove_bg.py --help
    parser = argparse.ArgumentParser(description="Remove the background from an image.")
    parser.add_argument("image", help="the image file to process")
    parser.add_argument(
        "--model",
        choices=MODELS.keys(),
        default=DEFAULT_MODEL,
        help="the AI model to use",
    )
    parser.add_argument(
        "--single-subject",
        action="store_true",  # "switch" option: present = enabled
        help="keep only the largest object (removes stray text, logos...)",
    )
    args = parser.parse_args()

    path = Path(args.image)
    if not path.exists():
        print(f"File not found: {path}")
        return

    print(f"Processing {path.name} with {args.model}...")
    print(f"  ({MODELS[args.model]})")
    output = process_file(path, args.model, args.single_subject)
    print(f"Done: {output}")


# Run main() only when this file is executed directly,
# not when another file (the web interface) imports it.
if __name__ == "__main__":
    main()
