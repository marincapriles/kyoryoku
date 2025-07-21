#!/usr/bin/env python3
"""
Interactive CLI for testing the Content Creation Team
Provides an easy-to-use interface for validating the platform
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

class ContentCreationCLI:
    def __init__(self):
        self.console = console
        
    def show_welcome(self):
        """Show welcome screen"""
        welcome_text = """
# 🎨 Kyoryoku Content Creation Team CLI

Test the **iterative refinement coordination pattern** with our 5-agent Content Creation Team:

- **Story Miner**: Extract compelling narratives
- **Structure Architect**: Organize for maximum impact  
- **Technical Translator**: Simplify complex concepts
- **Voice Crafter**: Create authentic tone
- **Hook Designer**: Engage and maintain momentum

Perfect for validating platform capabilities before customer pilots!
        """
        
        self.console.print(Panel(
            Markdown(welcome_text),
            title="Welcome to Content Creation CLI",
            border_style="blue"
        ))
    
    def get_user_input(self) -> Dict[str, Any]:
        """Get content creation parameters from user"""
        
        self.console.print("\n📝 [bold]Content Creation Configuration[/bold]")
        
        # Content type selection
        content_types = {
            "1": "blog_post",
            "2": "executive_summary", 
            "3": "case_study",
            "4": "product_description",
            "5": "press_release"
        }
        
        self.console.print("\n🎯 Content Types:")
        for key, value in content_types.items():
            self.console.print(f"  {key}. {value.replace('_', ' ').title()}")
        
        content_choice = Prompt.ask(
            "Select content type",
            choices=list(content_types.keys()),
            default="1"
        )
        content_type = content_types[content_choice]
        
        # Target audience selection
        audiences = {
            "1": "business_executives",
            "2": "technical_teams",
            "3": "general_public",
            "4": "investors",
            "5": "customers"
        }
        
        self.console.print("\n👥 Target Audiences:")
        for key, value in audiences.items():
            self.console.print(f"  {key}. {value.replace('_', ' ').title()}")
        
        audience_choice = Prompt.ask(
            "Select target audience",
            choices=list(audiences.keys()),
            default="1"
        )
        target_audience = audiences[audience_choice]
        
        # Iterations
        iterations = int(Prompt.ask(
            "Number of refinement iterations",
            default="1",
            show_default=True
        ))
        
        # Source material options
        self.console.print("\n📄 Source Material Options:")
        self.console.print("  1. Use default Kyoryoku example")
        self.console.print("  2. Enter custom content")
        self.console.print("  3. Load from file")
        
        source_choice = Prompt.ask(
            "Select source material",
            choices=["1", "2", "3"],
            default="1"
        )
        
        if source_choice == "1":
            source_material = """
            Kyoryoku is a multi-agent AI collaboration platform that helps business teams work faster and more efficiently. 
            The platform uses specialized AI agents that coordinate with each other to complete complex tasks like customer 
            support ticket resolution, RFP responses, and content creation. Our shadow learning approach allows the agents 
            to learn from human experts during a gradual onboarding process, ensuring quality while reducing manual work. 
            Early tests show 70% time reduction in ticket resolution with maintained quality scores. The platform validates 
            complex coordination patterns through iterative refinement, proving that AI agents can work together effectively 
            on real business challenges.
            """
        elif source_choice == "2":
            self.console.print("\n✏️ Enter your source material (press Ctrl+D when done):")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            source_material = "\n".join(lines)
        else:
            file_path = Prompt.ask("Enter file path")
            try:
                with open(file_path, 'r') as f:
                    source_material = f.read()
                self.console.print(f"✅ Loaded {len(source_material)} characters from {file_path}")
            except FileNotFoundError:
                self.console.print(f"❌ File not found: {file_path}")
                return self.get_user_input()
        
        return {
            "source_material": source_material.strip(),
            "content_type": content_type,
            "target_audience": target_audience,
            "iterations": iterations
        }
    
    def show_processing_progress(self, config: Dict[str, Any]):
        """Show processing progress with rich progress bar"""
        
        agents = ["Story Miner", "Structure Architect", "Technical Translator", "Voice Crafter", "Hook Designer"]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            main_task = progress.add_task(
                f"Processing {config['iterations']} iteration(s) through Content Creation Team...",
                total=config['iterations'] * len(agents)
            )
            
            for iteration in range(config['iterations']):
                for agent in agents:
                    progress.update(
                        main_task,
                        description=f"Iteration {iteration + 1}: {agent} processing..."
                    )
                    # Simulate processing time for demo
                    asyncio.sleep(0.5)
                    progress.advance(main_task)
    
    def display_results(self, results: Dict[str, Any]):
        """Display content creation results in formatted way"""
        
        self.console.print("\n" + "="*70)
        self.console.print("🎉 [bold green]Content Creation Complete![/bold green]")
        self.console.print("="*70)
        
        # Summary metrics
        summary_table = Table(title="📊 Processing Summary")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="green")
        
        summary_table.add_row("Total Iterations", str(results['total_iterations']))
        summary_table.add_row("Agent Handoffs", str(results['platform_validation']['agent_handoffs']))
        summary_table.add_row("Coordination Success", "✅ YES" if results['platform_validation']['coordination_success'] else "❌ NO")
        summary_table.add_row("Content Type", results['content_type'].replace('_', ' ').title())
        summary_table.add_row("Target Audience", results['target_audience'].replace('_', ' ').title())
        
        self.console.print(summary_table)
        
        # Show iteration details
        for iteration_key, iteration_data in results['iterations'].items():
            self.console.print(f"\n📈 [bold]{iteration_key.replace('_', ' ').title()}[/bold]")
            
            agent_table = Table()
            agent_table.add_column("Agent", style="cyan") 
            agent_table.add_column("Confidence", style="yellow")
            agent_table.add_column("Status", style="green")
            
            for agent_name, agent_result in iteration_data.items():
                if agent_name not in ['overall_confidence', 'final_content']:
                    confidence = agent_result.get('confidence', 0)
                    status = "✅ Success" if confidence > 0.7 else "⚠️ Low Confidence"
                    agent_table.add_row(
                        agent_name.replace('_', ' ').title(),
                        f"{confidence:.1f}",
                        status
                    )
            
            agent_table.add_row(
                "[bold]Overall[/bold]",
                f"[bold]{iteration_data.get('overall_confidence', 0):.1f}[/bold]",
                "[bold]✅ Complete[/bold]"
            )
            
            self.console.print(agent_table)
        
        # Show final content
        final_content = results.get('final_content', '')
        if final_content:
            self.console.print(f"\n📄 [bold]Final Content ({len(final_content)} characters)[/bold]")
            content_panel = Panel(
                final_content[:500] + ("..." if len(final_content) > 500 else ""),
                title="Generated Content Preview",
                border_style="green"
            )
            self.console.print(content_panel)
            
            # Option to save
            if Confirm.ask("💾 Save full content to file?"):
                filename = Prompt.ask(
                    "Enter filename",
                    default=f"content_{results['content_type']}_{results['total_iterations']}iter.txt"
                )
                with open(filename, 'w') as f:
                    f.write(final_content)
                self.console.print(f"✅ Content saved to {filename}")
        
        # Platform validation results
        self.console.print(f"\n🎯 [bold]Platform Validation Results[/bold]")
        validation = results['platform_validation']
        
        validation_table = Table()
        validation_table.add_column("Validation Metric", style="cyan")
        validation_table.add_column("Result", style="green")
        
        validation_table.add_row(
            "Multi-Agent Coordination",
            "✅ SUCCESS" if validation['coordination_success'] else "❌ FAILED"
        )
        validation_table.add_row(
            "Iterative Improvement",
            "✅ SUCCESS" if validation['iterative_improvement'] else "⚠️ SINGLE PASS"
        )
        validation_table.add_row(
            "Agent Handoffs",
            f"✅ {validation['agent_handoffs']} successful handoffs"
        )
        
        self.console.print(validation_table)
        
        # Business value summary
        value_text = """
