# PPDS 2023 Krupa

This branch is dedicated to the 5th assignment - CUDA. We will transform colorful images
to grayscale by using GPU and comparing it with using only CPU. Using GPU for this task
can speed up the process time. GPU is more useful/faster than CPU in cases when we have 
one instruction for multiple data. We can use GPU for development thanks to CUDA. CUDA is programming
platform for parallel computing created by NVIDIA.

### Libraries

To use CUDA we will be using library _numba_. Unfortunately, in this repository we will use CUDA simulator, so we will not use 
our own GPU. Because of this the results will differ from situation where we would use our own computers GPU, they will be much longer.
To use this simulator we will set environment variable NUMBA_ENABLE_CUDASIM=1.
Other libraries we will use are _matplotlib_, _os_, _glob_, _cv2_ to work with images. and _time_ to measure time.

### Implementation

We prepared 20 different images that are stored in folder _images_.
Program loops through each image, resizes it to 300x300 and transform it into grayscale first by using GPU,
measure its time and then with CPU and measure its time. Resulting images are saved in folder _grayscaled_images_.
Images are opened and saved with libraries _matplotlib.pyplot_, _os_, _glob_. Resizing image is done by _cv2_.

When transforming image with only CPU we call the function _transform_to_grayscale_cpu_ 
```
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
   ```
We loop through each pixel and calculate its new rgb with this pattern "0.299 * r + 0.587 * g + 0.114 * b" to achieve grayscaling.
The new pixels are stored in prepared array _gray_image_

When transforming image with using GPU we prepare data with function _prepare_data_for_gpu_
```
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
```

where we initialize block dimensions (30, 30) (10, 10) because we have image 300x300. Meaning 30*30*10*10 equals 300*300.
Then we call function _transform_to_grayscale_gpu[tpb][bpg]_ passing our dimensions.
```
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
```

The function has decorator @cuda.jit, that 
tells compiler to use cuda gpu for this function. Method _cuda.grid(2)_ returns the absolute position of the current thread in the entire grid of blocks.
It is  computed by this pattern "cuda.threadIdx.x + cuda.blockIdx.x * cuda.blockDim.x".
After we calculate grayscaled rgb like in CPU example.

### Results
After running this program with our 20 images resized to 300x300. We got these results:

Average time to transform image with GPU: 20,4245939846 seconds
Average time to transform image with CPU: 0,50639241928 seconds

After running this program with our 20 images resized to 400x400. We got these results:

Average time to transform image with GPU: 37,00862162   seconds
Average time to transform image with CPU: 0,90052851438 seconds

Results are a bit of from what we expected but its due to the fact that we are using numba simulator and not directly our own GPU.
Using our own GPU should give us lower time than using only CPU. Results for each image are stored in _tests.txt_.

![alt text](https://github.com/simonkrupa/Krupa_104510_feippds/blob/05/images/image1.jpg?raw=true)

![alt text](https://github.com/simonkrupa/Krupa_104510_feippds/blob/05/grayscaled_images/gs_image_cpu1.jpg?raw=true)