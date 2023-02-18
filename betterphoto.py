import cv2
import sys
import numpy as np
from numpy.lib.function_base import select


bufferSize = 3 # frames

print("CMRR photography. Keys to use:")
print("I, O, K, L: change lightness and darkness")
print("N, M: to change buffer size.")
print("P: to take photo")
print("-----------------")

print('init cap')
luminance = 1.0
darkinance = 1.0

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(3, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


print('reading first frame')
_, frame_0 = cap.read()
print('converting frame to float')
frame_x = np.float32(frame_0)
frame_h, frame_w, number_of_channels = np.shape(frame_0)
print('allocating memory')
buffer = np.zeros((bufferSize, frame_h, frame_w, number_of_channels), np.float32)
print('starting loop')

i = 0
while True:
    i += 1
    n = i % bufferSize
    _, frame_now = cap.read()
    try:
        buffer[n] = np.float32(frame_now)
        frame_x -= frame_x
        for j in range(bufferSize):
            x = (n + j) % bufferSize
            frame_x += buffer[x]

    except IndexError:
        print(np.shape(buffer))
        print(np.shape(buffer))

    frame_x /= bufferSize
    c = cv2.flip(frame_x, 1)

    c *= luminance
    c[c<0] = 0
    c[c>255] = 255
    c = 255 - c
    c *= darkinance
    c = 255 - c
    c[c<0] = 0
    c[c>255] = 255
    
    # print(np.average(frame_x))
    cv2.imshow('x', np.uint8(c))
    a = cv2.waitKey(1)

    if a == 113:
        exit(0)
    elif a == ord('p'):
        cv2.imwrite(f'a{i}.jpg', c)
        print(f'image saved: ./a{i}.jpg')
    elif a == ord('o'):
        luminance += 0.1
    elif a == ord('i'):
        luminance -= 0.1
    elif a == ord('l'):
        darkinance += 0.1
    elif a == ord('k'):
        darkinance -= 0.1
    elif a == ord('m'):
        bufferSize += 1
        if np.shape(buffer)[0] < bufferSize:
            buffer = np.append(buffer, np.array([np.float32(frame_now)]), 0)
    elif a == ord('n'):
        bufferSize -= 1
        if bufferSize <= 0:
            bufferSize = 1
    
    if a != -1:
        print(f'luminance = {"{:.1f}".format(luminance)}  darkinance="{"{:.1f}".format(darkinance)} bufferSize={bufferSize}')

