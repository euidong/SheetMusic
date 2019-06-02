import sys
import subprocess
import cv2
import time
import numpy as np
from best_fit import fit
from rectangle import Rectangle
from note import Note
from random import randint
from midiutil.MidiFile import MIDIFile, MIDITrack

quarter_files = [
    "resources/template/quarter.png",
    "resources/template/solid-note.png"]
sharp_files = [
    "resources/template/sharp.png"]
flat_files = [
    "resources/template/flat-line.png",
    "resources/template/flat-space.png"]
half_files = [
    "resources/template/half-space.png",
    "resources/template/half-note-line.png",
    "resources/template/half-line.png",
    "resources/template/half-note-space.png"]
whole_files = [
    "resources/template/whole-space.png",
    "resources/template/whole-note-line.png",
    "resources/template/whole-line.png",
    "resources/template/whole-note-space.png"]

wholeRest_files = [
    "resources/template/bar-rest.png", #쉼표 이미지
    "resources/template/bar-rest2.png"]
halfRest_files = [
    "resources/template/half_rest.png"]
quarterRest_files=[
    "resources/template/quarter_rest.png"]
eighthRest_files=[
    "resources/template/eight_rest.png",
    "resources/template/eight_rest2.png"]

replay_end_files = [
    "resources/template/replay_end.png",
    "resources/template/replay_end2.png"] #도돌이표 이미지 추가
replay_start_files = [
    "resources/template/replay_start.png"]

quarter_imgs = [cv2.imread(quarter_file, 0) for quarter_file in quarter_files]
sharp_imgs = [cv2.imread(sharp_files, 0) for sharp_files in sharp_files]
flat_imgs = [cv2.imread(flat_file, 0) for flat_file in flat_files]
half_imgs = [cv2.imread(half_file, 0) for half_file in half_files]
whole_imgs = [cv2.imread(whole_file, 0) for whole_file in whole_files]

wholeRest_imgs = [cv2.imread(wholeRest_file,0) for wholeRest_file in wholeRest_files]
halfRest_imgs = [cv2.imread(halfRest_file,0) for halfRest_file in halfRest_files]
quarterRest_imgs = [cv2.imread(quarterRest_file,0) for quarterRest_file in quarterRest_files]
eighthRest_imgs = [cv2.imread(eighthRest_file,0) for eighthRest_file in eighthRest_files]

replay_start_imgs = [cv2.imread(replay_start_file, 0) for replay_start_file in replay_start_files]#replay추가
replay_end_imgs = [cv2.imread(replay_end_file, 0) for replay_end_file in replay_end_files]

sharp_lower, sharp_upper, sharp_thresh = 50, 150, 0.70
flat_lower, flat_upper, flat_thresh = 50, 150, 0.77
quarter_lower, quarter_upper, quarter_thresh = 50, 100, 0.77
half_lower, half_upper, half_thresh = 50, 150, 0.70
whole_lower, whole_upper, whole_thresh = 50, 150, 0.70

wholeRest_lower,wholeRest_upper,wholeRest_thresh =50,150,0.80
halfRest_lower, halfRest_upper, halfRest_thresh =50,150,0.80
quarterRest_lower, quarterRest_upper, quarterRest_thresh =50,150,0.70
eighthRest_lower, eighthRest_upper,eighthRest_thresh= 50,100,0.85

replay_start_lower, replay_start_upper, replay_start_thresh = 50, 150, 0.70
replay_end_lower, replay_end_upper, replay_end_thresh = 50, 150, 0.70

#줄별로 이미지 분
def CutMeasures2(img):
    line = [-1, -1, -1, -1, -1]
    lineSize = [0, 0, 0, 0, 0]
    l = 0
    measure = []
    for i in range(np.size(img, 0)):
        count = 0
        for j in range(np.size(img, 1)):
            if img[i, j] == 0:
                count += 1

        if (count / np.size(img, 1)) > 0.6:
            k = 0
            while k < 5:
                if line[k] == -1:
                    break
                k += 1

            if k == 0:
                line[0] = i
                lineSize[0] += 1
            elif line[k-1] + lineSize[k-1] == i:
                lineSize[k-1] += 1
            else:
                line[k] = i
                lineSize[k] += 1
        elif line[4] != -1:
            gap = line[1] - line[0]
            measure.append(Rectangle(0, line[0] - (gap * 4), np.size(img, 1), line[4] + (gap * 8) - line[0]))

            for m in range(5):
                line[m] = -1
                lineSize[m] = 0
            l += 1

    return measure

