# Oracle NoSQL Yelp Key-Value Project

This repository contains the Oracle NoSQL part of a university project for Key-Value NoSQL Databases.

The project uses:

* Oracle NoSQL Database / KVLite in Docker
* Python SDK `borneo`
* Yelp dataset subset
* Key-value table `kv_store`
* Query scenarios and performance measurements

The Redis part is implemented separately by other team members. This repository contains only the Oracle NoSQL implementation.

---

## 1. Project Goal

The goal of this part of the project is to import Yelp dataset data into Oracle NoSQL Database and use it through a key-value data model.

The implementation demonstrates:

* installation of Oracle NoSQL
* preprocessing of Yelp data
* importing data into Oracle NoSQL
* key-value data modeling
* denormalized / aggregated keys
* query scenarios
* performance measurements
* results prepared for comparison with Redis

---

## 2. Technologies Used

* macOS
* Docker Desktop
* Oracle NoSQL Database Community Edition / KVLite
* Python 3
* Python package `borneo`
* pandas
* tqdm
* matplotlib
* Yelp dataset

---

## 3. Project Structure

```text
oracle-nosql-yelp-keyvalue/
│
├── scripts/
│   ├── test_oracle.py
│   ├── prepare_yelp_subset.py
│   ├── import_yelp_oracle.py
│   ├── query_oracle_clean.py
│   ├── performance_oracle.py
│   ├── plot_oracle_performance.py
│   └── prepare_oracle_comparison_csv.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── results/
│   ├── oracle_query_examples.txt
│   ├── oracle_performance.csv
│   ├── oracle_performance_output.txt
│   ├── oracle_performance_chart.png
│   └── oracle_performance_for_comparison.csv
│
├── docs/
│   └── oracle_notes.md
│
├── .gitignore
└── README.md
```

Important: the `data/` folder is not uploaded to GitHub because the Yelp dataset files are large.

---

## 4. Prerequisites

Before running the project, install:

1. Docker Desktop
2. Python 3
3. Git
4. VS Code, optional but recommended

Check Docker:

```bash
docker --version
```

Check Python:

```bash
python3 --version
```

---

## 5. Clone the Repository

```bash
git clone https://github.com/marijaapr/oracle-nosql-yelp-keyvalue.git
cd oracle-nosql-yelp-keyvalue
```

---

## 6. Start Oracle NoSQL with Docker

Pull the Oracle NoSQL image:

```bash
docker pull ghcr.io/oracle/nosql:latest-ce
docker tag ghcr.io/oracle/nosql:latest-ce oracle/nosql:ce
```

Start KVLite:

```bash
docker run -d \
  --name=kvlite \
  --hostname=kvlite \
  --env KV_PROXY_PORT=8080 \
  -p 8080:8080 \
  oracle/nosql:ce
```

Check if the container is running:

```bash
docker ps
```

If the container already exists, start it with:

```bash
docker start kvlite
```

Oracle NoSQL will be available at:

```text
http://localhost:8080
```

---

