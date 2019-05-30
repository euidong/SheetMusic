import sys
import subprocess
import cv2
import numpy as np
from best_fit import fit #사용자 지정함수 입니다.
from rectangle import Rectangle
from note import Note
from random import randint
from midiutil.MidiFile import MIDIFile

# 라인의 모양을 저장한 위치를 가진 변수
staff_files = [
    "resources/template/staff2.png",
    "resources/template/staff.png"]

# 음표의 모양을 저장한 위치를 가진 변수(안이 꽉 찬 모양)
quarter_files = [
    "resources/template/quarter.png",
    "resources/template/solid-note.png"]

# 샾의 모양을 저장한 위치를 가진 변수
sharp_files = [
    "resources/template/sharp.png",
    "resources/template/f-sharp.png",
    "resources/template/f-sharp2.png"]

# 플랫의 모양을 저장한 위치를 가진 변수
flat_files = [
    "resources/template/flat-line.png",
    "resources/template/flat-space.png" ]

# 2분음표의 모양을 저장한 위치를 가진 변수 (안이 비어있음) - 선의 모양도 같이 저장(맨윗줄, 맨아랫줄은 두꺼움)
half_files = [
    "resources/template/half-space.png",
    "resources/template/half-note-line.png",
    "resources/template/half-line.png",
    "resources/template/half-note-space.png"]

# 온음표의 모양을 저장한 위치를 가진 변수 (안이 비어있음) - 선의 모양도 같이 저장
whole_files = [
    "resources/template/whole-space.png",
    "resources/template/whole-note-line.png",
    "resources/template/whole-line.png",
    "resources/template/whole-note-space.png"]

# 이미지를 불러옵니다.
staff_imgs = [cv2.imread(staff_file, 0) for staff_file in staff_files] #오선에 대한 이미집니다.
quarter_imgs = [cv2.imread(quarter_file, 0) for quarter_file in quarter_files]
sharp_imgs = [cv2.imread(sharp_files, 0) for sharp_files in sharp_files] # 샾 이미지
flat_imgs = [cv2.imread(flat_file, 0) for flat_file in flat_files]
half_imgs = [cv2.imread(half_file, 0) for half_file in half_files]
whole_imgs = [cv2.imread(whole_file, 0) for whole_file in whole_files]


staff_lower, staff_upper, staff_thresh = 50, 150, 0.50    # thresh original: 0.77
sharp_lower, sharp_upper, sharp_thresh = 50, 150, 0.65    # thresh original : 0.70
flat_lower, flat_upper, flat_thresh = 50, 150, 0.77
quarter_lower, quarter_upper, quarter_thresh = 50, 150, 0.70
half_lower, half_upper, half_thresh = 50, 150, 0.70
whole_lower, whole_upper, whole_thresh = 50, 150, 0.70

def CutMeasures(img):
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
            measure.append(img[line[0] - (gap * 4) : line[4] + (gap * 4), : ])

            for m in range(5):
                line[m] = -1
                lineSize[m] = 0
            l += 1
    return measure


def locate_images(img, templates, start, stop, threshold): # 오선의 위치 찾는 함수
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

if __name__ == "__main__":
    img_file = sys.argv[1:][0] # 실행 시의 인자로 이미지 받아오기
    img = cv2.imread(img_file, 0)
    img_gray = img#cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img_gray,cv2.COLOR_GRAY2RGB)
    ret,img_gray = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY)
    img_width, img_height = img_gray.shape[::-1]

    measures = CutMeasures(img_gray)

    for idx, cut_measure in enumerate(measures):
        cv2.imwrite('cutting{}.png'.format(idx), cut_measure)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("Matching staff image...")# 악보의 오선 받기.
    staff_recs = locate_images(img_gray, staff_imgs, staff_lower, staff_upper, staff_thresh) # staff_lower, staff_upper, staff_thresh = 50, 150, 0.77
    
    
    print("Filtering weak staff matches...")
    staff_recs = [j for i in staff_recs for j in i]
    heights = [r.y for r in staff_recs] + [0]
    histo = [heights.count(i) for i in range(0, max(heights) + 1)]
    avg = np.mean(list(set(histo)))
    staff_recs = [r for r in staff_recs if histo[r.y] > avg]
    
    print("merging staff image results...")
    staff_recs = merge_recs(staff_recs, 0.01)
    staff_recs_img = img.copy()
    for r in staff_recs:
        r.draw(staff_recs_img, (0, 0, 255), 2)
    cv2.imwrite('staff_recs_img.png', staff_recs_img)
    open_file('staff_recs_img.png')
    
    print("discovering staff locations...")
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
    
    print("Merging quarter image results...")
    quarter_recs = merge_recs([j for i in quarter_recs for j in i], 0.5)
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
        quarter_notes = [Note(r, "4,8", box)
            for r in quarter_recs if abs(r.middle[1] - box.middle[1]) < box.h*5.0/8.0]
        half_notes = [Note(r, "2", box)
            for r in half_recs if abs(r.middle[1] - box.middle[1]) < box.h*5.0/8.0]
        whole_notes = [Note(r, "1", box)
            for r in whole_recs if abs(r.middle[1] - box.middle[1]) < box.h*5.0/8.0]
        staff_notes = quarter_notes + half_notes + whole_notes
        staff_notes.sort(key=lambda n: n.rec.x)
        staffs = [r for r in staff_recs if r.overlap(box) > 0]
        staffs.sort(key=lambda r: r.x)

            # 음계 파악
        key_sharps = []    # 조표의 샾
        key_flats = []    # 조표의 플랫
        # x좌표 기준 첫 번째 음표 찾기
        # 샾의 x좌표와 첫 번째 음표 x좌표 비교해서 작은 샾만 조표로 판단
        if len(staff_notes) > 0:
            key_sharps = [sharp for sharp in staff_sharps if sharp.rec.x < staff_notes[0].rec.x]
            key_flats = [flat for flat in staff_flats if flat.rec.x < staff_notes[0].rec.x]

        for note in whole_notes:
            note.set_key(key_sharps)

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
    
    #midi = MIDIFile(1)
    
    #track = 0
    #time = 0
    #channel = 0
    #volume = 100
    
    #midi.addTrackName(track, time, "Track")
    #midi.addTempo(track, time, 140)
    
    #for note_group in note_groups:
    #    duration = None
    #    for note in note_group:
    #        note_type = note.sym
    #        if note_type == "1":
    #            duration = 4
    #        elif note_type == "2":
    #            duration = 2
    #        elif note_type == "4,8":
    #            duration = 1 if len(note_group) == 1 else 0.5
    #        pitch = note.pitch
    #        midi.addNote(track,channel,pitch,time,duration,volume)
    #        time += duration
    
    #midi.addNote(track,channel,pitch,time,4,0)
    ## And write it to disk.
    #binfile = open("output.mid", 'wb')
    #midi.writeFile(binfile)
    #binfile.close()
    #open_file('output.mid')