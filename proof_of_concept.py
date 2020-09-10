#!/usr/bin/env python3
# The template for this was taken from the url below
# http://docs.aws.amazon.com/general/latest/gr/sigv4_signing.html
import sys, os, base64, datetime, hashlib, hmac
import requests # pip install requests

# Didn't work? Set your AWS environment variables to a valid role

services = {
  "application-autoscaling:application-autoscaling": [
    "AnyScaleFrontendService.DeleteScalingPolicy",
    "AnyScaleFrontendService.DeleteScheduledAction",
    "AnyScaleFrontendService.DeregisterScalableTarget",
    "AnyScaleFrontendService.DescribeScalableTargets",
    "AnyScaleFrontendService.DescribeScalingActivities",
    "AnyScaleFrontendService.DescribeScalingPolicies",
    "AnyScaleFrontendService.DescribeScheduledActions",
    "AnyScaleFrontendService.PutScalingPolicy",
    "AnyScaleFrontendService.PutScheduledAction"
  ],
  "appstream:appstream2": [
    "PhotonAdminProxyService.CreateDirectoryConfig",
    "PhotonAdminProxyService.CreateUsageReportSubscription",
    "PhotonAdminProxyService.CreateUser",
    "PhotonAdminProxyService.DeleteDirectoryConfig",
    "PhotonAdminProxyService.DeleteUsageReportSubscription",
    "PhotonAdminProxyService.DeleteUser",
    "PhotonAdminProxyService.DescribeDirectoryConfigs",
    "PhotonAdminProxyService.DescribeSessions",
    "PhotonAdminProxyService.DescribeUsageReportSubscriptions",
    "PhotonAdminProxyService.DescribeUserStackAssociations",
    "PhotonAdminProxyService.DescribeUsers",
    "PhotonAdminProxyService.DisableUser",
    "PhotonAdminProxyService.EnableUser",
    "PhotonAdminProxyService.ExpireSession",
    "PhotonAdminProxyService.UpdateDirectoryConfig"
  ],
  "athena:athena": [
    "AmazonAthena.ListDataCatalogs",
    "AmazonAthena.ListWorkGroups"
  ],
  "autoscaling-plans:autoscaling-plans": [
    "AnyScaleScalingPlannerFrontendService.CreateScalingPlan",
    "AnyScaleScalingPlannerFrontendService.DeleteScalingPlan",
    "AnyScaleScalingPlannerFrontendService.DescribeScalingPlanResources",
    "AnyScaleScalingPlannerFrontendService.DescribeScalingPlans",
    "AnyScaleScalingPlannerFrontendService.GetScalingPlanResourceForecastData",
    "AnyScaleScalingPlannerFrontendService.UpdateScalingPlan"
  ],
  "aws-marketplace:entitlement.marketplace": [
    "AWSMPEntitlementService.GetEntitlements"
  ],
  "aws-marketplace:metering.marketplace": [
    "AWSMPMeteringService.BatchMeterUsage",
    "AWSMPMeteringService.MeterUsage",
    "AWSMPMeteringService.RegisterUsage",
    "AWSMPMeteringService.ResolveCustomer"
  ],
  "cloudhsm:cloudhsm": [
    "CloudHsmFrontendService.AddTagsToResource",
    "CloudHsmFrontendService.CreateHapg",
    "CloudHsmFrontendService.CreateHsm",
    "CloudHsmFrontendService.CreateLunaClient",
    "CloudHsmFrontendService.DeleteHapg",
    "CloudHsmFrontendService.DeleteHsm",
    "CloudHsmFrontendService.DeleteLunaClient",
    "CloudHsmFrontendService.DescribeHapg",
    "CloudHsmFrontendService.DescribeHsm",
    "CloudHsmFrontendService.DescribeLunaClient",
    "CloudHsmFrontendService.GetConfig",
    "CloudHsmFrontendService.ListAvailableZones",
    "CloudHsmFrontendService.ListHapgs",
    "CloudHsmFrontendService.ListHsms",
    "CloudHsmFrontendService.ListLunaClients",
    "CloudHsmFrontendService.ListTagsForResource",
    "CloudHsmFrontendService.ModifyHapg",
    "CloudHsmFrontendService.ModifyLunaClient",
    "CloudHsmFrontendService.RemoveTagsFromResource"
  ],
  "cloudhsm:cloudhsmv2": [
    "BaldrApiService.DescribeBackups",
    "BaldrApiService.DescribeClusters"
  ],
  "codecommit:codecommit": [
    "CodeCommit_20150413.CreateApprovalRuleTemplate",
    "CodeCommit_20150413.DeleteApprovalRuleTemplate",
    "CodeCommit_20150413.GetApprovalRuleTemplate",
    "CodeCommit_20150413.ListApprovalRuleTemplates",
    "CodeCommit_20150413.ListRepositories",
    "CodeCommit_20150413.ListRepositoriesForApprovalRuleTemplate",
    "CodeCommit_20150413.UpdateApprovalRuleTemplateContent",
    "CodeCommit_20150413.UpdateApprovalRuleTemplateDescription",
    "CodeCommit_20150413.UpdateApprovalRuleTemplateName"
  ],
  "codepipeline:codepipeline": [
    "CodePipeline_20150709.AcknowledgeJob",
    "CodePipeline_20150709.AcknowledgeThirdPartyJob",
    "CodePipeline_20150709.GetJobDetails",
    "CodePipeline_20150709.GetThirdPartyJobDetails",
    "CodePipeline_20150709.ListActionTypes",
    "CodePipeline_20150709.ListPipelines",
    "CodePipeline_20150709.ListWebhooks",
    "CodePipeline_20150709.PutJobFailureResult",
    "CodePipeline_20150709.PutJobSuccessResult",
    "CodePipeline_20150709.PutThirdPartyJobFailureResult",
    "CodePipeline_20150709.PutThirdPartyJobSuccessResult"
  ],
  "codestar:codestar": [
    "CodeStar_20170419.DescribeUserProfile",
    "CodeStar_20170419.ListProjects",
    "CodeStar_20170419.ListUserProfiles"
  ],
  "comprehend:comprehend": [
    "Comprehend_20171127.BatchDetectDominantLanguage",
    "Comprehend_20171127.BatchDetectEntities",
    "Comprehend_20171127.BatchDetectKeyPhrases",
    "Comprehend_20171127.BatchDetectSentiment",
    "Comprehend_20171127.BatchDetectSyntax",
    "Comprehend_20171127.ClassifyDocument",
    "Comprehend_20171127.CreateDocumentClassifier",
    "Comprehend_20171127.CreateEndpoint",
    "Comprehend_20171127.CreateEntityRecognizer",
    "Comprehend_20171127.DeleteDocumentClassifier",
    "Comprehend_20171127.DeleteEndpoint",
    "Comprehend_20171127.DeleteEntityRecognizer",
    "Comprehend_20171127.DescribeDocumentClassificationJob",
    "Comprehend_20171127.DescribeDocumentClassifier",
    "Comprehend_20171127.DescribeDominantLanguageDetectionJob",
    "Comprehend_20171127.DescribeEndpoint",
    "Comprehend_20171127.DescribeEntitiesDetectionJob",
    "Comprehend_20171127.DescribeEntityRecognizer",
    "Comprehend_20171127.DescribeKeyPhrasesDetectionJob",
    "Comprehend_20171127.DescribeSentimentDetectionJob",
    "Comprehend_20171127.DescribeTopicsDetectionJob",
    "Comprehend_20171127.DetectDominantLanguage",
    "Comprehend_20171127.DetectEntities",
    "Comprehend_20171127.DetectKeyPhrases",
    "Comprehend_20171127.DetectSentiment",
    "Comprehend_20171127.DetectSyntax",
    "Comprehend_20171127.ListDocumentClassificationJobs",
    "Comprehend_20171127.ListDocumentClassifiers",
    "Comprehend_20171127.ListDominantLanguageDetectionJobs",
    "Comprehend_20171127.ListEndpoints",
    "Comprehend_20171127.ListEntitiesDetectionJobs",
    "Comprehend_20171127.ListEntityRecognizers",
    "Comprehend_20171127.ListKeyPhrasesDetectionJobs",
    "Comprehend_20171127.ListSentimentDetectionJobs",
    "Comprehend_20171127.ListTagsForResource",
    "Comprehend_20171127.ListTopicsDetectionJobs",
    "Comprehend_20171127.StartDocumentClassificationJob",
    "Comprehend_20171127.StartDominantLanguageDetectionJob",
    "Comprehend_20171127.StartEntitiesDetectionJob",
    "Comprehend_20171127.StartKeyPhrasesDetectionJob",
    "Comprehend_20171127.StartSentimentDetectionJob",
    "Comprehend_20171127.StartTopicsDetectionJob",
    "Comprehend_20171127.StopDominantLanguageDetectionJob",
    "Comprehend_20171127.StopEntitiesDetectionJob",
    "Comprehend_20171127.StopKeyPhrasesDetectionJob",
    "Comprehend_20171127.StopSentimentDetectionJob",
    "Comprehend_20171127.StopTrainingDocumentClassifier",
    "Comprehend_20171127.StopTrainingEntityRecognizer",
    "Comprehend_20171127.TagResource",
    "Comprehend_20171127.UntagResource",
    "Comprehend_20171127.UpdateEndpoint"
  ],
  "cur:cur": [
    "AWSOrigamiServiceGatewayService.DescribeReportDefinitions"
  ],
  "datapipeline:datapipeline": [
    "DataPipeline.ActivatePipeline",
    "DataPipeline.AddTags",
    "DataPipeline.CreatePipeline",
    "DataPipeline.DeactivatePipeline",
    "DataPipeline.DeletePipeline",
    "DataPipeline.DescribeObjects",
    "DataPipeline.DescribePipelines",
    "DataPipeline.EvaluateExpression",
    "DataPipeline.GetPipelineDefinition",
    "DataPipeline.ListPipelines",
    "DataPipeline.PollForTask",
    "DataPipeline.PutPipelineDefinition",
    "DataPipeline.QueryObjects",
    "DataPipeline.RemoveTags",
    "DataPipeline.ReportTaskProgress",
    "DataPipeline.ReportTaskRunnerHeartbeat",
    "DataPipeline.SetStatus",
    "DataPipeline.SetTaskStatus",
    "DataPipeline.ValidatePipelineDefinition"
  ],
  "dax:dax": [
    "AmazonDAXV3.CreateCluster",
    "AmazonDAXV3.CreateParameterGroup",
    "AmazonDAXV3.CreateSubnetGroup",
    "AmazonDAXV3.DecreaseReplicationFactor",
    "AmazonDAXV3.DeleteCluster",
    "AmazonDAXV3.DeleteParameterGroup",
    "AmazonDAXV3.DeleteSubnetGroup",
    "AmazonDAXV3.DescribeClusters",
    "AmazonDAXV3.DescribeDefaultParameters",
    "AmazonDAXV3.DescribeEvents",
    "AmazonDAXV3.DescribeParameterGroups",
    "AmazonDAXV3.DescribeParameters",
    "AmazonDAXV3.DescribeSubnetGroups",
    "AmazonDAXV3.IncreaseReplicationFactor",
    "AmazonDAXV3.ListTags",
    "AmazonDAXV3.RebootNode",
    "AmazonDAXV3.TagResource",
    "AmazonDAXV3.UntagResource",
    "AmazonDAXV3.UpdateCluster",
    "AmazonDAXV3.UpdateParameterGroup",
    "AmazonDAXV3.UpdateSubnetGroup"
  ],
  "directconnect:directconnect": [
    "OvertureService.AcceptDirectConnectGatewayAssociationProposal",
    "OvertureService.AllocateConnectionOnInterconnect",
    "OvertureService.AllocateHostedConnection",
    "OvertureService.AllocatePrivateVirtualInterface",
    "OvertureService.AllocatePublicVirtualInterface",
    "OvertureService.AllocateTransitVirtualInterface",
    "OvertureService.AssociateConnectionWithLag",
    "OvertureService.AssociateHostedConnection",
    "OvertureService.AssociateVirtualInterface",
    "OvertureService.ConfirmConnection",
    "OvertureService.ConfirmPrivateVirtualInterface",
    "OvertureService.ConfirmPublicVirtualInterface",
    "OvertureService.ConfirmTransitVirtualInterface",
    "OvertureService.CreateBGPPeer",
    "OvertureService.CreateConnection",
    "OvertureService.CreateDirectConnectGateway",
    "OvertureService.CreateDirectConnectGatewayAssociation",
    "OvertureService.CreateDirectConnectGatewayAssociationProposal",
    "OvertureService.CreateInterconnect",
    "OvertureService.CreateLag",
    "OvertureService.CreatePrivateVirtualInterface",
    "OvertureService.CreatePublicVirtualInterface",
    "OvertureService.CreateTransitVirtualInterface",
    "OvertureService.DeleteBGPPeer",
    "OvertureService.DeleteConnection",
    "OvertureService.DeleteDirectConnectGateway",
    "OvertureService.DeleteDirectConnectGatewayAssociation",
    "OvertureService.DeleteDirectConnectGatewayAssociationProposal",
    "OvertureService.DeleteInterconnect",
    "OvertureService.DeleteLag",
    "OvertureService.DeleteVirtualInterface",
    "OvertureService.DescribeConnectionLoa",
    "OvertureService.DescribeConnections",
    "OvertureService.DescribeConnectionsOnInterconnect",
    "OvertureService.DescribeDirectConnectGatewayAssociationProposals",
    "OvertureService.DescribeDirectConnectGatewayAssociations",
    "OvertureService.DescribeDirectConnectGatewayAttachments",
    "OvertureService.DescribeDirectConnectGateways",
    "OvertureService.DescribeHostedConnections",
    "OvertureService.DescribeInterconnectLoa",
    "OvertureService.DescribeInterconnects",
    "OvertureService.DescribeLags",
    "OvertureService.DescribeLoa",
    "OvertureService.DescribeLocations",
    "OvertureService.DescribeTags",
    "OvertureService.DescribeVirtualGateways",
    "OvertureService.DescribeVirtualInterfaces",
    "OvertureService.DisassociateConnectionFromLag",
    "OvertureService.ListVirtualInterfaceTestHistory",
    "OvertureService.StartBgpFailoverTest",
    "OvertureService.StopBgpFailoverTest",
    "OvertureService.TagResource",
    "OvertureService.UntagResource",
    "OvertureService.UpdateDirectConnectGatewayAssociation",
    "OvertureService.UpdateLag",
    "OvertureService.UpdateVirtualInterfaceAttributes"
  ],
  "discovery:discovery": [
    "AWSPoseidonService_V2015_11_01.AssociateConfigurationItemsToApplication",
    "AWSPoseidonService_V2015_11_01.BatchDeleteImportData",
    "AWSPoseidonService_V2015_11_01.CreateApplication",
    "AWSPoseidonService_V2015_11_01.CreateTags",
    "AWSPoseidonService_V2015_11_01.DeleteApplications",
    "AWSPoseidonService_V2015_11_01.DeleteTags",
    "AWSPoseidonService_V2015_11_01.DescribeAgents",
    "AWSPoseidonService_V2015_11_01.DescribeConfigurations",
    "AWSPoseidonService_V2015_11_01.DescribeContinuousExports",
    "AWSPoseidonService_V2015_11_01.DescribeExportConfigurations",
    "AWSPoseidonService_V2015_11_01.DescribeExportTasks",
    "AWSPoseidonService_V2015_11_01.DescribeImportTasks",
    "AWSPoseidonService_V2015_11_01.DescribeTags",
    "AWSPoseidonService_V2015_11_01.DisassociateConfigurationItemsFromApplication",
    "AWSPoseidonService_V2015_11_01.ExportConfigurations",
    "AWSPoseidonService_V2015_11_01.GetDiscoverySummary",
    "AWSPoseidonService_V2015_11_01.ListConfigurations",
    "AWSPoseidonService_V2015_11_01.ListServerNeighbors",
    "AWSPoseidonService_V2015_11_01.StartContinuousExport",
    "AWSPoseidonService_V2015_11_01.StartDataCollectionByAgentIds",
    "AWSPoseidonService_V2015_11_01.StartExportTask",
    "AWSPoseidonService_V2015_11_01.StartImportTask",
    "AWSPoseidonService_V2015_11_01.StopContinuousExport",
    "AWSPoseidonService_V2015_11_01.StopDataCollectionByAgentIds",
    "AWSPoseidonService_V2015_11_01.UpdateApplication"
  ],
  "forecast:forecast": [
    "AmazonForecast.CreateDataset",
    "AmazonForecast.CreateDatasetGroup",
    "AmazonForecast.CreateDatasetImportJob",
    "AmazonForecast.CreateForecast",
    "AmazonForecast.CreateForecastExportJob",
    "AmazonForecast.CreatePredictor",
    "AmazonForecast.DeleteDataset",
    "AmazonForecast.DeleteDatasetGroup",
    "AmazonForecast.DeleteDatasetImportJob",
    "AmazonForecast.DeleteForecast",
    "AmazonForecast.DeleteForecastExportJob",
    "AmazonForecast.DeletePredictor",
    "AmazonForecast.DescribeDataset",
    "AmazonForecast.DescribeDatasetGroup",
    "AmazonForecast.DescribeDatasetImportJob",
    "AmazonForecast.DescribeForecast",
    "AmazonForecast.DescribeForecastExportJob",
    "AmazonForecast.DescribePredictor",
    "AmazonForecast.GetAccuracyMetrics",
    "AmazonForecast.ListDatasetGroups",
    "AmazonForecast.ListDatasetImportJobs",
    "AmazonForecast.ListDatasets",
    "AmazonForecast.ListForecastExportJobs",
    "AmazonForecast.ListForecasts",
    "AmazonForecast.ListPredictors",
    "AmazonForecast.ListTagsForResource",
    "AmazonForecast.TagResource",
    "AmazonForecast.UntagResource",
    "AmazonForecast.UpdateDatasetGroup"
  ],
  "gamelift:gamelift": [
    "GameLift.AcceptMatch",
    "GameLift.CreateGameSession",
    "GameLift.CreatePlayerSession",
    "GameLift.CreatePlayerSessions",
    "GameLift.CreateVpcPeeringAuthorization",
    "GameLift.CreateVpcPeeringConnection",
    "GameLift.DeleteVpcPeeringAuthorization",
    "GameLift.DeleteVpcPeeringConnection",
    "GameLift.DescribeEC2InstanceLimits",
    "GameLift.DescribeFleetAttributes",
    "GameLift.DescribeFleetCapacity",
    "GameLift.DescribeFleetUtilization",
    "GameLift.DescribeGameSessionDetails",
    "GameLift.DescribeGameSessionPlacement",
    "GameLift.DescribeGameSessionQueues",
    "GameLift.DescribeGameSessions",
    "GameLift.DescribeMatchmaking",
    "GameLift.DescribeMatchmakingConfigurations",
    "GameLift.DescribeMatchmakingRuleSets",
    "GameLift.DescribePlayerSessions",
    "GameLift.DescribeVpcPeeringAuthorizations",
    "GameLift.DescribeVpcPeeringConnections",
    "GameLift.GetGameSessionLogUrl",
    "GameLift.ListAliases",
    "GameLift.ListBuilds",
    "GameLift.ListFleets",
    "GameLift.ListGameServerGroups",
    "GameLift.ListScripts",
    "GameLift.SearchGameSessions",
    "GameLift.StartMatchBackfill",
    "GameLift.StartMatchmaking",
    "GameLift.StopGameSessionPlacement",
    "GameLift.StopMatchmaking",
    "GameLift.UpdateGameSession",
    "GameLift.ValidateMatchmakingRuleSet"
  ],
  "health:health": [
    "AWSHealth_20160804.DescribeAffectedAccountsForOrganization",
    "AWSHealth_20160804.DescribeAffectedEntitiesForOrganization",
    "AWSHealth_20160804.DescribeEntityAggregates",
    "AWSHealth_20160804.DescribeEventAggregates",
    "AWSHealth_20160804.DescribeEventDetailsForOrganization",
    "AWSHealth_20160804.DescribeEventTypes",
    "AWSHealth_20160804.DescribeEvents",
    "AWSHealth_20160804.DescribeEventsForOrganization",
    "AWSHealth_20160804.DescribeHealthServiceStatusForOrganization",
    "AWSHealth_20160804.DisableHealthServiceAccessForOrganization",
    "AWSHealth_20160804.EnableHealthServiceAccessForOrganization"
  ],
  "identitystore:identitystore": [
    "AWSIdentityStore.DescribeGroup",
    "AWSIdentityStore.DescribeUser",
    "AWSIdentityStore.ListGroups",
    "AWSIdentityStore.ListUsers"
  ],
  "kinesis:kinesis": [
    "Kinesis_20131202.ListStreams"
  ],
  "kinesisanalytics:kinesisanalytics": [
    "KinesisAnalytics_20150814.ListApplications",
    "KinesisAnalytics_20180523.ListApplications"
  ],
  "macie:macie": [
    "MacieService.AssociateMemberAccount",
    "MacieService.AssociateS3Resources",
    "MacieService.DisassociateMemberAccount",
    "MacieService.DisassociateS3Resources",
    "MacieService.ListMemberAccounts",
    "MacieService.ListS3Resources",
    "MacieService.UpdateS3Resources"
  ],
  "mediastore:mediastore": [
    "MediaStore_20170901.ListContainers"
  ],
  "mgh:migrationhub-config": [
    "AWSMigrationHubMultiAccountService.CreateHomeRegionControl",
    "AWSMigrationHubMultiAccountService.DescribeHomeRegionControls",
    "AWSMigrationHubMultiAccountService.GetHomeRegion"
  ],
  "mturk-requester:mturk-requester": [
    "MTurkRequesterServiceV20170117.AcceptQualificationRequest",
    "MTurkRequesterServiceV20170117.ApproveAssignment",
    "MTurkRequesterServiceV20170117.AssociateQualificationWithWorker",
    "MTurkRequesterServiceV20170117.CreateAdditionalAssignmentsForHIT",
    "MTurkRequesterServiceV20170117.CreateHIT",
    "MTurkRequesterServiceV20170117.CreateHITType",
    "MTurkRequesterServiceV20170117.CreateHITWithHITType",
    "MTurkRequesterServiceV20170117.CreateQualificationType",
    "MTurkRequesterServiceV20170117.CreateWorkerBlock",
    "MTurkRequesterServiceV20170117.DeleteHIT",
    "MTurkRequesterServiceV20170117.DeleteQualificationType",
    "MTurkRequesterServiceV20170117.DeleteWorkerBlock",
    "MTurkRequesterServiceV20170117.DisassociateQualificationFromWorker",
    "MTurkRequesterServiceV20170117.GetAccountBalance",
    "MTurkRequesterServiceV20170117.GetAssignment",
    "MTurkRequesterServiceV20170117.GetFileUploadURL",
    "MTurkRequesterServiceV20170117.GetHIT",
    "MTurkRequesterServiceV20170117.GetQualificationScore",
    "MTurkRequesterServiceV20170117.GetQualificationType",
    "MTurkRequesterServiceV20170117.ListAssignmentsForHIT",
    "MTurkRequesterServiceV20170117.ListBonusPayments",
    "MTurkRequesterServiceV20170117.ListHITs",
    "MTurkRequesterServiceV20170117.ListHITsForQualificationType",
    "MTurkRequesterServiceV20170117.ListQualificationRequests",
    "MTurkRequesterServiceV20170117.ListQualificationTypes",
    "MTurkRequesterServiceV20170117.ListReviewPolicyResultsForHIT",
    "MTurkRequesterServiceV20170117.ListReviewableHITs",
    "MTurkRequesterServiceV20170117.ListWorkerBlocks",
    "MTurkRequesterServiceV20170117.ListWorkersWithQualificationType",
    "MTurkRequesterServiceV20170117.NotifyWorkers",
    "MTurkRequesterServiceV20170117.RejectAssignment",
    "MTurkRequesterServiceV20170117.RejectQualificationRequest",
    "MTurkRequesterServiceV20170117.SendBonus",
    "MTurkRequesterServiceV20170117.SendTestEventNotification",
    "MTurkRequesterServiceV20170117.UpdateExpirationForHIT",
    "MTurkRequesterServiceV20170117.UpdateHITReviewStatus",
    "MTurkRequesterServiceV20170117.UpdateHITTypeOfHIT",
    "MTurkRequesterServiceV20170117.UpdateNotificationSettings",
    "MTurkRequesterServiceV20170117.UpdateQualificationType"
  ],
  "opsworks-cm:opsworks-cm": [
    "OpsWorksCM_V2016_11_01.DescribeAccountAttributes"
  ],
  "personalize:personalize": [
    "AmazonPersonalize.ListDatasetGroups",
    "AmazonPersonalize.ListRecipes",
    "AmazonPersonalize.ListSchemas"
  ],
  "redshift-data:redshift-data": [
    "RedshiftData.CancelStatement",
    "RedshiftData.DescribeStatement",
    "RedshiftData.GetStatementResult",
    "RedshiftData.ListStatements"
  ],
  "route53domains:route53domains": [
    "Route53Domains_v20140515.AcceptDomainTransferFromAnotherAwsAccount",
    "Route53Domains_v20140515.CancelDomainTransferToAnotherAwsAccount",
    "Route53Domains_v20140515.CheckDomainAvailability",
    "Route53Domains_v20140515.CheckDomainTransferability",
    "Route53Domains_v20140515.DeleteTagsForDomain",
    "Route53Domains_v20140515.DisableDomainAutoRenew",
    "Route53Domains_v20140515.DisableDomainTransferLock",
    "Route53Domains_v20140515.EnableDomainAutoRenew",
    "Route53Domains_v20140515.EnableDomainTransferLock",
    "Route53Domains_v20140515.GetContactReachabilityStatus",
    "Route53Domains_v20140515.GetDomainDetail",
    "Route53Domains_v20140515.GetDomainSuggestions",
    "Route53Domains_v20140515.GetOperationDetail",
    "Route53Domains_v20140515.ListDomains",
    "Route53Domains_v20140515.ListOperations",
    "Route53Domains_v20140515.ListTagsForDomain",
    "Route53Domains_v20140515.RegisterDomain",
    "Route53Domains_v20140515.RejectDomainTransferFromAnotherAwsAccount",
    "Route53Domains_v20140515.RenewDomain",
    "Route53Domains_v20140515.ResendContactReachabilityEmail",
    "Route53Domains_v20140515.RetrieveDomainAuthCode",
    "Route53Domains_v20140515.TransferDomain",
    "Route53Domains_v20140515.TransferDomainToAnotherAwsAccount",
    "Route53Domains_v20140515.UpdateDomainContact",
    "Route53Domains_v20140515.UpdateDomainContactPrivacy",
    "Route53Domains_v20140515.UpdateDomainNameservers",
    "Route53Domains_v20140515.UpdateTagsForDomain",
    "Route53Domains_v20140515.ViewBilling"
  ],
  "route53resolver:route53resolver": [
    "Route53Resolver.AssociateResolverQueryLogConfig",
    "Route53Resolver.CreateResolverQueryLogConfig",
    "Route53Resolver.DeleteResolverQueryLogConfig",
    "Route53Resolver.DisassociateResolverQueryLogConfig",
    "Route53Resolver.GetResolverQueryLogConfig",
    "Route53Resolver.GetResolverQueryLogConfigAssociation",
    "Route53Resolver.GetResolverQueryLogConfigPolicy",
    "Route53Resolver.ListResolverEndpoints",
    "Route53Resolver.ListResolverQueryLogConfigAssociations",
    "Route53Resolver.ListResolverQueryLogConfigs",
    "Route53Resolver.ListResolverRuleAssociations",
    "Route53Resolver.ListResolverRules",
    "Route53Resolver.PutResolverQueryLogConfigPolicy"
  ],
  "sagemaker:api.sagemaker": [
    "SageMaker.GetSearchSuggestions",
    "SageMaker.ListAlgorithms",
    "SageMaker.ListAutoMLJobs",
    "SageMaker.ListCodeRepositories",
    "SageMaker.ListCompilationJobs",
    "SageMaker.ListDomains",
    "SageMaker.ListEndpointConfigs",
    "SageMaker.ListEndpoints",
    "SageMaker.ListExperiments",
    "SageMaker.ListFlowDefinitions",
    "SageMaker.ListHumanTaskUis",
    "SageMaker.ListHyperParameterTuningJobs",
    "SageMaker.ListLabelingJobs",
    "SageMaker.ListModelPackages",
    "SageMaker.ListModels",
    "SageMaker.ListMonitoringExecutions",
    "SageMaker.ListMonitoringSchedules",
    "SageMaker.ListNotebookInstanceLifecycleConfigs",
    "SageMaker.ListNotebookInstances",
    "SageMaker.ListProcessingJobs",
    "SageMaker.ListSubscribedWorkteams",
    "SageMaker.ListTrainingJobs",
    "SageMaker.ListTransformJobs",
    "SageMaker.ListWorkforces",
    "SageMaker.ListWorkteams",
    "SageMaker.RenderUiTemplate",
    "SageMaker.Search"
  ],
  "secretsmanager:secretsmanager": [
    "secretsmanager.CancelRotateSecret",
    "secretsmanager.CreateSecret",
    "secretsmanager.DeleteResourcePolicy",
    "secretsmanager.DeleteSecret",
    "secretsmanager.DescribeSecret",
    "secretsmanager.GetRandomPassword",
    "secretsmanager.GetResourcePolicy",
    "secretsmanager.GetSecretValue",
    "secretsmanager.ListSecretVersionIds",
    "secretsmanager.ListSecrets",
    "secretsmanager.PutResourcePolicy",
    "secretsmanager.PutSecretValue",
    "secretsmanager.RestoreSecret",
    "secretsmanager.RotateSecret",
    "secretsmanager.TagResource",
    "secretsmanager.UntagResource",
    "secretsmanager.UpdateSecret",
    "secretsmanager.UpdateSecretVersionStage",
    "secretsmanager.ValidateResourcePolicy"
  ],
  "shield:shield": [
    "AWSShield_20160616.AssociateDRTLogBucket",
    "AWSShield_20160616.AssociateProactiveEngagementDetails",
    "AWSShield_20160616.CreateSubscription",
    "AWSShield_20160616.DeleteSubscription",
    "AWSShield_20160616.DescribeDRTAccess",
    "AWSShield_20160616.DescribeEmergencyContactSettings",
    "AWSShield_20160616.DescribeSubscription",
    "AWSShield_20160616.DisableProactiveEngagement",
    "AWSShield_20160616.DisassociateDRTLogBucket",
    "AWSShield_20160616.DisassociateDRTRole",
    "AWSShield_20160616.EnableProactiveEngagement",
    "AWSShield_20160616.GetSubscriptionState",
    "AWSShield_20160616.ListAttacks",
    "AWSShield_20160616.ListProtections",
    "AWSShield_20160616.UpdateEmergencyContactSettings",
    "AWSShield_20160616.UpdateSubscription"
  ],
  "sms:sms": [
    "AWSServerMigrationService_V2016_10_24.CreateApp",
    "AWSServerMigrationService_V2016_10_24.CreateReplicationJob",
    "AWSServerMigrationService_V2016_10_24.DeleteApp",
    "AWSServerMigrationService_V2016_10_24.DeleteAppLaunchConfiguration",
    "AWSServerMigrationService_V2016_10_24.DeleteAppReplicationConfiguration",
    "AWSServerMigrationService_V2016_10_24.DeleteAppValidationConfiguration",
    "AWSServerMigrationService_V2016_10_24.DeleteReplicationJob",
    "AWSServerMigrationService_V2016_10_24.DeleteServerCatalog",
    "AWSServerMigrationService_V2016_10_24.DisassociateConnector",
    "AWSServerMigrationService_V2016_10_24.GenerateChangeSet",
    "AWSServerMigrationService_V2016_10_24.GenerateTemplate",
    "AWSServerMigrationService_V2016_10_24.GetApp",
    "AWSServerMigrationService_V2016_10_24.GetAppLaunchConfiguration",
    "AWSServerMigrationService_V2016_10_24.GetAppReplicationConfiguration",
    "AWSServerMigrationService_V2016_10_24.GetAppValidationConfiguration",
    "AWSServerMigrationService_V2016_10_24.GetAppValidationOutput",
    "AWSServerMigrationService_V2016_10_24.GetConnectors",
    "AWSServerMigrationService_V2016_10_24.GetReplicationJobs",
    "AWSServerMigrationService_V2016_10_24.GetReplicationRuns",
    "AWSServerMigrationService_V2016_10_24.GetServers",
    "AWSServerMigrationService_V2016_10_24.ImportAppCatalog",
    "AWSServerMigrationService_V2016_10_24.ImportServerCatalog",
    "AWSServerMigrationService_V2016_10_24.LaunchApp",
    "AWSServerMigrationService_V2016_10_24.ListApps",
    "AWSServerMigrationService_V2016_10_24.NotifyAppValidationOutput",
    "AWSServerMigrationService_V2016_10_24.PutAppLaunchConfiguration",
    "AWSServerMigrationService_V2016_10_24.PutAppReplicationConfiguration",
    "AWSServerMigrationService_V2016_10_24.PutAppValidationConfiguration",
    "AWSServerMigrationService_V2016_10_24.StartAppReplication",
    "AWSServerMigrationService_V2016_10_24.StartOnDemandAppReplication",
    "AWSServerMigrationService_V2016_10_24.StartOnDemandReplicationRun",
    "AWSServerMigrationService_V2016_10_24.StopAppReplication",
    "AWSServerMigrationService_V2016_10_24.TerminateApp",
    "AWSServerMigrationService_V2016_10_24.UpdateApp",
    "AWSServerMigrationService_V2016_10_24.UpdateReplicationJob"
  ],
  "snowball:snowball": [
    "AWSIESnowballJobManagementService.CancelCluster",
    "AWSIESnowballJobManagementService.CancelJob",
    "AWSIESnowballJobManagementService.CreateAddress",
    "AWSIESnowballJobManagementService.CreateCluster",
    "AWSIESnowballJobManagementService.CreateJob",
    "AWSIESnowballJobManagementService.DescribeAddress",
    "AWSIESnowballJobManagementService.DescribeAddresses",
    "AWSIESnowballJobManagementService.DescribeCluster",
    "AWSIESnowballJobManagementService.DescribeJob",
    "AWSIESnowballJobManagementService.GetJobManifest",
    "AWSIESnowballJobManagementService.GetJobUnlockCode",
    "AWSIESnowballJobManagementService.GetSnowballUsage",
    "AWSIESnowballJobManagementService.GetSoftwareUpdates",
    "AWSIESnowballJobManagementService.ListClusterJobs",
    "AWSIESnowballJobManagementService.ListClusters",
    "AWSIESnowballJobManagementService.ListCompatibleImages",
    "AWSIESnowballJobManagementService.ListJobs",
    "AWSIESnowballJobManagementService.UpdateCluster",
    "AWSIESnowballJobManagementService.UpdateJob"
  ],
  "support:support": [
    "AWSSupport_20130415.AddAttachmentsToSet",
    "AWSSupport_20130415.AddCommunicationToCase",
    "AWSSupport_20130415.CreateCase",
    "AWSSupport_20130415.DescribeAttachment",
    "AWSSupport_20130415.DescribeCases",
    "AWSSupport_20130415.DescribeCommunications",
    "AWSSupport_20130415.DescribeServices",
    "AWSSupport_20130415.DescribeSeverityLevels",
    "AWSSupport_20130415.DescribeTrustedAdvisorCheckRefreshStatuses",
    "AWSSupport_20130415.DescribeTrustedAdvisorCheckResult",
    "AWSSupport_20130415.DescribeTrustedAdvisorCheckSummaries",
    "AWSSupport_20130415.DescribeTrustedAdvisorChecks",
    "AWSSupport_20130415.RefreshTrustedAdvisorCheck",
    "AWSSupport_20130415.ResolveCase"
  ],
  "tagging:tagging": [
    "ResourceGroupsTaggingAPI_20170126.DescribeReportCreation",
    "ResourceGroupsTaggingAPI_20170126.GetComplianceSummary",
    "ResourceGroupsTaggingAPI_20170126.GetResources",
    "ResourceGroupsTaggingAPI_20170126.GetTagKeys",
    "ResourceGroupsTaggingAPI_20170126.GetTagValues",
    "ResourceGroupsTaggingAPI_20170126.StartReportCreation",
    "ResourceGroupsTaggingAPI_20170126.TagResources",
    "ResourceGroupsTaggingAPI_20170126.UntagResources"
  ],
  "textract:textract": [
    "Textract.AnalyzeDocument",
    "Textract.DetectDocumentText",
    "Textract.GetDocumentAnalysis",
    "Textract.GetDocumentTextDetection",
    "Textract.StartDocumentAnalysis",
    "Textract.StartDocumentTextDetection"
  ],
  "translate:translate": [
    "AWSShineFrontendService_20170701.DeleteTerminology",
    "AWSShineFrontendService_20170701.DescribeTextTranslationJob",
    "AWSShineFrontendService_20170701.GetTerminology",
    "AWSShineFrontendService_20170701.ImportTerminology",
    "AWSShineFrontendService_20170701.ListTerminologies",
    "AWSShineFrontendService_20170701.ListTextTranslationJobs",
    "AWSShineFrontendService_20170701.StartTextTranslationJob",
    "AWSShineFrontendService_20170701.StopTextTranslationJob",
    "AWSShineFrontendService_20170701.TranslateText"
  ],
  "workmail:workmail": [
    "WorkMailService.AssociateDelegateToResource",
    "WorkMailService.AssociateMemberToGroup",
    "WorkMailService.CreateAlias",
    "WorkMailService.CreateGroup",
    "WorkMailService.CreateResource",
    "WorkMailService.CreateUser",
    "WorkMailService.DeleteAccessControlRule",
    "WorkMailService.DeleteAlias",
    "WorkMailService.DeleteGroup",
    "WorkMailService.DeleteMailboxPermissions",
    "WorkMailService.DeleteResource",
    "WorkMailService.DeleteRetentionPolicy",
    "WorkMailService.DeleteUser",
    "WorkMailService.DeregisterFromWorkMail",
    "WorkMailService.DescribeGroup",
    "WorkMailService.DescribeOrganization",
    "WorkMailService.DescribeResource",
    "WorkMailService.DescribeUser",
    "WorkMailService.DisassociateDelegateFromResource",
    "WorkMailService.DisassociateMemberFromGroup",
    "WorkMailService.GetAccessControlEffect",
    "WorkMailService.GetDefaultRetentionPolicy",
    "WorkMailService.GetMailboxDetails",
    "WorkMailService.ListAccessControlRules",
    "WorkMailService.ListAliases",
    "WorkMailService.ListGroupMembers",
    "WorkMailService.ListGroups",
    "WorkMailService.ListMailboxPermissions",
    "WorkMailService.ListOrganizations",
    "WorkMailService.ListResourceDelegates",
    "WorkMailService.ListResources",
    "WorkMailService.ListTagsForResource",
    "WorkMailService.ListUsers",
    "WorkMailService.PutAccessControlRule",
    "WorkMailService.PutMailboxPermissions",
    "WorkMailService.PutRetentionPolicy",
    "WorkMailService.RegisterToWorkMail",
    "WorkMailService.ResetPassword",
    "WorkMailService.TagResource",
    "WorkMailService.UntagResource",
    "WorkMailService.UpdateMailboxQuota",
    "WorkMailService.UpdatePrimaryEmailAddress",
    "WorkMailService.UpdateResource"
  ]
}  

