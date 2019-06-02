import sys
import subprocess
import cv2
import time
import numpy as np
from best_fit import fit
from rectangle import Rectangle
from note import Note
from random import randint
from midiutil.MidiFile import MIDIFile

# 라인의 모양을 저장한 위치를 가진 변수
staff_files = [
    "resources/template/staff2.png",
    "resources/template/staff.png"]
# 높은음자리표 파일 경로
g_clef_files=[
    "resources/template/g_clef.png"
    ]
# 낮음음자리표 파일 경로
bass_clef_files=[
    "resources/template/bass_clef.png"
    ]
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
key_changer_files = [
    "resources/template/bar_key_change.png"
]
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
right_down_tuplet_files = [
    "resources/template/tuplet_rd.png"]
right_up_tuplet_files = [
    "resources/template/tuplet_ru.png"]

staff_imgs = [cv2.imread(staff_file, 0) for staff_file in staff_files]
g_clef_imgs = [cv2.imread(g_clef_file, 0) for g_clef_file in g_clef_files]
bass_clef_imgs = [cv2.imread(bass_clef_file, 0) for bass_clef_file in bass_clef_files]
quarter_imgs = [cv2.imread(quarter_file, 0) for quarter_file in quarter_files]
sharp_imgs = [cv2.imread(sharp_files, 0) for sharp_files in sharp_files] # 샾 이미지
flat_imgs = [cv2.imread(flat_file, 0) for flat_file in flat_files]
key_changer_imgs = [cv2.imread(key_changer_file, 0) for key_changer_file in key_changer_files]
half_imgs = [cv2.imread(half_file, 0) for half_file in half_files]
whole_imgs = [cv2.imread(whole_file, 0) for whole_file in whole_files]
right_down_tuplet_imgs = [cv2.imread(right_down_tuplet_file, 0) for right_down_tuplet_file in right_down_tuplet_files]
right_up_tuplet_imgs = [cv2.imread(right_up_tuplet_file, 0) for right_up_tuplet_file in right_up_tuplet_files]

staff_lower, staff_upper, staff_thresh = 50, 150, 0.77
sharp_lower, sharp_upper, sharp_thresh = 50, 150, 0.65    # thresh original : 0.70
flat_lower, flat_upper, flat_thresh = 50, 150, 0.77
quarter_lower, quarter_upper, quarter_thresh = 50, 150, 0.70
half_lower, half_upper, half_thresh = 50, 150, 0.70
whole_lower, whole_upper, whole_thresh = 50, 150, 0.70
right_down_tuplet_lower, right_down_tuplet_upper, right_down_tuplet_thresh = 50, 150, 0.7
right_up_tuplet_lower, right_up_tuplet_upper, right_up_tuplet_thresh = 50, 150, 0.7

def CutMeasures(img):
    line = [-1, -1, -1, -1, -1]
    lineSize = [0, 0, 0, 0, 0]
    measure = []
    gaplist=[]
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
            gaplist.append(gap)
            for m in range(5):
                line[m] = -1
                lineSize[m] = 0
            l += 1
    return measure, gaplist

def deleteMeasures(img):
    for i in range(np.size(img, 0)):
        count = 0
        for j in range(np.size(img, 1)):
            if img[i, j] == 0:
                count += 1
        if (count / np.size(img, 1)) > 0.6:
            k = 0
            for h in range(np.size(img,1)):
                img[i, h] = 255

