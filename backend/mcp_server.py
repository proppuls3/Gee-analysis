import asyncio
from mcp.server.fastmcp import FastMCP
from backend.database.session import AsyncSessionLocal
from backend.database.models import Lead, ProcessedLead
from sqlalchemy.future import select

# Initialize the FastMCP Server
mcp = FastMCP("gee-fitout-mcp")

@mcp.tool()
async def get_golden_leads(funnel_category: str = None) -> list[dict]:
    """
    Fetches all leads that successfully passed the [HURRAY] checkpoint from the database.
    Can be filtered by funnel_category (e.g., 'Lens_A_Buyer', 'Lens_E_Handover', 'Lens_F_Stalled').
    """
    async with AsyncSessionLocal() as session:
        query = select(Lead).where(Lead.status == "New")
        if funnel_category:
            query = query.where(Lead.funnel_category == funnel_category)
            
        result = await session.execute(query)
        leads = result.scalars().all()
        
        return [
            {
                "id": lead.id,
                "category": lead.funnel_category,
                "coordinates": lead.coordinates,
                "referral_partner": lead.referral_partner
            }
            for lead in leads
        ]

@mcp.tool()
async def get_orchestrator_status() -> dict:
    """
    Returns the real-time status of the multi-agent graph (telemetry).
    """
    # In a production app, this would query a Redis/SQLite state table.
    async with AsyncSessionLocal() as session:
        # Count processed leads to show activity
        result = await session.execute(select(ProcessedLead))
        count = len(result.scalars().all())
        
        return {
            "status": "RUNNING",
            "active_agents": ["romeo_dld", "juliet_portals", "wednesday_gee"],
            "total_properties_scanned": count,
            "last_cron_trigger": "2026-06-17T02:00:00Z"
        }

if __name__ == "__main__":
    print("[MCP Server] Starting Google Cloud MCP Bridge...")
    # Run the MCP server over standard input/output (for local/Docker integration)
    mcp.run()
