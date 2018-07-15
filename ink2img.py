'''
This code snap id for generating img from inkml files and it's odd to see no reliable tools to convert inkml file to img, thus this file is meaningful
This project is encountered during dataset generation in MSRA
'''
import xml.etree.ElementTree
import numpy as np
import os
from scipy.misc import imsave
import cv2
import math
from lxml import etree

for f in os.listdir('C:\\Users\\Administrator\\Desktop\\dataset\\test2014inkml\\'):
    
    filepath = 'C:\\Users\\Administrator\\Desktop\\dataset\\test2014inkml\\' + f
    name = f.split('.')[0]
    print(name)
	# below are typical template for parsing inkml file
    root = xml.etree.ElementTree.parse(filepath).getroot()
    strokes = sorted(root.findall('{http://www.w3.org/2003/InkML}trace'), key=lambda child: child.attrib['id'])  # this is to extract strokes
    recording = []
    time = 0
    for stroke in strokes:
            stroke = stroke.text.strip().split(',')
            stroke = [point.strip().split(' ') for point in stroke]
            if len(stroke[0]) == 3:
                # if the name is TrainData the size is much larger than normal
                if name.startswith('TrainData') or name.startswith('2009'):
                    stroke = [{'x': float(x), 'y': float(y), 'time': float(t)} for x, y, t in stroke]
                else:
                    stroke = [{'x': float(x), 'y': float(y), 'time': float(t)} for x, y, t in stroke]
            else:
                if name.startswith('TrainData') or name.startswith('2009'):
                    stroke = [{'x': float(x), 'y': float(y)} for x, y in stroke]
                else:
                    stroke = [{'x': float(x), 'y': float(y)} for x, y in stroke]
                new_stroke = []
                for p in stroke:
                    new_stroke.append({'x': p['x'], 'y': p['y']})
                stroke = new_stroke
            recording.append(stroke)
    
    strokes = []
    
    for r in recording:
    	strokes.append(r)
    
    
    x = []
    y = []
    
    max_x = max([pair['x'] for s in strokes for pair in s])
    min_x = min([pair['x'] for s in strokes for pair in s])
    max_y = max([pair['y'] for s in strokes for pair in s])
    min_y = min([pair['y'] for s in strokes for pair in s])
    
    mean_dis = 0
    point_num = 1

    for s in strokes:
        pre_x = s[0]['x']
        pre_y = s[0]['y']
        for pair in s:
            if pair['x'] == pre_x and pair['y'] == pre_y:
                continue
            delta_x = pair['x'] - pre_x
            delta_y = pair['y'] - pre_y
            mean_dis += math.sqrt(delta_x * delta_x + delta_y * delta_y)
            pre_x = pair['x']
            pre_y = pair['y']
            point_num += 1

    mean_dis /= point_num

    scale = 2.0/mean_dis        # this part is to calculate scale rate for images according to distance between pixels which is very useful, because some files have huge size due to long distance

    canvas = np.zeros(( int((max_y - min_y) * scale + 20), int((max_x - min_x) * scale + 20)))

    lineThickness = 2

    for s in strokes:
        x = [pair['x'] for pair in s]
        y = [pair['y'] for pair in s]
        if len(x) == 1:
            x1 = int((x[0] - min_x) * scale + 10)
            y1 = int((y[0] - min_y) * scale + 10)
            #print('x ', x1, 'y ', y1)
            canvas[y1 - 1: y1 + 2, x1 - 1: x1 + 2] = 255
            continue
        for i in range(len(x) - 1):
            x1 = int((x[i] - min_x) * scale + 10)
            y1 = int((y[i] - min_y) * scale + 10)
            x2 = int((x[i + 1] - min_x) * scale + 10)
            y2 = int((y[i + 1] - min_y) * scale + 10)
            #print('x1 ', x1, 'y1 ', y1, 'x2 ', x2, 'y2 ', y2)
            canvas = cv2.line(canvas, (x1, y1), (x2, y2), (255, 255, 255), lineThickness)
    print(canvas.shape)
    
    imsave('2014test\\' + name + '.bmp', canvas)
