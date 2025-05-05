
# Dosage Optimization via Monte Carlo Ternary Search 💊

This project implements a Python based optimization algorithm for finding the optimal dosage in scenarios where feedback is noisy and evaluation opportunities are limited. It combines Monte Carlo style averaging with a ternary search inspired interval reduction strategy.

---

## 📈 Problem Overview

The objective is to find a value \( x \in [0, 1] \) that maximizes an unknown unimodal function \( f(x) \), where:

- Function outputs include **random noise**, simulating real world uncertainty.
- Only **K** evaluations are allowed per round.
- You may repeat the process for **R** rounds.
- The algorithm must adapt, filter noise, and converge efficiently.

### Algorithm Visualization:
![Dosage Optimization](assets/optimaldosage.png)

---

## 🧠 Key Techniques

- **Monte Carlo Averaging** – Smooths noisy outputs by averaging multiple evaluations per point.
- **Ternary Search (Adapted)** – Narrows the search range around the best performing values.
- **Dynamic Sampling** – Adjusts segment spacing to increase precision over time.

---

## 🛠️ How It Works

1. Divide the interval [0, 1] into `K` points.
2. Evaluate each point and log results.
3. Average results at each point across rounds to filter out noise.
4. Focus the next search window around the point with the highest average.
5. Repeat this process for `R` rounds.
6. Output the point with the best overall performance.

---

## 💻 Example Output

```
Iteration 1: Sampled [0.0, 0.25, 0.5, 0.75]
Values: [0.16, 0.41, 0.66, 0.91]
...
Final estimated max dosage: 0.84
```

---

## 📦 File Overview

| File         | Purpose                                     |
|--------------|---------------------------------------------|
| `main.py`    | Complete implementation of the optimization |

---

## 🩺 Real World Applications

- **Medical dosage optimization**
- **Hyperparameter tuning for ML models**
- **Sensor calibration under uncertainty**
- **Decision making with noisy signals**

---

## 🔧 Future Improvements

- **Adaptive Averaging**: Use weighted averaging to prioritize recent results or higher confidence evaluations.
- **Sampling Density Control**: Increase sample density near high gradient regions dynamically.
- **Alternative Strategies**: Compare performance with other search methods like golden-section search or Bayesian optimization.

---

## 🧬 Author

Built by Vince Allen to demonstrate applied search techniques under real world constraints, such as noise, limited evaluations, and adaptive refinement.