## 7. Create Python Virtual Environment

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install borneo pandas tqdm matplotlib
```

Optional:

```bash
python -m pip install --upgrade pip
```

---

## 8. Test Oracle NoSQL Connection

Run:

```bash
python scripts/test_oracle.py
```

Expected result:

```text
Tabela kv_store e kreirana.
Procitan zapis:
...
```

This confirms that Oracle NoSQL is running and Python can connect to it.

---

## 9. Download Yelp Dataset

The full Yelp dataset is not included in this repository because it is too large for GitHub.

Download the Yelp dataset manually from Kaggle:

```text
https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset
```

After downloading and extracting it, place these files inside:

```text
data/raw/
```

Required files:

```text
data/raw/yelp_academic_dataset_business.json
data/raw/yelp_academic_dataset_review.json
data/raw/yelp_academic_dataset_user.json
```

The final structure should look like:

```text
data/raw/yelp_academic_dataset_business.json
data/raw/yelp_academic_dataset_review.json
data/raw/yelp_academic_dataset_user.json
```

---

## 10. Preprocess the Yelp Dataset

Run:

```bash
python scripts/prepare_yelp_subset.py
```

This script creates a smaller subset of the Yelp dataset.

The preprocessing step:

* selects only relevant files: business, review, user
* filters businesses by city and category
* keeps restaurants in Philadelphia
* keeps only reviews related to selected businesses
* keeps only users related to selected reviews
* saves the processed data into `data/processed/`

Generated files:

```text
data/processed/business_subset.jsonl
data/processed/review_subset.jsonl
data/processed/user_subset.jsonl
```

To check the number of records:

```bash
wc -l data/processed/*.jsonl
```

---

## 11. Import Data into Oracle NoSQL

Run:

```bash
python scripts/import_yelp_oracle.py
```

The data is imported into the Oracle NoSQL table:

```text
kv_store
```

The table uses a key-value structure:

```text
k -> key
v -> JSON value
```

---

## 12. Key-Value Data Model

The project uses one physical Oracle NoSQL table:

```text
kv_store
```

However, the data is logically organized into two modeling levels.

### Level 1: Basic Key-Value Model

Each main entity is stored directly by ID:

```text
business:{business_id}
user:{user_id}
review:{review_id}
```

Examples:

```text
business:MTSW4McQd7CbVtyjqoe9mw
user:{user_id}
review:{review_id}
```

### Level 2: Denormalized / Aggregated Model

Additional keys are created for faster access:

```text
business_reviews:{business_id}
user_reviews:{user_id}
city_category:Philadelphia:Restaurants
stats:business:{business_id}
```

These keys support access patterns that would normally require joins in a relational database.

---

## 13. Run Query Scenarios

Run:

```bash
python scripts/query_oracle_clean.py
```

To save the output:

```bash
python scripts/query_oracle_clean.py | tee results/oracle_query_examples.txt
```

Implemented query scenarios:

1. Get restaurants in Philadelphia
2. Get business by ID
3. Get all reviews for a business
4. Get business statistics
5. Get review by ID
6. Get user by ID

---

## 14. Run Performance Measurements

Run:

```bash
python scripts/performance_oracle.py
```

This creates:

```text
results/oracle_performance.csv
```

The script measures average execution time for multiple key-value access scenarios.

---

## 15. Create Performance Chart

Run:

```bash
python scripts/plot_oracle_performance.py
```

This creates:

```text
results/oracle_performance_chart.png
```

The chart can be used in the written report and presentation.

---

## 16. Prepare Oracle Results for Redis Comparison

Run:

```bash
python scripts/prepare_oracle_comparison_csv.py
```

This creates:

```text
results/oracle_performance_for_comparison.csv
```

This file should be shared with the Redis team so they can compare their results using the same query scenarios.

---

## 17. Visual Management in VS Code

Install the VS Code extension:

```text
Oracle NoSQL Database Connector
```

Create a connection with:

```text
Connection Name: Local_KVLite
Profile Type: Onprem
Endpoint: http://localhost:8080
```

Then open:

```text
Oracle NoSQL DB → Local_KVLite → Tables → kv_store
```

Example query:

```sql
SELECT * FROM kv_store WHERE k = 'city_category:Philadelphia:Restaurants'
```

---

## 18. Important Files for Review

The most important files are:

```text
scripts/prepare_yelp_subset.py
scripts/import_yelp_oracle.py
scripts/query_oracle_clean.py
scripts/performance_oracle.py
scripts/plot_oracle_performance.py
docs/oracle_notes.md
results/oracle_performance.csv
results/oracle_performance_chart.png
results/oracle_performance_for_comparison.csv
```

---

## 19. Notes

The raw Yelp dataset is not uploaded to GitHub because it is too large.

The `data/raw/` and `data/processed/` folders are ignored by Git.

To reproduce the project, download the Yelp dataset manually, place the required files in `data/raw/`, and run the preprocessing and import scripts.

---

## 20. Troubleshooting

### Docker container already exists

Use:

```bash
docker start kvlite
```

### Check if Oracle NoSQL is running

```bash
docker ps
```

### Stop Oracle NoSQL

```bash
docker stop kvlite
```

### Remove Oracle NoSQL container

```bash
docker rm -f kvlite
```

### Python import error with StoreAccessTokenProvider

Use this import:

```python
from borneo.kv import StoreAccessTokenProvider
```

not:

```python
from borneo import StoreAccessTokenProvider
```

---

## 21. Summary

This repository demonstrates the Oracle NoSQL implementation for a Key-Value NoSQL database project using the Yelp dataset.

It includes:

* Oracle NoSQL installation with Docker
* Yelp dataset preprocessing
* key-value data modeling
* data import
* denormalized and aggregated keys
* query scenarios
* performance measurements
* results prepared for comparison with Redis

