import optimizers.WOA as woa

import random
import numpy as np


WORKING_SCHEDULE = []


def createPrefs(nurse_num, nurse_shift):
    """ Creates random arrays of nurse preferences """
    nurse_prefs = []
    for i in range(nurse_num):
        pref = []
        for iter in range(nurse_shift):
            pref.append(random.randint(1,5))
        nurse_prefs.append(pref)
    return nurse_prefs


def createSchedule(nurse_num, nurse_shift):
    """ Creates a random schedule """
    global WORKING_SCHEDULE
    WORKING_SCHEDULE = []
    for i in range(nurse_shift): # 14 for night & day shifts for a week
        WORKING_SCHEDULE.append(random.randint(0, nurse_num - 1))
    return WORKING_SCHEDULE


def hardConstraints(nurse_num, nurse_shift):
    """ Creates hard constraints for each nurse 
        Hard Constraints include:
            1: A nurse cannot work morning and night shift on the same day
            2: Cannot work 5 days in a row
            3: Cannot work more than 6 days a week
            """
    global WORKING_SCHEDULE

    # maybe use set here with pairs like 2nd hard constraint
    paired_arrays_within_big_array = []
    for index, shift in enumerate(WORKING_SCHEDULE):
        if index % 2 == 0:
            paired_arrays_within_big_array.append([])
        paired_arrays_within_big_array[-1].append(shift)


    def hardConstraint1():
        """ Nurses cannot work both shifts in a day """
        index1 = 0
        index2 = 1
        counter = 0
        while index2 in range(len(WORKING_SCHEDULE)):
            if WORKING_SCHEDULE[index1] == WORKING_SCHEDULE[index2]:
                return False
            index1 += 2
            index2 += 2



    def hardConstraint2():
        """"" Nurses cannot work 5 days in a row """
        for nurse in range(nurse_num):
            days_in_row = 0
            day = 0
            while day < 7:
                if nurse in paired_arrays_within_big_array[day]:
                    days_in_row += 1
                else:
                    days_in_row = 0
                if days_in_row == 5:
                    return False
                day += 1


    def hardConstraint3():
        """ Nurses cannot work more than 6 days a week  """
        for nurse in range(nurse_num):
            if WORKING_SCHEDULE.count(nurse) > 5:
                return False
    
    # Hard Constraint Checks
    constraint_check1 = hardConstraint1()
    if constraint_check1 == False:
        WORKING_SCHEDULE = createSchedule(nurse_num, nurse_shift)

    constraint_check2 = hardConstraint2()
    if constraint_check2 == False:
        WORKING_SCHEDULE = createSchedule(nurse_num, nurse_shift)

    constraint_check3 = hardConstraint3()
    if constraint_check3 == False:
        WORKING_SCHEDULE = createSchedule(nurse_num, nurse_shift)
    return WORKING_SCHEDULE



def softConstraints(nurse_prefs):
    """ Creates soft constraints for each nurse """
    global WORKING_SCHEDULE
    violations = 0

    for i, nurse in enumerate(WORKING_SCHEDULE):
        violations += nurse_prefs[nurse][i]
    return violations


def its_whale_time(nurse_num, nurse_shifts):
    def objf(): 
        # returns violation score
        createSchedule(nurse_num, nurse_shifts) # creates initial schedule
        hardConstraints(nurse_num, nurse_shifts)

        sc = softConstraints(createPrefs(nurse_num, nurse_shifts))
        return sc # returns violation score

    search_agents = 100
    max_iter = 40
    test_answer = woa.WOA(objf, 1, nurse_num, nurse_shifts, search_agents, max_iter)
    return test_answer


def main():
    w = its_whale_time(49, 14)
    print("BESTINDIVID :", w.bestIndividual) #Leader position -> only changes when fitness is less than current Leader score
    print("CONVERGENT :", w.convergence) #Convergence curve -> fitness number (violation number)
    print("BEST: ", w.best) # The best value out of all the iterations

main()
