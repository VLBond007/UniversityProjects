import cv2

ext = '.jpg'

img = cv2.imread("image.jpg")

blue = img[:, :, 0]
green = img[:, :, 1]
red = img[:, :, 2]

for rgb, color in zip((red, green, blue), ('красный', 'зеленый', 'синий')):
    print('Печатаем', color, 'цвет')
    cv2.imwrite(color + ext, rgb)