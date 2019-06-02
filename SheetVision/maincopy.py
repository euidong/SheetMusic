import sys
import subprocess
import cv2
import time
import numpy as np
from best_fit import fit #return best_location, best_scale
from rectangle import Rectangle# class Rectangle(x,y,w,h), overlap, distance, merge, draw 
from note import Note# class Note()rec, sym, staff_rec, sharpnotes, flatnotes

from random import randint
from midiutil.MidiFile3 import MIDIFile

#비교될 template파일들의 상대경로를 각각 종류의 리스트에 저장
staff_files = [
    "resources/template/staff2.png", #오선 이미지 템플릿
    "resources/template/staff.png"]
quarter_files = [
    "resources/template/quarter.png", #1/4음표 이미지
    "resources/template/solid-note.png"]
sharp_files = [
    "resources/template/sharp.png"] # 샵 이미지
flat_files = [
    "resources/template/flat-line.png",  # 플랫 이미지
    "resources/template/flat-space.png" ]
half_files = [
    "resources/template/half-space.png", #1/2음표 이미지
    "resources/template/half-note-line.png",
    "resources/template/half-line.png", 
    "resources/template/half-note-space.png"]
whole_files = [
    "resources/template/whole-space.png", # 온음 이미지
    "resources/template/whole-note-line.png",
    "resources/template/whole-line.png", 
    "resources/template/whole-note-space.png"]
replay_files = [
    "resources/template/replay.png",
    "resources/template/dodol.png"]#도돌이표 이미지 추가
rest_files = [
    "resources/template/bar-rest.png"]#쉼표 이미지 추가


#imread - save to ㅁ_imgs
#이미지 불러옴
staff_imgs = [cv2.imread(staff_file, 0) for staff_file in staff_files]
quarter_imgs = [cv2.imread(quarter_file, 0) for quarter_file in quarter_files]
sharp_imgs = [cv2.imread(sharp_files, 0) for sharp_files in sharp_files]
flat_imgs = [cv2.imread(flat_file, 0) for flat_file in flat_files]
half_imgs = [cv2.imread(half_file, 0) for half_file in half_files]
whole_imgs = [cv2.imread(whole_file, 0) for whole_file in whole_files]

replay_imgs = [cv2.imread(replay_file, 0) for replay_file in replay_files]#replay추가
rest_imgs = [cv2.imread(rest_file, 0) for rest_file in rest_files]#replay추가

# template과 real sheet에서 비교해줄 때 확대축소 비율의 최소치 최대치와 같다. 판정의 임계값을 상수화
staff_lower, staff_upper, staff_thresh = 50, 150, 0.77
sharp_lower, sharp_upper, sharp_thresh = 50, 150, 0.70
flat_lower, flat_upper, flat_thresh = 50, 150, 0.77
quarter_lower, quarter_upper, quarter_thresh = 50, 150, 0.70
half_lower, half_upper, half_thresh = 50, 150, 0.70
whole_lower, whole_upper, whole_thresh = 50, 150, 0.70

replay_lower, replay_upper, replay_thresh = 50, 150, 0.60#replay추가
rest_lower, rest_upper, rest_thresh = 50, 150, 0.80#replay추가


def CutMeasures2(img):
    line = [-1, -1, -1, -1, -1]
    lineSize = [0, 0, 0, 0, 0]
    measure = []

    l = 0

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
    locations, scale = fit(img, templates, start, stop, threshold)#return best_location, best_scale
    #호출 결과 리스트에 template타입 별 sheet내의 비슷한 좌표가 location으로 return
    #scale : template의 확대비
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
        recs.sort(key=lambda rec: rec.distance(r)) #현재 기준과의 중앙점 좌표값 차이(x차제곰+y차제곱)을 기준 나머지 정렬
        merged = True
        while(merged):
            merged = False
            i = 0
            for _ in range(len(recs)):
                if r.overlap(recs[i]) > threshold or recs[i].overlap(r) > threshold:
                    r = r.merge(recs.pop(i))
                    merged = True
                elif recs[i].distance(r) > r.w/2 + recs[i].w/2:
                    break
                else:
                    i += 1
        filtered_recs.append(r)
    return filtered_recs

def open_file(path):
    cmd = {'linux':'eog', 'win32':'explorer', 'darwin':'open'}[sys.platform]
    subprocess.run([cmd, path])



#img_gray: 받아오는 이미지
def match_and_merge(temp_img, temp_imgs, temp_lower, temp_upper, temp_thresh):
    #locate_image받아옴
    temp_recs = locate_images(temp_img, temp_imgs, temp_lower, temp_upper, temp_thresh)
    temp_recs = merge_recs([j for i in temp_recs for j in i], 0.5)
    temp_recs_img = temp_img.copy()
    return temp_recs

