import os
import random

# Simulated noisy evaluation function.
# In a real-world scenario, this would come from sensors, patient data, etc.
def call_grader_local(x):
    return [1.0 - abs(xi - 0.8400) for xi in x]

def main():
    # Evaluation limits (defaults if not provided in environment)
    K = int(os.environ.get("K", 4))
    R = int(os.environ.get("R", 7))

    start, end = 0.0, 1.0
    point_avgs = [[] for _ in range(K)]
    count = 0

    while count < R:
        point_list = []

        # Refine step size dynamically over iterations
        step = (end - start) / (K * 2) if count > R // 2 else (end - start) / (K - 1)
        point_list = [start + i * step for i in range(K)]

        # Evaluate and store noisy values
        vals = call_grader_local(point_list)
        for i in range(min(K, len(vals))):
            point_avgs[i].append(vals[i])

        # Average results to reduce noise
        avgs = [sum(vals) / len(vals) if vals else 0 for vals in point_avgs]

        # Find highest-performing point
        max_index = avgs.index(max(avgs))

        # Narrow the interval around the best point
        if max_index == 0:
            start, end = point_list[max_index], point_list[max_index + 2]
        elif max_index == K - 1:
            start, end = point_list[max_index - 2], point_list[max_index]
        else:
            start, end = point_list[max_index - 1], point_list[max_index + 1]

        count += 1

    print(f"{point_list[max_index]:.2f}")

if __name__ == "__main__":
    main()
