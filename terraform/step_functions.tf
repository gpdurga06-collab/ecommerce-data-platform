resource "aws_sfn_state_machine" "pipeline" {
  name     = "${var.project_name}-${var.environment}-pipeline"
  role_arn = aws_iam_role.step_function_role.arn

  definition = jsonencode({
    Comment = "E-commerce data pipeline"
    StartAt = "StartCrawler"
    States = {
      
      StartCrawler = {
      Type     = "Task"
      Resource = "arn:aws:states:::aws-sdk:glue:startCrawler"
      Parameters = {
      Name = aws_glue_crawler.glue_crawler.name
  }
      Next = "RunGlueJob"
      Catch = [        
    {
      ErrorEquals = ["Glue.CrawlerRunningException"]
      Next        = "RunGlueJob"
    }
  ]
}
      RunGlueJob = {
      Type     = "Task"
      Resource = "arn:aws:states:::glue:startJobRun.sync"
      Parameters = {
        JobName = aws_glue_job.glue_job.name
      }
      Next = "RunEMR"  
    }
    RunEMR = {
      Type     = "Task"
      Resource = "arn:aws:states:::elasticmapreduce:addStep.sync"
      Parameters = {
        ClusterId = aws_emr_cluster.emr_cluster.id
        Step = {
          Name = "BusinessLogic"
          ActionOnFailure = "CONTINUE"
          HadoopJarStep = {
            Jar = "command-runner.jar"
            Args = [
              "spark-submit",
              "--deploy-mode", "cluster",
              "s3://ecommerce-data-platform-dev-raw/scripts/business_logic_emr.py"
            ]
          }
        }
      }
      End = true
    }
  }
})

  tags = {
    Name        = "${var.project_name}-${var.environment}-pipeline"
    Environment = var.environment
    Project     = var.project_name
  }
}