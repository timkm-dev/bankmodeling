//
// Created by tmuny on 28/06/2026.
//
#include <iostream>
#include <iomanip>
#include "Common.h"
#include "SimulationEngine.h"
#include "StatsAnalyzer.h"

void displayInputWindow(int& customerCount) {
    std::cout << "==================================================\n";
    std::cout << "                INPUT WINDOW                      \n";
    std::cout << "==================================================\n";
    std::cout << " Arrival Distribution: Uniform(0.5, 3.0) minutes\n";
    std::cout << " Service Distribution: Uniform(1.0, 4.0) minutes\n";
    std::cout << " Enter number of customers to simulate (e.g., 100): ";
    std::cin >> customerCount;
    std::cout << "\nSimulation running...\n\n";
}

void displayOutputWindow(const std::vector<Customer>& customers, const QueueStatistics& stats) {
    std::cout << "========================================================================================\n";
    std::cout << "                                     OUTPUT WINDOW                                      \n";
    std::cout << "========================================================================================\n";
    std::cout << std::left
              << std::setw(6)  << "ID"
              << std::setw(10) << "InterArr"
              << std::setw(10) << "ArrTime"
              << std::setw(12) << "ServTime"
              << std::setw(14) << "ServStart"
              << std::setw(10) << "WaitTime"
              << std::setw(12) << "ServEnd"
              << "TimeInSys\n";
    std::cout << "----------------------------------------------------------------------------------------\n";

    std::cout << std::fixed << std::setprecision(2);

    for (const auto& c : customers) {
        std::cout << std::left
                  << std::setw(6)  << c.id
                  << std::setw(10) << c.interarrivalTime
                  << std::setw(10) << c.arrivalTime
                  << std::setw(12) << c.serviceTime
                  << std::setw(14) << c.serviceStartTime
                  << std::setw(10) << c.waitTime
                  << std::setw(12) << c.serviceEndTime
                  << c.timeInSystem << "\n";
    }

    std::cout << "========================================================================================\n";
    std::cout << "                                  QUEUE STATISTICS                                      \n";
    std::cout << "========================================================================================\n";
    std::cout << " Total Customers Processed : " << stats.totalCustomers << "\n";
    std::cout << " Average Waiting Time      : " << stats.averageWaitTime << " minutes\n";
    std::cout << " Average Time in System    : " << stats.averageTimeInSystem << " minutes\n";
    std::cout << " Server Utilization Rate   : " << stats.serverUtilization << "%\n";
    std::cout << "========================================================================================\n";
}

int main() {
    int totalCustomers = 100;

    displayInputWindow(totalCustomers);

    SimulationEngine engine;
    std::vector<Customer> simulationData = engine.runSimulation(totalCustomers);

    QueueStatistics stats = StatsAnalyzer::calculateMetrics(simulationData);

    displayOutputWindow(simulationData, stats);

    return 0;
}
