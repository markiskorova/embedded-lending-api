# Embedded Lending API — AWS Infrastructure Plan

This document outlines a high-level, production-ready AWS architecture for the Embedded Lending API. It aligns with a Python/Django + DRF + Postgres stack, containerized with Docker, deployed on ECS Fargate, provisioned via Terraform, and built/released via GitHub Actions.

---

## 1) Architecture Overview (High-Level)

```
Users
  │
  ▼
Route 53 (DNS)
  │
  ├─► CloudFront (optional, for SPA/static)
  │      └─► S3 (SPA assets)
  │
  └─► ALB (ACM TLS, HTTP/HTTPS)
          │
          └─► ECS (Fargate) Service/Tasks  ◄─── ECR (images)
                    │
                    └─► RDS (PostgreSQL)
                    │
                    └─► Prometheus + Grafana (optional, as ECS tasks)
                    
VPC (2–3 AZs): public subnets (ALB), private subnets (ECS/RDS)
Security Groups: ALB → ECS, ECS → RDS
Secrets Manager for DB creds/JWT; IAM + KMS for encryption
CloudWatch (logs/metrics/alarms); CloudTrail/Config optional
WAF optional (in front of ALB)
```

---

## 2) Core Runtime

- **ECS on Fargate (private subnets):** Runs the Django/DRF API container(s).
- **RDS PostgreSQL (multi‑AZ):** Production database with automated backups and encryption at rest.
- **Application Load Balancer (public subnets):** TLS termination via **ACM**; routes traffic to ECS tasks.
- **ECR:** Stores built Docker images for deployments.

---

## 3) Networking, Security, and Configuration

- **VPC** spanning 2–3 Availability Zones with:
  - Public subnets: **ALB**
  - Private subnets: **ECS tasks** and **RDS**
- **Security Groups:**
  - **ALB → ECS:** allow HTTP/HTTPS from ALB to ECS service
  - **ECS → RDS:** allow Postgres from ECS tasks to DB
- **Route 53:** Public DNS for the API domain.
- **Secrets Manager:** Stores DB credentials, JWT secrets, 3rd‑party tokens.
- **IAM & KMS:** IAM roles for ECS tasks; KMS for RDS/secrets/S3 encryption.
- **WAF (optional):** Managed rules in front of the ALB.

---

## 4) CI/CD and Infrastructure‑as‑Code

- **GitHub Actions** (or CodePipeline/CodeBuild) for:
  - Build → Test → Docker **build/push** to **ECR**
  - Deploy step to update **ECS service** (rolling/blue‑green)
- **Terraform (or AWS CDK/CloudFormation)** to provision:
  - **VPC**, **Subnets**, **NAT/IGW**, **Route tables**
  - **ALB**, **Target groups**, **Listeners**
  - **ECS Cluster/Service/Task Definitions**
  - **ECR Repositories**
  - **RDS Postgres**
  - **IAM Roles/Policies**
  - **Security Groups**
  - **Route 53**, **ACM certs**

### Suggested Terraform Module Layout

```
infra/
├─ envs/
│  ├─ dev/
│  └─ prod/
├─ modules/
│  ├─ vpc/
│  ├─ alb/
│  ├─ ecs_service/
│  ├─ ecr/
│  ├─ rds/
│  ├─ iam/
│  └─ route53_acm/
└─ main.tf
```

### GitHub Actions (Skeleton)

```yaml
name: ci-cd

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install deps & run tests
        run: |
          pip install -r requirements.txt
          pytest -q

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-west-2

      - name: Login to ECR
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build and push image
        run: |
          IMAGE_TAG=${{ github.sha }}
          ECR_URI=${{ secrets.ECR_URI }}
          docker build -t $ECR_URI:$IMAGE_TAG .
          docker push $ECR_URI:$IMAGE_TAG

      - name: Update ECS service
        uses: aws-actions/amazon-ecs-deploy-task-definition@v2
        with:
          task-definition: ecs/task-def.json
          service: embedded-lending-api
          cluster: embedded-lending-cluster
          wait-for-service-stability: true
```

> Swap in CodePipeline/CodeBuild if you prefer fully-managed AWS CI/CD.

---

## 5) Observability

- **CloudWatch** Logs/Metrics/Alarms for ECS tasks, ALB, and RDS.
- **(Optional) Prometheus + Grafana**:
  - Run as sidecar or separate ECS services for app-specific metrics.
  - Useful dashboards: API latency, DB connections, task health, error rates.

---

## 6) Optional Components (Phase‑as‑You‑Grow)

- **ElastiCache (Redis):** If enabling **Celery** for background jobs (underwriting, repayment scheduling).
- **CloudTrail & Config:** Audit/API event logging and config drift monitoring.
- **CloudFront + S3 (SPA):** If a separate admin UI/dashboard is added later.

---

## 7) Rollout Strategy

1. **Dev/Stage Environment:** Stand up the full stack with small instance sizes.
2. **Smoke Tests & Load Tests:** Validate ALB routing, ECS task health checks, DB connections, and failover.
3. **Prod Cutover:** Use DNS switch via Route 53 after canary/blue‑green deploy.
4. **Cost/Posture Review:** Scale Fargate tasks, RDS class/storage, and alarms per usage.

---

## 8) Rationale

- **Managed services (Fargate, RDS, ACM):** Reduce ops overhead, improve security posture.
- **Separation of concerns:** Public ALB, private compute/data subnets.
- **Scalability:** ECS services and RDS tiers scale independently.
- **Security:** IAM/KMS/Secrets Manager + SG boundaries; WAF optional.
- **Repeatability:** Terraform modules + CI/CD pipelines keep infra reproducible.
