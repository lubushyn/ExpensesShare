__author__ = 'aliubushyn'


class ShareCalculator:
    def __init__(self, participants, payments):
        self.participants_count = len(participants)
        self.participants = participants
        self.payments = payments
        #Create empty calculation matrix
        self.calculation_matrix = [[0] * self.participants_count
                                   for x in xrange(self.participants_count)]


    def analize_participant(self, participant):
        debit_calculation = []
        credit_calculation = []
        debit = 0
        credit = 0
        i = 0
        who = self.get_participant_id(participant['id'])
        calced = 0
        for m in self.calculation_matrix[who]:
        #            if m > 0:
            calced = m - self.calculation_matrix[i][who]
            if calced > 0:
                debit_calculation.append({"name": self.participants[i]['name'],
                                          "id": self.participants[i]['id'],
                                          "total": str(calced)})
                debit += calced
            if calced < 0:
                credit_calculation.append({"name": self.participants[i]['name'],
                                           "id": self.participants[i]['id'],
                                           "total": str(abs(calced))})
                credit += calced
            i += 1

        report = {"participant": {"name": str(participant['name']),
                                  "id": str(participant['id'])},
                  "result": {"total_debit": round(debit,2), "total_credit": abs(round(credit,2)),
                             "debit": debit_calculation,
                             "credit": credit_calculation}}
        return report

    def analize_calculation_matrix(self):
        report = []
        for participant in self.participants:
            report.append(self.analize_participant(participant))
        return report

    def add_dept(self, who, whom, how):
        self.calculation_matrix[who][whom] = self.calculation_matrix[who][whom] + how

    def get_participant_id(self, participant_id):
        index = 0
        for p in self.participants:
            if str(p['id']) == str(participant_id):
                return index
            index += 1

    def Run(self):
        #Fill matrix
        for payment in self.payments:
            calculation = payment['calculation']
            whom = payment['payer']
            for p in payment['participants']:
                id = self.get_participant_id(p)
                whom_id = self.get_participant_id(whom)
                if len(calculation)>id:
                    self.add_dept(id, whom_id, calculation[id]["share"])
        report = self.analize_calculation_matrix()
        return report
