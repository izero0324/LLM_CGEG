import sys
import time
import signal
from io import StringIO

# Define a timeout handler
def timeout_handler(signum, frame):
    raise TimeoutError("Execution time exceeded 2 seconds")

# Set the signal alarm
signal.signal(signal.SIGALRM, timeout_handler)

def test_code(txt_code, input_json, debug=False):
    # Use exec to run the code with input mocking
    original_stdout = sys.stdout
    
    timeout = 2
    results = []
    time_used = []
    expected = input_json["outputs"]

    # Redirect output to capture prints
    for inp in input_json["inputs"]:
        #print(inp)
        # Override the input function and sys.stdout
        def mock_input():
            return inp
        input = mock_input
        
        buffer = StringIO()  # Use a buffer to capture print statements
        sys.stdout = buffer  # Redirect stdout to capture print

        start_time = time.time()
        # Execute the code
        try:
            # Execute the code
            signal.alarm(timeout)
            exec(txt_code)
            signal.alarm(0)

        except TimeoutError as e:
            return -1, float('inf'), f"Error: {e}"
        except Exception as e:
            # If there is an error, record it as the result
            sys.stdout = original_stdout  # Restore stdout before writing to results
            results.append(f"Error: {e}")
            return -1, float('inf'), f"Error: {e}"
        else:
            buffer.seek(0)  # Go to the start of StringIO buffer
            output = buffer.read().strip()  # Read the output
            results.append(output)
        finally:
            time_used.append(time.time() - start_time)
            sys.stdout = original_stdout  # Always restore stdout
            signal.alarm(0) 
    
    total_ans = len(expected)
    score = 0
    for i in range(total_ans):
        score += (results[i] == expected[i])
    #print(score/total_ans, sum(time_used)/total_ans)
        
    if debug:
        # Print the results and check if they match the expected outputs
        print("Results:", results)
        print("Expected:", expected)
        print("Test Success:", results == expected)
    
    return score/total_ans, sum(time_used)/total_ans, False


# if __name__ == "__main__":
#     #txt_code = "var1 = var2 = 0\ninput()\nfor var3 in input():\n    var1 += (var2 == var3)\n    var2 = var3\nprint(var1)"
#     #input_json = {"inputs": ["3\nRRG", "5\nRRRRR", "4\nBRBG"], "outputs": ["1", "4", "0"]}
#     input_json =  {'inputs': ["3", "5", "6"], 'outputs': ["0", "1", "1"]}
#     txt_code = "var1 = int(input())\\nvar1 = (var1 % 4)\\nif ((var1 == 3) or (var1 == 0)):\\n    print(0)\\nelse:\\n    print(1)"
#     score, avg_time, error = test_code(txt_code, input_json)
#     if error: print(error)
#     print(score, avg_time)
