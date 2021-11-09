# import optimizers.WOA as woa

from pprint import pprint
import math
import random
import itertools
import time
import datetime
import os
import numpy as np


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
    schedule = []
    for i in range(14): # 14 for night & day shifts for a week
        schedule.append(random.randint(0, nurse_num - 1))
    return schedule


def hardConstraints(schedule, nurse_num):
    """ Creates hard constrain  ts for each nurse 
        Hard Constraints include:
            1: A nurse cannot work morning and night shift on the same day
            2: Cannot work 5 days in a row
            3: Cannot work more than 6 days a week
            """

    # maybe use set here with pairs like 2nd hard constraint
    paired_arrays_within_big_array = []
   
    for index, shift in enumerate(schedule):
        if index % 2 == 0:
            paired_arrays_within_big_array.append([])
        paired_arrays_within_big_array[-1].append(shift)
        
    def hardConstraint1():
        """ Nurses cannot work both shifts in a day """
        index1 = 0
        index2 = 1
        counter = 0
        while index2 in range(len(schedule)):
            if schedule[index1] == schedule[index2]:
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
            if schedule.count(nurse) > 5:
                return False

    # Hard Constraint Checks
    constraint_check1 = hardConstraint1()
    if constraint_check1 == False:
        createSchedule(nurse_num)
        
    constraint_check2 = hardConstraint2()
    if constraint_check2 == False:
        createSchedule(nurse_num)

    constraint_check3 = hardConstraint3()
    if constraint_check3 == False:
        createSchedule(nurse_num)
        
    return "Working schedule created"


                
def softConstraints(schedule, nurse_prefs):
    """ Creates soft constraints for each nurse """
    violations = 0
    print("NURSE PREFS = ", nurse_prefs)
    for i, nurse in enumerate(schedule):
        # for i in range(len(schedule)):
        print("i = ", i)
        print("NURSE", nurse)
        print("ADDED VALUE = ", nurse_prefs[nurse][i])
        violations += nurse_prefs[nurse][i]
    return violations


def woa(schedule, violation_num, nurse_prefs):
    best_fitness = []

    if violation_num < softConstraints(best_fitness, nurse_prefs):
        best_fitness = schedule

    return best_fitness




def main():
    nurse_num = 10
    messed_schedule = [1,2,1,9,1,7,4,5,1,3,1,2,1,4]
    arrays = createPrefs(nurse_num)
    schedule = createSchedule(nurse_num)
    constraint_num = hardConstraints(schedule, nurse_num)
    violation_num = softConstraints(schedule, arrays)
    count = 0
    for array in arrays:
        print(f"pref_array{count} =  {array}")
        count += 1
    print("schedule = ", schedule)
    print("constraint", constraint_num)
    print("violation_num = ", violation_num)

    iter = 10
    for i in range(iter):
        woa_output = "something something"
        print(woa_output)

main()