def locate_images(img, templates, start, stop, threshold):
    locations, scale = fit(img, templates, start, stop, threshold)
    img_locations = []
    for i in range(len(templates)):
        w, h = templates[i].shape[::-1]
        w *= scale
        h *= scale
        img_locations.append([Rectangle(pt[0], pt[1], w, h) for pt in zip(*locations[i][::-1])])
    return img_locations


def merge_recs(recs, threshold):
    filtered_recs = []
    while len(recs) > 0:
        r = recs.pop(0)
        recs.sort(key=lambda rec: rec.distance(r))
        merged = True
        while (merged):
            merged = False
            i = 0
            for _ in range(len(recs)):
                if r.overlap(recs[i]) > threshold or recs[i].overlap(r) > threshold:
                    r = r.merge(recs.pop(i))
                    merged = True
                elif recs[i].distance(r) > r.w / 2 + recs[i].w / 2:
                    break
                else:
                    i += 1
        filtered_recs.append(r)
    return filtered_recs


def open_file(path):
    cmd = {'linux': 'eog', 'win32': 'explorer', 'darwin': 'open'}[sys.platform]
    subprocess.run([cmd, path])

    
def match_and_merge(temp_img, temp_imgs, temp_lower, temp_upper, temp_thresh):
    #locate_image받아옴
    temp_recs = locate_images(temp_img, temp_imgs, temp_lower, temp_upper, temp_thresh)
    temp_recs = merge_recs([j for i in temp_recs for j in i], 0.5)
    temp_recs_img = temp_img.copy()
    print("Matching & Merging image...")
    '''
    for r in temp_recs:
        r.draw(temp_recs_img, (0, 0, 255), 2)
    cv2.imwrite('result.png', temp_recs_img)
    open_file('result.png')
    '''
    return temp_recs

