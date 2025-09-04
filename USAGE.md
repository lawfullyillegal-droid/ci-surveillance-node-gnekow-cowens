# Police Scanner Accountability System - Usage Guide

## Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Configuration
The system uses `config.json` for configuration. Key settings:

- **Scanner Frequencies**: Police radio frequencies to monitor
- **Location**: Your monitoring station coordinates
- **Monitoring Intervals**: How often to scan for signals
- **Accountability Settings**: Pattern analysis thresholds

### 3. Basic Usage

#### Start Continuous Monitoring
```bash
python3 cli.py start
```

#### Run System Test
```bash
python3 cli.py test
```

#### Generate Accountability Report
```bash
python3 cli.py report
python3 cli.py report --officer 123  # Specific officer
python3 cli.py report --output report.json  # Save to file
```

#### Test Triangulation
```bash
python3 cli.py triangulate --mac "00:1A:2B:3C:4D:5E"
```

## Core Functionality

### Police Scanner Monitoring
- Monitors configured police radio frequencies
- Automatically detects and logs incidents
- Identifies officer IDs from transmissions
- Categorizes incident types (traffic stops, arrests, etc.)

### MAC Address Tracking
- Scans for police device MAC addresses
- Triangulates officer locations using signal strength
- Tracks movement patterns during incidents
- Correlates device locations with scanner activity

### Incident Logging
- Automatic incident detection and logging
- Timestamp and location correlation
- Officer identification and tracking
- Incident type classification

### Pattern Analysis
- Tracks officer activity patterns
- Identifies high-activity officers
- Flags potential profiling patterns
- Generates accountability alerts

### Accountability Reporting
- Comprehensive officer activity reports
- Pattern analysis summaries
- Incident trend analysis
- Audit trail generation

## File Structure

```
├── scanner_bot.py          # Main application
├── triangulate.py          # Triangulation engine
├── cli.py                  # Command line interface
├── config.json             # Configuration file
├── requirements.txt        # Dependencies
├── data/
│   ├── incidents/          # Incident logs
│   ├── officers/           # Officer profiles
│   └── patterns/           # Pattern analysis
└── logs/                   # System logs
```

## Legal Considerations

This system is designed for legal transparency and accountability monitoring:

- Only monitors publicly accessible police scanner frequencies
- Does not intercept private communications
- Focuses on public accountability and transparency
- Intended to support legal oversight of law enforcement

## Technical Notes

### Signal Processing
- Uses RSSI (Received Signal Strength Indicator) for distance estimation
- Implements multi-point triangulation for location accuracy
- Provides confidence scoring for position estimates

### Data Management
- JSON-based data storage for portability
- Configurable log retention periods
- Automatic data organization by date and officer

### Extensibility
- Modular design for easy feature addition
- Configuration-driven operation
- Plugin-ready architecture for additional data sources

## System Requirements

- Python 3.8+
- SDR hardware for scanner monitoring (optional for simulation)
- Network interface for MAC address scanning
- Sufficient storage for log retention

## Accountability Features

### Officer Tracking
- Individual officer activity profiles
- Incident count and type analysis
- Geographic activity patterns
- Time-based activity analysis

### Pattern Detection
- High-activity officer identification
- Unusual incident pattern detection
- Geographic clustering analysis
- Time pattern analysis

### Audit Trails
- Complete incident-to-booking tracking
- Officer identification chain
- Evidence preservation
- Report generation for legal use

## Support

This system provides the foundation for police accountability monitoring. Additional features can be added based on specific legal and operational requirements.