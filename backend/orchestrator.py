import asyncio
import json
from datetime import datetime

# Local imports
from backend.database.session import AsyncSessionLocal
from backend.database.models import ProcessedLead, Lead
from sqlalchemy.future import select

# We will import the specialized Agents here
# from backend.agents.romeo import AgentDLD
# from backend.agents.juliet import AgentPortals
# from backend.agents.wednesday import AgentGEE

class Orchestrator:
    def __init__(self):
        print("[Orchestrator] Initializing Multi-Agent State Graph...")
        self.hurray_flag = "[HURRAY_PREFIX_VALIDATED]"

    async def is_duplicate(self, lead_id: str) -> bool:
        """O(1) Deduplication Check via SQL"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(ProcessedLead).where(ProcessedLead.id == lead_id))
            exists = result.scalars().first()
            return exists is not None

    async def mark_as_processed(self, lead_id: str, source: str):
        """Records a lead ID in the database so scouts never process it again."""
        async with AsyncSessionLocal() as session:
            processed = ProcessedLead(id=lead_id, source=source)
            session.add(processed)
            await session.commit()

    async def run_residential_loop(self):
        """
        The Checkpoint Loop for Residential (Romeo + Juliet + Friday -> Evaluator)
        """
        print("\n[Orchestrator] Triggering Residential Loop...")
        # TODO: Instantiate Romeo, Juliet, Friday
        
        while True:
            # 1. Scout grabs a raw lead
            print("[Romeo/Juliet] Hunting for a potential lead...")
            await asyncio.sleep(1) # Mock scraping
            
            mock_lead_id = f"TR-RES-{int(datetime.utcnow().timestamp())}"
            
            # 2. Check Deduplication
            if await self.is_duplicate(mock_lead_id):
                print(f"[Orchestrator] {mock_lead_id} already processed. Skipping.")
                continue

            print(f"[Orchestrator] Found new raw lead: {mock_lead_id}. Sending to Evaluator.")
            
            # 3. Checkpoint Eval
            # mock_eval_output = await evaluator.run(mock_lead_data)
            await asyncio.sleep(1)
            # Simulating a failed check vs a successful check
            success = True # Hardcoded for pilot demonstration
            
            if success:
                print(f"[Evaluator] {self.hurray_flag} Lead passed all logic checks.")
                # 4. Save to Database
                await self.mark_as_processed(mock_lead_id, "DLD_Romeo")
                print(f"[Auditor] Lead {mock_lead_id} successfully saved to SQL Database.")
                break # Break the loop because we found a Golden Lead!
            else:
                print("[Evaluator] REJECTED. False positive. Forcing Scout to loop again.")
                # The loop continues indefinitely until a Golden Lead is found

    async def run_cron_schedule(self):
        """The main execution graph. Runs indefinitely."""
        print("==========================================================")
        print("  STARTING MULTI-AGENT ORCHESTRATOR (ZERO-BLOAT GRAPH)  ")
        print("==========================================================\n")
        
        while True:
            print(f"\n--- Waking up Agents at {datetime.utcnow().strftime('%H:%M:%S')} ---")
            
            # Dispatch Sub-Agent Loops concurrently
            await asyncio.gather(
                self.run_residential_loop(),
                # self.run_commercial_loop(),
                # self.run_stalled_flip_loop()
            )
            
            print("\n[Orchestrator] Daily tasks complete. Going back to sleep.")
            # In production, this would be 24 hours (86400 seconds)
            await asyncio.sleep(5) # Set to 5 seconds for testing

if __name__ == "__main__":
    orchestrator = Orchestrator()
    try:
        asyncio.run(orchestrator.run_cron_schedule())
    except KeyboardInterrupt:
        print("\n[Orchestrator] Shutting down gracefully.")
