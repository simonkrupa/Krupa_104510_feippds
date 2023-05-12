__authors__ = "Šimon Krupa" \
              "Mgr. Ing. Matúš Jókay, PhD., " \
              "Tomáš Vavro"
__licence__ = "MIT"


from numba import cuda
import time
import matplotlib.pyplot as plt
import cv2


@cuda.jit
def transform_to_grayscale_gpu(pixels, gray_image):
    row, col = cuda.grid(2)
    if row < len(pixels) and col < len(pixels[row]):  # check array bounds
        r, g, b = pixels[row][col]
        gray_image[row][col] = int(0.299 * r + 0.587 * g + 0.114 * b)


def transform_to_grayscale_cpu(pixels):
    height, width, c = pixels.shape
    # Prepare for output
    gray_image = [[0 for i in range(width)] for j in range(height)]

    for j in range(height):
        for i in range(width):
            r, g, b = pixels[j][i]
            gray_image[j][i] = int(0.299 * r + 0.587 * g + 0.114 * b)
    return gray_image


def prepare_data_for_gpu(pixels):
    tpb = (30, 30)
    bpg = (10, 10)
    height, width, c = pixels.shape
    gray_image = [[0 for i in range(width)] for j in range(height)]
    transform_to_grayscale_gpu[bpg, tpb](pixels, gray_image)
    return gray_image


if __name__ == "__main__":

    start = time.time()
    pixels = plt.imread("images/image1.jpg")
    pixels = cv2.resize(pixels, (300, 300))

    gray_image = prepare_data_for_gpu(pixels)
    # gray_image = transform_to_grayscale_cpu(pixels)
    end = time.time()
    print(end - start)
    plt.imshow(gray_image, cmap="gray")
    plt.show()

    # plt.imsave("m-i-gs3.jpg", gray_image, format="jpg", cmap="gray")