def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def getSignatureKey(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

def make_call(signing_name, service_target, action):
    method = 'POST'
    service = signing_name
    host = service_target+'.us-east-1.amazonaws.com'
    region = 'us-east-1'
    endpoint = 'https://'+service_target+'.us-east-1.amazonaws.com/'
    content_type = 'application/x-amz-json-1.0'
    amz_target = action

    request_parameters = "{}"

    t = datetime.datetime.utcnow()
    amz_date = t.strftime('%Y%m%dT%H%M%SZ')
    date_stamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope

    canonical_uri = '/'

    canonical_querystring = ''

    canonical_headers = 'content-type:' + content_type + '\n' + 'host:' + host + '\n' + 'x-amz-date:' + amz_date + '\n' + 'x-amz-target:' + amz_target + '\n'

    signed_headers = 'content-type;host;x-amz-date;x-amz-target'

    payload_hash = hashlib.sha256(request_parameters.encode('utf-8')).hexdigest()

    canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash


    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = date_stamp + '/' + region + '/' + service + '/' + 'aws4_request'
    string_to_sign = algorithm + '\n' +  amz_date + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

    signing_key = getSignatureKey(secret_key, date_stamp, region, service)

    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()


    authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

    headers = {'Content-Type':content_type,
           'X-Amz-Date':amz_date,
           'X-Amz-Target':amz_target,
           'X-Amz-Security-Token':session_token,
           'Authorization':authorization_header}


    r = requests.post(endpoint, data=request_parameters, headers=headers)

    #if r.status_code == 403:
    #    print("You do not have permissions to call %s:%s" % (service,action))
    if r.status_code == 404:
        print("You have permissions to call %s:%s" % (service,action))


access_key = os.environ.get('AWS_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
session_token = os.environ.get('AWS_SESSION_TOKEN')
if access_key is None or secret_key is None:
    print('No access key is available.')
    sys.exit()

now = datetime.datetime.now()
print("Time:",now.strftime("%H:%M:%S"))
for item in services:
    for action in services[item]:
        make_call(item[:item.find(":")], item[item.find(":")+1:], action)

now = datetime.datetime.now()
print("Time:",now.strftime("%H:%M:%S"))
