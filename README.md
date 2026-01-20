# 🚀 End-to-End Real-time Crypto Data Pipeline on GCP

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Spark](https://img.shields.io/badge/Apache%20Spark-Structured%20Streaming-orange)
![GCP](https://img.shields.io/badge/Google%20Cloud-Dataproc%20%7C%20BigQuery%20%7C%20GCS-green)

> A scalable, low-latency streaming pipeline that ingests live crypto market data, processes it via Spark on Dataproc, and visualizes trends in real-time.

## 🏛 Architecture & Data Flow

This project implements the **File-based Streaming (Landing Zone)** pattern to decouple ingestion from processing, ensuring high availability and fault tolerance.

```mermaid
graph LR
    API[CoinGecko API] -->|HTTP GET JSON| PRODUCER(Python Producer)
    PRODUCER -->|Upload NDJSON| GCS[GCS Bucket\nLanding Zone]
    GCS -->|Trigger| SPARK[Spark Structured Streaming\nDataproc Cluster]
    SPARK -->|Checkpointing| GCS_CHK[GCS Checkpoint]
    SPARK -->|Micro-batch| BQ[(BigQuery\nData Warehouse)]
    BQ -->|Query| DASHBOARD[Looker Studio]
    
    style SPARK fill:#faac58,stroke:#333,stroke-width:2px
    style BQ fill:#66c2a5,stroke:#333,stroke-width:2px
    style GCS fill:#4285F4,stroke:#fff,stroke-width:2px,color:#fff
```
## 📊 Real-time Dashboard Demo

Visualizing live price movements (BTC, ETH, ...) using Logarithmic Scale.

<img width="704" height="486" alt="Screenshot 2026-01-20 at 01 10 14" src="https://github.com/user-attachments/assets/f6a56a3b-57da-4c62-9bd7-b2f849f198c0" />

## 🛠 Tech Stack
  
  **Ingestion:**           Python (Custom Producer), Google Cloud Storage (Staging).

  **Processing:**          Apache Spark Structured Streaming (Dataproc).

  **Warehouse:**           Google BigQuery (Partitioned Tables).

  **Visualization:**       Looker Studio.
  
## 💡 Key Technical Challenges & Solutions

### 1. Handling API Rate Limits & Data Quality

-   **Challenge:** The CoinGecko API restricts the number of requests
    and occasionally returns error messages instead of JSON data, which
    could crash the pipeline.
-   **Solution:** Implemented a robust **Python Producer** with
    `try-except` blocks and `time.sleep()` backoff strategies. Added
    data validation (`isinstance(info, dict)`) to filter out bad
    responses before ingestion.

### 2. Dependency Hell & Connector Issues

-   **Challenge:** The standard Spark-PubSub connector was
    deprecated/unavailable for the specific Spark version on Dataproc.
-   **Solution:** Pivoted to a **File-based Streaming Architecture**
    using GCS as a trigger. This native Spark approach removed external
    dependency risks and simplified the debugging process (since raw
    files are readable in the bucket).

### 3. Fault Tolerance

-   **Challenge:** Ensuring the streaming job can resume after a failure
    without losing data.
-   **Solution:** Configured Spark **Checkpointing** in GCS. This allows
    the job to track processed files (`offsets`) and resume exactly
    where it left off in case of a cluster restart.

---

<details>
<summary><strong>🏃‍♂️ Click here to see "How to Run"</strong></summary>

### Prerequisites

* GCP Account (Dataproc, BigQuery, GCS enabled).
* Google Cloud SDK installed.

### Quick Start

1. **Setup Infra:**
bash gsutil mb -l us-central1 gs://YOUR_BUCKET_NAME/ bq mk --location=us-central1 streaming_dataset
3. **Run Producer:**
bash pip install google-cloud-storage requests python producer_file.py
4. **Submit Spark Job:**
bash gcloud dataproc jobs submit pyspark spark_streaming_files.py \ --cluster=spark-streaming-cluster \ --region=us-central1 \ --project=YOUR_PROJECT_ID

</details>
