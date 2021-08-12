import cv2
import numpy as np
from PIL import Image

video = cv2.VideoCapture('episode1.mp4')


def calcDiferenc(frame, lastFrame):
    absDifference = cv2.absdiff(frame, lastFrame).astype(np.uint8)
    percentage = np.sum(absDifference)/lastFrame.shape[0]/lastFrame.shape[1]/3.
    return percentage


def detectTransition(frame, currentFrameNumber, lastFrame, lastTransitionFrameNumber, threshold):
    if lastFrame is not None:
        dif = calcDiferenc(frame, lastFrame)
        # if dif > 30:
        # print('threshold: ' + str(dif) +
        #      'frame: ' + str(currentFrameNumber))
        if dif >= threshold and currentFrameNumber - lastTransitionFrameNumber > 30:
            return True
        return False
    else:
        print('==========')
        return False


def formatedImg(npImg):
    imageFormated = cv2.cvtColor(npImg, cv2.COLOR_BGR2RGB)
    return Image.fromarray(imageFormated)


def main():
    threshold = 50
    lastFrame = None
    lastTransitionFrameNumber = 0
    gif = []

    while True:
        (rv, img) = video.read()

        if not rv:
            break

        currentFrameNumber = video.get(cv2.CAP_PROP_POS_FRAMES)

        if detectTransition(img, currentFrameNumber, lastFrame, lastTransitionFrameNumber, threshold):
            #cv2.imwrite(str(video.get(cv2.CAP_PROP_POS_FRAMES)) + '.jpg', img)
            if len(gif) > 0:
                print('===== GIF CRIADO =====')
                gif[0].save(fp='frames/gif' + str(lastTransitionFrameNumber) + '.gif',
                            format='GIF', save_all=True, append_images=gif)
                gif = []
                gif.append(formatedImg(img))

            lastTransitionFrameNumber = currentFrameNumber
        else:
            print('Adicionando frame')
            gif.append(formatedImg(img))

        lastFrame = img


main()
