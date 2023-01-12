import os
file_path = 'C:/Users/user/PythonImageWorkspace/얼굴인식플젝'
file_list = os.listdir(file_path)
#OpenCV를 사용한다
import cv2
# 미디어파이프 사용
import mediapipe as mp

#얼굴을 찾고 찾은 얼굴에 표시를 하기 위한 변수
#얼굴 검출을 위한 face_detection모듈 사용
mp_face_detection = mp.solutions.face_detection
#얼굴의 특징을 그리기위한 drawing 모듈 사용
mp_drawing = mp.solutions.drawing_utils

#4채널을 3채널로 바꾸는 함수
def channel_changer(image, x,y,w,h,overlay_image):
    alpha = overlay_image[:,:,3]
    mask_image = alpha/255
    for c in range(0,3):
        image[y-h:y+h, x-w:x+w,c] = (overlay_image[:,:,c]*mask_image)+(image[y-h:y+h,x-w:x+w,c]*(1-mask_image))

#블러처리하는 함수
def blurring(files): 
    IMAGE_FILES = files
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        for idx, file in enumerate(IMAGE_FILES):
            image = cv2.imread(file)#이미지 파일 들고옴

            # BGR image을 RGB로 바꿈.
            results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # 발견한 모든 얼굴에 표시하기 위해 점 찍음
            if not results.detections:
                continue
            annotated_image = image.copy()
            overlay = image.copy()

            i = 0
            for detection in results.detections:                                
                    print(i,'번째 사람 얼굴 위치\n',detection.location_data.relative_bounding_box)                
                    print('코 끝 좌표:')        
                    print(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
                    i=i+1
                    
                    nose = mp_face_detection.get_key_point
                    (detection, mp_face_detection.FaceKeyPoint.NOSE_TIP)
                    h,w,_ = image.shape
                    
                    #실제 코와 얼굴 반쪽 너비
                    nose = (int(nose.x*w),int(nose.y*h))
                    radius = int(detection.location_data.relative_bounding_box.width*w/2)
                    
                    #동그라미 그릴 예정(대상,중심점,반지름,색깔,선두께,선특징)
                    cv2.circle(overlay,nose, radius, (227, 237, 248),cv2.FILLED,cv2.LINE_AA)#파란색
                    alpha = 0.9 #투명도
                    annotated_image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)                

            # 윈도우에 보여주는 작업
            cv2.imshow('Blurring...',annotated_image)

            result = cv2.imwrite('result/'+selected[idx]+'_blurred.png',annotated_image)
            if result : print('\033[31m' +'저장성공'+'\033[0m')

            #기다림
            key = cv2.waitKey(0)
            if(key == 32) : 
                print('스페이스바 눌려서 다 끔')            
                
    cap.release()
    cv2.destroyAllWindows()

#흑백처리하는 함수
def gray_coloring(files):
    for i in range (0,len(files)):
        gray_image = cv2.imread(files[int(i)],cv2.IMREAD_GRAYSCALE)
        cv2.imshow('Gray Coloring...',gray_image)
        cv2.waitKey(0)
        result = cv2.imwrite('result/'+files[int(i)]+'_gray.png',gray_image)
        if result : print('\033[31m' +'저장성공'+'\033[0m')
        cv2.destroyAllWindows()


#필터를 씌우는 함수
def filtering(files):
    #이미지 불러 오기
    face_filter = cv2.imread('face_filter.png',cv2.IMREAD_UNCHANGED)

    IMAGE_FILES = files
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        for idx, file in enumerate(IMAGE_FILES):
            image = cv2.imread(file)#이미지 파일 들고옴

            # BGR image을 RGB로 바꿈.
            results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # 발견한 모든 얼굴에 표시하기 위해 점 찍음
            if not results.detections:
                continue
            annotated_image = image.copy()

            i = 0
            for detection in results.detections:                                
                    full_face = detection.location_data.relative_bounding_box
                    print(i,'번째 사람 얼굴 위치\n',full_face) 
                    i=i+1
                    
                    nose = mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.NOSE_TIP)
                    print('코 끝 좌표\n',nose)
                    h,w,_ = image.shape
                    
                    #실제 코 위치에서 좀 더 위
                    face_height = int(full_face.height*h)
                    nose = (int(nose.x*w),int(nose.y*h-face_height/2))
                    
                    #channel_changer(image, x,y,w,h,overlay_image)
                    channel_changer(annotated_image,*nose,150,75,face_filter)               

            # 윈도우에 보여주는 작업
            cv2.imshow('Filtering...',annotated_image)

            result = cv2.imwrite('result/'+selected[idx]+'_filtered.png',annotated_image)
            if result : print('\033[31m' +'저장성공'+'\033[0m')

            #기다림
            key = cv2.waitKey(0)
            if(key == 32) : 
                print('스페이스바 눌려서 다 끔')            
                
    cap.release()
    cv2.destroyAllWindows()
    

print('\033[104m'+'--------사진을 수정하는 공간입니다--------'+'\033[0m')
print('[폴더의 이미지 목록]')
for index in range (0,len(file_list)):
    if (file_list[int(index)].endswith('.png') or 
    file_list[int(index)].endswith('.jpg') or file_list[int(index)].endswith('.jpeg') ):
        print('고유 인덱스:',index, '(파일명:',file_list[int(index)],')')

# print('\n[동영상 목록]')
# for index in range (0,len(file_list)):
#     if file_list[int(index)].endswith('.mp4'):
#         print('고유 인덱스:',index, '(파일명:',file_list[int(index)],')')

print('\033[43m'+'수정할 이미지들의 고유 인덱스를 입력하세요(콤마구분)'+ '\033[0m')
selected = input(':').split(',')
for i in range (0,len(selected)):
    selected_index = selected[i]
    selected[i]=file_list[int(selected_index)]

print('\033[43m'+' 선택된 파일들은 다음과 같습니다.'+ '\033[0m \n',selected)

print('\n\033[102m'+'원하는 작업 번호를 숫자로 입력해주세요'+'\033[0m')
print('1) 사람 얼굴 모두 블러')
print('2) 사람 얼굴에 필터씌우기')
print('3) 모두 흑백 처리')
actions = ['사람 얼굴 모두 블러','사람 얼굴에 필터씌우기','모두 흑백 처리']
action = input(':')


if int(action)==1 : #블러
    print('\033[102m'+'<사람 얼굴 모두 블러>를 수행합니다.'+ '\033[0m')
    blurring(selected)
elif int(action)==2: #필터
    print('\033[102m'+'<사람 얼굴에 필터씌우기>를 수행합니다.'+ '\033[0m')
    filtering(selected)
else : #흑백
    print('\033[102m'+'<모두 흑백 처리>를 수행합니다.'+ '\033[0m')
    gray_coloring(selected)


