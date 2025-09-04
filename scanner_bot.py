#!/usr/bin/env python3
"""
Police Scanner Accountability Bot

Main application for monitoring police scanner communications,
tracking officer locations, and logging incidents for accountability.
"""

import json
import time
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scanner_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ScannerBot:
    """Main scanner bot class for police accountability monitoring"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config = self.load_config(config_file)
        self.active_incidents = {}
        self.officer_locations = {}
        self.mac_addresses = {}
        
        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)
        os.makedirs("data/incidents", exist_ok=True)
        os.makedirs("data/officers", exist_ok=True)
        os.makedirs("data/patterns", exist_ok=True)
        
        logger.info("Scanner Bot initialized")
    
    def load_config(self, config_file: str) -> Dict:
        """Load configuration file or create default config"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default config
            default_config = {
                "scanner_frequencies": [
                    {"freq": "154.8000", "description": "Police Dispatch"},
                    {"freq": "155.7750", "description": "Police Tactical"},
                    {"freq": "460.2250", "description": "Police Admin"}
                ],
                "location": {
                    "latitude": 40.7128,
                    "longitude": -74.0060,
                    "name": "Default Location"
                },
                "monitoring": {
                    "mac_scan_interval": 30,
                    "scanner_scan_interval": 5,
                    "log_retention_days": 365
                }
            }
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
    
    def monitor_scanner(self):
        """Monitor police scanner communications"""
        logger.info("Starting scanner monitoring...")
        
        # Simulate scanner monitoring (replace with actual SDR implementation)
        sample_transmission = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "frequency": "154.8000",
            "channel": "Police Dispatch",
            "transmission": "Unit 123 responding to traffic stop at Main St and 5th Ave",
            "officer_id": "123",
            "incident_type": "traffic_stop",
            "location": "Main St and 5th Ave",
            "signal_strength": -65
        }
        
        self.log_incident(sample_transmission)
        return sample_transmission
    
    def track_mac_addresses(self) -> List[Dict]:
        """Track MAC addresses for officer location triangulation"""
        logger.info("Scanning for MAC addresses...")
        
        # Simulate MAC address detection (replace with actual network scanning)
        detected_macs = [
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "mac": "00:1A:2B:3C:4D:5E",
                "vendor": "Motorola Solutions",
                "signal_strength": -45,
                "estimated_distance": 50,
                "device_type": "police_radio"
            },
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "mac": "AA:BB:CC:DD:EE:FF",
                "vendor": "Panasonic",
                "signal_strength": -60,
                "estimated_distance": 100,
                "device_type": "police_vehicle"
            }
        ]
        
        # Log MAC addresses for triangulation
        for mac_data in detected_macs:
            self.log_mac_address(mac_data)
        
        return detected_macs
    
    def log_incident(self, incident_data: Dict):
        """Log incident data for accountability tracking"""
        incident_id = f"incident_{int(time.time())}"
        incident_data["incident_id"] = incident_id
        
        # Save incident data
        incident_file = f"data/incidents/{incident_id}.json"
        with open(incident_file, 'w') as f:
            json.dump(incident_data, f, indent=2)
        
        # Add to active incidents
        self.active_incidents[incident_id] = incident_data
        
        logger.info(f"Logged incident: {incident_id}")
        
        # Check for patterns
        self.analyze_patterns(incident_data)
    
    def log_mac_address(self, mac_data: Dict):
        """Log MAC address data for triangulation"""
        mac_address = mac_data["mac"]
        timestamp = str(int(time.time()))
        
        # Create triangulation log
        triangulation_file = f"logs/triangulation_{timestamp}.json"
        with open(triangulation_file, 'w') as f:
            json.dump(mac_data, f, indent=2)
        
        # Update MAC address tracking
        self.mac_addresses[mac_address] = mac_data
        
        logger.info(f"Logged MAC address: {mac_address}")
    
    def analyze_patterns(self, incident_data: Dict):
        """Analyze patterns for potential profiling or misconduct"""
        officer_id = incident_data.get("officer_id")
        incident_type = incident_data.get("incident_type")
        
        if not officer_id:
            return
        
        # Load officer history
        officer_file = f"data/officers/{officer_id}.json"
        try:
            with open(officer_file, 'r') as f:
                officer_history = json.load(f)
        except FileNotFoundError:
            officer_history = {
                "officer_id": officer_id,
                "incidents": [],
                "patterns": {},
                "accountability_flags": []
            }
        
        # Add incident to history
        officer_history["incidents"].append(incident_data)
        
        # Analyze patterns
        incident_types = [inc.get("incident_type") for inc in officer_history["incidents"]]
        pattern_analysis = {
            "total_incidents": len(officer_history["incidents"]),
            "incident_type_counts": {},
            "recent_activity": len([inc for inc in officer_history["incidents"] 
                                  if (datetime.now(timezone.utc) - 
                                      datetime.fromisoformat(inc["timestamp"].replace('Z', '+00:00'))).days <= 30])
        }
        
        # Count incident types
        for inc_type in incident_types:
            if inc_type:
                pattern_analysis["incident_type_counts"][inc_type] = \
                    pattern_analysis["incident_type_counts"].get(inc_type, 0) + 1
        
        officer_history["patterns"] = pattern_analysis
        
        # Check for potential flags
        if pattern_analysis["total_incidents"] > 50:
            officer_history["accountability_flags"].append({
                "flag": "high_activity",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "description": "Officer has unusually high incident count"
            })
        
        # Save updated officer data
        with open(officer_file, 'w') as f:
            json.dump(officer_history, f, indent=2)
        
        logger.info(f"Updated pattern analysis for officer {officer_id}")
    
    def generate_accountability_report(self, officer_id: Optional[str] = None) -> Dict:
        """Generate accountability report for specific officer or all officers"""
        report = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "report_type": "accountability_summary",
            "officers": {}
        }
        
        if officer_id:
            # Single officer report
            officer_files = [f"data/officers/{officer_id}.json"]
        else:
            # All officers report
            officer_files = [f for f in os.listdir("data/officers") if f.endswith(".json")]
            officer_files = [f"data/officers/{f}" for f in officer_files]
        
        for officer_file in officer_files:
            try:
                with open(officer_file, 'r') as f:
                    officer_data = json.load(f)
                    report["officers"][officer_data["officer_id"]] = officer_data
            except FileNotFoundError:
                continue
        
        # Save report
        report_file = f"data/patterns/accountability_report_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def run(self):
        """Main run loop for the scanner bot"""
        logger.info("Starting Police Scanner Accountability Bot")
        
        try:
            while True:
                # Monitor scanner
                self.monitor_scanner()
                
                # Track MAC addresses
                self.track_mac_addresses()
                
                # Sleep between scans
                time.sleep(self.config["monitoring"]["scanner_scan_interval"])
                
        except KeyboardInterrupt:
            logger.info("Scanner Bot stopped by user")
        except Exception as e:
            logger.error(f"Scanner Bot error: {e}")
            raise

def main():
    """Main entry point"""
    bot = ScannerBot()
    
    # Generate initial report
    report = bot.generate_accountability_report()
    print(f"Generated accountability report with {len(report['officers'])} officers")
    
    # Run a single monitoring cycle for demonstration
    bot.monitor_scanner()
    bot.track_mac_addresses()
    
    print("Scanner Bot demonstration complete. Run with 'bot.run()' for continuous monitoring.")

if __name__ == "__main__":
    main()