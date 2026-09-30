# 💳 PayShield: Enterprise FinTech Payment Gateway & Cloud-Native DevOps Platform

[![Author](https://img.shields.io/badge/Author-Priyanshu%20(he99codes)-blue.svg?style=for-the-badge&logo=github)](https://github.com/he99codes)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.30-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Docker](https://img.shields.io/badge/Docker-Multi--Stage-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Jenkins](https://img.shields.io/badge/Jenkins-Declarative%20CI%2FCD-D24939?style=for-the-badge&logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![Ansible](https://img.shields.io/badge/Ansible-Automation-EE0000?style=for-the-badge&logo=ansible&logoColor=white)](https://www.ansible.com/)
[![Terraform](https://img.shields.io/badge/Terraform-AWS%20IaC-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)](https://www.terraform.io/)
[![PCI-DSS](https://img.shields.io/badge/Compliance-PCI--DSS%20v4-10B981?style=for-the-badge&logo=shield&logoColor=white)](https://www.pcisecuritystandards.org/)

> **PayShield** is an enterprise-grade, high-availability financial payment gateway and multi-cloud delivery pipeline. It demonstrates an automated, secure **zero-downtime release lifecycle** across AWS, Docker, Jenkins, Ansible, and Kubernetes with integrated fraud evaluation, auto-scaling, and Prometheus telemetry.

---

## 🌟 Live Interactive Showcase & Pipeline Simulator

The project includes an **interactive web showcase application** featuring:
- 🚀 **Live CI/CD Pipeline Simulator**: Watch real-time streaming console logs of SCM triggers, security audits, PyTest execution, container builds, Ansible tasks, and Kubernetes rollouts.
- 💳 **Live Payment Sandbox**: Submit live simulated payment transactions, test risk scoring, and verify latency and cluster nodes.
- 📊 **SLO & Metrics Dashboard**: 99.995% availability, 1,420 TPS, sub-30ms p99 response times.

### 🌐 Hosting Options

| Platform | Deployment Method | Time |
|:---|:---|:---:|
| **Local Docker** | `docker compose up -d` (Opens at `http://localhost:8080`) | 30s |
| **GitHub Pages** | Settings > Pages > Source: `Deploy from branch main / root` | 1 min |
| **Vercel / Netlify** | Connect repo, root directory: `/` (Automatic static deployment) | 1 min |
| **Local Python** | `python -m http.server 8080` | Instant |

---

## 🏗️ End-to-End System Architecture

```mermaid
flowchart TD
    subgraph Developer["🧑‍💻 Engineer & SCM"]
        DEV["Priyanshu (he99codes)"] -->|git push origin main| GITHUB["GitHub Repository\nhe99codes/payshield-devops"]
    end

    subgraph CI["⚙️ Continuous Integration (Jenkins)"]
        GITHUB -->|Webhook Trigger| JENKINS["Jenkins Master Server\n(Declarative Pipeline)"]
        JENKINS -->|Stage 1| LINT["PCI-DSS Security Audit\n& Syntax Compilation"]
        JENKINS -->|Stage 2| TEST["PyTest Unit & Integration\nTest Suite (6/6 Passed)"]
        JENKINS -->|Stage 3| DOCKER_BUILD["Multi-Stage Docker Build\n(Non-root user 10001)"]
        JENKINS -->|Stage 4| REGISTRY["DockerHub Registry\nhe99codes/payshield-payment-api:v2.4.0"]
    end

    subgraph CD["🚀 Orchestration & Configuration (Ansible)"]
        REGISTRY --> ANSIBLE["Ansible Control Node\n(inventory.ini)"]
        ANSIBLE -->|SSH Orchestration| DOCKER_HOSTS["Payment Edge Docker Nodes\n(Rolling Image Pull)"]
    end

    subgraph K8S["☸️ Production Kubernetes Cluster (AWS EKS)"]
        ANSIBLE -->|Rolling Update / Blue-Green| K8S_CLUSTER["AWS EKS / K8s Cluster\nNamespace: payshield-production"]
        K8S_CLUSTER --> POD1["Pod Replica 1\npayshield-api"]
        K8S_CLUSTER --> POD2["Pod Replica 2\npayshield-api"]
        K8S_CLUSTER --> POD3["Pod Replica 3\npayshield-api"]
        HPA["Horizontal Pod Autoscaler\n(3 to 10 Replicas @ 75% CPU)"] -.-> K8S_CLUSTER
        SVC["K8s NodePort 30080\n& AWS Network Load Balancer"] --> K8S_CLUSTER
    end

    subgraph Observability["📊 Monitoring & Telemetry"]
        K8S_CLUSTER -->|Scrapes /api/v1/metrics| PROM["Prometheus Server :9090"]
        PROM --> GRAFANA["Grafana Dashboards :3000\n(TPS, Latency, Error Rates)"]
    end

    classDef dev fill:#1e1e2e,stroke:#89b4fa,stroke-width:2px,color:#cdd6f4;
    classDef ci fill:#181926,stroke:#f9e2af,stroke-width:2px,color:#cdd6f4;
    classDef cd fill:#181926,stroke:#cba6f7,stroke-width:2px,color:#cdd6f4;
    classDef k8s fill:#11111b,stroke:#a6e3a1,stroke-width:2px,color:#cdd6f4;
    classDef obs fill:#1e2030,stroke:#89dceb,stroke-width:2px,color:#cdd6f4;

    class DEV,GITHUB dev;
    class JENKINS,LINT,TEST,DOCKER_BUILD,REGISTRY ci;
    class ANSIBLE,DOCKER_HOSTS cd;
    class K8S_CLUSTER,POD1,POD2,POD3,HPA,SVC k8s;
    class PROM,GRAFANA obs;
```

---

## 📁 Repository Directory Structure

```
PayShield-DevOps/
├── README.md                          # Comprehensive project documentation & architecture
├── LICENSE                            # MIT License © 2026 Priyanshu (he99codes)
├── docker-compose.yml                 # Instant 1-command local hosting stack
├── index.html                         # Interactive Web Showcase & Pipeline Simulator (Root)
│
├── app/                               # Core FinTech Payment Gateway Microservice
│   ├── app.py                         # Production Flask API (Transactions, Health, Metrics)
│   ├── requirements.txt               # App dependencies (Flask, Gunicorn, PyTest, Redis)
│   ├── Dockerfile                     # Multi-stage hardened non-root container (PCI-DSS)
│   └── tests/
│       └── test_payment_api.py        # Automated unit and integration test suite
│
├── terraform/                         # Infrastructure as Code (AWS Multi-AZ VPC & SGs)
│   ├── main.tf                        # VPC, subnets, route tables, security groups
│   ├── variables.tf                   # Parameterized FinTech configurations
│   └── outputs.tf                     # Exported network & cluster metadata
│
├── ansible/                           # Automated Configuration Management
│   ├── inventory.ini                  # Managed nodes (Control, Docker, K8s)
│   └── deploy-payment-gateway.yml     # Zero-downtime container rollout playbook
│
├── kubernetes/                        # Cloud-Native Production Manifests
│   ├── 01-namespace.yaml              # Isolated 'payshield-production' namespace
│   ├── 02-configmap-secrets.yaml      # Environmental configs & encrypted secrets
│   ├── 03-deployment.yaml             # 3-replica rolling update deployment
│   ├── 04-service.yaml                # NodePort (30080) & AWS Network LoadBalancer
│   ├── 05-hpa.yaml                    # Horizontal Pod Autoscaler (HPA)
│   └── 06-blue-green-cutover.yaml     # Zero-downtime Blue/Green traffic routing
│
├── jenkins/                           # Enterprise Continuous Integration & Delivery
│   └── Jenkinsfile                    # 8-stage declarative pipeline script
│
└── showcase/                          # Standalone Interactive Showcase Assets
    └── index.html                     # Interactive Simulator UI
```

---

## ⚡ Quickstart Guide

### 1. Run the Entire Stack Locally (Docker Compose)
Launch the FinTech API, Redis cache, and Interactive Showcase with one command:
```bash
docker compose up -d
```
- **Showcase Dashboard**: [http://localhost:8080](http://localhost:8080)
- **Payment Gateway API**: [http://localhost:5000](http://localhost:5000)
- **Health Check**: [http://localhost:5000/api/v1/health](http://localhost:5000/api/v1/health)
- **Prometheus Metrics**: [http://localhost:5000/api/v1/metrics](http://localhost:5000/api/v1/metrics)

---

### 2. Run Automated Unit Tests
```bash
python -m pip install -r app/requirements.txt
pytest app/tests/ -v
```
**Test Results:**
```
app/tests/test_payment_api.py::test_index_route PASSED                   [ 16%]
app/tests/test_payment_api.py::test_health_check PASSED                  [ 33%]
app/tests/test_payment_api.py::test_successful_transaction PASSED        [ 50%]
app/tests/test_payment_api.py::test_fraud_flagged_transaction PASSED     [ 66%]
app/tests/test_payment_api.py::test_invalid_payload PASSED               [ 83%]
app/tests/test_payment_api.py::test_prometheus_metrics_export PASSED     [100%]
============================== 6 passed in 0.83s ==============================
```

---

### 3. Provision AWS Cloud Infrastructure (Terraform)
```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve
```

---

### 4. Deploy via Ansible Automation
```bash
ansible-playbook -i ansible/inventory.ini ansible/deploy-payment-gateway.yml
```

---

### 5. Deploy to Kubernetes Cluster
```bash
# Apply namespace, configurations, deployment, and service
kubectl apply -f kubernetes/01-namespace.yaml
kubectl apply -f kubernetes/02-configmap-secrets.yaml
kubectl apply -f kubernetes/03-deployment.yaml
kubectl apply -f kubernetes/04-service.yaml
kubectl apply -f kubernetes/05-hpa.yaml

# Inspect active pods and service
kubectl get pods -n payshield-production
kubectl get svc payshield-service -n payshield-production
```

---

### 6. Zero-Downtime Blue/Green Deployment Cutover
```bash
# Deploy both Blue (v2.3.9) and Green (v2.4.0)
kubectl apply -f kubernetes/06-blue-green-cutover.yaml

# Seamlessly switch production traffic to Green with zero downtime
kubectl patch service payshield-active-traffic-router -n payshield-production \
  -p '{"spec":{"selector":{"version":"green"}}}'
```

---

## 🔒 Security & FinTech Compliance Highlights

1. **Non-Root Container Hardening**: Containers run under UID `10001` (`payshield`), satisfying PCI-DSS Section 6.5 standards.
2. **Network Isolation**: Strict AWS VPC with private database subnets and restricted security groups.
3. **Automated Fraud Detection**: Transactions > $50,000 are automatically flagged for review with high risk scoring.
4. **Idempotency & Resilience**: Redis caching layer prevents duplicate payment chargebacks during network retries.

---

## 👤 Author & Maintainer

**Priyanshu (`he99codes`)**  
- **GitHub**: [@he99codes](https://github.com/he99codes)  
- **Email**: priyanshu2164@gmail.com  
- **Role**: Cloud DevOps & Infrastructure Engineer  

---

*This project is distributed under the MIT License. See [LICENSE](LICENSE) for details.*
