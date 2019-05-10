import cv2
import matplotlib.pyplot as plt
import numpy as np

#입력된 확대축소범위에 따라 종류별 2~3개 정도의 template을
# realsheet와 비교하면서 확대비에 따른 비교일치 수치가 임계값을 넘는 위치와 개수를 location에 저장
# 확대비 하나 당 얼마나 비슷한지 개수 그래프로 보여주고
# best_location(max)는 확대비 하나 돌릴 때마다 가장 많이 같을 경우
# 저장됨
# 결국 가장 많이 비슷한 확대비와 sheet내 비슷한 위치리스트가 return
def fit(img, templates, start_percent, stop_percent, threshold):
    img_width, img_height = img.shape[::-1]
    best_location_count = -1
    best_locations = []
    best_scale = 1

    plt.axis([0, 2, 0, 1])
    plt.show(block=False)

    x = []
    y = []
    for scale in [i/100.0 for i in range(start_percent, stop_percent + 1, 3)]:
        locations = []
        location_count = 0
        for template in templates:
            template = cv2.resize(template, None,
                fx = scale, fy = scale, interpolation = cv2.INTER_CUBIC)
            result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            result = np.where(result >= threshold)
            location_count += len(result[0])
            locations += [result]
        print("scale: {0}, hits: {1}".format(scale, location_count))
        x.append(location_count)
        y.append(scale)
        plt.plot(y, x)
        plt.pause(0.00001)
        if (location_count > best_location_count):
            best_location_count = location_count
            best_locations = locations
            best_scale = scale
            plt.axis([0, 2, 0, best_location_count])
        elif (location_count < best_location_count):
            pass
    plt.close()

    return best_locations, best_scale