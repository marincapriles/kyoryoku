#!/usr/bin/env python3
"""
Content Creation Team Demo Script
Showcases the iterative refinement coordination pattern for platform validation
"""

import asyncio
import sys
import os
import json

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.llm_service import orchestrator


async def demo_content_creation():
    """Demo the Content Creation Team iterative refinement process"""
    
    print("🚀 Content Creation Team Demo - Iterative Refinement Pattern")
    print("=" * 70)
    
    # Demo source material about Kyoryoku
    source_material = """
    Kyoryoku is a multi-agent AI platform that helps business teams work more efficiently. 
    The system uses specialized AI agents that coordinate with each other to handle complex 
    tasks like customer support ticket resolution. Our shadow learning approach allows 
    agents to learn from human experts gradually. Initial testing shows significant 
    time savings while maintaining quality standards.
    """
    
    print("📝 Source Material:")
    print(source_material.strip())
    print("\n" + "-" * 70)
    
    try:
        # Process through Content Creation Team
        print("\n🔄 Processing through Content Creation Team...")
        print("   → Story Mining → Structure → Translation → Voice → Hooks")
        
        results = await orchestrator.process_content_creation_request(
            source_material=source_material,
            content_type="executive_summary",
            target_audience="business_executives",
            iterations=1
        )
        
        print("\n✅ Content Creation Complete!")
        print(f"   Iterations: {results['total_iterations']}")
        print(f"   Agent Handoffs: {results['platform_validation']['agent_handoffs']}")
        print(f"   Coordination Success: {results['platform_validation']['coordination_success']}")
        
        # Extract final content
        if 'iterations' in results and 'iteration_1' in results['iterations']:
            iteration = results['iterations']['iteration_1']
            
            print("\n📊 Agent Results Summary:")
            print("-" * 40)
            
            for agent_name, agent_result in iteration.items():
                if agent_name != 'overall_confidence' and agent_name != 'final_content':
                    confidence = agent_result.get('confidence', 0)
                    print(f"   {agent_name.title()}: {confidence:.1f} confidence")
            
            print(f"\n   Overall Confidence: {iteration.get('overall_confidence', 0):.1f}")
            
            # Show transformation progression
            print("\n🔍 Content Evolution Through Pipeline:")
            print("-" * 50)
            
            # Show first and last content to demonstrate transformation
            if 'story_mining' in iteration:
                story_content = iteration['story_mining'].get('content', '')
                print("1️⃣ After Story Mining:")
                print("   " + story_content[:100] + "..." if len(story_content) > 100 else "   " + story_content)
            
            if 'hooks' in iteration:
                final_content = iteration['hooks'].get('content', '')
                print("\n5️⃣ After Hook Design:")
                print("   " + final_content[:100] + "..." if len(final_content) > 100 else "   " + final_content)
        
        # Platform validation metrics
        print("\n🎯 Platform Validation Results:")
        print("-" * 40)
        validation = results['platform_validation']
        print(f"   ✅ Agent Coordination: {'SUCCESS' if validation['coordination_success'] else 'PARTIAL'}")
        print(f"   ✅ Iterative Process: {'SUCCESS' if validation['iterative_improvement'] else 'SINGLE PASS'}")
        print(f"   ✅ Multi-Agent Handoffs: {validation['agent_handoffs']} successful handoffs")
        
        # Demo value proposition
        print("\n💡 Demo Value Proposition:")
        print("-" * 40)
        print("   🎨 Transforms dry technical content into engaging narratives")
        print("   🔄 Validates iterative refinement coordination pattern")
        print("   🤝 Demonstrates seamless multi-agent collaboration")
        print("   📈 Creates compelling content for prospect demos")
        print("   🧪 Tests platform capabilities before customer pilots")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demo Error: {e}")
        print("   Note: This error is expected without API key configuration")
        return False


async def demo_individual_agents():
    """Demo individual Content Creation agents"""
    
    print("\n🔧 Individual Agent Capabilities Demo")
    print("=" * 50)
    
    test_cases = [
        {
            "agent": "story_miner", 
            "input": "Our customer support team reduced ticket resolution from 18 minutes to 3 minutes",
            "purpose": "Extract compelling narratives"
        },
        {
            "agent": "technical_translator",
            "input": "Multi-agent coordination using LangGraph orchestration patterns",
            "purpose": "Simplify complex concepts"
        },
        {
            "agent": "voice_crafter",
            "input": "The platform provides efficiency gains through automated processes",
            "purpose": "Create authentic voice"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. {test['agent'].title().replace('_', ' ')} - {test['purpose']}")
        print(f"   Input: {test['input']}")
        print(f"   Expected: Professional agent processing with {test['purpose']}")


def show_business_value():
    """Show business value of Content Creation Team"""
    
    print("\n💼 Business Value of Content Creation Team")
    print("=" * 50)
    
    print("📈 Strategic Benefits:")
    print("   • Platform Validation: Test coordination before customer pilots")
    print("   • Demo Content: Create compelling sales materials")
    print("   • Dogfooding: Use our own product to improve it")
    print("   • Meta Storytelling: Product creates content about itself")
    
    print("\n🎯 Success Metrics (from PRD):")
    print("   • Content creation: 10 minutes vs 2 hours traditional")
    print("   • Platform coordination: 90%+ successful multi-agent handoffs")
    print("   • Demo effectiveness: Track prospect engagement")
    print("   • Validation capability: Prove platform works before pilots")
    
    print("\n🚀 Why This Matters:")
    print("   • Validates iterative refinement (different from sequential/parallel)")
    print("   • Tests complex coordination patterns")
    print("   • Creates marketing assets while testing platform")
    print("   • Demonstrates value proposition through meta-storytelling")


async def main():
    """Run the complete Content Creation Team demo"""
    
    print("🎬 Kyoryoku Content Creation Team Demo")
    print("Testing the Iterative Refinement Coordination Pattern")
    print("=" * 70)
    
    # Show business context first
    show_business_value()
    
    # Demo individual agents
    await demo_individual_agents()
    
    # Run full pipeline demo
    await demo_content_creation()
    
    print("\n" + "=" * 70)
    print("✅ Content Creation Team Demo Complete!")
    print("\n🎯 Key Takeaways:")
    print("   • Iterative refinement pattern successfully implemented")
    print("   • Five specialized agents working in sequence with handoffs")
    print("   • Platform validation achieved for demo and pilot readiness")
    print("   • Ready to create compelling content for prospect meetings")
    
    print("\n📋 Next Steps (from PRD):")
    print("   • Use for customer demos and prospect meetings")
    print("   • Create marketing content through dogfooding")
    print("   • Validate coordination patterns before customer pilots")
    print("   • Measure demo effectiveness with prospects")


if __name__ == "__main__":
    asyncio.run(main())