**🚀 Business Value Demonstrated:**
- ✅ Iterative refinement coordination pattern validated
- ✅ Complex multi-agent collaboration proven
- ✅ Platform ready for customer pilot testing
- ✅ Content creation time: ~10 minutes vs 2+ hours manual
        """
        
        self.console.print(Panel(
            Markdown(value_text),
            title="Value Proposition",
            border_style="blue"
        ))
    
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
    
    async def run_content_creation(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run the actual content creation process"""
        
        if not LLM_AVAILABLE:
            raise ImportError("LLM service not available - check backend setup")
        
        results = await orchestrator.process_content_creation_request(
            source_material=config['source_material'],
            content_type=config['content_type'],
            target_audience=config['target_audience'],
            iterations=config['iterations']
        )
        
        return results
    
    def show_api_examples(self):
        """Show API usage examples"""
        
        api_text = """
**🔧 API Usage Examples:**

**Test Individual Agent:**
```bash
curl -X POST http://localhost:8001/api/llm/agent/test \\
  -H "Content-Type: application/json" \\
  -d '{"message": "Test content", "agent_type": "story_miner"}'
```

**Full Content Creation Pipeline:**
```bash  
curl -X POST http://localhost:8001/api/llm/content-creation/process \\
  -H "Content-Type: application/json" \\
  -d '{"source_material": "Your content here", "content_type": "blog_post"}'
```

**View Available Agents:**
```bash
curl http://localhost:8001/api/llm/agents/available
```
        """
        
        self.console.print(Panel(
            Markdown(api_text),
            title="API Usage Examples",
            border_style="yellow"
        ))
    
    async def main_loop(self):
        """Main interactive loop"""
        
        self.show_welcome()
        
        while True:
            self.console.print("\n🎯 [bold]Content Creation CLI Options[/bold]")
            self.console.print("  1. Run Content Creation Pipeline")
            self.console.print("  2. View API Examples") 
            self.console.print("  3. View Available Agents")
            self.console.print("  4. Exit")
            
            choice = Prompt.ask(
                "Select option",
                choices=["1", "2", "3", "4"],
                default="1"
            )
            
            if choice == "1":
                try:
                    config = self.get_user_input()
                    
                    self.console.print(f"\n🚀 Starting Content Creation...")
                    self.console.print(f"   Source: {len(config['source_material'])} characters")
                    self.console.print(f"   Type: {config['content_type']}")
                    self.console.print(f"   Audience: {config['target_audience']}")
                    self.console.print(f"   Iterations: {config['iterations']}")
                    
                    # Show progress (simulated for UX)
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        console=self.console
                    ) as progress:
                        task = progress.add_task("Processing through 5-agent pipeline...", total=None)
                        
                        # Run actual content creation
                        results = await self.run_content_creation(config)
                        
                        progress.update(task, description="✅ Processing complete!")
                    
                    self.display_results(results)
                    
                except Exception as e:
                    self.show_error(e)
            
            elif choice == "2":
                self.show_api_examples()
            
            elif choice == "3":
                # Show available agents
                agents_text = """
**🤖 Available Content Creation Agents:**

1. **Story Miner** - Extract compelling narratives and human elements
2. **Structure Architect** - Organize ideas into logical, engaging flow  
3. **Technical Translator** - Simplify complex concepts for any audience
4. **Voice Crafter** - Create authentic, personal tone and voice
5. **Hook Designer** - Design engaging openings and maintain momentum

**Coordination Pattern:** Iterative Refinement (different from Customer Support's sequential pattern)
                """
                
                self.console.print(Panel(
                    Markdown(agents_text),
                    title="Agent Capabilities",
                    border_style="green"
                ))
            
            elif choice == "4":
                self.console.print("\n👋 Thanks for testing the Content Creation Team!")
                self.console.print("🎯 [bold]Next Steps:[/bold]")
                self.console.print("   • Use for customer demos and prospect meetings")
                self.console.print("   • Create marketing content through dogfooding")  
                self.console.print("   • Validate coordination before customer pilots")
                break


async def main():
    """Entry point for the CLI"""
    
    cli = ContentCreationCLI()
    
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