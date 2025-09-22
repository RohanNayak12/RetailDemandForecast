## Retail Demand Forecast (Prophet + DVC + Flask)

A production-style, end-to-end retail demand forecasting project. It ingests historical Walmart sales data, trains per-store Prophet models, evaluates performance, and serves single-date forecasts via a Flask web UI. The pipeline is orchestrated with DVC for reproducibility.

### Features
- **End-to-end pipeline**: ingestion → base model prep → training → evaluation → prediction
- **Per-store models**: one Prophet model per store for targeted accuracy
- **Reproducible runs**: DVC stages with tracked inputs/outputs
- **Metrics & tracking**: MAPE/MAE evaluation with optional MLflow logging (Dagshub)
- **Web UI**: Flask app to query a specific store and date

### Tech Stack
- Python, Prophet, pandas, scikit-learn
- DVC for pipelines
- MLflow (optional) for experiment tracking
- Flask + Tailwind template for the UI

---

## Project Structure
```text
RetailDemandForecast/
├─ app.py                         # Flask app entrypoint
├─ main.py                        # Sequential runner for all pipeline stages
├─ dvc.yaml, dvc.lock             # DVC pipeline definitions and lockfile
├─ config/
│  └─ config.yaml                 # Paths & base settings (artifacts, model dirs)
├─ params.yaml                    # Training/eval parameters
├─ src/retailDemand/
│  ├─ pipeline/                   # Stage orchestrators
│  │  ├─ stage01_data_injestion.py
│  │  ├─ stage02_creating_model.py
│  │  ├─ stage03_model_train.py
│  │  ├─ stage04_model_eval.py
│  │  └─ stage05_model_pred.py
│  ├─ components/                 # Stage implementations
│  │  ├─ data_injestion.py
│  │  ├─ base_model_creation.py
│  │  ├─ model_train.py
│  │  ├─ model_eval.py
│  │  └─ model_pred.py
│  ├─ config/                     # Configuration manager
│  │  └─ configuration.py
│  ├─ entity/                     # Typed config dataclasses
│  │  └─ config_entity.py
│  ├─ constants/                  # Global constants (paths)
│  │  └─ __init__.py
│  └─ __init__.py                 # Logger setup (writes to logs/)
├─ templates/
│  └─ index.html                  # Web UI template
├─ artifacts/                     # DVC-tracked outputs (created at runtime)
├─ requirements.txt               # Python dependencies
├─ LICENSE
└─ README.md
```

---

## Setup
### Prerequisites
- Python 3.9–3.11
- Git
- Optional: DVC (`pip install dvc`), recommended for reproducible runs

### Installation
```bash
# Clone the repository
git clone <your-fork-or-repo-url>
cd RetailDemandForecast

# Create and activate a virtual environment (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Configuration
- `config/config.yaml`
  - Controls artifact directories, dataset/model paths, and base-model settings.
- `params.yaml`
  - Controls training/eval parameters such as `TRAIN_SPLIT`, `FORECAST_PERIODS`, `FREQUENCY`, and column names.

Update these files to point to your data source and adjust training hyperparameters as needed.

---

## Data
The ingestion stage downloads a zipped dataset from Google Drive as specified in `config/config.yaml` under `data_injestion.source_url`. It then:
- Extracts the archive into `artifacts/data_injestion/`
- Merges `train.csv`, `features.csv`, and `stores.csv`
- Engineers time features and writes `final_data.csv`

If hosting data elsewhere, replace `source_url` with your link or modify `components/data_injestion.py` accordingly.

---

## Running the Pipeline
You can run the full pipeline either directly via Python or with DVC.

### Option A: Python (sequential)
```bash
python main.py
```
This executes, in order:
1. Data Ingestion
2. Base Model Preparation
3. Model Training
4. Model Evaluation
5. (Prediction is used by the app; not executed here automatically)

### Option B: DVC (reproducible)
```bash
# Reproduce the entire pipeline
dvc repro

# Or run a specific stage
dvc repro data_injestion
```
DVC stages are defined in `dvc.yaml` and produce outputs under `artifacts/`.

---

## Launch the Web App
Once models are trained and saved to `artifacts/model_train/trained_models/`, start the Flask app:
```bash
python app.py
```
Open `http://127.0.0.1:5000/` and enter a `Store ID` and a `Date` to get a sales forecast with confidence bounds.

---

## MLflow Tracking (Optional)
This project can log evaluation metrics to MLflow (e.g., Dagshub). Set these environment variables before running evaluation:
```bash
# Example (PowerShell)
$env:MLFLOW_TRACKING_URI = "https://dagshub.com/<user>/<repo>.mlflow"
$env:MLFLOW_TRACKING_USERNAME = "<your-username>"
$env:MLFLOW_TRACKING_PASSWORD = "<your-token>"
```
Ensure you do not commit secrets to the repository. The code will log metrics like Median MAPE per run.

---

## Artifacts
- `artifacts/data_injestion/final_data.csv`: Merged and cleaned dataset
- `artifacts/prepare_base_model/base_model.pkl`: Base Prophet model template
- `artifacts/model_train/trained_models/prophet_{store}.pkl`: Per-store trained models
- `artifacts/model_evaluation/`: Evaluation summary CSV and logs

Logs are written to `logs/running_logs.log`.

---

## Troubleshooting
- Windows `PYTHONPATH` in DVC is handled in `dvc.yaml` via `set PYTHONPATH=.`; if running stages manually, ensure your working directory is the repo root.
- If downloading from Google Drive fails, verify the link in `config/config.yaml` and your network access.
- Prophet may require a working compiler toolchain depending on backend; the pinned version in `requirements.txt` is selected to minimize friction.

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.