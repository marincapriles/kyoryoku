#!/usr/bin/env python3
"""
General-Purpose Multi-Agent Team CLI
Test multiple agent teams through an easy-to-use interface
"""

import asyncio
import sys
import os
import json
from typing import Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.markdown import Markdown

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

try:
    from app.services.llm_service import orchestrator
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False

console = Console()

class MultiAgentCLI:
    def __init__(self):
        self.console = console
        self.available_teams = {
            "1": {
                "name": "Customer Support Team",
                "description": "4-agent team for handling customer support requests",
                "agents": ["Triage Specialist", "Solution Researcher", "Response Crafter", "Escalation Analyst"],
                "pattern": "Sequential workflow",
                "status": "Production Ready"
            },
            "2": {
                "name": "Content Creation Team", 
                "description": "5-agent iterative refinement for content creation",
                "agents": ["Story Miner", "Structure Architect", "Technical Translator", "Voice Crafter", "Hook Designer"],
                "pattern": "Iterative refinement",
                "status": "Demo/Validation"
            },
            "3": {
                "name": "Content Marketing Team",
                "description": "2-agent prototype for marketing content production",
                "agents": ["Content Strategist", "Content Producer"],
                "pattern": "Strategy → Production",
                "status": "Prototype"
            },
            "4": {
                "name": "Guest Concierge Team",
                "description": "2-agent team for hospitality concierge services",
                "agents": ["Guest Experience Agent", "Concierge Coordinator"],
                "pattern": "Experience Analysis → Coordination",
                "status": "Prototype"
            }
        }
        
    def show_welcome(self):
        """Show welcome screen"""
        welcome_text = """
# 🤖 Kyoryoku Multi-Agent Teams CLI

Test different **multi-agent coordination patterns** across various professional domains:

- **Customer Support**: Production-ready 4-agent sequential workflow
- **Content Creation**: Demo 5-agent iterative refinement
- **Content Marketing**: Prototype 2-agent strategy → production
- **Guest Concierge**: Prototype 2-agent hospitality services

Each team demonstrates different coordination patterns and business applications.
        """
        
        self.console.print(Panel(
            Markdown(welcome_text),
            title="Welcome to Multi-Agent Teams CLI",
            border_style="blue"
        ))
    
    def show_available_teams(self):
        """Display available teams in a formatted table"""
        
        teams_table = Table(title="🤖 Available Agent Teams")
        teams_table.add_column("#", style="cyan", width=3)
        teams_table.add_column("Team Name", style="bold blue", width=20)
        teams_table.add_column("Agents", style="green", width=15)
        teams_table.add_column("Pattern", style="yellow", width=20)
        teams_table.add_column("Status", style="magenta", width=15)
        teams_table.add_column("Description", style="white", width=35)
        
        for key, team in self.available_teams.items():
            agent_count = f"{len(team['agents'])} agents"
            teams_table.add_row(
                key,
                team["name"],
                agent_count,
                team["pattern"],
                team["status"],
                team["description"]
            )
        
        self.console.print(teams_table)
    
    def select_team(self) -> Dict[str, Any]:
        """Let user select a team to test"""
        
        self.show_available_teams()
        
        team_choice = Prompt.ask(
            "\n🎯 Select team to test",
            choices=list(self.available_teams.keys()),
            default="1"
        )
        
        selected_team = self.available_teams[team_choice]
        
        self.console.print(f"\n✅ Selected: [bold]{selected_team['name']}[/bold]")
        self.console.print(f"   Agents: {', '.join(selected_team['agents'])}")
        self.console.print(f"   Pattern: {selected_team['pattern']}")
        
        return {
            "key": team_choice,
            "team": selected_team
        }
    
    def get_team_input(self, team_selection: Dict[str, Any]) -> Dict[str, Any]:
        """Get team-specific input from user"""
        
        team_key = team_selection["key"]
        team = team_selection["team"]
        
        self.console.print(f"\n📝 [bold]{team['name']} Configuration[/bold]")
        
        if team_key == "1":  # Customer Support
            return self._get_customer_support_input()
        elif team_key == "2":  # Content Creation
            return self._get_content_creation_input()
        elif team_key == "3":  # Content Marketing
            return self._get_content_marketing_input()
        elif team_key == "4":  # Guest Concierge
            return self._get_guest_concierge_input()
        else:
            return {}
    
    def _get_customer_support_input(self) -> Dict[str, Any]:
        """Get customer support specific input"""
        
        self.console.print("\n🎯 Customer Support Scenario Types:")
        scenarios = {
            "1": "Login/Authentication Issue",
            "2": "Billing Question", 
            "3": "Technical Problem",
            "4": "Feature Request",
            "5": "Account Management",
            "6": "Custom Issue"
        }
        
        for key, scenario in scenarios.items():
            self.console.print(f"  {key}. {scenario}")
        
        scenario_choice = Prompt.ask(
            "Select scenario type",
            choices=list(scenarios.keys()),
            default="1"
        )
        
        if scenario_choice == "6":
            request = Prompt.ask("Enter custom support request")
        else:
            request = scenarios[scenario_choice] + " - " + Prompt.ask("Describe the specific issue")
        
        # Customer context
        tier = Prompt.ask("Customer tier", choices=["free", "premium", "enterprise"], default="premium")
        urgency = Prompt.ask("Urgency level", choices=["low", "medium", "high", "critical"], default="medium")
        
        return {
            "type": "customer_support",
            "request": request,
            "customer_context": {
                "customer_tier": tier,
                "urgency": urgency,
                "account_type": "business" if tier != "free" else "personal"
            }
        }
    
    def _get_content_creation_input(self) -> Dict[str, Any]:
        """Get content creation specific input"""
        
        # Content type selection
        content_types = {
            "1": "blog_post",
            "2": "executive_summary", 
            "3": "case_study",
            "4": "product_description"
        }
        
        self.console.print("\n🎯 Content Types:")
        for key, value in content_types.items():
            self.console.print(f"  {key}. {value.replace('_', ' ').title()}")
        
        content_choice = Prompt.ask(
            "Select content type",
            choices=list(content_types.keys()),
            default="1"
        )
        
        # Source material
        use_default = Confirm.ask("Use default Kyoryoku example content?", default=True)
        
        if use_default:
            source_material = """
            Kyoryoku is a multi-agent AI platform that helps business teams work more efficiently. 
            The platform uses specialized AI agents that coordinate with each other to complete complex 
            tasks like customer support and content creation. Our shadow learning approach allows 
            agents to learn from human experts. Early tests show 70% time reduction with maintained quality.
            """
        else:
            source_material = Prompt.ask("Enter your source material")
        
        iterations = int(Prompt.ask("Number of refinement iterations", default="1"))
        
        return {
            "type": "content_creation",
            "source_material": source_material.strip(),
            "content_type": content_types[content_choice],
            "target_audience": "business_executives",
            "iterations": iterations
        }
    
    def _get_content_marketing_input(self) -> Dict[str, Any]:
        """Get content marketing specific input"""
        
        self.console.print("\n🎯 Content Marketing Request Types:")
        request_types = {
            "1": "Blog post about product features",
            "2": "Social media campaign content",
            "3": "Email newsletter content", 
            "4": "Website copy optimization",
            "5": "Custom marketing content"
        }
        
        for key, req_type in request_types.items():
            self.console.print(f"  {key}. {req_type}")
        
        request_choice = Prompt.ask(
            "Select request type",
            choices=list(request_types.keys()),
            default="1"
        )
        
        if request_choice == "5":
            request = Prompt.ask("Describe your content marketing needs")
        else:
            request = request_types[request_choice]
        
        # Target audience
        audiences = {
            "1": "business_executives",
            "2": "technical_teams", 
            "3": "marketing_professionals",
            "4": "general_consumers"
        }
        
        self.console.print("\n👥 Target Audiences:")
        for key, audience in audiences.items():
            self.console.print(f"  {key}. {audience.replace('_', ' ').title()}")
        
        audience_choice = Prompt.ask(
            "Select target audience",
            choices=list(audiences.keys()),
            default="1"
        )
        
        return {
            "type": "content_marketing",
            "request": request,
            "target_audience": audiences[audience_choice],
            "content_type": "blog_post",
            "brand_context": {
                "industry": "technology",
                "tone": "professional_friendly"
            }
        }
    
    def _get_guest_concierge_input(self) -> Dict[str, Any]:
        """Get guest concierge specific input"""
        
        self.console.print("\n🎯 Guest Request Types:")
        request_types = {
            "1": "Restaurant recommendation and reservation",
            "2": "Local attraction and activity planning",
            "3": "Transportation and logistics",
            "4": "Special event or celebration planning",
            "5": "Business meeting arrangements",
            "6": "Custom guest request"
        }
        
        for key, req_type in request_types.items():
            self.console.print(f"  {key}. {req_type}")
        
        request_choice = Prompt.ask(
            "Select request type", 
            choices=list(request_types.keys()),
            default="1"
        )
        
        if request_choice == "6":
            guest_request = Prompt.ask("Describe the guest's request")
        else:
            base_request = request_types[request_choice]
            details = Prompt.ask(f"Additional details for {base_request.lower()}")
            guest_request = f"{base_request}: {details}"
        
        # Guest context
        budget = Prompt.ask("Budget level", choices=["moderate", "premium", "luxury"], default="premium")
        party_size = Prompt.ask("Party size", default="2")
        location = Prompt.ask("Location/City", default="downtown")
        
        return {
            "type": "guest_concierge",
            "guest_request": guest_request,
            "guest_context": {
                "budget": budget,
                "party_size": int(party_size),
                "preferences": "high_quality_experience"
            },
            "location": location
        }
    
    async def process_team_request(self, team_selection: Dict[str, Any], team_input: Dict[str, Any]) -> Dict[str, Any]:
        """Process request through selected team"""
        
        if not LLM_AVAILABLE:
            raise ImportError("LLM service not available - check backend setup")
        
        team_key = team_selection["key"]
        input_type = team_input["type"]
        
        # Route to appropriate orchestrator method
        if input_type == "customer_support":
            return await orchestrator.process_customer_support_request(
                request=team_input["request"],
                customer_context=team_input["customer_context"]
            )
        elif input_type == "content_creation":
            return await orchestrator.process_content_creation_request(
                source_material=team_input["source_material"],
                content_type=team_input["content_type"],
                target_audience=team_input["target_audience"],
                iterations=team_input["iterations"]
            )
        elif input_type == "content_marketing":
            return await orchestrator.process_content_marketing_request(
                request=team_input["request"],
                target_audience=team_input["target_audience"],
                content_type=team_input["content_type"],
                brand_context=team_input["brand_context"]
            )
        elif input_type == "guest_concierge":
            return await orchestrator.process_guest_concierge_request(
                guest_request=team_input["guest_request"],
                guest_context=team_input["guest_context"],
                location=team_input["location"]
            )
        else:
            raise ValueError(f"Unknown team type: {input_type}")
    
    def display_results(self, team_selection: Dict[str, Any], team_input: Dict[str, Any], results: Dict[str, Any]):
        """Display results in team-specific format"""
        
        team_name = team_selection["team"]["name"]
        
        self.console.print("\n" + "="*70)
        self.console.print(f"🎉 [bold green]{team_name} Complete![/bold green]")
        self.console.print("="*70)
        
        input_type = team_input["type"]
        
        if input_type == "customer_support":
            self._display_customer_support_results(results)
        elif input_type == "content_creation":
            self._display_content_creation_results(results)
        elif input_type == "content_marketing":
            self._display_content_marketing_results(results)
        elif input_type == "guest_concierge":
            self._display_guest_concierge_results(results)
    
    def _display_customer_support_results(self, results: Dict[str, Any]):
        """Display customer support specific results"""
        
        # Show pipeline stages
        stages_table = Table(title="📊 Support Pipeline Results")
        stages_table.add_column("Stage", style="cyan")
        stages_table.add_column("Agent", style="blue")
        stages_table.add_column("Confidence", style="yellow")
        stages_table.add_column("Status", style="green")
        
        stage_names = {
            "triage": "Triage & Routing",
            "research": "Solution Research",
            "response": "Response Crafting",
            "escalation": "Escalation Analysis"
        }
        
        for stage_key, stage_name in stage_names.items():
            if stage_key in results:
                stage_result = results[stage_key]
                confidence = stage_result.confidence
                status = "✅ Complete" if confidence > 0.7 else "⚠️ Low Confidence"
                
                stages_table.add_row(
                    stage_name,
                    stage_key.replace('_', ' ').title(),
                    f"{confidence:.1f}",
                    status
                )
        
        self.console.print(stages_table)
        
        # Show final response if available
        if "response" in results:
            final_response = results["response"].content
            self.console.print(f"\n📄 [bold]Final Response[/bold]")
            response_panel = Panel(
                final_response[:300] + ("..." if len(final_response) > 300 else ""),
                title="Customer Response",
                border_style="green"
            )
            self.console.print(response_panel)
    
    def _display_content_creation_results(self, results: Dict[str, Any]):
        """Display content creation specific results"""
        
        # Show iteration summary
        summary_table = Table(title="📊 Content Creation Summary")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="green")
        
        summary_table.add_row("Total Iterations", str(results.get('total_iterations', 0)))
        summary_table.add_row("Agent Handoffs", str(results.get('platform_validation', {}).get('agent_handoffs', 0)))
        summary_table.add_row("Coordination Success", "✅ YES" if results.get('platform_validation', {}).get('coordination_success') else "❌ NO")
        
        self.console.print(summary_table)
        
        # Show final content
        final_content = results.get('final_content', '')
        if final_content:
            self.console.print(f"\n📄 [bold]Generated Content ({len(final_content)} characters)[/bold]")
            content_panel = Panel(
                final_content[:400] + ("..." if len(final_content) > 400 else ""),
                title="Final Content",
                border_style="green"
            )
            self.console.print(content_panel)
    
    def _display_content_marketing_results(self, results: Dict[str, Any]):
        """Display content marketing specific results"""
        
        # Show agent results
        agents_table = Table(title="📊 Content Marketing Pipeline")
        agents_table.add_column("Agent", style="cyan")
        agents_table.add_column("Role", style="blue")
        agents_table.add_column("Confidence", style="yellow")
        agents_table.add_column("Status", style="green")
        
        agents_table.add_row(
            "Content Strategist",
            "Strategy & Planning",
            f"{results.get('strategy', {}).confidence:.1f}" if 'strategy' in results else "N/A",
            "✅ Complete"
        )
        
        agents_table.add_row(
            "Content Producer", 
            "Content Creation",
            f"{results.get('production', {}).confidence:.1f}" if 'production' in results else "N/A",
            "✅ Complete"
        )
        
        self.console.print(agents_table)
        
        # Show final content
        final_content = results.get('final_content', '')
        if final_content:
            self.console.print(f"\n📄 [bold]Marketing Content[/bold]")
            content_panel = Panel(
                final_content[:400] + ("..." if len(final_content) > 400 else ""),
                title="Ready-to-Publish Content",
                border_style="green"
            )
            self.console.print(content_panel)
    
    def _display_guest_concierge_results(self, results: Dict[str, Any]):
        """Display guest concierge specific results"""
        
        # Show concierge pipeline
        concierge_table = Table(title="📊 Concierge Service Pipeline")
        concierge_table.add_column("Agent", style="cyan")
        concierge_table.add_column("Role", style="blue")
        concierge_table.add_column("Confidence", style="yellow")
        concierge_table.add_column("Status", style="green")
        
        concierge_table.add_row(
            "Guest Experience Agent",
            "Experience Analysis",
            f"{results.get('experience_analysis', {}).confidence:.1f}" if 'experience_analysis' in results else "N/A",
            "✅ Complete"
        )
        
        concierge_table.add_row(
            "Concierge Coordinator",
            "Logistics & Coordination", 
            f"{results.get('coordination_plan', {}).confidence:.1f}" if 'coordination_plan' in results else "N/A",
            "✅ Complete"
        )
        
        self.console.print(concierge_table)
        
        # Show recommendations
        recommendations = results.get('final_recommendations', '')
        if recommendations:
            self.console.print(f"\n🎯 [bold]Concierge Recommendations[/bold]")
            rec_panel = Panel(
                recommendations[:400] + ("..." if len(recommendations) > 400 else ""),
                title="Guest Experience Plan",
                border_style="green"
            )
            self.console.print(rec_panel)
    
    def show_error(self, error: Exception):
        """Show error in user-friendly way"""
        
        error_text = f"""
**❌ Processing Error:**

{str(error)}

**💡 Common Solutions:**
- Ensure backend server is running: `python3 -m uvicorn app.main:app --reload --port 8001`
- Check ANTHROPIC_API_KEY in .env file
- Verify database is running: `brew services start postgresql`
        """
        
        self.console.print(Panel(
            Markdown(error_text),
            title="Error Occurred",
            border_style="red"
        ))
    
    async def main_loop(self):
        """Main interactive loop"""
        
        self.show_welcome()
        
        while True:
            self.console.print("\n🎯 [bold]Multi-Agent Teams CLI Options[/bold]")
            self.console.print("  1. Test Agent Team")
            self.console.print("  2. View Team Details")
            self.console.print("  3. Compare Team Patterns")
            self.console.print("  4. Exit")
            
            choice = Prompt.ask(
                "Select option",
                choices=["1", "2", "3", "4"],
                default="1"
            )
            
            if choice == "1":
                try:
                    # Team selection and testing workflow
                    team_selection = self.select_team()
                    team_input = self.get_team_input(team_selection)
                    
                    self.console.print(f"\n🚀 Processing through {team_selection['team']['name']}...")
                    
                    # Show processing progress
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        console=self.console
                    ) as progress:
                        task = progress.add_task("Processing through agent team...", total=None)
                        
                        # Run actual processing
                        results = await self.process_team_request(team_selection, team_input)
                        
                        progress.update(task, description="✅ Processing complete!")
                    
                    self.display_results(team_selection, team_input, results)
                    
                except Exception as e:
                    self.show_error(e)
            
            elif choice == "2":
                self.show_available_teams()
                
                # Show detailed team info
                detail_choice = Prompt.ask(
                    "\nSelect team for details (or press Enter to continue)",
                    choices=list(self.available_teams.keys()) + [""],
                    default=""
                )
                
                if detail_choice:
                    team = self.available_teams[detail_choice]
                    
                    detail_text = f"""
**{team['name']}**

**Description:** {team['description']}

**Agents:** {', '.join(team['agents'])}

**Coordination Pattern:** {team['pattern']}

**Status:** {team['status']}

**Use Cases:**
- Production workflows requiring this coordination pattern
- Validation of multi-agent collaboration
- Demonstration of platform capabilities
                    """
                    
                    self.console.print(Panel(
                        Markdown(detail_text),
                        title=f"{team['name']} Details",
                        border_style="blue"
                    ))
            
            elif choice == "3":
                # Compare coordination patterns
                comparison_text = """
**🔄 Agent Coordination Patterns:**

**Sequential Workflow** (Customer Support):
- Agents process in linear order: Triage → Research → Response → Escalation
- Each agent depends on previous agent's output
- Best for: Structured processes with clear dependencies

**Iterative Refinement** (Content Creation):
- All agents work in rounds, each building on the previous round
- Multiple iterations until quality threshold met
- Best for: Creative processes requiring multiple perspectives

**Strategy → Production** (Content Marketing):
- Two-stage process: strategic planning then execution
- Clear handoff between planning and production phases
- Best for: Workflows with distinct planning and execution phases  

**Experience → Coordination** (Guest Concierge):
- Analysis phase followed by coordination/execution phase
- Focus on understanding needs then delivering solutions
- Best for: Service delivery requiring personalization
                """
                
                self.console.print(Panel(
                    Markdown(comparison_text),
                    title="Coordination Pattern Comparison",
                    border_style="yellow"
                ))
            
            elif choice == "4":
                self.console.print("\n👋 Thanks for testing the Multi-Agent Teams!")
                self.console.print("🎯 [bold]Key Insights:[/bold]")
                self.console.print("   • Different coordination patterns suit different use cases")
                self.console.print("   • Multi-agent teams outperform single agents on complex tasks")
                self.console.print("   • Platform validates multiple business applications")
                break


async def main():
    """Entry point for the CLI"""
    
    cli = MultiAgentCLI()
    
    try:
        await cli.main_loop()
    except KeyboardInterrupt:
        console.print("\n\n👋 Goodbye!")
    except Exception as e:
        console.print(f"\n❌ Unexpected error: {e}")
        console.print("💡 Try running the backend server first: `python3 -m uvicorn app.main:app --reload --port 8001`")


if __name__ == "__main__":
    # Check for required dependencies
    try:
        import rich
    except ImportError:
        print("❌ Missing required dependency: rich")
        print("💡 Install with: pip install rich")
        sys.exit(1)
    
    asyncio.run(main())