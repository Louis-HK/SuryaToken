# SuryaToken  
**Tokenized incentives for Indonesia’s energy transition.**  
> Aligning capital flows with decarbonization through blockchain-native mechanisms.

## 🚀 Overview  
SuryaToken is a blockchain-powered strategic initiative to accelerate Indonesia's shift away from coal by creating financial incentives for renewable energy adoption. Built at the intersection of sustainable infrastructure, token economics, and decentralized finance, SuryaToken aims to reduce CO₂ emissions while unlocking new liquidity channels via asset-backed, tokenized green credits.

## 🎯 Objectives
- Tokenize renewable energy adoption incentives to create measurable impact.  
- Support Indonesia’s 2030 CO₂ reduction target (29%) through transparent tracking and reward mechanisms.  
- Enable new capital flows (impact capital, carbon credit markets) via programmable, blockchain-native instruments.  
- Build a governance-ready ecosystem for future scaling (validators, stakeholders, partners).

## 🧩 Core Components
- **Incentive Layer (Smart Contracts)** – ERC-based token(s) representing green credits and reward flows.  
- **Oracle & Data Mesh** – Reliable measurement of energy generation and carbon displacement (Chainlink / custom oracles).  
- **Token Economics Simulator** – Python/On-chain models to simulate issuance, vesting, and revenue alignment.  
- **Funding & Treasury** – Structured funds (SPV, SBLC overlays) to back token value and guarantee liquidity.  
- **Dashboard & Reporting** – Transparent metrics: emissions reduced, tokens minted/redeemed, participant performance.

## 🛠️ Tech Stack
- Solidity (smart contracts for SuryaToken issuance & staking)  
- Python (tokenomics simulation, data ingestion, reconciliation)  
- Chainlink oracles (or custom data pipelines)  
- Docker / Hetzner (deployment of backend services and validator infra)  
- GitHub Actions (CI for contract tests / simulation validation)  

## 📦 Getting Started

### Prerequisites
- Node.js >= 18 (if front-end / scripts)  
- Python >= 3.11  
- Docker  
- Wallet with permissions (for testnet / governance)  
- Environment config (.env)

### Installation 
```bash
git clone https://github.com/Louis-HK/surya-token.git
cd surya-token
# install Python dependencies
pip install -r requirements.txt
# run tokenomics simulation
python simulate_tokenomics.py

## Simulation snapshot

Baseline and stress scenarios were run to validate token issuance dynamics and treasury stabilisation.

**Key results (example):**
- Total SYT issued over 30 days (baseline): _<insert value from output>_  
- Total SYT issued (stress): _<insert>_  
- Treasury buffer remaining (baseline): see CSV  
- Urgency factor behavior: dynamic increase when gap is large.

### Visual sample
<img src="./simulations/baseline_daily_reward.png" alt="Baseline daily reward" width="600"/>

### Next steps from simulation
- Feed urgency-adjusted issuance into on-chain oracle contract.  
- Sweep parameters (`BASE_REWARD_PER_MWH`, `TARGET_GAP`) to produce sensitivity report.  
- Export the best/worst-case summaries into release notes.

