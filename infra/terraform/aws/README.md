# AWS Terraform module

Provisions:

* ECS Fargate cluster running the `api`, `worker`, and `web` images from
  ghcr.io.
* RDS PostgreSQL 16 single-AZ for dev / multi-AZ for prod (toggle).
* ElastiCache Redis (single-node dev / cluster-mode prod).
* S3 bucket for attachments (replacement for MinIO).
* Application Load Balancer with ACM-issued cert and WAF rules.
* CloudWatch log group with PDPL-mindful retention default of 30 days.

> **Status:** scaffold only. Variables and skeleton are committed; full
> module implementation lands in Phase 7b. Until then, use the
> docker-compose.prod.yml workflow or the Helm chart on a managed
> Kubernetes cluster (EKS).
