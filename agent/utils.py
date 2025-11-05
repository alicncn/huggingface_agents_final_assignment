"""
Error handling and logging utilities for the agent.
"""
import logging
import traceback
from typing import Optional, Dict, Any
from datetime import datetime


class AgentLogger:
    """Enhanced logger for agent operations."""
    
    def __init__(self, name: str = "agent"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create console handler
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def log_tool_usage(self, tool_name: str, params: Dict[str, Any], success: bool = True):
        """Log tool usage."""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"Tool [{tool_name}] - {status} - Params: {list(params.keys())}")
    
    def log_error(self, error: Exception, context: Optional[str] = None):
        """Log an error with full traceback."""
        error_msg = f"Error"
        if context:
            error_msg += f" in {context}"
        error_msg += f": {str(error)}"
        
        self.logger.error(error_msg)
        self.logger.debug(traceback.format_exc())
    
    def log_agent_decision(self, decision: str, reason: Optional[str] = None):
        """Log agent decision making."""
        msg = f"Agent Decision: {decision}"
        if reason:
            msg += f" - Reason: {reason}"
        self.logger.info(msg)
    
    def log_state_update(self, state_key: str, value: Any):
        """Log state updates."""
        self.logger.debug(f"State Update: {state_key} = {value}")


class ErrorHandler:
    """Error handling utilities."""
    
    @staticmethod
    def safe_execute(func, *args, error_message: str = "Operation failed", **kwargs):
        """
        Safely execute a function with error handling.
        
        Args:
            func: Function to execute
            *args: Positional arguments
            error_message: Custom error message
            **kwargs: Keyword arguments
            
        Returns:
            Tuple of (result, error) where error is None on success
        """
        try:
            result = func(*args, **kwargs)
            return result, None
        except Exception as e:
            return None, f"{error_message}: {str(e)}"
    
    @staticmethod
    def format_error(error: Exception, include_traceback: bool = False) -> str:
        """
        Format an error message.
        
        Args:
            error: The exception
            include_traceback: Whether to include full traceback
            
        Returns:
            Formatted error string
        """
        error_msg = f"{type(error).__name__}: {str(error)}"
        if include_traceback:
            error_msg += f"\n\n{traceback.format_exc()}"
        return error_msg
    
    @staticmethod
    def is_retryable_error(error: Exception) -> bool:
        """
        Determine if an error is retryable.
        
        Args:
            error: The exception to check
            
        Returns:
            True if the error might be resolved by retrying
        """
        retryable_errors = [
            "timeout",
            "connection",
            "network",
            "rate limit",
            "temporarily unavailable"
        ]
        
        error_str = str(error).lower()
        return any(keyword in error_str for keyword in retryable_errors)


class PerformanceMonitor:
    """Monitor agent performance metrics."""
    
    def __init__(self):
        self.metrics = {
            "tool_calls": 0,
            "errors": 0,
            "start_time": datetime.now(),
            "tool_usage": {},
            "error_types": {}
        }
    
    def record_tool_call(self, tool_name: str):
        """Record a tool call."""
        self.metrics["tool_calls"] += 1
        if tool_name not in self.metrics["tool_usage"]:
            self.metrics["tool_usage"][tool_name] = 0
        self.metrics["tool_usage"][tool_name] += 1
    
    def record_error(self, error: Exception):
        """Record an error."""
        self.metrics["errors"] += 1
        error_type = type(error).__name__
        if error_type not in self.metrics["error_types"]:
            self.metrics["error_types"][error_type] = 0
        self.metrics["error_types"][error_type] += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        runtime = (datetime.now() - self.metrics["start_time"]).total_seconds()
        
        return {
            "runtime_seconds": runtime,
            "total_tool_calls": self.metrics["tool_calls"],
            "total_errors": self.metrics["errors"],
            "success_rate": (
                (self.metrics["tool_calls"] - self.metrics["errors"]) / 
                max(self.metrics["tool_calls"], 1)
            ) * 100,
            "most_used_tools": sorted(
                self.metrics["tool_usage"].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5],
            "error_breakdown": self.metrics["error_types"]
        }
    
    def print_summary(self):
        """Print performance summary."""
        summary = self.get_summary()
        
        print("\n" + "="*70)
        print("PERFORMANCE SUMMARY")
        print("="*70)
        print(f"Runtime: {summary['runtime_seconds']:.2f} seconds")
        print(f"Tool Calls: {summary['total_tool_calls']}")
        print(f"Errors: {summary['total_errors']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        
        if summary['most_used_tools']:
            print("\nMost Used Tools:")
            for tool, count in summary['most_used_tools']:
                print(f"  • {tool}: {count} calls")
        
        if summary['error_breakdown']:
            print("\nError Breakdown:")
            for error_type, count in summary['error_breakdown'].items():
                print(f"  • {error_type}: {count}")
        
        print("="*70)


# Global instances
agent_logger = AgentLogger("agent")
error_handler = ErrorHandler()
performance_monitor = PerformanceMonitor()
