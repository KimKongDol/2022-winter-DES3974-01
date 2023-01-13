import os
file_path = 'C:/Users/user/PythonImageWorkspace/얼굴인식플젝'
file_list = os.listdir(file_path)
#OpenCV를 사용한다
import cv2
# 미디어파이프 사용
import mediapipe as mp

def vid_blur(file):
    #얼굴을 찾고 찾은 얼굴에 표시를 하기 위한 변수
    #얼굴 검출을 위한 face_detection모듈 사용
    mp_face_detection = mp.solutions.face_detection
    #얼굴의 특징을 그리기위한 drawing 모듈 사용
    mp_drawing = mp.solutions.drawing_utils

    # 동영상 파일 열기
    cap = cv2.VideoCapture(file)

    #자동으로 파일을 닫기 위해 with문 사용
    #model_seletction은 mediapipe에서 모델을 캐치하는 방식(0은 2m근거리 얼굴, 1은 5m장거리 얼굴)
    #min_detection_confidence는 어느 퍼센트 정도 확신하면 얼굴이라고 인정할 것인지 정하는 것(높을 수록 견고)

    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        while cap.isOpened():
            #프레임하나씩 읽어서 image로 저장
            success, image = cap.read()
            if not success:
                print("종료")
            # continue를 사용하면 웹캠을 쓸 수도 있게됨.
                break;

            # 성능향상을 위해 비디오를 수정할 수 없도록 지정(mediapip참고)  
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)#BGR를 RGB로 변경
            results = face_detection.process(image)

            # 작업이 끝나면 얼굴 부분을 그릴 수 있도록 비디오 수정하게 함
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            overlay = image.copy()
            
            #검출된 얼굴이 있으면 darawing
            if results.detections:
                for detection in results.detections:
                    # mp_drawing.draw_detection(image, detection)
                    #6개의 특징: 오른쪽 눈, 왼쪽 눈, 코 끝부분, 입 중심, 오른쪽 귀, 왼쪽 귀
                    print(detection)
                    
                    #특정위치 가져오기
                    keypoints = detection.location_data.relative_keypoints
                    right_eye = keypoints[0]
                    left_eye = keypoints[1]
                    nose = keypoints[2]
                    mouth = keypoints[3]
                    right_ear = keypoints[4]
                    left_ear = keypoints[5]

                    full_face = detection.location_data.relative_bounding_box
                    
                    #이미지의 크기를 가져와서 정확한 실제 위치 계산
                    h, w, _ = image.shape #height, width, channel : 이미지로부터 세로,가로 크기 가져옴
                    nose = (int(nose.x*w), int(nose.y*h)) #튜플 형태로 저장
                    radius = int(full_face.height*h/2)
                    
                    #동그라미 그릴 예정(대상,중심점,반지름,색깔,선두께,선특징)
                    cv2.circle(overlay,nose, radius, (227, 237, 248),cv2.FILLED,cv2.LINE_AA)#파란색
                    alpha = 0.8 #투명도
                    image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)    
                    
            
            # 윈도우에 보여주는 작업
            cv2.imshow('Blurred Video.....', cv2.resize(image,None,fx=0.5,fy=0.5))
            #Q누르면 빠져나오기
            if cv2.waitKey(1) == ord('q'): 
                break
    cap.release()
    cv2.destroyAllWindows()

