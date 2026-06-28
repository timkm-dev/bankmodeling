#ifndef COMMON_H
#define COMMON_H

#include <vector>

// Represents a single customer's timeline
struct Customer {
    int id;
    double interarrivalTime;
    double arrivalTime;
    double serviceTime;
    double serviceStartTime;
    double waitTime;
    double serviceEndTime;
    double timeInSystem;
};

// Summary metrics computed at the end
struct QueueStatistics {
    double averageWaitTime;
    double averageTimeInSystem;
    double serverUtilization;
    int totalCustomers;
};

#endif
