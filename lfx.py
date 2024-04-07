from PIL import Image
import numpy as np
import glob
import cv2 as cv
import random
import math
import imageio

frame = []
frameLights = []
frameFinal = []
frameIdx = 0
for i in range(0, 10):
    count = 0
    folder = "/Users/ryanzrymiak/Downloads/OneDrive_2_2024-03-20/*"
    for file in glob.glob(folder):
        count+=1
        if count%2==0:
            img = Image.open(file)
            frame.append(np.asarray(img))
        #print((np.asarray(img)).shape)
    frameLights.append(frame)
    frame = []
    #myImage.show()
print(frameLights[0][3].shape) #first is frame number, second is shot/lighting number
#img = (2*frameList[0][0]+frameList[0][1]+frameList[0][2]+frameList[0][3])
img = cv.addWeighted(frameLights[0][0], 0.25, frameLights[0][1], 0.25, 0)
img2 = cv.addWeighted(frameLights[0][2], 0.25, frameLights[0][3], 0.25, 0)
finalImg = cv.addWeighted(img, 1, img2, 1, 0)
#finalImg = cv.convertScaleAbs(finalImg, 1, 1)
Image.fromarray(finalImg).show()

def lightning(frameLights, frameFinal, start, end):

    #make sure end is after start
    if end <= start:
        return frameFinal
    
    #randomly choose the frames where lightning will occur
    #update random choice parameters if necessary
    lightningIdx = []
    for i in range (0, ((end-start)//17)+1):
        lightningIdx.append(random.randint(start, end))

    gamma = [0] * 4
    for frameIdx in range(start, end):
        #initialize light gamma value, 0.25 by default
        for i in range(0, 4):
            gamma[i] = 0.25
        if(frameIdx in lightningIdx):
            gamma[random.randint(0, 3)] = random.uniform(2, 3)
        
        img = cv.addWeighted(frameLights[frameIdx][0], gamma[0], frameLights[frameIdx][1], gamma[1], 0)
        img2 = cv.addWeighted(frameLights[frameIdx][2], gamma[2], frameLights[frameIdx][3], gamma[3], 0)
        finalImg = cv.addWeighted(img, 1, img2, 1, 0)
        frameFinal.append(finalImg)
        #Image.fromarray(finalImg).show()

    return frameFinal

#assumed to start at day, should add bool flag if starting at night??
def daycycle(frameLights, frameFinal, start, end):

    #make sure end is after start
    if end <= start:
        return frameFinal
    
    gamma = [0] * 4
    for frameIdx in range(0, end-start):
        for i in range(0, 4):
            gamma[i] = 0.25*(0.4*(math.sin((frameIdx/math.pi)+(math.pi)/2)+1.5))
            #0.25 is default (daytime) gamma term
            #add by 1.5 to keep gamma >0
            #divide frameIdx by Pi to lengthen cycle across frames, adjust if necessary

        img = cv.addWeighted(frameLights[frameIdx][0], gamma[0], frameLights[frameIdx][1], gamma[1], 0)
        img2 = cv.addWeighted(frameLights[frameIdx][2], gamma[2], frameLights[frameIdx][3], gamma[3], 0)
        finalImg = cv.addWeighted(img, 1, img2, 1, 0)
        frameFinal.append(finalImg)
        Image.fromarray(finalImg).show()
    
    return frameFinal

#Image.fromarray(frameList[0][0]).show()
#frameFinal = lightning(frameLights, frameFinal, 0, 10)
frameFinal = daycycle(frameLights, frameFinal, 0, 10)
#print(len(frameFinal))
#Image.fromarray(frameFinal[0]).show()

#once frame lighting effects are finalized,
#export all frames to gif
def export_to_gif(frameFinal):
    #with imageio.get_writer('/Users/ryanzrymiak/Downloads/final.gif', mode='I') as writer:
    #    for frame in range(0,len(frameFinal)):
    #        print(frame)
    #        writer.append_data(frameFinal[frame])
    #    writer.close()
    imgs = [Image.fromarray(frameFinal[i]) for i in range(0,len(frameFinal))]
    imgs[0].save('/Users/ryanzrymiak/Downloads/final.gif', save_all=True, append_images=imgs[1:], duration=200, loop=0)

    print("Export to GIF complete\n")

#export_to_gif(frameFinal)