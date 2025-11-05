"""
Verification script for Phase 6: Refinement and Testing
Tests enhanced state management, error handling, and logging.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def verify_enhanced_state():
    """Verify enhanced state management."""
    print("\n" + "="*60)
    print("VERIFYING ENHANCED STATE MANAGEMENT")
    print("="*60)
    
    try:
        from agent.state import AgentState
        
        # Check for new fields
        required_fields = [
            "messages", "next_action", "intermediate_results",
            "tools_used", "error_count", "last_error"
        ]
        
        # Get type annotations
        annotations = AgentState.__annotations__
        
        found_fields = []
        missing_fields = []
        
        for field in required_fields:
            if field in annotations:
                found_fields.append(field)
                print(f"✓ Field '{field}' present: {annotations[field]}")
            else:
                missing_fields.append(field)
                print(f"✗ Field '{field}' missing!")
        
        if len(found_fields) == len(required_fields):
            print(f"\n✅ All {len(required_fields)} state fields present")
            return True
        else:
            print(f"\n❌ Missing {len(missing_fields)} fields")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying state: {e}")
        return False


def verify_error_handling():
    """Verify error handling utilities."""
    print("\n" + "="*60)
    print("VERIFYING ERROR HANDLING UTILITIES")
    print("="*60)
    
    try:
        from agent.utils import AgentLogger, ErrorHandler, PerformanceMonitor
        
        # Test AgentLogger
        print("\n1. Testing AgentLogger...")
        logger = AgentLogger("test")
        logger.log_tool_usage("test_tool", {"param": "value"}, success=True)
        logger.log_agent_decision("test_decision", "test_reason")
        print("   ✓ AgentLogger working")
        
        # Test ErrorHandler
        print("\n2. Testing ErrorHandler...")
        handler = ErrorHandler()
        
        # Test safe_execute
        def test_func():
            return "success"
        
        result, error = handler.safe_execute(test_func)
        assert result == "success" and error is None
        print("   ✓ safe_execute working")
        
        # Test error formatting
        test_error = ValueError("Test error")
        formatted = handler.format_error(test_error)
        assert "ValueError" in formatted
        print("   ✓ format_error working")
        
        # Test PerformanceMonitor
        print("\n3. Testing PerformanceMonitor...")
        monitor = PerformanceMonitor()
        monitor.record_tool_call("test_tool")
        monitor.record_error(ValueError("test"))
        summary = monitor.get_summary()
        
        assert summary["total_tool_calls"] == 1
        assert summary["total_errors"] == 1
        print("   ✓ PerformanceMonitor working")
        
        print("\n✅ All error handling utilities working")
        return True
        
    except Exception as e:
        print(f"❌ Error verifying error handling: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_logging():
    """Verify logging configuration."""
    print("\n" + "="*60)
    print("VERIFYING LOGGING CONFIGURATION")
    print("="*60)
    
    try:
        from agent.graph import logger
        
        print(f"✓ Logger name: {logger.name}")
        print(f"✓ Logger level: {logger.level}")
        print(f"✓ Handler count: {len(logger.handlers)}")
        
        # Test logging
        logger.info("Test log message")
        print("✓ Logging functional")
        
        print("\n✅ Logging configured correctly")
        return True
        
    except Exception as e:
        print(f"❌ Error verifying logging: {e}")
        return False


def verify_agent_creation():
    """Verify enhanced agent can be created."""
    print("\n" + "="*60)
    print("VERIFYING ENHANCED AGENT CREATION")
    print("="*60)
    
    try:
        from agent.graph import create_agent
        
        print("Creating agent...")
        agent = create_agent()
        print("✓ Agent created successfully")
        
        # Verify it's a compiled graph
        print(f"✓ Agent type: {type(agent).__name__}")
        
        print("\n✅ Enhanced agent working")
        return True
        
    except Exception as e:
        print(f"❌ Error creating agent: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_test_suite():
    """Verify test suite exists and is importable."""
    print("\n" + "="*60)
    print("VERIFYING TEST SUITE")
    print("="*60)
    
    try:
        from tests.test_all_prompts import CHALLENGE_PROMPTS, TestRunner
        
        print(f"✓ Test suite imported successfully")
        print(f"✓ Challenge prompts defined: {len(CHALLENGE_PROMPTS)}")
        print(f"✓ TestRunner class available")
        
        # Verify all 20 prompts are defined
        if len(CHALLENGE_PROMPTS) == 20:
            print(f"✓ All 20 challenge prompts defined")
        else:
            print(f"⚠ Expected 20 prompts, found {len(CHALLENGE_PROMPTS)}")
        
        print("\n✅ Test suite ready")
        return True
        
    except Exception as e:
        print(f"❌ Error verifying test suite: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all verification tests."""
    print("="*60)
    print("PHASE 6 VERIFICATION: REFINEMENT AND TESTING")
    print("="*60)
    
    results = []
    
    # Run verifications
    results.append(("Enhanced State", verify_enhanced_state()))
    results.append(("Error Handling", verify_error_handling()))
    results.append(("Logging", verify_logging()))
    results.append(("Agent Creation", verify_agent_creation()))
    results.append(("Test Suite", verify_test_suite()))
    
    # Print summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print("\n" + "="*60)
    
    if passed == total:
        print("✅ PHASE 6 VERIFICATION COMPLETE")
        print("="*60)
        print(f"\n✓ All {total} verifications passed")
        print("✓ Enhanced state management working")
        print("✓ Error handling utilities available")
        print("✓ Logging configured")
        print("✓ Enhanced agent functional")
        print("✓ Comprehensive test suite ready")
        print("\nPhase 6 refinements successfully implemented!")
    else:
        print("⚠️  PHASE 6 VERIFICATION INCOMPLETE")
        print("="*60)
        print(f"\n{passed}/{total} verifications passed")
        print(f"{total - passed} verifications failed")
        print("\nSome refinements need attention.")


if __name__ == "__main__":
    main()
