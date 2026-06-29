#ifndef SIMULATION_ENGINE_H
#define SIMULATION_ENGINE_H

#include "Common.h"
#include <random>

class SimulationEngine {
private:
    std::mt19937 rng;
    std::uniform_real_distribution<double> arrivalDist;
    std::uniform_real_distribution<double> serviceDist;

public:
    SimulationEngine() 
        : rng(std::random_device{}()), 
          arrivalDist(0.5, 3.0), 
          serviceDist(1.0, 4.0) {}

    std::vector<Customer> runSimulation(int totalCustomers) {
        std::vector<Customer> customers(totalCustomers);
        double currentClock = 0.0;
        double nextAvailableServerTime = 0.0;

        for (int i = 0; i < totalCustomers; ++i) {
            customers[i].id = i + 1;
            
            // First customer arrives at their interarrival time
            customers[i].interarrivalTime = arrivalDist(rng);
            currentClock += customers[i].interarrivalTime;
            customers[i].arrivalTime = currentClock;
            
            customers[i].serviceTime = serviceDist(rng);

            // Determine when service starts
            if (customers[i].arrivalTime < nextAvailableServerTime) {
                customers[i].serviceStartTime = nextAvailableServerTime;
            } else {
                customers[i].serviceStartTime = customers[i].arrivalTime;
            }

            // Calculations
            customers[i].waitTime = customers[i].serviceStartTime - customers[i].arrivalTime;
            customers[i].serviceEndTime = customers[i].serviceStartTime + customers[i].serviceTime;
            customers[i].timeInSystem = customers[i].serviceEndTime - customers[i].arrivalTime;

            // Move server clock forward
            nextAvailableServerTime = customers[i].serviceEndTime;
        }
        return customers;
    }
};

#endif
