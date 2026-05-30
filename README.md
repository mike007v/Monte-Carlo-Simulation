# Monte Carlo Simulation

This project uses Monte Carlo simulation to show how one set of trading strategy assumptions can lead to many different equity curve outcomes.

A single backtest only shows one possible path. Monte Carlo simulation helps visualize the range of outcomes that could have happened if the same strategy assumptions played out in a different sequence.

The goal of this project is not to prove that a trading strategy works. The goal is to better understand path dependency, drawdowns, variance, and the risk of relying on one clean equity curve.

## Important Note

All data used in this project is fully simulated.

The trade results are not real market data and should not be presented as real trading performance. The purpose of this project is educational: to demonstrate how Monte Carlo simulation can be used to study risk and outcome uncertainty.

## Project Overview

The simulation takes a set of simulated backtest results and generates 1,000 randomized equity paths.

Each path represents a possible sequence of trades using the same underlying assumptions. Even when the expected return profile stays the same, the final outcome can change significantly depending on the order of wins, losses, and drawdowns.

This helps answer questions such as:

- How much can the final equity vary?
- What does a bad sequence of trades look like?
- How large can drawdowns become?
- How stable is the strategy under different possible paths?
- Is one backtest result enough to understand the risk?

## Tech Stack

- Python
- NumPy
- pandas
- Plotly
- Kaleido

## Setup

**1. Clone the repository**

```bash
git clone <repo-url>
cd <repo-folder>
```

**2. Create a virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**
```bash
cp .env.example .env
# Open .env and fill in any real credentials if you extend this project
```

## Run

```bash
python3 monte_carlo_simulation.py
```

The script prints a summary table and writes charts to the `outputs/` folder.

## Outputs

| File | Description |
|---|---|
| `outputs/monte_carlo_one_page.png` | Static export (requires Kaleido) |
