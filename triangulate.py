#!/usr/bin/env python3
"""
Legacy triangulation module - now integrated with Scanner Bot
This module provides triangulation capabilities for MAC address tracking
in the Police Scanner Accountability System.
"""

import json
import time
import math
from datetime import datetime, timezone
from typing import List, Dict, Tuple, Optional

class TriangulationEngine:
    """Advanced triangulation engine for tracking officer locations"""
    
    def __init__(self):
        self.known_positions = []
        self.signal_readings = []
    
    def add_signal_reading(self, mac: str, signal_strength: int, 
                          position: Tuple[float, float], timestamp: Optional[str] = None):
        """Add a signal strength reading for triangulation"""
        if timestamp is None:
            timestamp = datetime.now(timezone.utc).isoformat()
        
        reading = {
            "mac": mac,
            "signal_strength": signal_strength,
            "position": position,
            "timestamp": timestamp,
            "estimated_distance": self.estimate_distance(signal_strength)
        }
        
        self.signal_readings.append(reading)
        return reading
    
    def estimate_distance(self, signal_strength: int) -> float:
        """Estimate distance based on signal strength (in meters)"""
        # Simple RSSI to distance conversion (this can be improved with calibration)
        # Formula: Distance = 10^((Tx Power - RSSI) / (10 * n))
        # Assuming Tx Power = 0 dBm, n = 2 (free space)
        if signal_strength >= 0:
            return 1.0
        
        distance = 10 ** ((-signal_strength) / 20.0)
        return min(distance, 1000.0)  # Cap at 1km
    
    def triangulate_position(self, mac: str) -> Optional[Dict]:
        """Triangulate position based on multiple signal readings"""
        # Get recent readings for this MAC address
        mac_readings = [r for r in self.signal_readings 
                       if r["mac"] == mac]
        
        if len(mac_readings) < 3:
            return None  # Need at least 3 points for triangulation
        
        # Use the 3 most recent readings
        recent_readings = sorted(mac_readings, 
                               key=lambda x: x["timestamp"], 
                               reverse=True)[:3]
        
        # Simple triangulation using weighted average
        total_weight = 0
        weighted_lat = 0
        weighted_lon = 0
        
        for reading in recent_readings:
            # Weight inversely proportional to distance
            weight = 1.0 / max(reading["estimated_distance"], 1.0)
            lat, lon = reading["position"]
            
            weighted_lat += lat * weight
            weighted_lon += lon * weight
            total_weight += weight
        
        if total_weight == 0:
            return None
        
        estimated_position = {
            "mac": mac,
            "estimated_latitude": weighted_lat / total_weight,
            "estimated_longitude": weighted_lon / total_weight,
            "confidence": min(len(recent_readings) / 3.0, 1.0),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "readings_used": len(recent_readings)
        }
        
        return estimated_position
    
    def create_triangulation_log(self, estimated_position: Dict):
        """Create a detailed triangulation log entry"""
        log_entry = {
            "triangulation_result": estimated_position,
            "signal_readings": [r for r in self.signal_readings 
                              if r["mac"] == estimated_position["mac"]],
            "analysis": {
                "total_readings": len([r for r in self.signal_readings 
                                     if r["mac"] == estimated_position["mac"]]),
                "triangulation_method": "weighted_average_rssi",
                "accuracy_estimate": "medium"
            }
        }
        
        # Save to logs
        filename = f"logs/triangulation_{int(time.time())}.json"
        with open(filename, "w") as f:
            json.dump(log_entry, f, indent=2)
        
        return log_entry

def main():
    """Demonstration of triangulation capabilities"""
    engine = TriangulationEngine()
    
    # Simulate police officer device detection at multiple locations
    mac_address = "00:1A:2B:3C:4D:5E"  # Police radio MAC
    
    # Add simulated readings from different monitoring stations
    engine.add_signal_reading(mac_address, -45, (40.7128, -74.0060))  # Station 1
    engine.add_signal_reading(mac_address, -60, (40.7130, -74.0058))  # Station 2
    engine.add_signal_reading(mac_address, -55, (40.7126, -74.0062))  # Station 3
    
    # Triangulate position
    position = engine.triangulate_position(mac_address)
    
    if position:
        print("Triangulation successful!")
        print(f"Estimated position: {position['estimated_latitude']:.6f}, {position['estimated_longitude']:.6f}")
        print(f"Confidence: {position['confidence']:.2f}")
        
        # Create detailed log
        log_entry = engine.create_triangulation_log(position)
        print(f"Triangulation log created with {log_entry['analysis']['total_readings']} readings")
    else:
        print("Triangulation failed - insufficient data points")

if __name__ == "__main__":
    main()
