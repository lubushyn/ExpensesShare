from bson import ObjectId

__author__ = 'aliubushyn'
from bson import ObjectId


class ShareCalculator:
    def __init__(self, participants, payments):
        self.participants_count = len(participants)
        self.participants = participants
        self.payments = payments
        #Create empty calculation matrix
        self.calculation_matrix = [[0 for x in xrange(self.participants_count)]
                                   for x in xrange(self.participants_count)]

    def add_dept(self, who, whom, how):
        self.calculation_matrix[who][whom] += how

    def get_participant_id(self, participant_id):
        index = 0
        for p in self.participants:
            if p['_id'] == ObjectId(participant_id):
                return index
            index += index

    def Run(self):
        report = {}
        #Fill matrix
        for payment in self.payments:
            calculation = payment['calculation']

        return report
