# HK Smart Factory R&D Project

A lightweight manufacturing line monitoring system for Hong Kong industrial facilities.

## Features

- **Production Line Monitoring**: Track multiple production lines and workstations
- **Real-time Metrics**: Monitor output rates and efficiency
- **Data Logging**: Automatic shift reports saved to JSON files
- **Web Dashboard**: Simple HTTP dashboard for remote monitoring
- **Configuration**: Customizable via configuration file

## Quick Start

### Run Production Monitor

```bash
python3 factory_monitor.py
```

This launches a basic production line simulation showing real-time output from multiple workstations.

### Start Web Dashboard

```bash
python3 web_dashboard.py
```

Then open http://localhost:8080 in your browser to view the dashboard.

### Test Data Logger

```bash
python3 production_logger.py
```

This demonstrates the shift report generation system.

## Configuration

Edit `hk_factory.conf` to customize:
- Production line settings
- Target production rates
- Quality inspection intervals
- Report storage location

## Project Structure

```
HK_SmartFactory_R-D_Project/
├── factory_monitor.py      # Main production monitor
├── web_dashboard.py        # HTTP dashboard server
├── production_logger.py    # Data logging utilities
├── hk_factory.conf         # Configuration file
└── production_data/        # Generated reports (auto-created)
```

## Generated Reports

Production reports are automatically saved to `production_data/` directory as JSON files containing:
- Shift summary statistics
- Production events log
- Timestamps and rates
- Line-specific metrics

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## License

MIT License