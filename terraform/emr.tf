# EMR Cluster
# Creates an EMR cluster with Spark to process
# millions of records from S3

resource "aws_emr_cluster" "emr_cluster" {
  name          = "${var.project_name}-${var.environment}-emr-cluster"
  release_label = "emr-6.13.0"
  applications  = ["Spark", "Hadoop"]
  service_role  = aws_iam_role.emr_role.arn

  termination_protection            = false
  keep_job_flow_alive_when_no_steps = false

  ec2_attributes {
    instance_profile = aws_iam_instance_profile.emr_instance_profile.arn
  }

  master_instance_group {
    instance_type = "m5.xlarge"
  }

  core_instance_group {
    instance_type  = "m5.xlarge"
    instance_count = 2

    ebs_config {
      size                 = "40"
      type                 = "gp2"
      volumes_per_instance = 1
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-emr-cluster"
    Environment = var.environment
    Project     = var.project_name
  }
}