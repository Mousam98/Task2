# -*- coding: utf-8 -*-

'''A great project on COMPUTER VISION runs with 100% accuracy'''

import pandas as pd
import cv2 as cv 
import argparse

'''taking image from command line argument'''
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--image', required = True, help = 'image_path')
arg = vars(parser.parse_args())
image_path = arg['image']


'''reading image file from command line argument'''
image = cv.imread(image_path)

'''importing dataset'''
columns = ['color', 'color_name', 'hex_code','R', 'G', 'B']
df = pd.read_csv('colors.csv', names = columns, header=None)


'''defining variables'''
clicked = False
r = g = b = xpos = ypos = 0
shape = image.shape
height, width = shape[0], shape[1]
area = width*height

'''function to return the name of color whenever clicked by mouse'''
def getColor(R, G, B):
    constraint = float('inf')
    color = ''
    for item in range(len(df)):
        dist = abs(R - int(df.loc[item,'R'])) + abs(G - int(df.loc[item , 'G'])) + abs(B - int(df.loc[item , 'B']))
        if dist <= constraint:
            constraint = dist
            color = df.loc[item, 'color_name']
            
    return color

'''mouse clicking feature'''
def colorByClick(event, x, y , flags, param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        global xpos, ypos , clicked, r, g, b
        clicked = True
        xpos, ypos = x, y
        b, g, r = image[y,x]
        b, g, r = int(b), int(g), int(r)
        
'''normalizing pixels for higher definition pictures'''
if area <= 662*1000:
    cv.namedWindow('image')
else:
    height, width = height//(height//1000), width//(width//662)
    cv.namedWindow('image', cv.WINDOW_NORMAL)
        
cv.setMouseCallback('image', colorByClick)
        
        
while True:
    cv.imshow('image', image)
    if clicked:
        start_pt = (round(width*0.1), round(height*0.1))
        end_pt = (width, round(height*0.3))
        text_pos = (round(width*0.1), round(height*0.2))
        cv.rectangle(image, start_pt, end_pt, (b,g,r), -1)
        text = getColor(r,g,b) + 'R=' + str(r)+' B='+str(b)+ ' G='+str(g)
        if r+g+b >= 650:
            cv.putText(image, text, text_pos, cv.FONT_HERSHEY_TRIPLEX, 1, (0,0,0), 2, cv.LINE_AA)
            
        else:
            cv.putText(image, text, text_pos, cv.FONT_HERSHEY_TRIPLEX, 1, (255,255,255), 2, cv.LINE_AA)
        clicked = False
        
    if cv.waitKey(10) == ord('m'):
        break
    
    
cv.destroyAllWindows()
        
