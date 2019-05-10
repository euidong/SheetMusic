import sys
import subprocess
import cv2
import time
import numpy as np
from best_fit import fit
from rectangle import Rectangle
from note import Note
from random import randint
from midiutil.MidiFile3 import MIDIFile

import matplotlib.pyplot as plt

#비교될 template파일들의 상대경로를 각각 종류의 리스트에 저장
staff_files = [
    "resources/template/staff2.png", 
    "resources/template/staff.png"]
quarter_files = [
    "resources/template/quarter.png", 
    "resources/template/solid-note.png"]
sharp_files = [
    "resources/template/sharp.png"]
flat_files = [
    "resources/template/flat-line.png", 
    "resources/template/flat-space.png" ]
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

#template들의 상대경로를 저장한 리스트로부터 cv2 imread로 로드한 list형태의 이미지데이터를 저장
staff_imgs = [cv2.imread(staff_file, 0) for staff_file in staff_files]
quarter_imgs = [cv2.imread(quarter_file, 0) for quarter_file in quarter_files]
sharp_imgs = [cv2.imread(sharp_files, 0) for sharp_files in sharp_files]
flat_imgs = [cv2.imread(flat_file, 0) for flat_file in flat_files]
half_imgs = [cv2.imread(half_file, 0) for half_file in half_files]
whole_imgs = [cv2.imread(whole_file, 0) for whole_file in whole_files]

#template과 real Sheet에서 비교해줄 때 확대축소비율의 최소치 최대치와 같다 판정의 임계값을 상수화
staff_lower, staff_upper, staff_thresh = 50, 150, 0.65
sharp_lower, sharp_upper, sharp_thresh = 50, 150, 0.70
flat_lower, flat_upper, flat_thresh = 50, 150, 0.77
quarter_lower, quarter_upper, quarter_thresh = 50, 150, 0.70
half_lower, half_upper, half_thresh = 50, 150, 0.70
whole_lower, whole_upper, whole_thresh = 50, 150, 0.70


#호출결과 template종류에 대한 sheet내에 가장 많이 비슷한 개수를
#가진 template확대비를 각 개수에 적용하여 그려지진 않고
#형태상 존재하게된 rectangle을 담은 list가 반환됨
def locate_images(img, templates, start, stop, threshold):
    locations, scale = fit(img, templates, start, stop, threshold)
    #호출결과 리스트에 template타입별 sheet내의 비슷한 좌표가 location으로 return
    #scale은 template의 확대비
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
        recs.sort(key=lambda rec: rec.distance(r)) #현재 기준과의 중앙점 좌표값 차이(x차제곱+y차제곱)를 기준 나머지 정렬시켜버림
        merged = True
        while(merged): #정렬기준 임계치 안되는 값이 나와버렸다? 그럼 뒤도 볼필요가 없다는 얘기 
            merged = False
            i = 0
            for _ in range(len(recs)):
                if r.overlap(recs[i]) > threshold or recs[i].overlap(r) > threshold: #두 rectangle의 오버랩 함수를 각각호출해 겹치는 정도를 받아 둘중 하나가 임계값을 넘을 경우
                    r = r.merge(recs.pop(i)) #rectangle 합쳐버리고 합침 당한놈 삭ㅡ제
                    merged = True
                elif recs[i].distance(r) > r.w/2 + recs[i].w/2: #중앙점거리가 x축길이의 대변값 보다 넘어가버렸다? 볼필요도 없다 이말이야
                    break
                else:
                    i += 1
        filtered_recs.append(r) #버려진 한줄에 대해 리스트에 한요소씩 리스트집단을 이루어저장
    return filtered_recs

def open_file(path):
    cmd = {'linux':'eog', 'win32':'explorer', 'darwin':'open'}[sys.platform]
    subprocess.run([cmd, path])

