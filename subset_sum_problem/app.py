from flask import Flask, render_template, request
from concurrent.futures import ThreadPoolExecutor
import itertools
import time

app = Flask(__name__, template_folder='templates')


def findSubsetsWithSum(nums, target):
    subsets = []
    for L in range(0, len(nums)+1):
        for subset in itertools.combinations(nums, L):
            if sum(subset) == target:
                subsets.append(subset)
    return subsets

def findSubsetsWithSumParallel(nums, target):
    if len(nums) < 20:  # Threshold for parallel execution
        return findSubsetsWithSum(nums, target)

    mid = len(nums) // 2
    left_nums = nums[:mid]
    right_nums = nums[mid:]

    with ThreadPoolExecutor() as executor:
        future_left = executor.submit(findSubsetsWithSumParallel, left_nums, target)
        future_right = executor.submit(findSubsetsWithSumParallel, right_nums, target)

        subsets_left = future_left.result()
        subsets_right = future_right.result()

    # Combine subsets found in left and right parts
    subsets = subsets_left + subsets_right
    return subsets

@app.route('/')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_subsets', methods=['POST'])
def find_subsets():
    try:
        nums = list(map(int, request.form.get('elements').split()))
        target = int(request.form.get('target'))
    except ValueError:
        return "Invalid input. Please enter valid numbers."
    start_time = time.time()  # Start time measurement
    subsets = findSubsetsWithSumParallel(nums, target)
    end_time = time.time()  # End time measurement
    execution_time = end_time - start_time 
    return render_template('result.html', subsets=subsets, execution_time=execution_time)

if __name__ == "__main__":
    app.run(debug=True)
