from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


STARTING_CAPITAL = 10_000
NUMBER_OF_SIMULATIONS = 1_000
TRADES_PER_SIMULATION = 250
WIN_RATE = 0.52
AVERAGE_WIN = 0.012
AVERAGE_LOSS = -0.010
WIN_STANDARD_DEVIATION = 0.006
LOSS_STANDARD_DEVIATION = 0.005
RANDOM_SEED = 42

OUTPUT_DIR = Path("outputs")
OUTPUT_FILE = OUTPUT_DIR / "monte_carlo_one_page.png"


def summary_table(ending_equity, max_drawdowns, starting_capital):
    return pd.DataFrame(
        [
            ("Median ending equity", f"${np.median(ending_equity):,.2f}"),
            ("Mean ending equity", f"${ending_equity.mean():,.2f}"),
            ("5th percentile ending equity", f"${np.percentile(ending_equity, 5):,.2f}"),
            ("95th percentile ending equity", f"${np.percentile(ending_equity, 95):,.2f}"),
            ("Best ending equity", f"${ending_equity.max():,.2f}"),
            ("Worst ending equity", f"${ending_equity.min():,.2f}"),
            ("Median max drawdown", f"{np.median(max_drawdowns):.2%}"),
            ("Worst max drawdown", f"{max_drawdowns.min():.2%}"),
            ("Probability ending below starting capital", f"{(ending_equity < starting_capital).mean():.2%}"),
        ],
        columns=["Statistic", "Value"],
    )


rng = np.random.default_rng(RANDOM_SEED)
shape = (TRADES_PER_SIMULATION, NUMBER_OF_SIMULATIONS)

is_win = rng.random(shape) < WIN_RATE
wins = np.clip(rng.normal(AVERAGE_WIN, WIN_STANDARD_DEVIATION, shape), 0.0001, None)
losses = np.clip(rng.normal(AVERAGE_LOSS, LOSS_STANDARD_DEVIATION, shape), None, -0.0001)
returns = np.where(is_win, wins, losses)

equity = STARTING_CAPITAL * np.vstack(
    [np.ones(NUMBER_OF_SIMULATIONS), np.cumprod(1 + returns, axis=0)]
)
ending_equity = equity[-1]
max_drawdowns = (equity / np.maximum.accumulate(equity, axis=0) - 1).min(axis=0)
summary = summary_table(ending_equity, max_drawdowns, STARTING_CAPITAL)

fig = make_subplots(
    rows=3,
    cols=1,
    subplot_titles=(
        "Simulated Monte Carlo Equity Paths",
        "Ending Equity Distribution",
        "Maximum Drawdown Distribution",
    ),
    row_heights=[0.52, 0.24, 0.24],
    vertical_spacing=0.08,
)

xs, ys = [], []
trade_axis = np.arange(TRADES_PER_SIMULATION + 1).tolist()
for i in range(NUMBER_OF_SIMULATIONS):
    xs.extend(trade_axis)
    xs.append(None)
    ys.extend(equity[:, i].tolist())
    ys.append(None)

fig.add_trace(
    go.Scattergl(x=xs, y=ys, mode="lines", line=dict(color="rgba(37, 99, 135, 0.08)", width=1), hoverinfo="skip", showlegend=False),
    row=1, col=1,
)
fig.add_trace(go.Histogram(x=ending_equity, nbinsx=45, marker_color="#256387"), row=2, col=1)
fig.add_trace(go.Histogram(x=max_drawdowns * 100, nbinsx=45, marker_color="#8A4F39"), row=3, col=1)

fig.update_layout(
    title="Simulated Monte Carlo Strategy Outcomes",
    template="plotly_white",
    height=1500,
    width=1400,
    margin=dict(l=80, r=40, t=100, b=70),
    showlegend=False,
)
fig.update_xaxes(title_text="Trade number", row=1, col=1)
fig.update_yaxes(title_text="Simulated equity ($)", row=1, col=1)
fig.update_xaxes(title_text="Ending equity ($)", row=2, col=1)
fig.update_yaxes(title_text="Number of simulations", row=2, col=1)
fig.update_xaxes(title_text="Maximum drawdown (%)", row=3, col=1)
fig.update_yaxes(title_text="Number of simulations", row=3, col=1)

OUTPUT_DIR.mkdir(exist_ok=True)
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    fig.write_image(OUTPUT_FILE, scale=2)

print("\nSIMULATED MONTE CARLO SUMMARY")
print("These results are simulated, not real trading performance.\n")
print(summary.to_string(index=False))
print(f"\nChart saved to {OUTPUT_FILE}")
