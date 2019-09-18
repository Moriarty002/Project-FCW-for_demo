import numpy as np
from PIL import Image
import video
import cv2 as cv


''' compute average horizontal variance for each image'''
def slow_horizontal_variance(im):
    '''Return average variance of horizontal lines of a grayscale image'''
    width, height = im.size
    if not width or not height: return 0
    vars = []
    pix = im.load()
    for y in range(height):
        row = [pix[x,y] for x in range(width)]
        mean = sum(row)/width
        variance = sum([(x-mean)**2 for x in row])/width
        vars.append(variance)
    return sum(vars)/height


#fn = Image.open('unknown.jpeg')
#im = fn.convert('L')

'''
def numpy2pil(np_array: np.ndarray) -> Image:
    """
    Convert an HxWx3 numpy array into an RGB Image
    """

    assert_msg = 'Input shall be a HxWx3 ndarray'
    assert isinstance(np_array, np.ndarray), assert_msg
    assert len(np_array.shape) == 3, assert_msg
    assert np_array.shape[2] == 3, assert_msg

    img = Image.fromarray(np_array, 'L')
    return img
'''

try:
    fn = sys.argv[1]
except:
    fn = 0
cv.namedWindow('video')
print(fn)
cap = video.create_capture(fn)

while True:
    ret, frame = cap.read()
    #im = numpy2pil(frame)
    #im = Image.fromarray(frame,'L')
    im = frame.convert('L')
    var = slow_horizontal_variance(im)
    fog = var < 443    # FOG THRESHOLD
    print ('%5.0f - %5s' % (var, fog and 'FOGGY' or 'SHARP'))