def find_g_clef(measure_img, g_clef_templates, bass_clef_templates):
    '''
    악보 이미지에서 음자리표 찾아 높은음자리표면 True를 반환하는 함수
    '''
    
    is_g_clef = True   # 높은음자리인지 판단. false면 낮은음자리표

    g_clef_lower, g_clef_upper, g_clef_thresh = 20, 150, 0.45
    bass_clef_lower, bass_clef_upper, bass_clef_thresh = 20, 150, 0.65

    # 높은음자리표 매칭
    print("Matching g_clef image...")
    g_clef_recs = locate_images(measure_img, g_clef_imgs, g_clef_lower, g_clef_upper, g_clef_thresh)
    
    print("Merging g_clef image results...")
    g_clef_recs = merge_recs([j for i in g_clef_recs for j in i], 0.5)
    g_clef_recs_img = measure_img.copy()
    for r in g_clef_recs:
        r.draw(g_clef_recs_img, (0, 0, 255), 2)
    cv2.imwrite('g_clef_recs_img.png', g_clef_recs_img)
    open_file('g_clef_recs_img.png')

    # 낮은음자리표 매칭
    print("Matching bass_clef image...")
    bass_clef_recs = locate_images(measure_img, bass_clef_imgs, bass_clef_lower, bass_clef_upper, bass_clef_thresh)

    print("Merging bass_clef image results...")
    bass_clef_recs = merge_recs([j for i in bass_clef_recs for j in i], 0.5)
    bass_clef_recs_img = measure_img.copy()
    for r in bass_clef_recs:
        r.draw(bass_clef_recs_img, (0, 0, 255), 2)
    cv2.imwrite('bass_clef_recs_img.png', bass_clef_recs_img)
    open_file('bass_clef_recs_img.png')

    # 낮은음자리표 검출되면 false
    if len(bass_clef_recs) > 0:
        is_g_clef = False

    return is_g_clef

def find_key_changer(measure_img, bar_templates):
    '''
    악보 이미지에서 조표 바뀌는 두 줄 바를 탐지해 rectangle list를 반환하는 함수
    '''

    lower, upper, thresh = 50, 150, 0.90

    print("Matching key changing bar image...")
    key_changer_recs = locate_images(measure_img, bar_templates, lower, upper, thresh)
    
    print("Merging key changing bar image results...")
    key_changer_recs = merge_recs([j for i in key_changer_recs for j in i], 0.5)
    key_changer_img = measure_img.copy()
    for r in key_changer_recs:
        r.draw(key_changer_img, (0, 0, 255), 2)
    cv2.imwrite('key_changer_recs_img.png', key_changer_img)
    open_file('key_changer_recs_img.png')

    key_changer_recs.sort(key=lambda r: r.x)

    return key_changer_recs

def locate_images(img, templates, start, stop, threshold): # 오선의 위치 찾는 함수
    locations, scale = fit(img, templates, start, stop, threshold)
    img_locations = []
    for i in range(len(templates)):
        w, h = templates[i].shape[::-1]
        w *= scale
        h *= scale
        img_locations.append([Rectangle(pt[0], pt[1], w, h) for pt in zip(*locations[i][::-1])])
    return img_locations

def isOcta(img, rec): #꼭 img로 deletemeasure된 이미지 넘겨줄것
    area=rec.w*rec.h
    cnt=0
    for i in range(int(rec.x),int(rec.x+rec.w)):
        for j in range(int(rec.y),int(rec.y+rec.h)):
            if img[j,i]==0:
                cnt+=1
    return cnt/area>=0.16

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


