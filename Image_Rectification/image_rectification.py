# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 21:32:25 2018

@author: Jo-Yao Hsu
"""

import numpy as np
from decimal import Decimal
import cv2
import glob
import time

def undistort(filename,**args):
    starttime = time.clock() 
    ori_im = cv2.imread(filename)
    row = np.size(ori_im,0)
    column = np.size(ori_im,1)
    rcorr = np.zeros((row*column,1))
    ccorr = np.zeros((row*column,1))
    i = np.arange(0,row,1)
    j = np.arange(0,column,1)
    i,j = np.meshgrid(i,j)
    x=(-0.5*p)*(1+float(column))+p*(j+1)
    y=(0.5*p)*(1+float(row))-p*(i+1)
    r=(x**2+y**2)**0.5  #radius
    dx = x0+a1*(r**2-r0**2)*x+a2*(r**4-r0**4)*x+a3*(r**6-r0**6)*x \
        +b1*x+b2*y \
        +(c1*(x**2-y**2)+c2*x**2*y**2+c3*(x**4-y**4))*x/c \
        +d1*x*y+d2*y**2+d3*x**2*y+d4*x*y**2+d5*x**2*y**2
    dy = y0+a1*(r**2-r0**2)*y+a2*(r**4-r0**4)*y+a3*(r**6-r0**6)*y \
        +(c1*(x**2-y**2)+c2*x**2*y**2+c3*(x**4-y**4))*y/c \
        +d6*x*y+d7*x**2+d8*x**2*y+d9*x*y**2+d10*x**2*y**2
    xcorr = x + dx
    ycorr = y + dy
    rcorr = (0.5*p*(1+float(row))-ycorr)/p-1
    ccorr = (0.5*p*(1+float(column))+xcorr)/p-1
    color_final = cv2.remap(ori_im, np.float32(ccorr.T-int(x0/p)), np.float32(rcorr.T-int(y0/p)), cv2.INTER_CUBIC)
    cv2.imwrite(filename.split('.')[0] + "_cal.tif", color_final)
    print('%s processed' %(filename))
    endtime = time.clock()
    print('%.2f sec' %(endtime-starttime))
    return color_final
    

if __name__ == '__main__':
    int_file = []
    p = 0.0053; #pixel size
    intf = open("ORIMA_interior.txt",'r') #interior parameter, use read_ORIMA_exterior.py output data
    r0 = 0.0
    for line in intf.readlines():
        line = line.strip().split(' ')
        int_file.append(line[1])
        exec("%s = %g" % (line[0],Decimal(line[1])))
    for i in glob.glob('*.tif'):
        undistort(i)