def vid_filter(file):
    #얼굴을 찾고 찾은 얼굴에 표시를 하기 위한 변수
    #얼굴 검출을 위한 face_detection모듈 사용
    mp_face_detection = mp.solutions.face_detection

    #4채널을 3채널로 바꾸는 함수
    def channel_changer(image, x,y,w,h,overlay_image):
        alpha = overlay_image[:,:,3]
        mask_image = alpha/255
        for c in range(0,3):
            image[y-h:y+h, x-w:x+w,c] = (overlay_image[:,:,c]*mask_image)+(image[y-h:y+h,x-w:x+w,c]*(1-mask_image))

    #이미지 불러 오기
    face_nose_filter = cv2.imread('cat_nose.png',cv2.IMREAD_UNCHANGED)
    face_heart_filter = cv2.imread('heart.png',cv2.IMREAD_UNCHANGED)

    # 동영상 파일 열기
    cap = cv2.VideoCapture(file)

    #자동으로 파일을 닫기 위해 with문 사용
    #model_seletction은 mediapipe에서 모델을 캐치하는 방식(0은 2m근거리 얼굴, 1은 5m장거리 얼굴)
    #min_detection_confidence는 어느 퍼센트 정도 확신하면 얼굴이라고 인정할 것인지 정하는 것(높을 수록 견고)

    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        while cap.isOpened():
            #프레임하나씩 읽어서 image로 저장
            success, image = cap.read()
            if not success:
                print("종료")
            # continue를 사용하면 웹캠을 쓸 수도 있게됨.
                break;

            # 성능향상을 위해 비디오를 수정할 수 없도록 지정(mediapip참고)  
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)#BGR를 RGB로 변경
            results = face_detection.process(image)

            # 작업이 끝나면 얼굴 부분을 그릴 수 있도록 비디오 수정하게 함
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
            #검출된 얼굴이 있으면 darawing
            if results.detections:
                for detection in results.detections:
                    #6개의 특징: 오른쪽 눈, 왼쪽 눈, 코 끝부분, 입 중심, 오른쪽 귀, 왼쪽 귀
                    print(detection)
                        
                    #특정위치 가져오기
                    keypoints = detection.location_data.relative_keypoints
                    full_face =  detection.location_data.relative_bounding_box
                    face_height = full_face.height
                    right_eye = keypoints[0]
                    left_eye = keypoints[1]
                    nose = keypoints[2]
                    mouth = keypoints[3]
                        
                    #이미지의 크기를 가져와서 정확한 실제 위치 계산
                    h, w, _ = image.shape #height, width, channel : 이미지로부터 세로,가로 크기 가져옴
                    right_eye = (int(right_eye.x*w), int(right_eye.y*h)) #튜플 형태로 저장
                    left_eye = (int(left_eye.x*w),int(left_eye.y*h))
                    nose = (int(nose.x*w),int( nose.y*h ))
                    mouth = (int(mouth.x*w),int(mouth.y*h))
                        
                    #양 눈에 동그라미 그릴 예정(대상,중심점,반지름,색깔,선두께,선특징)
                    # cv2.circle(image,right_eye, 50, (255,0,0),10,cv2.LINE_AA)#파란색
                    # cv2.circle(image,left_eye, 50, (0,255,0),10,cv2.LINE_AA)#초록색
                        
                    #channel_changer(image, x,y,w,h,overlay_image)
                    channel_changer(image,*nose,150,75,face_nose_filter)
                    channel_changer(image, *right_eye,75,75,face_heart_filter)                
                    channel_changer(image, *left_eye,75,75,face_heart_filter)             
                        
                
            # 윈도우에 보여주는 작업
            cv2.imshow('Face Filtering...', cv2.resize(image,None,fx=0.3,fy=0.3))
            # cv2.imshow('Finalllll Face Detection Testing.....', image)


            #Q누르면 빠져나오기
            if cv2.waitKey(1) == ord('q'): 
                break
    cap.release()
    cv2.destroyAllWindows()

print('\033[48;5;147m'+'--------영상을 수정하는 공간입니다--------'+'\033[0m')
print('\n[동영상 목록]')
for index in range (0,len(file_list)):
    if file_list[int(index)].endswith('.mp4'):
        print('고유 인덱스:',index, '(파일명:',file_list[int(index)],')')

print('\033[48;5;212m'+'수정할 영상의 고유 인덱스를 입력하세요'+ '\033[0m')
selected = input(':')
selected=file_list[int(selected)]

print('\033[48;5;212m'+' 선택된 영상은 다음과 같습니다.'+ '\033[0m \n',selected)

print('\n\033[48;5;149m'+'원하는 작업 번호를 숫자로 입력해주세요'+'\033[0m')
print('1) 사람 얼굴 모두 블러')
print('2) 사람 얼굴에 필터씌우기')
action = input(':')


if int(action)==1 : #블러
    print('\033[48;5;149m'+'<사람 얼굴 모두 블러>를 수행합니다.'+ '\033[0m')
    print(selected)
    vid_blur(selected)
else : #필터
    print('\033[48;5;149m'+'<사람 얼굴에 필터씌우기>를 수행합니다.'+ '\033[0m')
    vid_filter(selected)