#ifndef STATS_ANALYZER_H
#define STATS_ANALYZER_H

#include "Common.h"
#include <numeric>

class StatsAnalyzer {
public:
  static QueueStatistics
  calculateMetrics(const std::vector<Customer> &customers) {
    if (customers.empty())
      return {0.0, 0.0, 0.0, 0};

    double totalWaitTime = 0.0;
    double totalTimeInSystem = 0.0;
    double totalServiceTime = 0.0;

    for (const auto &c : customers) {
      totalWaitTime += c.waitTime;
      totalTimeInSystem += c.timeInSystem;
      totalServiceTime += c.serviceTime;
    }

    double totalSimulationTime = customers.back().serviceEndTime;

    QueueStatistics stats;
    stats.totalCustomers = static_cast<int>(customers.size());
    stats.averageWaitTime = totalWaitTime / stats.totalCustomers;
    stats.averageTimeInSystem = totalTimeInSystem / stats.totalCustomers;

    // Server busy time over total runtime window
    stats.serverUtilization = (totalServiceTime / totalSimulationTime) * 100.0;

    return stats;
  }
};

#endif
