import argparse
import os
import sys
from os.path import basename

import cv2

parser = argparse.ArgumentParser(
    "This script moves images that contain content to one directory and images that do not "
    "contain content to another directory"
)
parser.add_argument(
    "-p",
    "--path",
    type=str,
    required=True,
    help="The path to the directory containing the images",
)
parser.add_argument(
    "-b", "--black", action="store_true", help="Background color is black"
)
parser.add_argument(
    "-w", "--white", action="store_true", help="Background color is white"
)
args = parser.parse_args()


def check_image_file(image_path) -> bool:
    """
    If the image path ends with any of the extensions in the list, return True, otherwise return False

    :param image_path: The path to the image file
    :return: True or False
    """
    image_extensions = [".jpg", ".jpeg", ".tif", ".bmp", ".png", ".gif"]

    for image_ext in image_extensions:
        if image_path.endswith(image_ext):
            return True
    return False


def check_for_content(image_path, color_to_check) -> bool:
    """
    It takes an image path and a color range, and returns True if there is any pixel in the image that falls within that
    color range

    :param image_path: The path to the image you want to check
    :param color_to_check: This is a tuple of the lower and upper bounds of the color you want to check for
    :return: A boolean value.
    """

    img = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_gray = cv2.bitwise_not(img_gray)
    ret, mask = cv2.threshold(img_gray, *color_to_check)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        return True
    else:
        return False


def move_file(image_path, destination_path):
    """
    It moves the image and its corresponding .tfw file to the destination path

    :param image_path: The path to the image you want to move
    :param destination_path: The path to the directory where you want to move the files
    """
    tfw_path = image_path.replace("." + image_path.split(".")[-1], ".tfw")
    if os.path.exists(tfw_path):
        os.rename(tfw_path, os.path.join(destination_path, basename(tfw_path)))

    os.rename(image_path, os.path.join(destination_path, basename(image_path)))


def check_colors() -> list or tuple:
    """
    If the user specified both --black and --white, then print an error message and exit;
    otherwise, if the user specified
    --black, return [0, 0, 0]; otherwise, if the user specified --white, return [255, 255, 255];
    otherwise, print an error
    message and exit
    :return: a list of three integers.
    """
    if not os.path.exists(args.path):
        print("The path you specified does not exist")
        sys.exit(0)
    if args.black and args.white:
        print("You can only specified one of the two arguments --black or --white")
        sys.exit(0)
    elif args.black:
        return [0, 0, 0]
    elif args.white:
        return [255, 255, 255]
    else:
        print("You must specify one of the two arguments --black or --white")
        sys.exit(0)


def main():
    color = check_colors()
    path = args.path
    empty_dir = os.path.join(args.path, "no_content")
    edge_dir = os.path.join(args.path, "content")
    files = [file for file in os.listdir(path)]

    os.makedirs(empty_dir, exist_ok=True)
    os.makedirs(edge_dir, exist_ok=True)

    for file in files:
        if check_image_file(file):
            image = os.path.join(path, file)
            if check_for_content(image, color):
                move_file(image, edge_dir)
            else:
                move_file(image, empty_dir)


if __name__ == "__main__":
    main()
