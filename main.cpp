#include <iostream>
#include <iomanip>
#include <string>
#include <limits> // Required for input buffer clearing
#include "Common.h"
#include "SimulationEngine.h"
#include "StatsAnalyzer.h"

// Helper function to keep the console clean
void clearScreen() {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

// NEW: Robust input handler to prevent comma/letter crashing
template <typename T>
T getValidInput(const std::string& prompt) {
    T value;
    while (true) {
        std::cout << prompt;
        if (std::cin >> value) {
            // Success! Clear any trailing garbage (like the ',3' in '0.5,3') from the buffer
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            return value;
        } else {
            // Fail state triggered (e.g., user typed a letter instead of a number)
            std::cin.clear(); // Reset the error flags
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // Dump the bad input
            std::cout << "   [!] Invalid input. Please enter a valid number.\n";
        }
    }
}

void displayOutputWindow(const std::vector<Customer>& customers, const QueueStatistics& stats) {
    std::cout << "\n========================================================================================\n";
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
    SimulationEngine engine;
    bool running = true;

    while (running) {
        clearScreen();
        std::cout << "==================================================\n";
        std::cout << "          INTERACTIVE BANK QUEUE SIMULATOR        \n";
        std::cout << "==================================================\n";

        // 1. Gather Interactive Input securely
        int totalCustomers = getValidInput<int>(" [1] Enter number of customers to simulate: ");
        double arrMin      = getValidInput<double>(" [2] Enter Arrival Time MIN (e.g., 0.5): ");
        double arrMax      = getValidInput<double>(" [3] Enter Arrival Time MAX (e.g., 3.0): ");
        double srvMin      = getValidInput<double>(" [4] Enter Service Time MIN (e.g., 1.0): ");
        double srvMax      = getValidInput<double>(" [5] Enter Service Time MAX (e.g., 4.0): ");

        std::cout << "\n>>> Running Simulation...\n";

        // 2. Update Engine and Run
        engine.updateParameters(arrMin, arrMax, srvMin, srvMax);
        std::vector<Customer> simulationData = engine.runSimulation(totalCustomers);

        // 3. Process Stats
        QueueStatistics stats = StatsAnalyzer::calculateMetrics(simulationData);

        // 4. Render Output
        displayOutputWindow(simulationData, stats);

        // 5. Prompt to continue or exit securely
        char choice;
        std::cout << "\nWould you like to run another simulation? (y/n): ";
        std::cin >> choice;

        // Clear the buffer again just in case they typed "yes" instead of "y"
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

        if (choice == 'n' || choice == 'N') {
            running = false;
            std::cout << "Exiting simulator. Goodbye!\n";
        }
    }

    return 0;
}