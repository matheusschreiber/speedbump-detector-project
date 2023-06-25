# ================================================================= #

# CODE FOR MASKING WITH PPM IMAGES

# import cv2
# import numpy as np
# img = cv2.imread('0039.ppm')
# color = (43, 41, 42)  
# layer = np.zeros_like(img)
# layer[:] = color
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
# mask = cv2.merge([mask, mask, mask])
# mask = mask / 255.0
# alpha = 0.5
# result = cv2.addWeighted(img, 1 - alpha, layer, alpha, 0)
# # apply the mask only to non-transparent pixels
# result[np.where(mask[:, :, 0] == 1)] = result[np.where(mask[:, :, 0] == 1)] * mask[np.where(mask[:, :, 0] == 1)] + img[np.where(mask[:, :, 0] == 1)] * (1 - mask[np.where(mask[:, :, 0] == 1)]) 
# cv2.imwrite('0040.png', result)



# ================================================================= #

# CODE FOR MASKING WITH PNG IMAGES (NOT CHANGIN 
# THE COLOR, JUST GRAYSCALE)

# import cv2 as cv
# import numpy as np
# img = cv.imread("0039.png")
# hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
# lower = np.array([0,0,0])
# upper = np.array([10,10,10])
# mask = cv.inRange(hsv, lower, upper)
# mask_inv = cv.bitwise_not(mask)
# mask_inv = cv.cvtColor(mask_inv, cv.COLOR_GRAY2BGR)
# # added_img = cv.add(img, mask)
# red_color = np.zeros((0, 0, 3), dtype=np.uint8)
# cv.rectangle(red_color, (0, 0), (700, 700), (0,0,255), -1)
# color_mask = cv.addWeighted(mask, 1, red_color, 0.5, 0.0)
# added_img = cv.bitwise_and(img, mask_inv)
# res = cv.bitwise_and(img, img, mask=mask)
# background = cv.bitwise_and(img, img, mask = mask_inv)
# background = cv.bitwise_and(gray, gray, mask = mask_inv)
# background = np.stack((background,)*3, axis=-1)
#create resizable windows for the images
# cv.namedWindow("res", cv.WINDOW_NORMAL)
# cv.namedWindow("hsv", cv.WINDOW_NORMAL)
# cv.namedWindow("mask", cv.WINDOW_NORMAL)
# cv.namedWindow("added", cv.WINDOW_NORMAL)
# cv.namedWindow("back", cv.WINDOW_NORMAL)
# cv.namedWindow("mask_inv", cv.WINDOW_NORMAL)
# cv.namedWindow("gray", cv.WINDOW_NORMAL)
#display the images
# cv.imshow("back", background)
# cv.imshow("mask_inv", mask_inv)
# cv.imshow("added",added_img)
# cv.imshow("mask", mask)
# cv.imshow("gray", gray)
# cv.imshow("hsv", hsv)
# cv.imshow("res", res)
# if cv.waitKey(0):
#     cv.destroyAllWindows()

# ================================================================= #

# CODE TO CHANGE ALL COLORS OF TO A CERTAIN TONE (PNG)

# import cv2
# import numpy as np
# img = cv2.imread('0039.png')
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
# mask_inv = cv2.bitwise_not(mask)
# new_val = 100 
# img[mask_inv > 0] = new_val
# cv2.imwrite('0040.png', img)

# ================================================================= #

# CODE TO CHANGE A CERTAIN PART OF THE 
# IMAGE TO A CERTAIN TONE (PNG)

# import cv2
# import numpy as np
# img = cv2.imread('0039.png')
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
# mask_inv = cv2.bitwise_not(mask)
# color_mask = cv2.merge([mask_inv]*3)
# result = cv2.bitwise_and(img, color_mask)
# result[mask > 0] = [100, 100, 100]
# cv2.imwrite('0040.png', result)

# ================================================================= #

# CODE TO CHANGE A CERTAIN PART OF THE IMAGE TO A CERTAIN 
# TONE, AND EXCLUDING TRANSPARENT AREAS (PNG)

from PIL import Image
def change_black_tone(image_path):
  with Image.open(image_path) as img:
    img = img.convert('RGBA')
    pixels = img.load()
    for i in range(img.size[0]):
      for j in range(img.size[1]):
        color = pixels[i, j]
        if color[3] > 0 and color[0] < 10 and color[1] < 10 and color[2] < 10:
          pixels[i, j] = (30, 30, 30, color[3]) 
    img.save('modified_' + image_path)

change_black_tone("0039.png")