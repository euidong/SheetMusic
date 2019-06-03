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

# 높은음자리표 파일 경로
g_clef_files=[
    "resources/template/g_clef.png"]
# 낮음음자리표 파일 경로
bass_clef_files=[
    "resources/template/bass_clef.png"  ]
quarter_files = [
    "resources/template/quarter.png",
    "resources/template/solid-note.png"]
sharp_files = [
    "resources/template/sharp.png",
    "resources/template/f-sharp.png",
    "resources/template/f-sharp2.png"]
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
    "resources/template/bar-rest.png",
    "resources/template/bar-rest2.png"]
halfRest_files = [
    "resources/template/half_rest.png"]
quarterRest_files=[
    "resources/template/quarter_rest.png"]
eighthRest_files=[
    "resources/template/eight_rest.png",
    "resources/template/eight_rest2.png"]
replay_files = [
    "resources/template/replay.png",
    "resources/template/dodol.png"] #도돌이표 이미지 추가

quarter_imgs = [cv2.imread(quarter_file, 0) for quarter_file in quarter_files]
g_clef_imgs = [cv2.imread(g_clef_file, 0) for g_clef_file in g_clef_files]
bass_clef_imgs = [cv2.imread(bass_clef_file, 0) for bass_clef_file in bass_clef_files]
quarter_imgs = [cv2.imread(quarter_file, 0) for quarter_file in quarter_files]
sharp_imgs = [cv2.imread(sharp_files, 0) for sharp_files in sharp_files] # 샾 이미지
flat_imgs = [cv2.imread(flat_file, 0) for flat_file in flat_files]
half_imgs = [cv2.imread(half_file, 0) for half_file in half_files]
whole_imgs = [cv2.imread(whole_file, 0) for whole_file in whole_files]

wholeRest_imgs = [cv2.imread(wholeRest_file,0) for wholeRest_file in wholeRest_files]
halfRest_imgs = [cv2.imread(halfRest_file,0) for halfRest_file in halfRest_files]
quarterRest_imgs = [cv2.imread(quarterRest_file,0) for quarterRest_file in quarterRest_files]
eighthRest_imgs = [cv2.imread(eighthRest_file,0) for eighthRest_file in eighthRest_files]

replay_imgs = [cv2.imread(replay_file, 0) for replay_file in replay_files]#replay추가

sharp_lower, sharp_upper, sharp_thresh = 50, 150, 0.70
flat_lower, flat_upper, flat_thresh = 50, 150, 0.77
quarter_lower, quarter_upper, quarter_thresh = 50, 100, 0.77
half_lower, half_upper, half_thresh = 50, 150, 0.70
whole_lower, whole_upper, whole_thresh = 50, 150, 0.70

wholeRest_lower,wholeRest_upper,wholeRest_thresh =50,150,0.80
halfRest_lower, halfRest_upper, halfRest_thresh =50,150,0.80
quarterRest_lower, quarterRest_upper, quarterRest_thresh =50,150,0.70
eighthRest_lower, eighthRest_upper,eighthRest_thresh= 50,100,0.85

replay_lower, replay_upper, replay_thresh = 50, 150, 0.60

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

