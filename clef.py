import sys
import subprocess
import cv2
import time
import numpy as np
from best_fit import fit
from rectangle import Rectangle
from note import Note
from random import randint

g_clef_files=[
    "resources/template/g_clef.png"
    ]
bass_clef_files=[
    "resources/template/bass_clef.png"
    ]

g_clef_imgs = [cv2.imread(g_clef_file, 0) for g_clef_file in g_clef_files]
bass_clef_imgs = [cv2.imread(bass_clef_file, 0) for bass_clef_file in bass_clef_files]

g_clef_lower, g_clef_upper, g_clef_thresh = 20, 150, 0.45
bass_clef_lower, bass_clef_upper, bass_clef_thresh = 20, 150, 0.65

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



if __name__=="__main__":
    
    img = cv2.imread('resources/samples/lost.jpg', 0)
    img_gray = img#cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img_gray,cv2.COLOR_GRAY2RGB)
    ret,img_gray = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY)
    img_width, img_height = img_gray.shape[::-1]

    print("Matching g_clef image...")
    g_clef_recs = locate_images(img_gray, g_clef_imgs, g_clef_lower, g_clef_upper, g_clef_thresh)

    print("Merging g_clef image results...")
    g_clef_recs = merge_recs([j for i in g_clef_recs for j in i], 0.5)
    g_clef_recs_img = img.copy()
    for r in g_clef_recs:
        r.draw(g_clef_recs_img, (0, 0, 255), 2)
    cv2.imwrite('g_clef_recs_img.png', g_clef_recs_img)
    open_file('g_clef_recs_img.png')

    
    print("Matching bass_clef image...")
    bass_clef_recs = locate_images(img_gray, bass_clef_imgs, bass_clef_lower, bass_clef_upper, bass_clef_thresh)

    print("Merging bass_clef image results...")
    bass_clef_recs = merge_recs([j for i in bass_clef_recs for j in i], 0.5)
    bass_clef_recs_img = img.copy()
    for r in bass_clef_recs:
        r.draw(bass_clef_recs_img, (0, 0, 255), 2)
    cv2.imwrite('bass_clef_recs_img.png', bass_clef_recs_img)
    open_file('bass_clef_recs_img.png')

