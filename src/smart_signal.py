import random

class IntersectionSimulator:
    def __init__(self):
        # 4 directions for our standard intersection
        self.directions = ['North', 'South', 'East', 'West']
        
    def generate_density(self):
        """Simulated vehicle density (YOLOv8 integration in progress)."""
        return {
            'North': random.randint(5, 85),
            'South': random.randint(5, 85),
            'East': random.randint(5, 85),
            'West': random.randint(5, 85)
        }
        
    def run_fixed_time(self, densities, fixed_time=30):
        """Simulate legacy fixed-time signal logic. Each lane gets exactly 30 seconds."""
        total_delay = 0
        for direction, count in densities.items():
            # A simple rule: each vehicle takes ~2 seconds to clear the intersection.
            clearance_capacity = fixed_time / 2 
            vehicles_left_waiting = max(0, count - clearance_capacity)
            # Delay is proportional to vehicles that didn't make the green light
            total_delay += vehicles_left_waiting * 12 # 12s avg delay penalty per waiting car
        return total_delay
        
    def run_density_based(self, densities, cycle_length=120):
        """Simulate AI density-based signal logic (allocating time proportionally)."""
        total_cars = sum(densities.values())
        if total_cars == 0:
            return 0, {dir: 30 for dir in self.directions}
            
        allocations = {}
        total_delay = 0
        
        for direction, count in densities.items():
            # Allocate cycle time proportionally, bounded by safe min/max (10s to 60s)
            raw_alloc = (count / total_cars) * cycle_length
            alloc_time = max(10, min(60, raw_alloc))
            allocations[direction] = round(alloc_time)
            
            # Re-calculate delay based on actual intelligent allocated time
            clearance_capacity = alloc_time / 2
            vehicles_left_waiting = max(0, count - clearance_capacity)
            total_delay += vehicles_left_waiting * 12 # 12s avg delay penalty
            
        return total_delay, allocations

def demo_simulation(num_cycles=5):
    sim = IntersectionSimulator()
    total_fixed_delay = 0
    total_ai_delay = 0
    
    print("🚦 INITIATING SMART SIGNAL SIMULATION (Legacy vs AI Mode)")
    print("-" * 65)
    
    for i in range(1, num_cycles + 1):
        densities = sim.generate_density()
        
        fixed_delay = sim.run_fixed_time(densities)
        ai_delay, allocations = sim.run_density_based(densities)
        
        total_fixed_delay += fixed_delay
        total_ai_delay += ai_delay
        
        print(f"\n[🔄 CYCLE {i}] - Detected Vehicles: {densities}")
        print(f"   🔴 Legacy Fixed-Time | Green: 30s all | Delay Penalty: {fixed_delay}")
        print(f"   🟢 AI Smart-Signal   | Green: {allocations} | Delay Penalty: {ai_delay}")

    print("\n" + "="*65)
    print("📈 AGGREGATE METRICS OVER 5 CYCLES (Save for Project Report)")
    print("="*65)
    print(f"Total Wait Time (Legacy System) : {total_fixed_delay} penalty units")
    print(f"Total Wait Time (AI System)     : {total_ai_delay} penalty units")
    
    if total_fixed_delay > 0:
        improvement = ((total_fixed_delay - total_ai_delay) / total_fixed_delay) * 100
        print(f"\n🚀 Efficiency Improvement: {improvement:.2f}% reduced delay!")
        
    print("="*65)

if __name__ == "__main__":
    import time
    random.seed(time.time())  
    demo_simulation(5)