if __name__ == "__main__":
    img_file = sys.argv[1:][0] #실행 시의 인자로 이미지 받아오기
    img = cv2.imread(img_file, 0)
    img_gray = img #cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img_gray,cv2.COLOR_GRAY2RGB)
    ret,img_gray = cv2.threshold(img_gray,200,255,cv2.THRESH_BINARY)
    img_width, img_height = img_gray.shape[::-1]
    
        
    #staff 버려말아
    
    
    print("Matching staff image...")
    staff_recs = locate_images(img_gray, staff_imgs, staff_lower, staff_upper, staff_thresh)

    print("Filtering weak staff matches...")
    staff_recs = [j for i in staff_recs for j in i]
    heights = [r.y for r in staff_recs] + [0]
    histo = [heights.count(i) for i in range(0, max(heights) + 1)]
    avg = np.mean(list(set(histo)))
    staff_recs = [r for r in staff_recs if histo[r.y] > avg]

    print("Merging staff image results...")
    staff_recs = merge_recs(staff_recs, 0.01)
    staff_recs_img = img.copy()
    for r in staff_recs:
        r.draw(staff_recs_img, (0, 0, 255), 2)
    cv2.imwrite('staff_recs_img.png', staff_recs_img)
    open_file('staff_recs_img.png')


    
    staff_boxes = CutMeasures2(img_gray)

    #sharp
    sharp_recs = match_and_merge(img_gray, sharp_imgs, sharp_lower, sharp_upper, sharp_thresh)
    #flat
    flat_recs = match_and_merge(img_gray, flat_imgs, flat_lower, flat_upper, flat_thresh)
    #rest
    rest_recs = match_and_merge(img_gray, rest_imgs, rest_lower, rest_upper, rest_thresh)
    #replay
    replay_recs = match_and_merge(img_gray, replay_imgs, replay_lower, replay_upper, replay_thresh)
    #quarter
    quarter_recs = match_and_merge(img_gray, quarter_imgs, quarter_lower, quarter_upper, quarter_thresh)
    #half
    half_recs = match_and_merge(img_gray, half_imgs, half_lower, half_upper, half_thresh)
    #whole
    whole_recs = match_and_merge(img_gray, whole_imgs, whole_lower, whole_upper, whole_thresh)


    
    note_groups = []
    for box in staff_boxes:
        staff_sharps = [Note(r, "sharp", box) 
            for r in sharp_recs if abs(r.middle[1] - box.middle[1]) < box.h*5.0/8.0]
        staff_flats = [Note(r, "flat", box) 
            for r in flat_recs if abs(r.middle[1] - box.middle[1]) < box.h*5.0/8.0]
        quarter_notes = [Note(r, "4,8", box, staff_sharps, staff_flats) 
            for r in quarter_recs if abs(r.middle[1] - box.middle[1]) < box.h*5.0/8.0]
        half_notes = [Note(r, "2", box, staff_sharps, staff_flats) 
            for r in half_recs if abs(r.middle[1] - box.middle[1]) < box.h*5.0/8.0]
        whole_notes = [Note(r, "1", box, staff_sharps, staff_flats) 
            for r in whole_recs if abs(r.middle[1] - box.middle[1]) < box.h*5.0/8.0]
        staff_notes = quarter_notes + half_notes + whole_notes
        staff_notes.sort(key=lambda n: n.rec.x)
        staffs = [r for r in staff_recs if r.overlap(box) > 0]
        staffs.sort(key=lambda r: r.x)
        note_color = (randint(0, 255), randint(0, 255), randint(0, 255))

        note_group = [] #악보 꼬리별로 분류, 꼬리 묶여 있으면 하나의 엘리먼트
        i = 0; j = 0;
        while(i < len(staff_notes)): #꼬리 묶여있는 음표 그룹화
            #j 번째 오선 rect 가 i번째
            if (staff_notes[i].rec.x > staffs[j].x and j < len(staffs)):
                r = staffs[j] # 오선지 Rectangle
                j += 1; # 다음 오선지 Rectangle 검색
                if len(note_group) > 0:
                    note_groups.append(note_group) # 꼬리로 묶여 있는 그룹 append
                    note_group = [] # 새로운 그룹 만들기 위해 비움
                note_color = (randint(0, 255), randint(0, 255), randint(0, 255))
            #j번째 오선 rect와 rect사이에 음표가 여러개 있으면 여러번 수행 됨
            else:
                note_group.append(staff_notes[i]) # i번째 음표 추가
                staff_notes[i].rec.draw(img, note_color, 2) # 악보 이미지 객체에 사각형 그림
                i += 1 # 다음 음표 탐색
        note_groups.append(note_group) # 음표 그룹에 추가

    for r in staff_boxes:
        r.draw(img, (0, 0, 255), 2)
    for r in sharp_recs:
        r.draw(img, (0, 0, 255), 2)
    flat_recs_img = img.copy()
    for r in flat_recs:
        r.draw(img, (0, 0, 255), 2)
        
    cv2.imwrite('res.png', img)
    open_file('res.png')
   
    for note_group in note_groups:
        print([ note.note + " " + note.sym for note in note_group])

    # note를 미디 파일로 저장
    midi = MIDIFile(1)
     
    track = 0   
    time = 0
    channel = 0
    volume = 100
    
    midi.addTrackName(track, time, "Track")
    midi.addTempo(track, time, 140)
    
    for note_group in note_groups:
        duration = None
        for note in note_group:
            note_type = note.sym
            if note_type == "1":
                duration = 4
            elif note_type == "2":
                duration = 2
            elif note_type == "4,8":
                duration = 1 if len(note_group) == 1 else 0.5
            pitch = note.pitch
            midi.addNote(track,channel,pitch,time,duration,volume)
            time += duration

    midi.addNote(track,channel,pitch,time,4,0)
    # And write it to disk.
    binfile = open("output.mid", 'wb')
    midi.writeFile(binfile)
    binfile.close()
    open_file('output.mid')
    
