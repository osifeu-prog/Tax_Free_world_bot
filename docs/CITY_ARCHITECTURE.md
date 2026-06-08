# TON City Architecture

## Overview
TON City transforms the bot into a living economic metropolis.

### Districts
- **Central Bank**  Pension calculator
- **Family Municipality**  Household budgeting
- **University**  Academy courses
- **Community Center**  Donations & referrals
- **Statistics Bureau**  Analytics & reports
- **Stock Exchange**  TON City Index (market sentiment)

### Data Flow
User -> Telegram -> Aiogram Router -> Handlers -> Database -> /city Aggregator

### Anti-Regression Measures
- Smoke test: `/city`, `/market`
- DB integrity: `events_log` for all state changes
- Backup: daily JSON export via `/admin export`
- Monitoring: Railway logs + Log Drain to Discord

## Commands
- `/city`  City dashboard
- `/market`  Stock exchange & clock
- `/report`  Statistics bureau
