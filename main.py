# from main import convertToCsv
import optimizers.WOA as woa
from pprint import pprint
import random
import numpy as np
import collections
import datetime
import csv
import plot_boxplot as boxplot


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
        createSchedule(nurse_num, nurse_shifts) # creates new sschedule
        hardConstraints(nurse_num, nurse_shifts)
        sc = softConstraints(prefs)
        return sc # returns violation score
    prefs = createPrefs(nurse_num, nurse_shifts)
    search_agents = 70
    max_iter = 35000
    runs = 5
    test_answers = []
    iter_list = []
    for i in range(runs):
        print("Starting Run: ", i+1)
        result = woa.WOA(objf, 0, nurse_num, nurse_shifts, search_agents, max_iter)
        print("Result Convergence = ", result.convergence)
        existing_point = set()
        current_iter = 0
        for iter, point in enumerate(result.convergence):
            if point not in existing_point:
                print(f"The convergence changed to {point} at iteration {iter+1}")
                current_iter = iter + 1
            existing_point.add(point)
        test_answers.append(result)
        iter_list.append(current_iter)
    return format_results(test_answers, max_iter, search_agents, runs, iter_list)


def format_results(results, max_iters, search_agents, runs, avg_tries):
    """ Creates average results """
    current_date = datetime.datetime.now()
    average_time = 0
    average_best = 0
    average_worst = 0
    average_iter = 0
    for result in results:
        average_time += result.executionTime
        average_best += result.best
        average_worst += result.convergence[0]
    for iter in avg_tries:
        average_iter += iter
    average_time /= runs
    average_best /= runs
    average_worst /= runs
    average_iter /= runs
    return current_date, average_time, average_best, average_worst, max_iters, search_agents, runs, average_iter


def createCsv(current_date, average_time, average_best, average_worst, max_iters, search_agents, runs, avg_tries):
    """ Takes results, outputs CSV """
    csv_name = f"averageResults{max_iters}Iters{search_agents}SearchAgents.csv"
    with open(csv_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Current Date', 'Avg Time', 'Avg Best', 'Avg Worst', 'Max Iterations', 'Search Agents', 'Runs', "Avg Iterations For Result"])
        writer.writerow([current_date, average_time, average_best, average_worst, max_iters, search_agents, runs, avg_tries])
    file.close()

    with open("allResults.csv", "a", newline='') as file:
        writer = csv.writer(file)
        # writer.writerow(['Current Date', 'Avg Time', 'Avg Best', 'Avg Worst', 'Max Iterations', 'Search Agents', 'Runs', "Avg Iterations For Result"])
        writer.writerow([current_date, average_time, average_best, average_worst, max_iters, search_agents, runs, avg_tries])
    file.close()
    
# def createBoxplot():
#   boxplot("/WOA_results.csv", "WOA", 100)

def main():
    current_date, average_time, average_best, average_worst, max_iters, search_agents, runs, avg_tries = its_whale_time(99, 14)
    # print("NURSE PREFERENCES WERE :", pref)
    # print("w attributes = ", w.__dict__)
    # print("BESTINDIVID :", w.bestIndividual) #Leader position -> only changes when fitness is less than current Leader score
    # print("CONVERGENT :", w.convergence) #Convergence curve -> fitness number (violation number)
    # print("BEST : ", w.best) # The best value out of all the iterations
    createCsv(current_date, average_time, average_best, average_worst, max_iters, search_agents, runs, avg_tries)
main()
