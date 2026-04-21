# CloudWatch Dashboard for E-Commerce Data Platform
# Monitors Lambda, Step Functions, Glue and S3

resource "aws_cloudwatch_dashboard" "ecommerce_dashboard" {
  dashboard_name = "${var.project_name}-${var.environment}-dashboard"

  dashboard_body = jsonencode({
    widgets = [
      # ── Lambda Monitoring ──
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 8
        height = 6
        properties = {
          title  = "Lambda Invocations"
          metrics = [
            ["AWS/Lambda", "Invocations",
             "FunctionName",
             "${var.project_name}-${var.environment}-lambda"]
          ]
          period = 300
          stat   = "Sum"
          region = "us-east-2"
        }
      },
      {
        type   = "metric"
        x      = 8
        y      = 0
        width  = 8
        height = 6
        properties = {
          title  = "Lambda Errors"
          metrics = [
            ["AWS/Lambda", "Errors",
             "FunctionName",
             "${var.project_name}-${var.environment}-lambda"]
          ]
          period = 300
          stat   = "Sum"
          region = "us-east-2"
        }
      },
      {
        type   = "metric"
        x      = 16
        y      = 0
        width  = 8
        height = 6
        properties = {
          title  = "Lambda Duration (ms)"
          metrics = [
            ["AWS/Lambda", "Duration",
             "FunctionName",
             "${var.project_name}-${var.environment}-lambda"]
          ]
          period = 300
          stat   = "Average"
          region = "us-east-2"
        }
      },

      # ── Step Functions Monitoring ──
      {
        type   = "metric"
        x      = 0
        y      = 6
        width  = 8
        height = 6
        properties = {
          title  = "Step Functions Executions Started"
          metrics = [
            ["AWS/States", "ExecutionsStarted",
             "StateMachineArn",
             aws_sfn_state_machine.pipeline.arn]
          ]
          period = 300
          stat   = "Sum"
          region = "us-east-2"
        }
      },
      {
        type   = "metric"
        x      = 8
        y      = 6
        width  = 8
        height = 6
        properties = {
          title  = "Step Functions Executions Failed"
          metrics = [
            ["AWS/States", "ExecutionsFailed",
             "StateMachineArn",
             aws_sfn_state_machine.pipeline.arn]
          ]
          period = 300
          stat   = "Sum"
          region = "us-east-2"
        }
      },
      {
        type   = "metric"
        x      = 16
        y      = 6
        width  = 8
        height = 6
        properties = {
          title  = "Step Functions Executions Succeeded"
          metrics = [
            ["AWS/States", "ExecutionsSucceeded",
             "StateMachineArn",
             aws_sfn_state_machine.pipeline.arn]
          ]
          period = 300
          stat   = "Sum"
          region = "us-east-2"
        }
      },

      # ── Glue Monitoring ──
      {
        type   = "metric"
        x      = 0
        y      = 12
        width  = 8
        height = 6
        properties = {
          title  = "Glue Job Duration"
          metrics = [
            ["AWS/Glue", "glue.driver.aggregate.elapsedTime",
             "JobName",
             "${var.project_name}-${var.environment}-glue-job"]
          ]
          period = 300
          stat   = "Average"
          region = "us-east-2"
        }
      },

      # ── S3 Monitoring ──
      {
        type   = "metric"
        x      = 8
        y      = 12
        width  = 8
        height = 6
        properties = {
          title  = "S3 Raw Bucket Size"
          metrics = [
            ["AWS/S3", "BucketSizeBytes",
             "BucketName",
             "${var.project_name}-${var.environment}-raw",
             "StorageType", "StandardStorage"]
          ]
          period = 86400
          stat   = "Average"
          region = "us-east-2"
        }
      },
      {
        type   = "metric"
        x      = 16
        y      = 12
        width  = 8
        height = 6
        properties = {
          title  = "S3 Number of Objects"
          metrics = [
            ["AWS/S3", "NumberOfObjects",
             "BucketName",
             "${var.project_name}-${var.environment}-raw",
             "StorageType", "AllStorageTypes"]
          ]
          period = 86400
          stat   = "Average"
          region = "us-east-2"
        }
      }
    ]
  })
}

# ── CloudWatch Alarms ──

# Alert when Lambda errors > 5
resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "${var.project_name}-${var.environment}-lambda-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  alarm_description   = "Lambda errors exceeded 5 in 5 minutes!"

  dimensions = {
    FunctionName = "${var.project_name}-${var.environment}-lambda"
  }
}

# Alert when Step Functions fail
resource "aws_cloudwatch_metric_alarm" "step_functions_failed" {
  alarm_name          = "${var.project_name}-${var.environment}-pipeline-failed"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "ExecutionsFailed"
  namespace           = "AWS/States"
  period              = 300
  statistic           = "Sum"
  threshold           = 0
  alarm_description   = "Pipeline execution failed!"

  dimensions = {
    StateMachineArn = aws_sfn_state_machine.pipeline.arn
  }
}