from os import scandir, path, walk
import random
import json

n = 1
mypath = './Code_optimize/unzip_data/GEC/test/'

# Read file
def read_file(key, target, is_json=False):

    file_path = path.join(mypath, str(key), target)
    #print(file_path)
    if is_json:
        with open(file_path) as json_file:
            return json.load(json_file)
    try:
        with open(file_path, 'r') as file:
            return file.read() # Assign the content to the corresponding key in the dictionary
    except Exception as e:
        raise e

def get_best_solution(target_dict, key):
    _file_path = path.join(mypath, str(key), 'Acc_solutions')
    try:
        _file = sorted([files for root, dirs, files in walk(_file_path)])[0][0]
        return _file, float(_file.split(' ms')[0].replace(',','.'))
    except Exception as e:
        raise e

# pick sample
testcase = [ f.path for f in scandir(mypath) if f.is_dir()]
num_of_testcase = len(testcase)
samples = sorted(random.sample(range(0,num_of_testcase), n))
formatted_samples = [f"{num:04d}" for num in samples]

# Generate dict for evaluation
data_dict = {str(num): {} for num in formatted_samples}

# Update data_dict
for key in data_dict:
    best_sol_file, best_time = get_best_solution(data_dict, key)
    data_dict[key] = {
        'Question': read_file(key, 'Question.txt'),
        'IO': read_file(key, 'input_output.json', True),
        'Best_sol': read_file(key, path.join(
            'Acc_solutions',best_sol_file)).replace("\\n","\n").replace("\\t","\t"), # To be Fixed! 
        'Best_time' : best_time
    }

print(data_dict)