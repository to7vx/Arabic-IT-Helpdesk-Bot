variable "region" {
  description = "AWS region (e.g. me-south-1 for Bahrain to keep data in-Kingdom-adjacent)"
  type        = string
  default     = "me-south-1"
}

variable "name" {
  description = "Resource name prefix"
  type        = string
  default     = "arabic-helpdesk"
}

variable "image_tag" {
  description = "Image tag to deploy"
  type        = string
  default     = "0.1.0"
}

variable "domain_name" {
  description = "FQDN for the ALB (e.g. helpdesk.example.com)"
  type        = string
}

variable "db_multi_az" {
  description = "Use multi-AZ RDS in this environment"
  type        = bool
  default     = false
}

variable "tags" {
  description = "Common tags applied to all resources"
  type        = map(string)
  default = {
    Project = "arabic-helpdesk"
    ManagedBy = "terraform"
  }
}
