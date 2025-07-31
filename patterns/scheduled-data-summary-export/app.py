#!/usr/bin/env python3
import os

import aws_cdk as cdk

from scheduled_data_summary_export.scheduled_data_summary_export_stack import ScheduledDataSummaryExportStack


app = cdk.App()
ScheduledDataSummaryExportStack(app, "ScheduledDataSummaryExportStack",
    env = cdk.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"]
    )
)

app.synth()
