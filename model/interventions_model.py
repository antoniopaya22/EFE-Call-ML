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
                frame_interv.append(correct_errors(get_line_speaker(image, start_point_speaker, last_point_speaker))) # Get interventor ID
            start_point_speaker = 0
            last_point_speaker = 0
            last_purple = False
        i += 2
    frame_number = int(frame.split('\\')[-1].split('.')[0][5:])
    return [frame_number, count, frame_interv]


def correct_errors(user):
    """
    We need to correct some missidecntifications
    """
    if user == 6:
        return 0
    return user


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
        if len(comparations) > 25:
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

def load_manual_logs():
    total_logs = []
    frames = {}
    f = open("data/interventions_data/intervention_logs2.txt", "r")
    for line in f:  
        parts = line.split(',')
        start = int(parts[0])
        user = int(parts[1])
        if start not in frames:
            frames[start] = [user]
        elif user not in frames[start]:
            frames[start].append(user)

    f = open("data/interventions_data/intervention_logs3.txt", "r")
    for line in f:  
        parts = line.split(' ')
        start = parts[0].split(':')
        start = int(start[0])*60 + int(start[1])
        end = parts[1].split(':')
        end = int(end[0])*60 + int(end[1])
        user = int(parts[2])
        
        for i in range(start, end+1):
            if i not in frames:
                frames[i] = [user]
            elif user not in frames[i]:
                frames[i].append(user)
    
    for key in frames:
        total_logs.append([key, 0, frames[key]])
    return total_logs


def generate_logs(logs_by_seconds):
    interventions_in_process = {}
    number_of_interventions_by_user = {}
    new_logs = []
    last_interv_frame = logs_by_seconds[0][0]
    time_to_previous_user = 0
    time_to_previous_general = 0
    for i in range(0, len(logs_by_seconds)):
        log = logs_by_seconds[i]
        for interventor in log[2]:
            if interventor not in interventions_in_process:
                interventions_in_process[interventor] = [log[0], last_interv_frame]
                if interventor not in number_of_interventions_by_user:
                    number_of_interventions_by_user[interventor] = [1, log[0]]
                else:
                    number_of_interventions_by_user[interventor][0] += 1  
            to_append = []
            if len(logs_by_seconds)-1 > i:
                if interventor not in logs_by_seconds[i+1][2]:
                    duration =  log[0] - interventions_in_process[interventor][0] + 1
                    time_to_previous_user = interventions_in_process[interventor][0] - number_of_interventions_by_user[interventor][1] + 1
                    time_to_previous_general = interventions_in_process[interventor][0] - interventions_in_process[interventor][1] + 1
               
                    # Format: [start, end, duration, intervention number (user), user_id, time to previous user interv, time to previous interv]
                    to_append = [interventions_in_process[interventor][0], log[0], duration, number_of_interventions_by_user[interventor][0], interventor, time_to_previous_user, time_to_previous_general] 
                    interventions_in_process.pop(interventor, None)
                    number_of_interventions_by_user[interventor][1] = log[0]
                    last_interv_frame = log[0]
                    new_logs.append(to_append)
            else:
                duration =  log[0] - interventions_in_process[interventor][0] + 1
                time_to_previous_user = interventions_in_process[interventor][0] - number_of_interventions_by_user[interventor][1] + 1
                time_to_previous_general = interventions_in_process[interventor][0] - interventions_in_process[interventor][1] + 1
         
                # Format: [start, end, duration, intervention number (user), user_id, time to previous user interv, time to previous interv]
                to_append = [interventions_in_process[interventor][0], log[0], duration, number_of_interventions_by_user[interventor][0], interventor, time_to_previous_user, time_to_previous_general] 
                interventions_in_process.pop(interventor, None)
                number_of_interventions_by_user[interventor][1] = log[0]
                last_interv_frame = log[0]
                new_logs.append(to_append)
    return new_logs


def get_interventions_simple(folder_name, output_file):
    interv = load_manual_logs()
    i = 0
    for filename in os.listdir('data/frames/intervention_frames/training'):
        frame = number_of_interventions_in_frame(os.path.join('data/frames/intervention_frames/training',filename))
        interv.append(frame)
        i +=1
        if i%1000==0:
            print(i) 
    interv = sorted(interv, key=lambda x: x[0])
    with open(output_file, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['time', 'user_id'])
        for element in interv:
            for subelement in element[2]:
                writer.writerow([element[0], subelement])


def get_interventions(folder_name, output_file):
    print("===========> Parse intervention frames")
    interv = load_manual_logs()
    total_frames = os.listdir(folder_name)
    i = 0
    for filename in total_frames:
        i += 1
        frame = number_of_interventions_in_frame(os.path.join(folder_name,filename))
        interv.append(frame) 
        if i%1000==0:
            print(str(i)+'/'+str(len(total_frames)+i))
    interv = sorted(interv, key=lambda x: x[0])
    interv = generate_logs(interv)
    print("===========> Convert to logs")
    with open(output_file, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #writer.writerow(['start', 'end', 'duration', 'interv_number', 'user_id', 'time_to_previous_user', 'time_to_previous_general'])
        writer.writerow(['user_id', 'start', 'end','duration', 'time_to_previous_user', 'time_to_previous_general'])
        for element in interv:
            print(element)
            writer.writerow([element[4], element[0], element[1], element[2], element[5], element[6]])


if __name__ == '__main__':
    get_interventions('../data/frames/intervention_frames/training', '../data/interventions_data/intervention_logs.csv')
