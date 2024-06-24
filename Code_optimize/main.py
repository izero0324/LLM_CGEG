from get_data import get_n_evaluate_data
from run_txt import test_code

n = 100
bad_data = 0
score = 0
counter = 0
dataset = get_n_evaluate_data(n)
for key in dataset:
    # print(key)
    # print(dataset[key]['Best_sol'])
    # print(dataset[key]['IO'])
    (a,b,c) = test_code(dataset[key]['Best_sol'], dataset[key]['IO'])
    if a == -1:
        bad_data += 1
    else:
        score += a
    counter+=1
    if counter%10 ==0:
        print(counter, "%", " done!")

print(score, bad_data)