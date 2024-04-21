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
'''
for i in range(0, 10):
    count = 1
    folder = "/Users/ryanzrymiak/Downloads/OneDrive_2_2024-03-20/*"
    for file in sorted(glob.glob(folder)):
        #print(file)
        if count%2==0:
            img = Image.open(file)
            frame.append(np.asarray(img))
        #print((np.asarray(img)).shape)
        count+=1
    frameLights.append(frame)
    frame = []
    #myImage.show()
print(frameLights[0][3].shape) #first is frame number, second is shot/lighting number
#img = (2*frameList[0][0]+frameList[0][1]+frameList[0][2]+frameList[0][3])
img = cv.addWeighted(frameLights[0][0], 0.25, frameLights[0][1], 0.25, 0)
img2 = cv.addWeighted(frameLights[0][2], 0.25, frameLights[0][3], 0.25, 0)
finalImg = cv.addWeighted(img, 1, img2, 1, 0)
#finalImg = cv.convertScaleAbs(finalImg, 1, 1)
#Image.fromarray(finalImg).show()
'''

folder = "/Users/ryanzrymiak/Downloads/camera8/frame-*"
light1 = []
light2 = [] 
light3 = [] 
count = 0
for file in sorted(glob.glob(folder)):
    print(count, file)
    if count < 59:
        img = Image.open(file)
        light1.append(np.asarray(img))
    elif count < 59*2:
        img = Image.open(file)
        light2.append(np.asarray(img))
    elif count < 59*3:
        img = Image.open(file)
        light3.append(np.asarray(img))
    count += 1
#for i in range(0,59):
#    frameLights.append(frame[i])
#print(frame.shape)

#Image.fromarray(light1[0]).show()
#Image.fromarray(light2[0]).show()
#Image.fromarray(light3[0]).show()

#img = cv.addWeighted(frameLights[0][0], 0.33, frameLights[0][1], 0.33, 0)
#finalImg = cv.addWeighted(img, 1, frameLights[0][2], 0.33, 0)
#Image.fromarray(finalImg).show()

img = cv.addWeighted(light1[0], 0.33, light2[0], 0.33, 0)
finalImg = cv.addWeighted(img, 1, light3[0], 0.33, 0)
#Image.fromarray(finalImg).show()