def find_g_clef(measure_img, g_clef_templates, bass_clef_templates):
    '''
    악보 이미지에서 음자리표 찾아 높은음자리표면 True를 반환하는 함수
    '''
    is_g_clef = True   # 높은음자리인지 판단. false면 낮은음자리표

    g_clef_lower, g_clef_upper, g_clef_thresh = 20, 150, 0.45
    bass_clef_lower, bass_clef_upper, bass_clef_thresh = 20, 150, 0.65

    g_clef_imgs = [cv2.imread(g_clef_file, 0) for g_clef_file in g_clef_files]
    bass_clef_imgs = [cv2.imread(bass_clef_file, 0) for bass_clef_file in bass_clef_files]

    g_clef_recs = match_and_merge(img_gray, g_clef_imgs, g_clef_lower, g_clef_upper, g_clef_thresh)
    bass_clef_recs = match_and_merge(img_gray, bass_clef_imgs, bass_clef_lower, bass_clef_upper, bass_clef_thresh)

    # 낮은음자리표 검출되면 false
    if len(bass_clef_recs) > 0:
        is_g_clef = False

    return is_g_clef

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

    #img_gray: 받아오는 이미지
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
    '''
    for idx, cut_measure in enumerate(staff_boxes):
        cv2.imwrite('cutting{}.png'.format(idx), cut_measure)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    # sharp
    sharp_recs = match_and_merge(img_gray, sharp_imgs, sharp_lower, sharp_upper, sharp_thresh)
    # flat
    flat_recs = match_and_merge(img_gray, flat_imgs, flat_lower, flat_upper, flat_thresh)

    # note
    quarter_recs = match_and_merge(img_gray, quarter_imgs, quarter_lower, quarter_upper, quarter_thresh)
    '''
    half_recs = match_and_merge(img_gray, half_imgs, half_lower, half_upper, half_thresh)
    whole_recs = match_and_merge(img_gray, whole_imgs, whole_lower, whole_upper, whole_thresh)

    # rest
    wholeRest_recs = match_and_merge(img_gray, wholeRest_imgs, wholeRest_lower, wholeRest_upper, wholeRest_thresh)
    halfRest_recs = match_and_merge(img_gray, halfRest_imgs, halfRest_lower, halfRest_upper, halfRest_thresh)
    quarterRest_recs = match_and_merge(img_gray, quarterRest_imgs, quarterRest_lower, quarterRest_upper,quarterRest_thresh)
    eighthRest_recs = match_and_merge(img_gray, eighthRest_imgs, eighthRest_lower, eighthRest_upper,eighthRest_thresh)

    # replay
    replay_recs = match_and_merge(img_gray, replay_imgs, replay_lower, replay_upper, replay_thresh)
    '''
    note_group = []
    for box in staff_boxes:
        staff_sharps = [Note(r, "sharp", box)
                        for r in sharp_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        staff_flats =[Note(r, "flat", box)
                       for r in flat_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        quarter_notes = [Note(r, "4,8", box)
                         for r in quarter_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        '''
        half_notes = [Note(r, "2", box, staff_sharps, staff_flats)
                      for r in half_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        whole_notes = [Note(r, "1", box, staff_sharps, staff_flats)
                       for r in whole_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]

        whole_rests = [Note(r, "-1", box)
                       for r in wholeRest_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        half_rests = [Note(r, "-2", box)
                      for r in halfRest_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        quarter_rests = [Note(r, "-4", box)
                         for r in quarterRest_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        eighth_rests = [Note(r, "-8", box)
                        for r in eighthRest_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]

        replay = [Note(r, "-0", box)
                  for r in replay_recs if abs(r.middle[1] - box.middle[1]) < box.h * 5.0 / 8.0]
        '''
        staff_notes = quarter_notes # + half_notes + whole_notes + replay + quarter_rests + half_rests + whole_rests + eighth_rests
        staff_notes.sort(key=lambda n: n.rec.x)
        note_color = (randint(0, 255), randint(0, 255), randint(0, 255))

        i = 0
        while (i < len(staff_notes)):
            note_group.append(staff_notes[i])
            staff_notes[i].rec.draw(img, note_color, 2)
            i += 1
    # 음계 파악
    key_sharps = []    # 조표의 샾
    key_flats = []    # 조표의 플랫
    # x좌표 기준 첫 번째 음표 찾기
    # 샾의 x좌표와 첫 번째 음표 x좌표 비교해서 작은 샾만 조표로 판단
    if len(staff_notes) > 0:
        key_sharps = [sharp for sharp in staff_sharps if sharp.rec.x < staff_notes[0].rec.x]
        key_flats = [flat for flat in staff_flats if flat.rec.x < staff_notes[0].rec.x]

    #음자리표 결정
    isGclef = find_g_clef(staff_boxes[0], g_clef_files, bass_clef_files)

    for note in note_group:
        note.set_key(isGclef, key_sharps, staff_sharps, staff_flats)

    for r in staff_boxes:
        r.draw(img, (0, 0, 255), 2)
    for r in sharp_recs:
        r.draw(img, (0, 0, 255), 2)
    flat_recs_img = img.copy()
    for r in flat_recs:
        r.draw(img, (0, 0, 255), 2)

    cv2.imwrite('res.png', img)
    open_file('res.png')



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
    midi.addTempo(track, time, 130)


    duration = None
    for note in note_group:
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
