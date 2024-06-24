from os import scandir, path, walk
import random
import json

mypath = './unzip_data/GEC/train/'

# Read file
def read_file(key, target, is_json=False):

    file_path = path.join(mypath, str(key), target)
    if is_json:
        with open(file_path) as json_file:
            return json.load(json_file)
    try:
        with open(file_path, 'r') as file:
            return file.read() # Assign the content to the corresponding key in the dictionary
    except Exception as e:
        raise e

def get_best_solution(key):
    _file_path = path.join(mypath, str(key), 'Acc_solutions')
    try:
        _file = sorted([files for root, dirs, files in walk(_file_path)])[0][0]
        return _file, float(_file.split(' ms')[0].replace(',','.'))
    except Exception as e:
        return 0, 0
        #raise e

def sampleing(n):
    # pick sample
    testcase = [ f.path for f in scandir(mypath) if f.is_dir()]
    num_of_testcase = len(testcase)
    samples = sorted(random.sample(range(0,num_of_testcase), n))
    return [f"{num:04d}" for num in samples]


def get_n_evaluate_data(n):
    formatted_samples = sampleing(n)

    # Generate dict for evaluation
    data_dict = {str(num): {} for num in formatted_samples}

    # Update data_dict
    for key in data_dict:
        best_sol_file, best_time = get_best_solution(key)
        data_dict[key] = {
            'Question': read_file(key, 'Question.txt'),
            'IO': read_file(key, 'input_output.json', True),
            'Best_time' : best_time,
            'Best_sol' : read_file(key, 'Accepted.json').replace("\\n","\n").replace("\\t","\t")
        }

    return(data_dict)