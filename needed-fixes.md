# Remaining Review

The items below are the ones still left to fix or enhance after the changes already made.

## Provider And Module Compatibility

| Module Name | File path | Declared version | Expected to fail Due |
| --- | --- | --- | --- |
| AWS provider constraint | `modules/sgp-deployment/main.tf` | `>= 4.47` | Too wide. It allows AWS provider `6.x`, which is incompatible with the current VPC module line used in this repo. |
| `terraform-aws-modules/vpc/aws` | `modules/aws-base/vpc.tf` | `3.19.0` | This is the direct compatibility blocker. This module line still uses old AWS arguments removed from newer providers. |
| `terraform-aws-modules/eks/aws` | `modules/aws-base/eks.tf` | `~> 19.1` | Not the first blocker by itself. It is older, but it is not what currently breaks validation first. |
| `terraform-aws-modules/eks/aws//modules/eks-managed-node-group` | `modules/aws-base/eks.tf` | `~> 19.0` | Not the first blocker by itself. It follows the older EKS 19.x module line. |
| `terraform-aws-modules/eks/aws//modules/karpenter` | `modules/aws-base/iam.tf` | `19.21.0` | Not the first blocker by itself. It is tied to the same older EKS module family. |
| `terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks` | `modules/aws-base/iam.tf` | `5.16.0` | Not the current validation blocker. |
| `terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks` | `modules/frontend/iam.tf` | `5.16.0` | Not the current validation blocker. |
| `terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks` | `modules/backend/iam.tf` | `5.16.0` | Not the current validation blocker. |

## Suggested Exact Version Changes

### Minimal compatibility path

Make the smallest version changes first:

- In `modules/sgp-deployment/main.tf`, add:
  - `required_version = ">= 1.0"`
- In `modules/sgp-deployment/main.tf`, change the AWS provider constraint from:
  - `version = ">= 4.47"`
  - to `version = ">= 4.57, < 5.0"`
- Re-run `terraform init -upgrade` so both lock files resolve AWS provider to:
  - `hashicorp/aws = 4.67.0`

Keep these module versions unchanged for the minimal path:

- `terraform-aws-modules/vpc/aws = "3.19.0"`
- `terraform-aws-modules/eks/aws = "~> 19.1"`
- `terraform-aws-modules/eks/aws//modules/eks-managed-node-group = "~> 19.0"`
- `terraform-aws-modules/eks/aws//modules/karpenter = "19.21.0"`
- `terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks = "5.16.0"`

### If you want newer AWS provider lines

If you want AWS provider `5.x` or `6.x`, do not treat that as a provider-only bump. That should be a broader module upgrade, starting with the VPC module line and then re-validating the EKS-related module versions together.

- Add `required_version` to `modules/sgp-deployment/main.tf`.

## Reference Links

- AWS EKS supported Kubernetes versions: https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html
- AWS EKS cluster upgrade rules: https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html

