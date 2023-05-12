__authors__ = "Šimon Krupa" \
              "Mgr. Ing. Matúš Jókay, PhD., " \
              "Tomáš Vavro"
__licence__ = "MIT"


from numba import cuda
import time
import matplotlib.pyplot as plt
import cv2
import os
import glob


@cuda.jit
def transform_to_grayscale_gpu(pixels, gray_image):
    """Transform all pixels to grayscale using GPU.
    Check bounds of  data.
    Use grid() instead of manual pos computation.

    :param pixels: numpy array of rgb color
    :param gray_image: result array of rgb color
    """
    row, col = cuda.grid(2)
    # check array bounds
    if row < len(pixels) and col < len(pixels[row]):
        r, g, b = pixels[row][col]
        # calculate rgb
        gray_image[row][col] = int(0.299 * r + 0.587 * g + 0.114 * b)


def transform_to_grayscale_cpu(pixels):
    """Transform all pixels to grayscale using CPU.

    :param pixels: numpy array of rgb color
    :return: result array of rgb color
    """
    height, width, c = pixels.shape
    # Prepare for output
    gray_image = [[0 for i in range(width)] for j in range(height)]

    for j in range(height):
        for i in range(width):
            r, g, b = pixels[j][i]
            # calculate rgb
            gray_image[j][i] = int(0.299 * r + 0.587 * g + 0.114 * b)
    return gray_image


def prepare_data_for_gpu(pixels):
    """Prepare block dimensions for CUDA
    :param pixels: numpy array of rgb color
    :return: result array of rgb color
    """
    tpb = (30, 30)
    bpg = (10, 10)
    height, width, c = pixels.shape
    gray_image = [[0 for i in range(width)] for j in range(height)]
    transform_to_grayscale_gpu[bpg, tpb](pixels, gray_image)
    return gray_image


def start_process():
    """Function that start process of transforming.
    It loads images and in for loop transform each image
    by using GPU and by using CPU.
    Measure time for each.
    Save grayscale images.

    """
    image_directory = "images"
    # Load all images
    images_files = glob.glob(os.path.join(image_directory, "*.jpg"))
    for index, images_file in enumerate(images_files):
        # Part transforming image by GPU
        start = time.time()
        pixels = plt.imread(images_file)
        # Resize image
        pixels = cv2.resize(pixels, (300, 300))

        gray_image = prepare_data_for_gpu(pixels)

        plt.imsave("grayscaled_images/gs_image_gpu" + str(index + 1) + ".jpg", gray_image, format="jpg", cmap="gray")
        end = time.time()
        print(f'Time to transform with gpu image{index + 1}: {end - start}')

        # Part transforming image by CPU
        start = time.time()
        pixels = plt.imread(images_file)
        # Resize image
        pixels = cv2.resize(pixels, (300, 300))

        gray_image = transform_to_grayscale_cpu(pixels)

        plt.imsave("grayscaled_images/gs_image_cpu" + str(index + 1) + ".jpg", gray_image, format="jpg", cmap="gray")
        end = time.time()
        print(f'Time to transform with cpu image{index + 1}: {end - start}')


if __name__ == "__main__":
    start_process()


