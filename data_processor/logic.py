# co-relation betwn client amount vs credit grade

class GradeVs:
    def __init__(self, a, b):
        self.grade_a = a
        self.grade_b = b


def avg_helper(my_list):
    return sum(my_list)/len(my_list)

def percent_remover(percent):
    state = percent.split('%')
    return float(state[0])

def grade_avg(data):

    client_a, client_b = [], []
    state_a, state_b = [], []
    vs = []
    for row in data:
        # list of client amount and anuual income
        vs.append((row.CODE_GENDER, float(row.AMT_INCOME_TOTAL)))
        if row.CODE_GENDER == 'F':
            client_a.append(float(row.AMT_INCOME_TOTAL))
            state_a.append(float(row.AMT_CREDIT))

        elif row.CODE_GENDER == 'M':
            client_b.append(float(row.AMT_INCOME_TOTAL))
            state_b.append(float(row.AMT_CREDIT))

    client_data = GradeVs((avg_helper(client_a), len(client_a)), (avg_helper(client_b), len(client_b)))
    tate_data = GradeVs((avg_helper(state_a), len(state_a)),(avg_helper(state_b), len(state_b)))
    
    return client_data, tate_data, vs