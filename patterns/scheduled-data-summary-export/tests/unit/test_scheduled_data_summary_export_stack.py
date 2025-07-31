import aws_cdk as core
import aws_cdk.assertions as assertions

from scheduled_data_summary_export.scheduled_data_summary_export_stack import ScheduledDataSummaryExportStack

# example tests. To run these tests, uncomment this file along with the example
# resource in scheduled_data_summary_export/scheduled_data_summary_export_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ScheduledDataSummaryExportStack(app, "scheduled-data-summary-export")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
