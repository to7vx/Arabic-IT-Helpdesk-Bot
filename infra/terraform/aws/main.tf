terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.60" }
  }
}

provider "aws" {
  region = var.region
  default_tags { tags = var.tags }
}

# -----------------------------------------------------------------------------
# Phase 7 scaffold. Resources land in Phase 7b. The variable surface and
# module wiring are stable enough that downstream module composition can
# proceed against this signature today.
# -----------------------------------------------------------------------------

data "aws_availability_zones" "available" {
  state = "available"
}

output "region" { value = var.region }
output "name" { value = var.name }
output "domain_name" { value = var.domain_name }