if __name__ == "__main__":
    img_file = sys.argv[1:][0]
    img = cv2.imread(img_file, 0)
    img_gray = img  # cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)
    ret, img_gray = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
    img_width, img_height = img_gray.shape[::-1]

    measures, gaplist = CutMeasures(img_gray)

    line_delete_img = cv2.imread(img_file, 0)
    gray_line_delete_img = line_delete_img
    line_delete_img = cv2.cvtColor(gray_line_delete_img, cv2.COLOR_GRAY2RGB)
    ret, gray_line_delete_img = cv2.threshold(gray_line_delete_img, 127, 255, cv2.THRESH_BINARY)

    deleteMeasures(gray_line_delete_img)

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

    # 조표 바꾸는 세로 2줄(||) 매칭
    key_changer_recs = find_key_changer(img_gray, key_changer_imgs)

    print("Matching quarter image...")
    quarter_recs = locate_images(img_gray, quarter_imgs, quarter_lower, quarter_upper, quarter_thresh)
    
    print("Merging quarter image results...")
    quarter_recs = merge_recs([j for i in quarter_recs for j in i], 0.5)
    quarter_recs_img = img.copy()
    for r in quarter_recs:
        r.draw(quarter_recs_img, (0, 0, 255), 2)
    cv2.imwrite('quarter_recs_img.png', quarter_recs_img)
    open_file('quarter_recs_img.png')

    print("Matching right_down_tuplet image...")
    right_down_tuplet_recs = locate_images(img_gray, right_down_tuplet_imgs, right_down_tuplet_lower,
                                           right_down_tuplet_upper, right_down_tuplet_thresh)

    print("Matching right_up_tuplet image...")
    right_up_tuplet_recs = locate_images(img_gray, right_up_tuplet_imgs, right_up_tuplet_lower, right_up_tuplet_upper,
                                         right_up_tuplet_thresh)

    print("Merging tuplet image results...")
    tuplet_recs = right_down_tuplet_recs + right_up_tuplet_recs

    tuplet_recs = merge_recs([j for i in tuplet_recs for j in i], 0.5)
    # 이하는 tuplet matchtemplate결과 4분음표를 잡는 경우가 있어 이를 제거해주는 과정
    for staff in measures:
        staff_tuplet_recs = [r for r in tuplet_recs if staff.y <= r.y and staff.y + staff.h >= r.y]
        staff_quarter_recs = [r for r in quarter_recs if staff.y <= r.y and staff.y + staff.h >= r.y]
        staff_tuplet_recs.sort(key=lambda r: r.x)
        staff_quarter_recs.sort(key=lambda r: r.x)
        for quarter in staff_quarter_recs:
            for tuplet in staff_tuplet_recs:
                if quarter.overlap(tuplet) > 0:
                    tuplet_recs.remove(tuplet)
                elif quarter.x + quarter.w <= tuplet.x:
                    break
    tuplet_recs_img = img.copy()
    for r in tuplet_recs:
        r.draw(tuplet_recs_img, (0, 0, 255), 2)
    cv2.imwrite("tuplet.png", tuplet_recs_img)
    open_file('tuplet.png')

    # 이하는 같은 오선 내에서 tuplet과 동일한 x좌표에 있는 quarter대가리를 octa로 분류시켜주는 작업
    octa_recs = []
    for staff in measures:

        staff_tuplet_recs = [r for r in tuplet_recs if staff.y <= r.y and staff.y + staff.h >= r.y]
        staff_quarter_recs = [r for r in quarter_recs if staff.y <= r.y and staff.y + staff.h >= r.y]
        staff_tuplet_recs.sort(key=lambda r: r.x)
        staff_quarter_recs.sort(key=lambda r: r.x)
        check_box = []
        for _ in range(len(staff_quarter_recs)):
            check_box.append(False)

        for tuplet in staff_tuplet_recs:

            for i in range(len(staff_quarter_recs)):

                if (staff_quarter_recs[i].x <= tuplet.x + tuplet.w + staff_quarter_recs[i].w / 2) and (
                        staff_quarter_recs[i].x >= tuplet.x - staff_quarter_recs[i].w):
                    check_box[i] = True
        for i in range(len(staff_quarter_recs)):
            if check_box[i]:
                quarter_recs.remove(staff_quarter_recs[i])
                octa_recs.append(staff_quarter_recs[i])

    # 이하는 이어진 8분음표가 아닌 홀로 떨어져있는 진짜 8분음표처럼 생긴애를 quarter중에 분류하는 작업
    for i in range(len(measures)):
        # cnt+=1
        # prtline="Staff{} ".format(str(cnt))
        middle_x, staff_middle_y = measures[i].middle
        # copy_copy_img=copy_img.copy()
        staff_quarter_recs = [r for r in quarter_recs if measures[i].y <= r.y and measures[i].y + measures[i].h >= r.y]
        staff_quarter_recs.sort(key=lambda r: r.x)
        # tempcnt=0
        for quarter in staff_quarter_recs:
            # tempcnt+=1
            if quarter.y > staff_middle_y - gaplist[i] / 2:  # 가운데아래 음표
                temp = Rectangle(quarter.x + quarter.w, quarter.y - gaplist[i] * 3 + int(quarter.h * 0.3),
                                 int(quarter.w / 2), quarter.h)
                if isOcta(gray_line_delete_img, temp):
                    quarter_recs.remove(quarter)
                    octa_recs.append(quarter)
            else:
                if quarter.y > staff_middle_y - gaplist[i] * 0.8:  # 가운데줄 음표
                    temp = Rectangle(quarter.x + int(quarter.w * 0.2),
                                     quarter.y + gaplist[i] * 3 - int(quarter.h * 0.3), int(quarter.w / 2), quarter.h)
                    if isOcta(gray_line_delete_img, temp):
                        quarter_recs.remove(quarter)
                        octa_recs.append(quarter)
                else:  # 가운데 위 음표
                    temp = Rectangle(quarter.x + int(quarter.w * 0.2),
                                     quarter.y + gaplist[i] * 3 - int(quarter.h * 0.3), int(quarter.w / 2), quarter.h)
                    if isOcta(gray_line_delete_img, temp):
                        quarter_recs.remove(quarter)
                        octa_recs.append(quarter)

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
                        for r in sharp_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        staff_flats = [Note(r, "flat", box)
                       for r in flat_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        octa_notes = [Note(r, "8", box, staff_sharps, staff_flats)
                         for r in octa_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        quarter_notes = [Note(r, "4", box, staff_sharps, staff_flats)
                         for r in quarter_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        half_notes = [Note(r, "2", box, staff_sharps, staff_flats)
                      for r in half_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        whole_notes = [Note(r, "1", box, staff_sharps, staff_flats)
                       for r in whole_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]

        staff_notes = quarter_notes + octa_notes + half_notes + whole_notes
        staff_notes.sort(key=lambda n: n.rec.x)
        staffs = [r for r in staff_recs if r.overlap(box) > 0]
        staffs.sort(key=lambda r: r.x)
        note_color = (randint(0, 255), randint(0, 255), randint(0, 255))

        if len(key_changer_recs) > 0:
            for bar in key_changer_recs:
                first_note = staff_notes[0]
                # 조 바뀜이 시작되는 첫 번째 음표 찾기
                for note in staff_notes:
                    if note.rec.x > bar.x:
                        first_note = note

                key_sharps = [sharp for sharp in staff_sharps if sharp.rec.x < staff_notes[0].rec.x]
                key_flats = [flat for flat in staff_flats if flat.rec.x < staff_notes[0].rec.x]

        # 음계 파악
        key_sharps = []    # 조표의 샾
        key_flats = []    # 조표의 플랫
        # x좌표 기준 첫 번째 음표 찾기
        # 샾의 x좌표와 첫 번째 음표 x좌표 비교해서 작은 샾만 조표로 판단
        if len(staff_notes) > 0:
            key_sharps = [sharp for sharp in staff_sharps if sharp.rec.x < staff_notes[0].rec.x]
            key_flats = [flat for flat in staff_flats if flat.rec.x < staff_notes[0].rec.x]

        for note in whole_notes:
            note.set_key(key_sharps, key_flats)

        note_group = []
        i = 0
        j = 0

        while (i < len(staff_notes)):
            if (staff_notes[i].rec.x > staffs[j].x and j < len(staffs)):
                r = staffs[j]
                j += 1
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
        print([note.note + " " + note.sym for note in note_group])

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
            elif note_type == "4":
                duration = 1
            elif note_type == "8":
                duration = 0.5
            pitch = note.pitch
            midi.addNote(track, channel, pitch, time, duration, volume)
            time += duration

    midi.addNote(track, channel, pitch, time, 4, 0)
    # And write it to disk.
    binfile = open("output.mid", 'wb')
    midi.writeFile(binfile)
    binfile.close()
    open_file('output.mid')