def lightning(light1, light2, light3, frameFinal, start, end):

    #make sure end is after start
    if end <= start:
        return frameFinal
    
    #randomly choose the frames where lightning will occur
    #update random choice parameters if necessary
    lightningIdx = []
    for i in range (0, ((end-start)//17)+1):
        lightningIdx.append(random.randint(start, end))

    gamma = [0] * 3#4
    for frameIdx in range(start, end):
        #initialize light gamma value, 0.25 by default
        for i in range(0, 3):#4):
            gamma[i] = 0.33#0.25
        if(frameIdx in lightningIdx):
            gamma[random.randint(0, 2)] = random.uniform(1.5, 2.25)
        
        #img = cv.addWeighted(frameLights[frameIdx][0], gamma[0], frameLights[frameIdx][1], gamma[1], 0)
        #img2 = cv.addWeighted(frameLights[frameIdx][2], gamma[2], frameLights[frameIdx][3], gamma[3], 0)
        #finalImg = cv.addWeighted(img, 1, img2, 1, 0)
        img = cv.addWeighted(light1[frameIdx], gamma[0], light2[frameIdx], gamma[1], 0)
        finalImg = cv.addWeighted(img, 1, light3[frameIdx], gamma[2], 0)
        frameFinal.append(finalImg)
        #Image.fromarray(finalImg).show()

    return frameFinal

#assumed to start at day, should add bool flag if starting at night??
def daycycle(light1, light2, light3, frameFinal, start, end):

    #make sure end is after start
    if end <= start:
        return frameFinal
    
    gamma = [0] * 3#4
    for frameIdx in range(0, end-start):
        for i in range(0, 3):#4):
            gamma[i] = 0.33*(0.4*(math.sin((frameIdx/math.pi)+(math.pi)/2)+1.5))
            #0.25 is default (daytime) gamma term
            #add by 1.5 to keep gamma >0
            #divide frameIdx by Pi to lengthen cycle across frames, adjust if necessary

        #img = cv.addWeighted(frameLights[frameIdx][0], gamma[0], frameLights[frameIdx][1], gamma[1], 0)
        #img2 = cv.addWeighted(frameLights[frameIdx][2], gamma[2], frameLights[frameIdx][3], gamma[3], 0)
        #finalImg = cv.addWeighted(img, 1, img2, 1, 0)
        img = cv.addWeighted(light1[frameIdx], gamma[0], light2[frameIdx], gamma[1], 0)
        finalImg = cv.addWeighted(img, 1, light3[frameIdx], gamma[2], 0)
        frameFinal.append(finalImg)
        #frameFinal.append(finalImg)
        #Image.fromarray(finalImg).show()
    
    return frameFinal

def daycycle_v2(light1, light2, light3, frameFinal, start, end):

    #make sure end is after start
    if end <= start:
        return frameFinal
    
    gamma = [0] * 3#4
    for i in range(0, 3):#4):
        gamma[i] = 0.33#0.25
    for frameIdx in range(0, end-start):
        #for i in range(0, 3):#4):
        #    gamma[i] = 0.33*(0.4*(math.sin((frameIdx/math.pi)+(math.pi)/2)+1.5))
            #0.25 is default (daytime) gamma term
            #add by 1.5 to keep gamma >0
            #divide frameIdx by Pi to lengthen cycle across frames, adjust if necessary

        #img = cv.addWeighted(frameLights[frameIdx][0], gamma[0], frameLights[frameIdx][1], gamma[1], 0)
        #img2 = cv.addWeighted(frameLights[frameIdx][2], gamma[2], frameLights[frameIdx][3], gamma[3], 0)
        #finalImg = cv.addWeighted(img, 1, img2, 1, 0)
        img = cv.addWeighted(light1[frameIdx], gamma[0], light2[frameIdx], gamma[1], 0)
        combinedImg = cv.addWeighted(img, 1, light3[frameIdx], gamma[2], 0)

        r,g,b = cv.split(combinedImg)
        r[:] = r[:]*(0.5*(math.sin((frameIdx/math.pi)+(math.pi)/2)+1))
        g[:] = g[:]*(0.25*(math.sin((frameIdx/math.pi)+(math.pi)/2)+3))
        b[:] = b[:]*(0.1*(math.sin((frameIdx/math.pi)+(math.pi)/2)+9))
        finalImg = cv.merge((r,g,b))

        frameFinal.append(finalImg)
        #frameFinal.append(finalImg)
        #Image.fromarray(finalImg).show()
    print(255*(0.5*(math.sin((59/math.pi)+(math.pi)/2)+1)))
    print(b)
    return frameFinal

def two_cycle(light1, light2, light3, frameFinal, start, end, initLight, dir):

    if end <= start:
        return frameFinal
    
    if dir==0: #clockwise
        #nextLight = initLight+1
        #if(nextLight > 4):
        #    nextLight = 1
        if(initLight == 1):
            currLight = light1
            nextLight = light3
        if(initLight == 2):
            currLight = light2
            nextLight = light1
        if(initLight == 3):
            currLight = light3
            nextLight = light2
        #if(initLight == 4):
        #    nextLight = 3

    elif dir==1: #counter-clockwise
        #nextLight = initLight-1
        #if(nextLight < 1):
        #    nextLight = 4
        if(initLight == 1):
            currLight = light1
            nextLight = light2
        if(initLight == 2):
            currLight = light2
            nextLight = light3
        if(initLight == 3):
            currLight = light3
            nextLight = light1
        #if(initLight == 4):
        #    nextLight = 1

    delta = 1/((end-start)-1)
    
    alpha = 1
    gamma = [0] * 2
    for frameIdx in range(0, end-start):
        gamma[0] = alpha
        gamma[1] = (1-alpha)
        finalImg = cv.addWeighted(currLight[frameIdx], gamma[0], nextLight[frameIdx], gamma[1], 0)
        frameFinal.append(finalImg)
        alpha -= delta

    return frameFinal
    
def four_cycle(frameLights, frameFinal, start, end, initLight, dir):

    if end <= start:
        return frameFinal
    
    frameFinal = (two_cycle(frameLights, frameFinal, start, end, 1, dir))
    frameFinal = (two_cycle(frameLights, frameFinal, start, end, 4, dir))
    frameFinal = (two_cycle(frameLights, frameFinal, start, end, 3, dir))
    frameFinal = (two_cycle(frameLights, frameFinal, start, end, 2, dir))
    
    return frameFinal

def police_lights(light1, light2, light3, frameFinal, start, end, red, blue):

    #make sure end is after start
    if end <= start:
        return frameFinal
    
    if red == 1:
        redLight = light1
    if red == 2:
        redLight = light2
    if red == 3:
        redLight = light3
    if blue == 1:
        blueLight = light1
    if blue == 2:
        blueLight = light2
    if blue == 3:
        blueLight = light3

    gamma = [0] * 3#4
    for frameIdx in range(start, end):
        #initialize light gamma value, 0.25 by default
        for i in range(0, 3):#4):
            gamma[i] = 0.33#0.25
        #if(frameIdx in lightningIdx):
        #    gamma[random.randint(0, 3)] = random.uniform(2, 3)
        
        if(frameIdx > 2):
            r1,g1,b1 = cv.split(redLight[frameIdx])
            r_val = math.ceil(93*(math.sin((4*frameIdx/math.pi)+(math.pi/2)))+93)
        #print(r_val)
            lim = 255-r_val
            #tmp = cv.addWeighted(light1[frameIdx], 0.33, light2[frameIdx], 0.33, 0)
            #grayImg = cv.addWeighted(tmp, 1, light3[frameIdx], 0.33, 0)
            grayImg = cv.cvtColor(redLight[frameIdx], cv.COLOR_BGR2GRAY)
            #r1[grayImg <= lim] += r_val
            r1[grayImg > lim] = 255
            #g1[grayImg > lim] /= 2 
            #b1[grayImg > lim] /= 2
            #b1[:] = 0
            #g1[:] = 0
            #g1[grayImg > lim] -= r_val
            #g1[g1 < 0] = 0
            #b1[grayImg > lim] -= r_val
            #b1[b1 < 0] = 0
        #r1[r1 <= lim] += r_val
        #lim = 255+r_val
        #b1[b1 > lim] -= r_val
        #b1[b1 <= lim] = 0
        #lim = 255+r_val
        #g1[g1 > lim] -= r_val
        #g1[g1 <= lim] = 0
        #g1[:] = 0
        #b1[:] = 0
            redLight[frameIdx] = cv.merge((r1,g1,b1))

        r2,g2,b2 = cv.split(blueLight[frameIdx])
        b_val = math.ceil(93*(math.sin((4*frameIdx/math.pi)-(math.pi/2)))+93)
        lim = 255-b_val
        #tmp = cv.addWeighted(light1[frameIdx], 0.33, light2[frameIdx], 0.33, 0)
        #grayImg = cv.addWeighted(tmp, 1, light3[frameIdx], 0.33, 0)
        grayImg = cv.cvtColor(blueLight[frameIdx], cv.COLOR_BGR2GRAY)
        #b2[grayImg <= lim] += b_val
        b2[grayImg > lim] = 255

        #r2[grayImg > lim] /= 2
        #g2[grayImg > lim] /= 2
        #b2[b2 <= lim] += b_val
        blueLight[frameIdx] = cv.merge((r2,g2,b2))


        if red == 1:
            light1[frameIdx] = redLight[frameIdx]
        if red == 2:
            light2[frameIdx] = redLight[frameIdx]
        if red == 3:
            light3[frameIdx] = redLight[frameIdx]
        if blue == 1:
            light1[frameIdx] = blueLight[frameIdx]
        if blue == 2:
            light2[frameIdx] = blueLight[frameIdx]
        if blue == 3:
            light3[frameIdx] = blueLight[frameIdx]
        #img = cv.addWeighted(frameLights[frameIdx][0], gamma[0], frameLights[frameIdx][1], gamma[1], 0)
        #img2 = cv.addWeighted(frameLights[frameIdx][2], gamma[2], frameLights[frameIdx][3], gamma[3], 0)
        #finalImg = cv.addWeighted(img, 1, img2, 1, 0)
        #finalImg = frameLights[frameIdx][0]
        img = cv.addWeighted(light1[frameIdx], gamma[0], light2[frameIdx], gamma[1], 0)
        finalImg = cv.addWeighted(img, 1, light3[frameIdx], gamma[2], 0)
        frameFinal.append(finalImg)
    #Image.fromarray(frameLights[0][0][:,:,0]).show()
    Image.fromarray(grayImg).show()

    return frameFinal

def disco(light1, light2, light3, frameFinal, start, end):

    #make sure end is after start
    if end <= start:
        return frameFinal
    
    #randomly choose the frames where lightning will occur
    #update random choice parameters if necessary
    gamma = [0] * 3#4
    for i in range(0, 3):#4):
        gamma[i] = 0.33#0.25
    for frameIdx in range(start, end):

        #img = cv.addWeighted(frameLights[frameIdx][0], gamma[0], frameLights[frameIdx][1], gamma[1], 0)
        #img2 = cv.addWeighted(frameLights[frameIdx][2], gamma[2], frameLights[frameIdx][3], gamma[3], 0)
        #combinedImg = cv.addWeighted(img, 1, img2, 1, 0)
        img = cv.addWeighted(light1[frameIdx], gamma[0], light2[frameIdx], gamma[1], 0)
        combinedImg = cv.addWeighted(img, 1, light3[frameIdx], gamma[2], 0)
        r,g,b = cv.split(combinedImg)
        if(frameIdx % 12 == 0 or frameIdx % 12 == 1):
            g[:] = 0 
            b[:] = 0
            finalImg = cv.merge((r,g,b))
        if(frameIdx % 12 == 2 or frameIdx % 12 == 3):
            b[:] = 0 
            finalImg = cv.merge((r,g,b))
        if(frameIdx % 12 == 4 or frameIdx % 12 == 5):
            r[:] = 0 
            finalImg = cv.merge((r,g,b))
        if(frameIdx % 12 == 6 or frameIdx % 12 == 7):
            g[:] = 0 
            finalImg = cv.merge((r,g,b))
        if(frameIdx % 12 == 8 or frameIdx % 12 == 9):
            r[:] = 0 
            g[:] = 0 
            finalImg = cv.merge((r,g,b))
        if(frameIdx % 12 == 10 or frameIdx % 12 == 11):
            r[:] = 0 
            b[:] = 0 
            finalImg = cv.merge((r,g,b))
        #r = 0, greenish-blue, looks like underwater, could make this an effect?
        #g = 0, purple
        #b = 0, yellowish-green
        #r,b = 0, green, looks like night vision goggles, coulg make this an effect?
        #r,g = 0, blue
        #g,b = 0, red            

        frameFinal.append(finalImg)
        #Image.fromarray(r).show()

    return frameFinal

def underwater(light1, light2, light3, frameFinal, start, end): #actually looks more like a nighttime effect

    #make sure end is after start
    if end <= start:
        return frameFinal
    
    #randomly choose the frames where lightning will occur
    #update random choice parameters if necessary
    gamma = [0] * 3#4
    for i in range(0, 3):#4):
        gamma[i] = 0.33#0.25
    for frameIdx in range(start, end):

        #img = cv.addWeighted(frameLights[frameIdx][0], gamma[0], frameLights[frameIdx][1], gamma[1], 0)
        #img2 = cv.addWeighted(frameLights[frameIdx][2], gamma[2], frameLights[frameIdx][3], gamma[3], 0)
        #combinedImg = cv.addWeighted(img, 1, img2, 1, 0)
        img = cv.addWeighted(light1[frameIdx], gamma[0], light2[frameIdx], gamma[1], 0)
        combinedImg = cv.addWeighted(img, 1, light3[frameIdx], gamma[2], 0)
        r,g,b = cv.split(combinedImg)
        r[:] = 0
        g[:] = g[:]/2
        finalImg = cv.merge((r,g,b))
        #r = 0, greenish-blue, looks like underwater, could make this an effect?
        #g = 0, purple
        #b = 0, yellowish-green
        #r,b = 0, green, looks like night vision goggles, coulg make this an effect?
        #r,g = 0, blue
        #g,b = 0, red            

        frameFinal.append(finalImg)
        #Image.fromarray(r).show()

    return frameFinal

#Image.fromarray(frameList[0][0]).show()
#frameFinal = lightning(light1, light2, light3, frameFinal, 0, 59)
#frameFinal = two_cycle(light1, light2, light3, frameFinal, 0, 10, 3, 0)
#frameFinal = four_cycle(frameLights, frameFinal, 0, 10, 1, 0)
#frameFinal = daycycle(light1, light2, light3, frameFinal, 0, 59)
frameFinal = daycycle_v2(light1, light2, light3, frameFinal, 0, 59)
#frameFinal = police_lights(light1, light2, light3, frameFinal, 0, 59, 1, 2)
#frameFinal = disco(light1, light2, light3, frameFinal, 0, 20)
#frameFinal = underwater(light1, light2, light3, frameFinal, 0, 59)
#print(len(frameFinal))
#Image.fromarray(frameFinal[0]).show()

#once frame lighting effects are finalized,
#export all frames to gif
def export_to_vid(frameFinal):
    #with imageio.get_writer('/Users/ryanzrymiak/Downloads/final.gif', mode='I') as writer:
    #    for frame in range(0,len(frameFinal)):
    #        print(frame)
    #        writer.append_data(frameFinal[frame])
    #    writer.close()
    #imgs = [Image.fromarray(frameFinal[i]) for i in range(0,len(frameFinal))]
    #imgs[0].save('/Users/ryanzrymiak/Downloads/final.gif', save_all=True, append_images=imgs[1:], duration=200, loop=0)
    video = cv.VideoWriter('/Users/ryanzrymiak/Downloads/final.mp4', cv.VideoWriter_fourcc(*'mp4v'), 10, (4096, 2160))

    for frame in range(0, len(frameFinal)):
        #opencv is on some crack and uses BRG colour format for some
        #unimaginable reason
        video.write(cv.cvtColor(frameFinal[frame], cv.COLOR_RGB2BGR))

    video.release()
    cv.destroyAllWindows()

    print("Export to video complete\n")

export_to_vid(frameFinal)
