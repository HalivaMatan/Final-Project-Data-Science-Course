from libs.action_recognition.utils.lib_classifier import ClassifierOnlineTest
import os

class MultiPersonClassifier(object):
    ''' This is a wrapper around ClassifierOnlineTest
        for recognizing actions of multiple people.
    '''

    def __init__(self, model_path, classes, window_size):

        self.dict_id2clf = {}  # human id -> classifier of this person

        # Define a function for creating classifier for new people.
        self._create_classifier = lambda human_id: ClassifierOnlineTest(
            model_path, classes, window_size, human_id)

    def classify(self, dict_id2skeleton):

        # Clear people not in view
        old_ids = set(self.dict_id2clf)
        cur_ids = set(dict_id2skeleton)
        humans_not_in_view = list(old_ids - cur_ids)
        for human in humans_not_in_view:
            del self.dict_id2clf[human]

        # Predict each person's action
        id2label = {}
        for id, skeleton in dict_id2skeleton.items():

            if id not in self.dict_id2clf:  # add this new person
                os.chdir('libs/action_recognition')
                self.dict_id2clf[id] = self._create_classifier(id)
                os.chdir('../..') 

            classifier = self.dict_id2clf[id]
            id2label[id] = classifier.predict(skeleton)  # predict label

        return id2label
