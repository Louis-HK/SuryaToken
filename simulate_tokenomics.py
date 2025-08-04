import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()  # loads .env in current directory

# --- Parameter loading with defaults ---
BASE_REWARD_PER_MWH = float(os.getenv("BASE_REWARD_PER_MWH", 100.0))
TARGET_GAP = float(os.getenv("TARGET_GAP", 1.0))
TREASURY_BUFFER = float(os.getenv("TREASURY_BUFFER", 200_000_000))  # in SYT
CAP_PER_MWH = float(os.getenv("CAP_PER_MWH", 200.0))
URGENCY_MAX = float(os.getenv("URGENCY_MAX_MULTIPLIER", 2.0))
SIM_DAYS = int(os.getenv("SIM_DAYS", 30))
DAILY_ENERGY_MEAN = float(os.getenv("DAILY_ENERGY_MEAN", 100.0))
DAILY_ENERGY_STD = float(os.getenv("DAILY_ENERGY_STD", 20.0))

# --- Core logic ---

def compute_urgency_factor(target_gap: float, current_gap: float, max_multiplier: float) -> float:
    """
    If current_gap is below target, urgency increases. 
    urgency = min(max_multiplier, target_gap / current_gap)
    Avoid division by zero.
    """
    if current_gap <= 0:
        return max_multiplier
    factor = target_gap / current_gap
    return min(factor, max_multiplier)

def compute_reward(mwh: float, base_reward: float, urgency_factor: float, cap_per_mwh: float) -> float:
    """
    Reward = base_reward * mwh * urgency_factor, capped at cap_per_mwh * mwh.
    """
    raw = base_reward * mwh * urgency_factor
    cap = cap_per_mwh * mwh
    return min(raw, cap)

def simulate_scenario(name: str, energy_generator, initial_gap: float, days: int):
    """
    Simulates token issuance over a number of days.
    energy_generator: function(day) -> MWh produced that day
    initial_gap: starting current_gap (normalized)
    Returns a DataFrame with daily metrics.
    """
    current_gap = initial_gap
    treasury = TREASURY_BUFFER
    history = []

    for day in range(1, days + 1):
        mwh = energy_generator(day)
        urgency = compute_urgency_factor(TARGET_GAP, current_gap, URGENCY_MAX)
        reward = compute_reward(mwh, BASE_REWARD_PER_MWH, urgency, CAP_PER_MWH)

        # Simple model: gap improves proportionally to energy (this is placeholder logic)
        improvement = (mwh / (DAILY_ENERGY_MEAN * days))  # normalized small effect
        current_gap = max(0.1, current_gap - improvement)  # gap decreases, floor to avoid zero

        # Treasury stabilization: if reward is too high relative to expected base, draw from buffer
        expected_base = BASE_REWARD_PER_MWH * mwh
        stabilization_adjustment = 0
        if reward > expected_base * 1.2:  # if issuance overshoots by >20%
            draw = (reward - expected_base) * 0.5  # heuristic: treasury absorbs half the overshoot
            draw = min(draw, treasury)
            treasury -= draw
            stabilization_adjustment = -draw  # negative because buffer used

        history.append({
            "day": day,
            "mwh": mwh,
            "current_gap": current_gap,
            "urgency_factor": urgency,
            "reward_issued": reward,
            "expected_base": expected_base,
            "treasury": treasury,
            "stabilization_adjustment": stabilization_adjustment,
        })

    df = pd.DataFrame(history)
    df["cumulative_reward"] = df["reward_issued"].cumsum()
    return df

def random_energy(day):
    # simple stochastic daily production
    return max(0, np.random.normal(DAILY_ENERGY_MEAN, DAILY_ENERGY_STD))

def low_adoption_energy(day):
    # lower-than-expected production
    return max(0, np.random.normal(DAILY_ENERGY_MEAN * 0.5, DAILY_ENERGY_STD * 0.5))

def stress_energy(day):
    # bursty with high variance
    base = np.random.normal(DAILY_ENERGY_MEAN, DAILY_ENERGY_STD * 1.5)
    spike = 0
    if np.random.rand() < 0.1:  # occasional big spike
        spike = np.random.uniform(50, 150)
    return max(0, base + spike)

def run_all_scenarios():
    scenarios = {
        "baseline": (random_energy, 1.0),
        "low_adoption": (low_adoption_energy, 1.2),
        "stress": (stress_energy, 0.8),
    }
    results = {}
    for name, (generator, initial_gap) in scenarios.items():
        df = simulate_scenario(name, generator, initial_gap, SIM_DAYS)
        results[name] = df
        # Save CSV
        df.to_csv(f"simulations_{name}.csv", index=False)
        print(f"[{name}] Total issued: {df['cumulative_reward'].iloc[-1]:.2f} SYT")

        # Simple plot
        plt.figure(figsize=(10,4))
        plt.plot(df["day"], df["reward_issued"], label="Daily Issued SYT")
        plt.plot(df["day"], df["urgency_factor"] * BASE_REWARD_PER_MWH, label="Effective base*urgency", linestyle="--")
        plt.title(f"{name} scenario: daily rewards and urgency-adjusted baseline")
        plt.xlabel("Day")
        plt.ylabel("SYT")
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{name}_daily_reward.png")
        plt.close()

    # Combined comparison of cumulative issuance
    plt.figure(figsize=(10,5))
    for name, df in results.items():
        plt.plot(df["day"], df["cumulative_reward"], label=f"{name} cumulative")
    plt.title("Cumulative SYT Issued Across Scenarios")
    plt.xlabel("Day")
    plt.ylabel("SYT")
    plt.legend()
    plt.tight_layout()
    plt.savefig("comparison_cumulative.png")

    return results

if __name__ == "__main__":
    # Ensure output directory exists
    run_all_scenarios()
