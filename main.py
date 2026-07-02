import asyncio
import sys
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession
from agents.recon_agent import ReconAgent
from agents.medical_agent import MedicalAgent
from agents.commander_agent import CommanderAgent

async def run_simulation():
    print("=== AeroRescue Swarm Simulation Started ===")
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["mcp_server/server.py"],
        # Ensure that it runs in the current directory or provide full path if needed
    )
    
    print("Starting MCP Server connection...")
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("MCP Server connected and initialized.")
                
                # Initialize Agents
                recon = ReconAgent()
                medical = MedicalAgent()
                commander = CommanderAgent()
                
                # Step 1: Recon maps disaster zones
                print("\n--- STEP 1: RECONNAISSANCE ---")
                critical_zones = await recon.analyze_zones(session)
                
                if not critical_zones:
                    print("No critical zones identified. Mission aborted.")
                    return
                
                # Step 2: Medical processes triage data for the identified zones
                print("\n--- STEP 2: MEDICAL TRIAGE ---")
                triage_data = await medical.process_triage(session, critical_zones)
                
                # Step 3: Commander strategizes and deploys drone swarm
                print("\n--- STEP 3: DEPLOYMENT STRATEGY ---")
                deployments = commander.strategize_deployments(critical_zones, triage_data)
                
                print("\n--- STEP 4: EXECUTION ---")
                commander.execute_mission(deployments)
                
    except Exception as e:
        print(f"Simulation encountered an error: {e}")

if __name__ == "__main__":
    asyncio.run(run_simulation())
