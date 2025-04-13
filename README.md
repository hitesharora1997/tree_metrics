# Tree Metrics Project

A Python application for processing LiDAR point cloud data to extract tree metrics such as height and diameter at breast height (DBH).

## Features
- Processes LiDAR point cloud data from LAS files
- Extracts tree metrics including **height** and **Diameter at Breast Height (DBH)**
- Exports results to CSV for further analysis
- Visualizes results with both 2D plots and 3D point cloud visualization
- Docker support for containerization

## Getting Started

### Prerequisites

- Python 3.8 or later
- Required Python packages (see requirements.txt)
- `virtualenv` or `venv` for creating virtual environments
- Docker (for containerization)


### Project Structure

```plaintext
├── src/                    # Source code for the application
│   ├── __init__.py
│   ├── io.py               # Functions for reading LAS files
│   ├── preprocessing.py    # Data preparation and filtering
│   ├── metrics.py          # Tree metrics calculation logic
│   ├── processor.py        # Main processing pipeline
│   ├── exporter.py         # Functions for exporting results
│   └── logger_config.py    # Logging configuration
├── tests/                  # Unit tests for the application
│   ├── __init__.py
│   ├── test_metrics.py     # Tests for metrics calculations
│   ├── test_preprocessing.py # Tests for preprocessing functions
│   ├── test_processor.py   # Tests for full processing pipeline
│   ├── test_exporter.py    # Tests for export functionality
│   └── test_io.py          # Tests for I/O functions
├── data/                   # Directory for input data
├── outputs/                # Directory for results (CSV, visualizations)
├── logs/                   # Log files (gitignored)
├── Dockerfile              # Dockerfile for containerization
├── Makefile                # Build/run shortcuts
├── requirements.txt        # Python dependencies
├── main.py                 # Driver script
├── config.py               # Configuration parameters
└── README.md               # Project documentation
```


### Input
The application expects a `.las` LiDAR file that includes:
- `x`, `y`, `z` coordinates
- Classification values (e.g., ground, trunk, canopy)
- Tree ID (field like `treeID`, `user_data`, or `point_source_id`)

### Output

**CSV file (tree_metrics.csv):**
```csv
tree_id,height,dbh
1,24.742,0.425
2,23.317,0.406
```

### Example Usage
#### Sample LAS Run
```bash
make run FILE=data/example_dataset.las
```

#### Run with Metric Visualizations
```bash
make run FILE=data/example_dataset.las OPTIONS="--visualize --log-level DEBUG"
```

#### Run with 3D Point Cloud Visualization (PyVista)
```bash
make run FILE=data/example_dataset.las OPTIONS="--visualize-3d --color-by tree_id"
```

Clone the repository:
   ```bash
   git clone https://github.com/hitesharora1997/tree-metrics.git
   cd tree-metrics
   ```

Create a virtual environment and install dependencies:
   ```bash
   make setup
   ```

Run the application:
   ```bash
   make run FILE=data/example_dataset.las
   ```

Run the test:
   ```bash
   make test
   ```

Building Docker Image
   ```bash
   make docker
   ```

Running Docker Image
   ```bash
   make docker-run FILE=data/example_dataset.las
   ```

Cleaning up the virtual environment and other generated files:
   ```bash
   make clean
   ```
Help
   ```bash
   make help
   ```

### Assumptions 
1. The ground in the LiDAR data is assumed to be flat.
2. Trees have been pre-segmented with unique tree IDs (0 = non-tree points)
3. Point classifications follow the convention specified in the assignment:
- 0 = ground
- 1 = trunk
- 2 = branch
- 3 = leaf/canopy

4. DBH is calculated at 1.3m ± 5cm
5. Minimum of 5 trunk points required at DBH height

### Limitations
- The current implementation focuses on simple tree metrics. Additional metrics could be added in future versions.
- Error handling can be improved. 
- Optimization needed for very large LAS files.