# aws_codebuild_codedeploy_nodeJs_demo
This repository contains sample codes to work with AWS 

This Project build_script directory contains build related script, check buildspec.yml file I have integrated the same. 

Deployment related scripts are in deployment_scripts directory, check appspec.yml file. 


This is a node.js project same, but change config as per your project requirement 


In codebuild.yml file in post build phase, line:
      - aws deploy push --application-name "${CODE_DEPLOY_APPLICATION_NAME}" --s3-location "s3://${CODE_DEPLOY_S3_BUCKET}/codedeploydemo/app.zip" --ignore-hidden-files --region us-west-2

You can enavironment variable in code build : CODE_DEPLOY_APPLICATION_NAME, CODE_DEPLOY_S3_BUCKET and the value will reflect in the command. 

Check Previous Videos to make sense of this implementation:



Keep learning , Keep improving 


aws deploy push --application-name "${CODE_DEPLOY_APPLICATION_NAME}" --s3-location "s3://${CODE_DEPLOY_S3_BUCKET}/codedeploydemo/app.zip" --ignore-hidden-files --region us-west-2


Data that need to be set up in user data while launching instance in order to install code deploy agent in ec2 instance on boot

#!/bin/bash
sudo apt-get update -y 
sudo apt-get install ruby -y
sudo apt-get install wget -y

cd /home/ubuntu

wget https://aws-codedeploy-us-west-2.s3.us-west-2.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto


node-app-youtube-demo


aws deploy push --application-name NodeAppServerDeployment --s3-location "s3://node-app-youtube-demo/codedeploydemo/app.zip" --ignore-hidden-files 

===================================================================


Codecommit-CICD-cnf.yml

A CodeBuild and CodePipeline template for Containerized Application
This template creates a custom CodePipeline pipeline for continuous integration and continuous delivery, for two environments named staging and production.

Steps
Retrieve source: fetches the latest version of a branch from a CodeCommit repository.
Build staging: builds the project using CodeBuild by executing the buildspec.yml file.
Deploy staging: deploys the output of step 2 using CodeBuild by executing the deployspec.yml file.
Manual approval.
Build production: builds the project using CodeBuild by executing the buildspec.yml file.
Deploy production: deploys the output of step 5 using CodeBuild by executing the deployspec.yml file.
CodeCommit repository
You need to create the CodeCommit repository before creating the stack, in the same AWS region as where you are creating the pipeline. The repository name is given as a parameter to the stack.

Environment variable
In steps 2 and 3 an ENVIRONMENT=staging variable will be set, while for steps 5 and 6 that will be ENVIRONMENT=production. This means that you can customize buildspec.yml and deployspec.yml files to behave differently between environments.

if [ "${ENVIRONMENT}" = "production" ]; then
  # Build/deploy for production
else
  # Build/deploy for staging
fi
Both buildspec.yml and deployspec.yml files are run in CodeBuild projects. Read this page for more information about the syntax to use.

Important note: in steps 2 and 5 you need to add deployspec.yml in artifacts.files section of the buildspec.yml among other output files in order for deployments to function.

artifacts:
  files:
    - ....
    - deployspec.yml
CodeBuild role
If you need to perofm an action in your build or deployment phase which requires particular permissions you can add a policy to the IAM role used by the CodeBuild projects. The role ARN is exported with this name: ${AWS::StackName}CodeBuildRoleArn.
