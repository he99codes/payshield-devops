# 📖 PayShield DevOps: Component-by-Component Guide
> **Author**: Priyanshu ([@he99codes](https://github.com/he99codes))  
> **Repository**: [he99codes/payshield-devops](https://github.com/he99codes/payshield-devops)  
> **Purpose**: A quick, plain-English reference explaining every layer, file, and tool in this project. Perfect for interview preparation, viva, and presentations.

---

## 1. What is this Project? (The Big Picture)

**PayShield** is an automated **FinTech Payment Gateway infrastructure**. 

In the real world, payment systems (like Stripe or PayPal) cannot afford even 1 second of downtime, and they must follow strict security rules (**PCI-DSS**). 

This project solves three key challenges:
1. **Zero Downtime**: Upgrading the application without kicking off active users (Blue-Green & Rolling updates).
2. **Automated Quality & Security**: Testing code and scanning for vulnerabilities on every single Git push.
3. **Reproducible Infrastructure**: Setting up the cloud environment using code instead of clicking in the AWS console.

---

## 2. Component Breakdown

### 🔹 Layer 1: Application Microservice (`app/`)
* **[`app/app.py`](app/app.py)**: The core REST API written in Python Flask.
  * `/api/v1/health`: Returns service health, uptime, and connected databases.
  * `/api/v1/transactions`: Handles payment authorization. Automatically flags transactions over $50,000 for fraud review.
  * `/api/v1/metrics`: Exports Prometheus performance metrics (requests per second, latency).
* **[`app/tests/test_payment_api.py`](app/tests/test_payment_api.py)**: Automated unit tests using **PyTest**. It verifies that healthy payments pass, fraudulent ones get flagged, and bad inputs return error 400.
* **[`app/requirements.txt`](app/requirements.txt)**: Lists dependencies (`flask`, `pytest`, `redis`, `prometheus_client`, `gunicorn`).

---

### 🔹 Layer 2: Secure Containerization (`Dockerfile`)
* **[`app/Dockerfile`](app/Dockerfile)**:
  * **Multi-Stage Build**: Keeps the image small (~120 MB) by separating the build tools from the final image.
  * **Non-Root User (`UID 10001 - payshield`)**: In financial apps, running containers as `root` is a security violation. PayShield creates a dedicated non-root user.
  * **Gunicorn WSGI**: Runs 3 concurrent worker processes to handle production traffic.

---

### 🔹 Layer 3: Infrastructure as Code (`terraform/`)
Instead of manually creating AWS resources in the AWS Web Console, **Terraform** provisions them automatically with code.
* **[`terraform/main.tf`](terraform/main.tf)**:
  * **AWS VPC**: Creates an isolated virtual private network (`10.0.0.0/16`).
  * **Public Subnets**: Spans two Availability Zones (`us-east-1a` & `us-east-1b`) for high availability.
  * **Security Groups**: Firewall rules allowing HTTPS (port 443), Payment API (port 30080), and internal Prometheus scraping (port 9090).
* **[`terraform/variables.tf`](terraform/variables.tf)** & **[`outputs.tf`](terraform/outputs.tf)**: Parameterizes region, environment, and exports VPC/Subnet IDs.

---

### 🔹 Layer 4: Configuration Management (`ansible/`)
**Ansible** connects via SSH to target servers to configure them and deploy containers automatically.
* **[`ansible/inventory.ini`](ansible/inventory.ini)**: An address book listing the server IP addresses (Jenkins server, Docker hosts, Kubernetes nodes).
* **[`ansible/deploy-payment-gateway.yml`](ansible/deploy-payment-gateway.yml)**: The automation script (playbook). It logs into target servers, pulls the latest `he99codes/payshield-payment-api` image, restarts the container cleanly, and waits for `/api/v1/health` to return 200 OK.

---

### 🔹 Layer 5: Cloud-Native Orchestration (`kubernetes/`)
Kubernetes manages our containers at scale, auto-heals crashed pods, and balances traffic.
* **[`01-namespace.yaml`](kubernetes/01-namespace.yaml)**: Isolates the project into `payshield-production`.
* **[`02-configmap-secrets.yaml`](kubernetes/02-configmap-secrets.yaml)**: Separates non-sensitive configurations (`APP_ENV=production`) from encrypted secrets (`DATABASE_URL`, `JWT_SECRET`).
* **[`03-deployment.yaml`](kubernetes/03-deployment.yaml)**: Runs **3 identical Pod replicas** with CPU/Memory limits, liveness probes, and readiness probes.
* **[`04-service.yaml`](kubernetes/04-service.yaml)**: Exposes the pods via a **NodePort (30080)** and prepares an AWS **Network Load Balancer (NLB)** on port 443.
* **[`05-hpa.yaml`](kubernetes/05-hpa.yaml)**: **Horizontal Pod Autoscaler**. If CPU usage exceeds 75%, it automatically scales up from 3 pods up to 10 pods.
* **[`06-blue-green-cutover.yaml`](kubernetes/06-blue-green-cutover.yaml)**: Runs Blue (old version) and Green (new version) side-by-side. Traffic switches instantly to Green with zero downtime using `kubectl patch service`.

---

### 🔹 Layer 6: Continuous Integration & Delivery (`jenkins/`)
* **[`jenkins/Jenkinsfile`](jenkins/Jenkinsfile)**: A Declarative Pipeline that automates the whole lifecycle whenever code is pushed:
  1. **Checkout**: Pulls latest code from `he99codes/payshield-devops`.
  2. **Lint & Security**: Runs syntax check and security scan.
  3. **Unit Tests**: Runs PyTest suite (all 6 tests must pass).
  4. **Quality Gate**: Stops the build if tests fail.
  5. **Docker Build**: Builds and packages the container.
  6. **Registry Push**: Pushes image to DockerHub (`he99codes/payshield-payment-api`).
  7. **Ansible Orchestration**: Configures edge Docker hosts.
  8. **Kubernetes Rollout**: Updates the K8s deployment and verifies pods are healthy.

---

### 🔹 Layer 7: Interactive Showcase & Live Hosting
* **[`index.html`](index.html)** & **[`showcase/index.html`](showcase/index.html)**:
  * **Pipeline Simulator**: Visitors click "Trigger Production Deployment" to watch live streaming console logs of the build and deploy steps.
  * **Payment Sandbox**: Interactive form to authorize payments and test fraud detection in real-time.
  * **Architecture Visualizer**: Clickable flow diagram of the entire platform.
* **[`netlify.toml`](netlify.toml)**: Enables 1-click deployment on Netlify.
* **[`docker-compose.yml`](docker-compose.yml)**: Spins up the Payment API (port 5000), Redis (port 6379), and the Showcase (port 8080) with one command: `docker compose up -d`.

---

## 3. Quick Summary Table for Interviews

| Tool / Technology | Role in PayShield | Why it was chosen |
|:---|:---|:---|
| **Python Flask + Gunicorn** | Core Payment Gateway API | Lightweight, fast execution, built-in Prometheus metrics |
| **PyTest** | Automated Testing | Catches bugs and regressions before code is containerized |
| **Docker (Multi-Stage)** | Container packaging | Creates lightweight, non-root, PCI-compliant images |
| **Terraform** | Cloud Infrastructure (AWS) | Automates VPC, Subnets, and Security Groups reproducibly |
| **Ansible** | Configuration Management | Agentless node setup and container deployment via SSH |
| **Kubernetes (K8s)** | Container Orchestration | Self-healing, auto-scaling (HPA), zero-downtime rolling updates |
| **Blue-Green Strategy** | Zero-downtime releases | Instant cutover and instantaneous rollback if an issue occurs |
| **Prometheus & Grafana** | Observability & Metrics | Real-time monitoring of TPS, latency, and system health |
| **Netlify & GitHub Pages** | Public Showcase Hosting | Free, high-speed CDN hosting for live demonstration |

---

## 4. Cheat Sheet: 3-Minute Interview Pitch

> *"In my PayShield project, I designed an enterprise-grade FinTech DevOps pipeline for a high-availability payment gateway. I containerized the API using hardened, non-root Docker images to comply with PCI-DSS standards. I used Terraform to provision an isolated multi-AZ AWS VPC network, Ansible to automate server configuration, and Kubernetes to orchestrate the services with Horizontal Pod Autoscaling and Blue-Green zero-downtime deployments. The entire release cycle is automated using a Jenkins declarative pipeline that runs PyTest unit tests, scans for vulnerabilities, pushes signed artifacts to DockerHub, and completes rollout verification in under 60 seconds."*
