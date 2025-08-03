# SuryaToken Operational Playbook

## Deployment Checklist
- [ ] .env configured with dev/test credentials  
- [ ] Smart contract tests pass  
- [ ] Tokenomics simulation results validated  
- [ ] Oracle feed verified  

## Failure Recovery
- Oracle failure: switch to backup feed  
- Token inflation: trigger treasury buyback or throttle rewards  
- Governance intervention if deviation > 15%

## Governance Triggers
- Increase rewards if adoption rate < target for 3 weeks  
- Activate reserve support if velocity > safe limit
