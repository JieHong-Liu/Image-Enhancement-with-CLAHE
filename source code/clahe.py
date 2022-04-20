import cv2
import numpy as np

from matplotlib import pyplot as plt


def split_RGBThreeChannel(img):
    (B, G, R) = cv2.split(img)  # 3 channel

    # make all zeros channel
    zeros = np.zeros(img.shape[:2], dtype=np.uint8)

    # print("R channel:")
    # show_img(merge_RGBThreeChannel(R=R, G=zeros, B=zeros))
    # print("G channel:")
    # show_img(merge_RGBThreeChannel(R=zeros, G=G, B=zeros))
    # print("B channel:")
    # show_img(merge_RGBThreeChannel(R=zeros, G=zeros, B=B))

    return R, G, B


def merge_RGBThreeChannel(R, G, B):
    img = cv2.merge([B, G, R])

    return img


def show_histogram(img):
    # 畫出 RGB 三種顏色的分佈圖
    color = ('b', 'g', 'r')
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 5))
    for idx, color in enumerate(color):
        histogram = cv2.calcHist([img], [idx], None, [256], [0, 256])
        plt.plot(histogram, color=color)
        plt.xlim([0, 256])

    plt.show()


def localEnhancement(img):
    sharped_img = np.zeros(img.shape, np.uint8)
    mask = np.zeros(img.shape, np.uint8)
    kernel_size = 3
    blur_gray = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):

            tmp = int(img[i, j])-int(blur_gray[i, j])
            if(tmp < 0):
                mask[i, j] = 0
            else:
                mask[i, j] = img[i, j]-blur_gray[i, j]
            tmp = int(img[i, j])+int(mask[i, j])
            if(tmp > 255):
                sharped_img[i, j] = 255
            else:
                sharped_img[i, j] = img[i, j]+mask[i, j]
    # print(sharped_img)
    return sharped_img


# read image
img = cv2.imread('butterfly.jpg')
# print(img.shape)
# convert the image into grayscale before doing histogram equalization
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
H, S, V = cv2.split(hsv)

# image equalization
# equalize_img = cv2.equalizeHist(gray_img)

# do local enhancement
V_local = localEnhancement(V)
cv2.imshow("V_local", V_local)

# create clahe image
clahe = cv2.createCLAHE()
V_clahe_img = clahe.apply(V_local)
clahe_img = cv2.merge([H, S, V_clahe_img])

# convert back to rgb
output_img = cv2.cvtColor(clahe_img, cv2.COLOR_HSV2BGR)


# show image
cv2.imshow("image", img)
# cv2.imwrite("equal_image.jpg", equalize_img)
cv2.imwrite("output_img.jpg", output_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# # plot image histogram
# plt.hist(gray_img.ravel(), 256, [0, 255], label='original image')
# plt.hist(equalize_img.ravel(), 256, [0, 255], label='equalize image')
# plt.hist(clahe_img.ravel(), 256, [0, 255], label='clahe image')
# plt.legend()
# plt.show()
