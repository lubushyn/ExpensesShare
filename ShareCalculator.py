__author__ = 'aliubushyn'




class ShareCalculator:
    def __init__(self, participants, payments):
        self.participants_count = len(participants)
        self.participants = participants
        self.payments = payments
        #Create empty calculation matrix
        self.calculation_matrix = [[0 for x in xrange(self.participants_count)]
                                   for x in xrange(self.participants_count)]


    def analize_participant(self, participant):
        report = {"name":participant["name"],"result":{"total_debit": 50, "total_credit": 100,
                  "debit":[{"name": "Alexander Liubushyn", "_id": "14328735", "total":10},
                           {"name": "Artem Gornostal", "_id": "148735", "total":40}],
                  "credit": [{"name": "Alexander Ivanov", "_id": "14328735", "total":10},
                           {"name": "Artem Azarov", "_id": "148735", "total":40}]}}
        return report

    def analize_calculation_matrix(self):
        report = []
        for participant in self.participants:
            report.append(self.analize_participant(participant))
        return report

    def add_dept(self, who, whom, how):
        self.calculation_matrix[who][whom] += how

    def get_participant_id(self, participant_id):
        index = 0
        for p in self.participants:
            if str(p["_id"]) == str(participant_id):
                return index
            index += 1

    def Run(self):
        #Fill matrix
        for payment in self.payments:
            calculation = payment['calculation']
            whom = payment['payer']
            for p in payment['participants']:
                id = self.get_participant_id(p["_id"])
                whom_id = self.get_participant_id(whom["_id"])
                self.add_dept(id, whom_id, calculation[id]["share"])
        report = self.analize_calculation_matrix()
        return report
