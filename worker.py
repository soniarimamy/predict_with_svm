import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflow import PredictWorkflow
from activities import call_predict, call_perf

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="ml-task-queue",
        workflows=[PredictWorkflow],
        activities=[call_predict, call_perf],
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