if __name__ == "__main__":
    img_file = sys.argv[1:][0]
    img = cv2.imread(img_file, 0)
    img_gray = img#cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img_gray,cv2.COLOR_GRAY2RGB)
    ret,img_gray = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY)
    img_width, img_height = img_gray.shape[::-1]
    #matching = real sheet에서 템플릿 스케일 조절해서
    #가장 많은 비슷한 template을 악보내에 보이는 scale에 대한
    #이론적 rectangle리스트를 만들어냄

    print("Matching staff image...")
    staff_recs = locate_images(img_gray, staff_imgs, staff_lower, staff_upper, staff_thresh)

    #무작위로 많은 template과 비슷한 이론적 rectangle을 찍어냈는데 그중에서
    #많이 나오는 rectangle의 최상단 왼쪽 좌표를 통해
    # 오선이 각각 어디줄 어디줄있는지 선별하고
    # 그 오선에 대한 rectangle만 남기는 작업같음
    print("Filtering weak staff matches...")
    '''print('before staff_recs_size : ',len(staff_recs))'''
    staff_recs = [j for i in staff_recs for j in i] #test결과 rectangle이 각 template에 대해 2차원으로 저장되어있던거를 1차원으로 선형화시킨거같은데
    '''staff_recs_img = img.copy()
    for r in staff_recs:
        r.draw(staff_recs_img, (0, 0, 255), 2)
    cv2.imwrite('test.png', staff_recs_img)
    open_file('test.png')
    print('after staff_recs_size : ',len(staff_recs))'''
    heights = [r.y for r in staff_recs] + [0]
    histo = [heights.count(i) for i in range(0, max(heights) + 1)]
    '''
    밑 구문으로 lost.jpg 확인결과 
    6개의 특정분포가 나타남애도 불구하고
    6개의 오선중 5개의 오선만 검출됨 임계치를 낮출 필요성이보임
    '''
    x=list(range(0, max(heights) + 1))
    plt.plot(histo,x)
    plt.show()
    
    avg = np.mean(list(set(histo)))
    print('avg : ',avg)
    staff_recs = [r for r in staff_recs if histo[r.y] > avg]
    print('after filtering staff_recs_size : ',len(staff_recs))
    '''
    이하로 테스트결과 lost.jpg의 5번째 오선 잘라버림..
    avg=np.mean부분에 대한 수정필요해보임
    '''
    staff_recs_img = img.copy()
    for r in staff_recs:
        r.draw(staff_recs_img, (0, 0, 255), 2)
    cv2.imwrite('test.png', staff_recs_img)
    open_file('test.png')
    
    #선별된 rectangle을 악보이미지와 결합하여 보여주는 작업
    print("Merging staff image results...")
    staff_recs = merge_recs(staff_recs, 0.01)
    print('merged list length : ',len(staff_recs))
    staff_recs_img = img.copy()
    for r in staff_recs:
        r.draw(staff_recs_img, (0, 0, 255), 2)
    cv2.imwrite('staff_recs_img.png', staff_recs_img)
    open_file('staff_recs_img.png')

    #각 높이가 같은 rectangle을 이어
    #최종적으로 각 줄에 대한 오선을 하나로 묶어주는 
    #rectangle을 찾는 작업같음
    print("Discovering staff locations...")
    staff_boxes = merge_recs([Rectangle(0, r.y, img_width, r.h) for r in staff_recs], 0.01)
    staff_boxes_img = img.copy()
    for r in staff_boxes:
        r.draw(staff_boxes_img, (0, 0, 255), 2)
    cv2.imwrite('staff_boxes_img.png', staff_boxes_img)
    open_file('staff_boxes_img.png')
    
    
    print("Matching sharp image...")
    sharp_recs = locate_images(img_gray, sharp_imgs, sharp_lower, sharp_upper, sharp_thresh)

    print("Merging sharp image results...")
    sharp_recs = merge_recs([j for i in sharp_recs for j in i], 0.5)
    sharp_recs_img = img.copy()
    for r in sharp_recs:
        r.draw(sharp_recs_img, (0, 0, 255), 2)
    cv2.imwrite('sharp_recs_img.png', sharp_recs_img)
    open_file('sharp_recs_img.png')
    
    print("Matching flat image...")
    flat_recs = locate_images(img_gray, flat_imgs, flat_lower, flat_upper, flat_thresh)

    print("Merging flat image results...")
    flat_recs = merge_recs([j for i in flat_recs for j in i], 0.5)
    flat_recs_img = img.copy()
    for r in flat_recs:
        r.draw(flat_recs_img, (0, 0, 255), 2)
    cv2.imwrite('flat_recs_img.png', flat_recs_img)
    open_file('flat_recs_img.png')
    
    print("Matching quarter image...")
    quarter_recs = locate_images(img_gray, quarter_imgs, quarter_lower, quarter_upper, quarter_thresh)
    print(len(quarter_recs[0])+len(quarter_recs[1]))
    print("Merging quarter image results...")
    quarter_recs =merge_recs([j for i in quarter_recs for j in i], 0.5)
    quarter_recs_img = img.copy()
    for r in quarter_recs:
        r.draw(quarter_recs_img, (0, 0, 255), 2)
    cv2.imwrite('quarter_recs_img.png', quarter_recs_img)
    open_file('quarter_recs_img.png')

    print("Matching half image...")
    half_recs = locate_images(img_gray, half_imgs, half_lower, half_upper, half_thresh)

    print("Merging half image results...")
    half_recs = merge_recs([j for i in half_recs for j in i], 0.5)
    half_recs_img = img.copy()
    for r in half_recs:
        r.draw(half_recs_img, (0, 0, 255), 2)
    cv2.imwrite('half_recs_img.png', half_recs_img)
    open_file('half_recs_img.png')

    print("Matching whole image...")
    whole_recs = locate_images(img_gray, whole_imgs, whole_lower, whole_upper, whole_thresh)

    print("Merging whole image results...")
    whole_recs = merge_recs([j for i in whole_recs for j in i], 0.5)
    whole_recs_img = img.copy()
    for r in whole_recs:
        r.draw(whole_recs_img, (0, 0, 255), 2)
    cv2.imwrite('whole_recs_img.png', whole_recs_img)
    open_file('whole_recs_img.png')
    
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
        note_group = []
        i = 0; j = 0;
        while(i < len(staff_notes)):
            if (staff_notes[i].rec.x > staffs[j].x and j < len(staffs)):
                r = staffs[j]
                j += 1;
                if len(note_group) > 0:
                    note_groups.append(note_group)
                    note_group = []
                note_color = (randint(0, 255), randint(0, 255), randint(0, 255))
            else:
                note_group.append(staff_notes[i])
                staff_notes[i].rec.draw(img, note_color, 2)
                i += 1
        note_groups.append(note_group)

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
    '''
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

    m1idi.addNote(track,channel,pitch,time,4,0)
    # And write it to disk.
    binfile = open("output.mid", 'wb')
    midi.writeFile(binfile)
    binfile.close()
    open_file('output.mid')
    '''
