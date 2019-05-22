import cv2
import matplotlib.pyplot as plt # 그래프를 그려주는 라이브러리
import numpy as np # 다차원 배열 객체를 다루는 라이브러리

def fit(img, templates, start_percent, stop_percent, threshold): # (전체이미지, 찾고 싶은 이미지, 50, 150, 0.77)
    img_width, img_height = img.shape[::-1] #img.shape에서 width랑 height가져오기
    best_location_count = -1
    best_locations = []
    best_scale = 1

    '''
    plt.axis([0, 2, 0, 1]) # 세로축의 값을 의미합니다.
    plt.show(block=False)

    x = []
    y = []
    '''

    for scale in [i/100.0 for i in range(start_percent, stop_percent + 1, 3)]: # 3pixel만큼 뛰면서 검색 (50,150)
        locations = []
        location_count = 0
        for template in templates:
            template = cv2.resize(template, None,
                fx = scale, fy = scale, interpolation = cv2.INTER_CUBIC) # 이미지를 축소 합니다.

            # 템플릿의 투명한 부분을 인식하도록 투명 마스크 생성
            transparent_mask = generate_transparent_mask(template)
            
            template_width,template_height=template.shape[::-1]
            if img_height>=template_height and img_width>=template_width:
                result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED, mask=transparent_mask)
                result = np.where(result >= threshold)
                location_count += len(result[0])
                locations += [result]
        '''
>>>>>>> 2f88d9f5db8d935c8d27e76abb1004df222ffdba
        print("scale: {0}, hits: {1}".format(scale, location_count))
        x.append(location_count)
        y.append(scale)
        plt.plot(y, x)
        plt.pause(0.00001)
        '''
        if (location_count > best_location_count):
            best_location_count = location_count
            best_locations = locations
            best_scale = scale
            plt.axis([0, 2, 0, best_location_count])
        elif (location_count < best_location_count):
            pass
            
    plt.close()

    return best_locations, best_scale

def generate_transparent_mask(img):
    '''
    투명화 마스크를 생성하여 리턴함
    '''
    channels = cv2.split(img)
    zero_channel = np.zeros_like(channels[0])
    mask = np.array(channels[3])
    mask[channels[3] == 0] = 1
    mask[channels[3] == 100] = 0
    transparent_mask = cv2.merge([zero_channel, zero_channel, zero_channel, mask])

    return transparent_mask