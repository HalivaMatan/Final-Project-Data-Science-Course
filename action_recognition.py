import numpy as np
import cv2
import argparse
import sys
import os
import libs.action_recognition.utils.lib_images_io as lib_images_io
import libs.action_recognition.utils.lib_plot as lib_plot
import libs.action_recognition.utils.lib_commons as lib_commons
from libs.action_recognition.utils.lib_openpose import SkeletonDetector
from libs.action_recognition.utils.lib_tracker import Tracker
from multi_person_classifier import MultiPersonClassifier
from libs.action_recognition.utils.lib_classifier import ClassifierOnlineTest

class Config:
      def __init__(self):
          cfg_all = lib_commons.read_yaml("libs/action_recognition/config/config.yaml")
          cfg = cfg_all["s5_test.py"]
          self.OPENPOSE_MODEL =  cfg["settings"]["openpose"]["model"]
          self.OPENPOSE_IMG_SIZE = cfg["settings"]["openpose"]["img_size"]
          self.SRC_MODEL_PATH = "models/trained_classifier.pickle"
          self.CLASSES = np.array(cfg_all["classes"])
          self.WINDOW_SIZE = cfg_all["features"]["window_size"]

class ActionRecognition:

    def __init__(self):

        self.config = Config()
        print(self.config.OPENPOSE_MODEL)
        print(self.config.OPENPOSE_IMG_SIZE)
        print(self.config.SRC_MODEL_PATH)
        self.skeleton_detector = SkeletonDetector(self.config.OPENPOSE_MODEL, self.config.OPENPOSE_IMG_SIZE)
        self.multiperson_tracker = Tracker()
        self.multiperson_classifier = MultiPersonClassifier(self.config.SRC_MODEL_PATH, self.config.CLASSES, self.config.WINDOW_SIZE)

    def detect_skeletons(self, img):
        humans = self.skeleton_detector.detect(img)
        print("len humans", len(humans))
        skeletons, scale_h = self.skeleton_detector.humans_to_skels_list(humans)
        print("len skeletons", len(skeletons))
        skeletons,humans = self.remove_skeletons_with_few_joints(skeletons, humans)

        return skeletons, humans, scale_h
    
    def remove_skeletons_with_few_joints(self, skeletons, old_humans):
        ''' Remove bad skeletons before sending to the tracker '''
        good_skeletons = []
        humans = []
        for idx, skeleton in enumerate(skeletons):

            num_valid_joints = self.get_num_of_joints(skeleton, 0, len(skeleton) - 1 )
            num_face_joints = self.get_num_of_joints(skeleton, 28, len(skeleton) - 1 )

            print("num_valid_joints", num_valid_joints,  "num_face_joints", num_face_joints)
            
            if num_valid_joints >= 4 and num_face_joints >= 2:
                good_skeletons.append(skeleton)
                humans.append(old_humans[idx])

        return good_skeletons,humans

    def recognize_action(self, dict_id2skeleton):
        if len(dict_id2skeleton):
            label = self.multiperson_classifier.classify(dict_id2skeleton)
        return label

    def people_track(self, skeletons):
        dict_id2skeleton = self.multiperson_tracker.track(skeletons)
        return dict_id2skeleton

    def get_num_of_joints(self, skeleton, start_index, end_index, step = 2):
        num_valid_joints = 0
        for i in range(start_index, end_index, step):
                if skeleton[i] != 0 and skeleton[i+1] != 0:
                    num_valid_joints += 1
        return num_valid_joints
        
        

