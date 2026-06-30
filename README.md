# 🏦 Bank Queue Simulator

A single-server **FIFO queue simulation** for modelling customer wait times, service times, and server utilization at a bank. Built with **C++** (console) and **Python/tkinter** (GUI).

---

## Features

- **Configurable Parameters** — set number of customers, arrival time range, and service time range
- **Uniform Random Distributions** — inter-arrival and service times drawn from user-defined uniform distributions
- **Queue Statistics** — average wait time, average time in system, and server utilization (%)
- **Visual GUI** — dark-themed Python interface with:
  - Input controls panel
  - Live statistics cards
  - Scrollable customer data table
  - Wait time bar chart
  - Server timeline visualization
- **Console Mode** — lightweight C++ terminal version with interactive prompts

---

## 📁 Project Structure

```
bankmodeling/
├── gui.py               # Python tkinter GUI (recommended)
├── main.cpp             # C++ console version
├── Common.h             # Shared data structures (Customer, QueueStatistics)
├── SimulationEngine.h   # Simulation logic (uniform distributions, FIFO queue)
├── StatsAnalyzer.h      # Metrics computation (averages, utilization)
└── README.md
```

---

## 🚀 How to Run

### GUI Version (Recommended)

> Requires **Python 3.x** (tkinter is included with standard Python installations).

```bash
python gui.py
```

1. Set the simulation parameters in the left panel
2. Click **▶ Run Simulation** (or press **Enter**)
3. View results across three tabs:
   - **📋 Customer Data** — full data table for every customer
   - **📊 Wait Time Chart** — bar chart comparing wait time vs time-in-system
   - **🕐 Server Timeline** — visual timeline of server busy/idle periods

### Console Version

> Requires a **C++17** compiler (g++, MSVC, or clang).

```bash
g++ -std=c++17 -o BankQueueSim main.cpp
./BankQueueSim
```

Follow the interactive prompts to enter parameters and view results in the terminal.

---

## 📐 Simulation Model

| Property           | Detail                              |
|--------------------|-------------------------------------|
| Queue Discipline   | FIFO (First In, First Out)          |
| Number of Servers  | 1                                   |
| Arrival Times      | Uniform distribution (configurable) |
| Service Times      | Uniform distribution (configurable) |
| Output Metrics     | Wait time, time in system, utilization |