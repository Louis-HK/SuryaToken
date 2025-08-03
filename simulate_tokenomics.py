import math

# Parameters (example)
base_reward_per_mwh = 100  # SYT
target_gap = 1.0  # normalized target (1 = on track)
current_gap = 0.5  # if below target, urgency increases

def compute_urgency_factor(target_gap, current_gap):
    # urgency increases when current_gap is smaller than target_gap
    if current_gap == 0:
        return 2.0
    factor = min(2.0, target_gap / current_gap)
    return factor

def adjusted_reward(mwh_generated, base_reward, urgency_factor):
    return mwh_generated * base_reward * urgency_factor

def main():
    mwh = 10  # example energy produced
    urgency = compute_urgency_factor(target_gap, current_gap)
    reward = adjusted_reward(mwh, base_reward_per_mwh, urgency)
    print(f"Energy: {mwh} MWh")
    print(f"Urgency Factor: {urgency:.2f}")
    print(f"Adjusted Reward: {reward:.2f} SYT")

if __name__ == "__main__":
    main()
