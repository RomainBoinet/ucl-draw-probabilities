# ⚽ Champions League Round of 16 Probability Simulator

Welcome to our **UEFA Champions League Round of 16 Probability Simulator** — a Python tool that calculates the probability of every possible matchup while respecting official UEFA draw rules. The simulator includes both a backend algorithm and a graphical user interface (GUI) built with Tkinter.

> 🏆 **Note:** This project was designed for the *former* Champions League format (valid until the **2023-2024** edition)  
> Starting from **2024-2025**, the competition follows a new league-phase system — meaning the traditional Round of 16 draw and its probabilistic constraints no longer exist  
> Nonetheless, this simulator remains an excellent case study in combinatorial probability, algorithm design, and sports data modeling
---

## 🎯 Project Overview

Every year, the Champions League Round of 16 draw follows strict rules:

- A group winner faces a group runner-up  
- Teams from the **same country** cannot face each other  
- Teams from the **same group** cannot meet again  

Because of these constraints, not all draws are equally likely — some matchups are statistically more probable than others.  
This simulator calculates these probabilities, for any set of teams and countries you choose.

---

## 🧮 How It Works

### Exact Probability Computation
The simulator generates **all valid draw configurations** between 8 group winners and 8 runners-up.  
Each configuration follows the UEFA rules. The probability of a matchup (e.g., *PSG vs Liverpool*) is then:

\[
P(\text{PSG-Liverpool}) = \frac{\text{Number of valid draws with this match}}{\text{Total number of valid draws}}
\]

Because 8! = 40,320 possible draws exist in the unrestricted case, computation can take a few minutes — but it’s fully exhaustive and accurate.

### Data Model
- **Team**: defined by name, country, group, and ranking (1st or 2nd)  
- **Match**: tuple of two teams  
- **Configuration**: list of 8 valid matches forming one possible draw

### Functions (in `logic.py`)
- `generate_configurations()`: builds all valid matchups using `itertools.permutations`  
- `match_possible()`: checks if a match follows UEFA rules  
- `calculate_probabilities()`: computes the final 8×8 probability matrix  
- `detect_errors()`: verifies user inputs for duplicates or inconsistencies

---

## 💻 Interface (in `app.py`)

The GUI lets you easily input teams, countries, and display results:

- **Team Table (left)** – Enter or edit team names (double-click a cell).  
- **Country Table (right)** – Enter or edit the corresponding countries.  
- **Probability Table (bottom)** – Displays matchup probabilities in %.  
- **Buttons**:
  - 🧮 *Calculate probabilities*: runs the full computation
  - 📄 *Export*: saves results as a `.csv` file
  - ℹ️ *Notice*: opens the user guide window

---

## 🧭 User Guide

1. Enter your **teams** (e.g., “Bayern”) and their **countries** (“Germany”)  
2. Click **Calculate probabilities** to launch the simulation  
   ⏱️ The computation may take 1–2 minutes depending on your machine  
3. Once done, the **bottom 8×8 table** displays matchup probabilities  
4. Click **Export** to save the data in CSV format  

---

## 🧩 Technical Overview

- **Language**: Python 3  
- **Libraries**: `itertools`, `tkinter`, `csv`  
- **Files**:
  - `logic.py` – backend probability calculations  
  - `app.py` – user interface  
  - `main.py` – application entry point  

---

## 🚀 Future Improvements

- Implement a faster approximate (Monte Carlo) method  
- Add team auto-fill using a football API  
- Visualize results dynamically with charts  

---

## 👥 Authors

- **Romain Boinet**

---

### ⚠️ Notes
The simulator is a **pedagogical and experimental tool**, not an official UEFA predictor.  
It’s meant to illustrate probability modeling and combinatorial computation in Python.

---