if __name__ == "__main__":
    img_file = sys.argv[1:][0]
    img = cv2.imread(img_file, 0)
    img_gray = img  # cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)
    ret, img_gray = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
    img_width, img_height = img_gray.shape[::-1]

    staff_boxes = CutMeasures2(img_gray)

    # sharp
    sharp_recs = match_and_merge(img_gray, sharp_imgs, sharp_lower, sharp_upper, sharp_thresh)
    # flat
    flat_recs = match_and_merge(img_gray, flat_imgs, flat_lower, flat_upper, flat_thresh)

    # note
    quarter_recs = match_and_merge(img_gray, quarter_imgs, quarter_lower, quarter_upper, quarter_thresh)

    half_recs = match_and_merge(img_gray, half_imgs, half_lower, half_upper, half_thresh)
    whole_recs = match_and_merge(img_gray, whole_imgs, whole_lower, whole_upper, whole_thresh)
    '''
    # rest
    wholeRest_recs = match_and_merge(img_gray, wholeRest_imgs, wholeRest_lower, wholeRest_upper, wholeRest_thresh)
    halfRest_recs = match_and_merge(img_gray, halfRest_imgs, halfRest_lower, halfRest_upper, halfRest_thresh)
    quarterRest_recs = match_and_merge(img_gray, quarterRest_imgs, quarterRest_lower, quarterRest_upper,quarterRest_thresh)
    eighthRest_recs = match_and_merge(img_gray, eighthRest_imgs, eighthRest_lower, eighthRest_upper,eighthRest_thresh)
    '''
    # replay
    replay_start_recs = match_and_merge(img_gray, replay_start_imgs, replay_start_lower, replay_start_upper, replay_start_thresh)
    replay_end_recs = match_and_merge(img_gray, replay_end_imgs, replay_end_lower, replay_end_upper, replay_end_thresh)

    note_group = []
    for box in staff_boxes:
        staff_sharps = [Note(r, "sharp", box)
                        for r in sharp_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        staff_flats = [Note(r, "flat", box)
                       for r in flat_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        quarter_notes = [Note(r, "4,8", box, staff_sharps, staff_flats)
                         for r in quarter_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        
        half_notes = [Note(r, "2", box, staff_sharps, staff_flats)
                      for r in half_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        whole_notes = [Note(r, "1", box, staff_sharps, staff_flats)
                       for r in whole_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]

        '''
        whole_rests = [Note(r, "-1", box)
                       for r in wholeRest_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        half_rests = [Note(r, "-2", box)
                      for r in halfRest_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        quarter_rests = [Note(r, "-4", box)
                         for r in quarterRest_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        eighth_rests = [Note(r, "-8", box)
                        for r in eighthRest_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        '''

        #note형으로 추가
        replay_start = [Note(r, "-0", box)
                  for r in replay_start_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        replay_end = [Note(r, "3", box)
                  for r in replay_end_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        
        staff_notes = quarter_notes + half_notes + whole_notes + replay_start + replay_end # + quarter_rests + half_rests + whole_rests + eighth_rests 
        staff_notes.sort(key=lambda n: n.rec.x)
        
        note_color = (randint(0, 255), randint(0, 255), randint(0, 255))

        
        
        i = 0
        while (i < len(staff_notes)):
                note_group.append(staff_notes[i])
                i += 1

    

    for r in staff_boxes:
        r.draw(img, (0, 0, 255), 2)
    for r in sharp_recs:
        r.draw(img, (0, 0, 255), 2)
    flat_recs_img = img.copy()
    for r in flat_recs:
        r.draw(img, (0, 0, 255), 2)
    for r in replay_end_recs:
        r.draw(img, (0, 0, 255), 2)
    for r in replay_start_recs:
        r.draw(img, (0, 0, 255), 2)

    cv2.imwrite('res.png', img)
    open_file('res.png')

    print("기존notegroup")
    for note in note_group:
        if (note.note != None):
            print([note.note + " " + note.sym])
        else:
            print([note.sym])

    #replay 찾아서 그 구간의 note 반복해서 append
    
    temp_idx = 0
    
    
    temp_notes = note_group[:]
    temp_between = 0 #반복 구간의 크기, 누적
    
    idx = 0 #all_notes에서 for문을 도는 idx
    s_idx = 0#도돌이표 시작 idx
    e_idx = 0#도돌이표 끝 idx

    s_check = 0
    e_check = 0


    for note in temp_notes:
        if (note.sym == "-0"):  # 도돌이표 시작
            s_idx = idx
            s_check = 1

        if (note.sym == "3"):  # 도돌이표 끝
            e_idx = idx
            e_check = 1

            temp_idx = e_idx + 1
            for i in range(e_idx - s_idx + 1):
                note_group.insert(temp_idx + temp_between, temp_notes[i + s_idx])
                temp_idx = temp_idx + 1

            temp_between = temp_between + e_idx - s_idx + 1
        idx = idx + 1

    temp_i = 0
    count = 0
    print("도돌이표 추가 note_group")
    temp_arr = note_group[:]
    for note in temp_arr:
        if (note.note != None):
            if(note.sym == "3" or note.sym == "-0"):
                del note_group[temp_i - count]
                count = count + 1

        temp_i = temp_i+1

    print("삭제한 notegroup")
    for note in note_group:
        if (note.note != None):
            print([note.note + " " + note.sym])
        else:
            print([note.sym])





    midi = MIDIFile(1)

    track = 0
    time = 0
    channel = 0
    volume = 100

    midi.addTrackName(track, time, "Track")
    midi.addTempo(track, time, 140)

    for note in note_group:
        duration = None
        note_type = note.sym
        if (len(note_type) != 2):
            if note_type == "1":
                duration = 4
            elif note_type == "2":
                duration = 2
            elif note_type == "4,8":
                duration = 1 if len(note_group) == 1 else 0.5
            pitch = note.pitch
            midi.addNote(track, channel, pitch, time, duration, volume)
            time += duration

        else:
            if note_type == "-1":
                duration = 4
            elif note_type == "-2":
                duration = 2
            elif note_type == "-4":
                duration = 1
            else:
                duration = 0.5
            pitch = note.pitch
            midi.addNote(track, channel, pitch, time, duration, 0)
            time += duration

    midi.addNote(track, channel, pitch, time, 4, 0)
    # And write it to disk.
    binfile = open("output.mid", 'wb')
    midi.writeFile(binfile)
    binfile.close()
    open_file('output.mid')

#python main.py C:\SheetVision\resources\samples\sheet.jpg
