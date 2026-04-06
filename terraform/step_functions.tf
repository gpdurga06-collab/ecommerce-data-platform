resource "aws_sfn_state_machine" "pipeline" {
  name     = "${var.project_name}-${var.environment}-pipeline"
  role_arn = aws_iam_role.step_function_role.arn

  definition = jsonencode({
    Comment = "E-commerce data pipeline"
    StartAt = "ValidateData"
    States = {
      ValidateData = {
        Type     = "Task"
        Resource = aws_lambda_function.lambda_function.arn
        Next     = "StartCrawler"
      }
      StartCrawler = {
        Type     = "Task"
        Resource = "arn:aws:states:::aws-sdk:glue:startCrawler"
        Next     = "RunGlueJob"
      }
      RunGlueJob = {
        Type     = "Task"
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        End      = true
      }
    }
  })

  tags = {
    Name        = "${var.project_name}-${var.environment}-pipeline"
    Environment = var.environment
    Project     = var.project_name
  }
}
