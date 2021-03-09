# from cluter_faces import ClusterFaces
# from face_detection import FaceDetection
from action_recognition import ActionRecognition
# import cv2
# import pandas as pd
# import face_recognition
# import numpy as np
# import time
# from tensorflow_object_detection import DetectorAPI
# from plot_utils import resize_image
# from matplotlib import pyplot as plt

# def get_person_id(face_encodings, unknown_face_encoding):
    
#     face_distances = face_recognition.face_distance(face_encodings, unknown_face_encoding)
#     best_match_index = np.argmin(face_distances)
#     print(best_match_index)
#     best_match = pca_df_all_data.iloc[best_match_index]
#     print("best_match name:  {}\n".format(best_match["image_path"]))
#     print("cluster:  {}\n".format(best_match["cluster"]))
#     print("distance:  {}".format(face_distances[best_match_index]))
    
#     return best_match

# def crop_person_from_image(frame, box):
#     # Crop person from image
#     y, x, y2, x2 = [ v for v in box ]

#     margin = 100

#     y = y - margin
#     x = x - margin
#     y2 = y2 + margin
#     x2 = x2 + margin

#     person = frame[y:y2, x:x2]

#     return person

# def draw_faces(image, faces):
#     for face in faces:
#             (x, y, x1, y1) = [ v for v in face["face_location"]]
#             cv2.rectangle(image, (x, y), (x1, y1), (255, 0, 0), 2)

def main():

    print("staart")

    action_recognition = ActionRecognition()
    # face_detection = FaceDetection() 
    # odapi = DetectorAPI()

    print("haliva")

    # object_threshold = 0.80
    # face_threshold = 0.30

    # vs = cv2.VideoCapture("../dataset/videos/a.mp4")
    # rec = []
    # counter = 0

    # #Loop Video Stream   
    # while True:

    #     (grabbed, frame) = vs.read()
        
    #     if frame is None:
    #         break

    #     image = frame.copy()

    #     counter += 1

    #     # Class 1 represents human
    #     persons = odapi.filter_detected_items(1, object_threshold, odapi, frame)
        
    #     # Visualization of the results of a detection.
    #     for person in persons:

    #         # Crop person from image
    #         human = crop_person_from_image(image, person["box"])

    #         # detect_faces
    #         faces = face_detection.detect_faces(human, "a.mp4", face_threshold)
            
    #         # detect_skeletons
    #         skeletons, humans, scale_h = action_recognition.detect_skeletons(human)
            
    #         draw_faces(human, faces)
    #         cv2.imshow('human',human)

    #         dict_id2skeleton = action_recognition.people_track(skeletons)

    #         print("faces")
    #         print(len(faces))

    #         print("skeletons")
    #         print(len(skeletons))
            
    #         if len(skeletons) > 0:

    #             dict_id2label = action_recognition.recognize_action(dict_id2skeleton)
    #             print("---------------------label---------------", dict_id2label)

    #             # person_id = get_person_id(face_encodings, face["face_encoding"])
    #             # date = time.asctime(time.localtime(time.time()))

    #             # rec.append({"time": date,"cluster":  person_id , "action": label})
                
    #     key = cv2.waitKey(1) & 0xFF

    #     if key == ord('q'):
    #         break
       
        
    # cv2.destroyAllWindows()

    # print(rec)

if __name__ == "__main__":
    main()