from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import call_predict, call_perf

@workflow.defn
class PredictWorkflow:
    @workflow.run
    async def run(self, mot: str):
        # 1. appeler predict
        prediction = await workflow.execute_activity(
            call_predict,
            mot,
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(maximum_attempts=3)
        )
        # 2. appeler performance
        perf = await workflow.execute_activity(
            call_perf,
            start_to_close_timeout=timedelta(seconds=10)
        )
        return {
            "prediction": prediction,
            "performance": perf
        }
