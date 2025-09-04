#!/usr/bin/env python3
"""
Police Scanner Bot CLI
Command line interface for the Police Scanner Accountability System
"""

import argparse
import json
import sys
from scanner_bot import ScannerBot
from triangulate import TriangulationEngine

def main():
    parser = argparse.ArgumentParser(
        description="Police Scanner Accountability System CLI"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Start monitoring command
    start_parser = subparsers.add_parser('start', help='Start continuous monitoring')
    start_parser.add_argument('--config', default='config.json', 
                             help='Configuration file path')
    
    # Generate report command
    report_parser = subparsers.add_parser('report', help='Generate accountability report')
    report_parser.add_argument('--officer', help='Specific officer ID')
    report_parser.add_argument('--output', help='Output file path')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Run system test')
    
    # Triangulate command
    triangulate_parser = subparsers.add_parser('triangulate', help='Test triangulation')
    triangulate_parser.add_argument('--mac', required=True, help='MAC address to triangulate')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'start':
        print("Starting Police Scanner Accountability System...")
        bot = ScannerBot(args.config)
        try:
            bot.run()
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")
    
    elif args.command == 'report':
        print("Generating accountability report...")
        bot = ScannerBot()
        report = bot.generate_accountability_report(args.officer)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Report saved to {args.output}")
        else:
            print(json.dumps(report, indent=2))
    
    elif args.command == 'test':
        print("Running system test...")
        bot = ScannerBot()
        
        # Test scanner monitoring
        print("Testing scanner monitoring...")
        transmission = bot.monitor_scanner()
        print(f"✓ Scanner monitoring: {transmission['incident_type']}")
        
        # Test MAC tracking
        print("Testing MAC address tracking...")
        macs = bot.track_mac_addresses()
        print(f"✓ MAC tracking: {len(macs)} devices detected")
        
        # Test report generation
        print("Testing report generation...")
        report = bot.generate_accountability_report()
        print(f"✓ Report generation: {len(report['officers'])} officers tracked")
        
        print("All tests passed!")
    
    elif args.command == 'triangulate':
        print(f"Testing triangulation for MAC: {args.mac}")
        engine = TriangulationEngine()
        
        # Add sample readings
        engine.add_signal_reading(args.mac, -45, (40.7128, -74.0060))
        engine.add_signal_reading(args.mac, -60, (40.7130, -74.0058))
        engine.add_signal_reading(args.mac, -55, (40.7126, -74.0062))
        
        position = engine.triangulate_position(args.mac)
        if position:
            print(f"Triangulated position: {position['estimated_latitude']:.6f}, {position['estimated_longitude']:.6f}")
            print(f"Confidence: {position['confidence']:.2f}")
        else:
            print("Triangulation failed")

if __name__ == "__main__":
    main()