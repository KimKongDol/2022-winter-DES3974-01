# 2022-winter-DES3974-01
Auto Face Blurer by Kim Seong Min

## 이미지 처리
![image](https://user-images.githubusercontent.com/80960504/212221128-d47c4d43-a1da-4bc5-aa3e-899f40fb587e.png)

|구분|원본|수정본|
|------|---|---|
|사람 얼굴 블러(단독)|<img src="https://user-images.githubusercontent.com/80960504/212223023-f94ecf1a-725c-48be-84cd-854a2a55a8e7.jpg" width="300"/>|<img src="https://user-images.githubusercontent.com/80960504/212223122-0d2c8dd7-4094-46ae-82b5-b79a87fc7e7e.png" width="300"/>|
|사람 얼굴 블러(다수)|<img src="https://user-images.githubusercontent.com/80960504/212223238-5eb601bc-ec2b-47a3-8475-15865c391f8e.jpg" width="300"/>|<img src="https://user-images.githubusercontent.com/80960504/212222794-a8571e26-ef86-44b4-a29b-3bb3635ce09d.png" width="300"/>|
|사람 얼굴 필터|<img src="https://user-images.githubusercontent.com/80960504/212223381-7438c885-934e-4b4d-8a5e-0ea16d533731.jpg" width="300"/>|<img src="https://user-images.githubusercontent.com/80960504/212223441-6e02eff5-442e-4e86-a43d-0f7e30d4331d.png" width="300"/>|
|사진 흑백 처리|<img src="https://user-images.githubusercontent.com/80960504/212223598-11e57622-79e4-496f-b32b-c51c95d53d81.jpg" width="300"/>|<img src="https://user-images.githubusercontent.com/80960504/212223553-8f2d4194-5bc0-4bee-a2bf-7837c7804aa4.png" width="300"/>|


## 영상 처리
![image](https://user-images.githubusercontent.com/80960504/212224663-9e9b8470-73c7-4812-838d-32073013ce45.png)

|구분|원본|수정본|
|------|---|---|
|영상 얼굴 블러|<img src="https://user-images.githubusercontent.com/80960504/212224986-8fa618be-21c4-414c-8694-002c43104a7a.png" width="300"/>|<img src="https://user-images.githubusercontent.com/80960504/212224800-cbe0fbf0-dcfa-4706-b687-0c83c4e7105b.png" width="300"/>|
|영상 얼굴 필터|<img src="https://user-images.githubusercontent.com/80960504/212225189-14f66ae8-a198-44ac-92a5-48086a1f32f1.png" width="300"/>|<img src="https://user-images.githubusercontent.com/80960504/212225100-3a68cf9d-db08-43ee-9a61-6a7d2c9694f8.png" width="300"/>|

## 눈여겨볼 코드
+ 사진에서 실제 얼굴 포인트 계산하기

```python
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
```

+ Mediapipe의 Face Detection에서 얼굴을 찾는 옵션

```python
#model_seletction은 mediapipe에서 모델을 캐치하는 방식(0은 2m근거리 얼굴, 1은 5m장거리 얼굴)
    #min_detection_confidence는 어느 퍼센트 정도 확신하면 얼굴이라고 인정할 것인지 정하는 것(높을 수록 견고)

    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
```

+ 파이썬에서 텍스트에 색 넣기
```python
print('\033[48;5;147m'+'이 텍스트는 265컬러 중 147번의 컬러로 **배경색**을 가질거예요'+'\033[0m')
print('\033[38;5;147m'+'이 텍스트는 265컬러 중 147번의 컬러로 **글자색**을 가질거예요'+'\033[0m')
```
