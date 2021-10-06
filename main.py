import cv2

img = cv2.imread("galaxy.jpg", 0)

print(type(img))
print(img.shape)
print(img.ndim)

w = img.shape[0] / 2
h = img.shape[1] / 2

resized = cv2.resize(img, (int(h),int(w)))

# cv2.imshow("Galaxy", resized)
cv2.imwrite("Galaxy_resized.jpg", resized)

cv2.waitKey(0)
