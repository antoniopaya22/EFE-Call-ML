import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import os
import csv


interventors = {}
# Recorded by professor [66, 52, 53]
# speak_color = [66, 52, 53]
# Recorded by student [98, 68, 67]
speak_color = [98, 68, 67]
# Intervals with threshold over speak color
th = 15
c0 = [speak_color[0] - th, speak_color[0] + th]
c1 = [speak_color[1] - th, speak_color[1] + th]
c2 = [speak_color[2] - th, speak_color[2] + th]

point_height = 8 # depends on resolution


def number_of_interventions_in_frame(frame):
    global speak_color
    global point_height
    image = cv2.imread(frame)
    height, width, channels = image.shape

    count = 0
    i = 0
    last_purple = False
    start_point_speaker = 0
    last_point_speaker = 0
    frame_interv = []
    while i < width:
        color = image[point_height, i]
        purple = is_purple(color)
        if last_purple == False and purple: # Take first appearance of purple color for one user
            last_purple = True
            start_point_speaker = i
            last_point_speaker = i
        elif last_purple == True and purple: # Take last appearance of purple color for one user
            last_point_speaker = i
        elif purple == False and last_purple == True: # Save intervention
            difference = last_point_speaker - start_point_speaker
            if difference > 5:  # Avoid false positives
                count += 1  
                frame_interv.append(get_line_speaker(image, start_point_speaker, last_point_speaker)) # Get interventor ID
            start_point_speaker = 0
            last_point_speaker = 0
            last_purple = False
        i += 2
    frame_number = int(frame.split('\\')[-1].split('.')[0][5:])
    return [frame_number, count, frame_interv]


def are_near_pixel_colors(color_a, color_b):
    return are_near_single_colors(color_a[0], color_b[0]) and are_near_single_colors(color_a[1], color_b[1]) and are_near_single_colors(color_a[2], color_b[2])


def are_near_single_colors(color_a, color_b):
    return color_b -8 <= color_a <= color_b +8


def is_grey(color):
    # Intervals with threshold
    th = 5
    c0 = [color[0] - th, color[0] + th]
    c1 = [color[1] - th, color[1] + th]
    c2 = [color[2] - th, color[2] + th]
    # Get overlap between intervals
    i_01 = min(c0[1], c1[1]) - max(c0[0], c1[0])
    i_02 = min(c0[1], c2[1]) - max(c0[0], c2[0])
    i_12 = min(c1[1], c2[1]) - max(c1[0], c2[0])
    # If there is overlap in every interval, color is grey
    return i_01 > 0 and i_02 > 0 and i_12 > 0


def is_purple(color):
    global speak_color
    global c0
    global c1
    global c2
    # Is color in intervals
    i_0 = c0[0] <= color[0] <= c0[1]
    i_1 = c1[0] <= color[1] <= c1[1]
    i_2 = c2[0] <= color[2] <= c2[1]
    # If color is intervals, color is purple
    return i_0 and i_1 and i_2


def get_line_speaker(image, start, last):
    global speak_color
    global point_height
    global interventors
    pixel_line = []
    height, width, channels = image.shape
    y = 30 # int(point_height + height/4)
    interval = 15
    for i in range(start, last):
        color = image[y, i]
        pixel_line.append(list(color))
    
    str_pixel_line = str(list(pixel_line))
    speaker_id = has_already_spoken(pixel_line) # Has interventor spoken?
    if speaker_id < 0:
        if len(interventors) == 0:
            interventors[str_pixel_line] = 0
        else:
            interventors[str_pixel_line] = len(interventors)
        return interventors[str_pixel_line]
    return speaker_id


def has_already_spoken(pixel_line):
    global interventors
    comparations = []
    for key in interventors:
        interv = eval(key)
        comparations = intersection(pixel_line, interv) # Intersection of pixels between the one being processed and the one in dictionary
        if len(comparations) > 30:
            return interventors[key]
    return -1


def near_color_in_list(color, lst):
    for el in lst:
        if are_near_pixel_colors(color, el):
            return True
    return False


def intersection(lst1, lst2): 
    """
        A pixel is in lst2 if its colors are similar to any pixel in lst2 and color is not purple
    """
    lst3 = [value for value in lst1 if near_color_in_list(value, lst2) and is_purple(value) == False] 
    return lst3 



def get_interventions(folder_name, output_file):
    interv = []
    i = 0
    for filename in os.listdir('../data/frames/intervention_frames/training'):
        frame = number_of_interventions_in_frame(os.path.join('../data/frames/intervention_frames/training',filename))
        interv.append(frame)
        i +=1
        if i%1000==0:
            print(i) 
    interv = sorted(interv, key=lambda x: x[0])
    print(len(interv))
    with open(output_file, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['time', 'user_id'])
        for element in interv:
            for subelement in element[2]:
                writer.writerow([element[0], subelement])

if __name__ == '__main__':
    get_interventions('../data/frames/intervention_frames/training', '../data/interventions_data/intervention_logs.csv')
