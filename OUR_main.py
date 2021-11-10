import optimizers.WOA as woa

from pprint import pprint
import math
import random
import itertools
import time
import datetime
import os
import numpy as np


WORKING_SCHEDULE = []



def createPrefs(nurse_num):
    """ Creates random arrays of nurse preferences """
    nurse_prefs = []
    for i in range(nurse_num):
        pref = []
        for iter in range(14):
            pref.append(random.randint(1,5))
        nurse_prefs.append(pref)
    return nurse_prefs

def createSchedule(nurse_num):
    """ Creates a random schedule """
    global WORKING_SCHEDULE
    WORKING_SCHEDULE = []
    for i in range(14): # 14 for night & day shifts for a week
        WORKING_SCHEDULE.append(random.randint(0, nurse_num - 1))
    return WORKING_SCHEDULE


def hardConstraints(nurse_num):
    """ Creates hard constrain  ts for each nurse 
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
        WORKING_SCHEDULE = createSchedule(nurse_num)
        
    constraint_check2 = hardConstraint2()
    if constraint_check2 == False:
        WORKING_SCHEDULE = createSchedule(nurse_num)

    constraint_check3 = hardConstraint3()
    if constraint_check3 == False:
        WORKING_SCHEDULE = createSchedule(nurse_num)
        
    return WORKING_SCHEDULE


                
def softConstraints(nurse_prefs):
    """ Creates soft constraints for each nurse """
    global WORKING_SCHEDULE
    violations = 0
    print("NURSE PREFS = ", nurse_prefs)
    for i, nurse in enumerate(WORKING_SCHEDULE):
        # for i in range(len(schedule)):
        # print("WORKING SCHEDULE = ", WORKING_SCHEDULE)
        # print("i = ", i)
        # print("NURSE", nurse)
        # print("NURSE PREFS = ", nurse_prefs)
        # print("ADDED VALUE = ", nurse_prefs[nurse][i])
        violations += nurse_prefs[nurse][i]
    return violations


# def woa(schedule, violation_num, nurse_prefs):
#     best_fitness = []

#     if violation_num < softConstraints(best_fitness, nurse_prefs):
#         best_fitness = schedule

#     return best_fitness

def testing_using_evolo_thing_help(nurse_num, num_shifts):
    # test_answer = woa(benchmark, lb, ub, dim, searchagents, max_iter)
    def objf(x): 
        # rounds every element, and then restructures into a rectangle
        assignment = createSchedule(nurse_num)
        hardConstraints(nurse_num)
        sc = softConstraints(createPrefs(nurse_num))
        return sc

    search_agents = 5
    max_iter = 30
    test_answer = woa.WOA(objf, 1, nurse_num, num_shifts, search_agents, max_iter)
    return test_answer

def main():
    # nurse_num = 10
    # messed_schedule = [1,2,1,9,1,7,4,5,1,3,1,2,1,4]
    # arrays = createPrefs(nurse_num)
    # schedule = createSchedule(nurse_num)
    # constraint_num = hardConstraints(nurse_num)
    # violation_num = softConstraints(arrays)
    # count = 0
    # for array in arrays:
    #     print(f"pref_array{count} =  {array}")
    #     count += 1
    # print("schedule = ", WORKING_SCHEDULE)
    # print("constraint", constraint_num)
    # print("violation_num = ", violation_num)

    # iter = 1
    # for i in range(iter):
    #     woa_output = "something something"
    #     print(woa_output)
    w = testing_using_evolo_thing_help(9, 13)

    print("TESTING WOA : ", w)
    print("BESTINDIVID :", w.bestIndividual, "CONVERGENT :", w.convergence, "BEST: ", w.best)

main()