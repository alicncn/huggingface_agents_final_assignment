"""Data analysis tools using Pandas for processing files and data."""
import os
import pandas as pd
from typing import Optional, List
from langchain_core.tools import tool
import io


@tool
def read_excel_file(file_path: str, sheet_name: Optional[str] = None) -> str:
    """
    Read an Excel file and return its contents.
    
    Args:
        file_path: Path to the Excel file (.xlsx, .xls)
        sheet_name: Optional sheet name to read (default: first sheet)
    
    Returns:
        Summary of the Excel data including columns and first few rows
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"
        
        # Read the Excel file
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            df = pd.read_excel(file_path)
        
        # Create summary
        summary = []
        summary.append(f"Excel file: {file_path}")
        summary.append(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        summary.append(f"\nColumns: {', '.join(df.columns.tolist())}")
        summary.append(f"\nFirst 5 rows:")
        summary.append(df.head().to_string())
        
        # Add data types
        summary.append(f"\nData types:")
        summary.append(df.dtypes.to_string())
        
        return "\n".join(summary)
        
    except Exception as e:
        return f"Error reading Excel file: {str(e)}"


@tool
def read_csv_file(file_path: str, delimiter: str = ",") -> str:
    """
    Read a CSV file and return its contents.
    
    Args:
        file_path: Path to the CSV file
        delimiter: Delimiter used in the CSV (default: comma)
    
    Returns:
        Summary of the CSV data including columns and first few rows
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"
        
        # Read the CSV file
        df = pd.read_csv(file_path, delimiter=delimiter)
        
        # Create summary
        summary = []
        summary.append(f"CSV file: {file_path}")
        summary.append(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        summary.append(f"\nColumns: {', '.join(df.columns.tolist())}")
        summary.append(f"\nFirst 5 rows:")
        summary.append(df.head().to_string())
        
        return "\n".join(summary)
        
    except Exception as e:
        return f"Error reading CSV file: {str(e)}"


@tool
def analyze_excel_data(file_path: str, query: str) -> str:
    """
    Analyze Excel data based on a natural language query.
    
    Args:
        file_path: Path to the Excel file
        query: Natural language query (e.g., "sum sales by category", "filter rows where price > 100")
    
    Returns:
        Result of the analysis
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"
        
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        # Convert query to lowercase for easier parsing
        query_lower = query.lower()
        
        result = []
        result.append(f"Analyzing: {file_path}")
        result.append(f"Query: {query}\n")
        
        # Handle common operations
        if "sum" in query_lower:
            # Find the column to sum
            for col in df.columns:
                if col.lower() in query_lower:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        total = df[col].sum()
                        result.append(f"Sum of '{col}': {total}")
        
        elif "count" in query_lower or "how many" in query_lower:
            result.append(f"Total rows: {len(df)}")
            
        elif "average" in query_lower or "mean" in query_lower:
            for col in df.columns:
                if col.lower() in query_lower:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        avg = df[col].mean()
                        result.append(f"Average of '{col}': {avg}")
        
        elif "group by" in query_lower or "by category" in query_lower or "by" in query_lower:
            # Try to find grouping column
            group_col = None
            value_col = None
            
            for col in df.columns:
                if "category" in col.lower() or "type" in col.lower() or "group" in col.lower():
                    group_col = col
                if "sales" in col.lower() or "amount" in col.lower() or "value" in col.lower():
                    value_col = col
            
            if group_col and value_col:
                grouped = df.groupby(group_col)[value_col].sum()
                result.append(f"\nGrouped by '{group_col}':")
                result.append(grouped.to_string())
        
        elif "filter" in query_lower or "where" in query_lower:
            # Show available columns for filtering
            result.append("Available columns for filtering:")
            result.append(", ".join(df.columns.tolist()))
            result.append("\nPlease use execute_python_code for complex filtering")
        
        else:
            # General statistics
            result.append("Summary statistics:")
            result.append(df.describe().to_string())
        
        if len(result) == 2:  # Only header and query
            result.append("Could not parse query. Available columns:")
            result.append(", ".join(df.columns.tolist()))
        
        return "\n".join(result)
        
    except Exception as e:
        return f"Error analyzing Excel data: {str(e)}"


@tool
def filter_excel_data(file_path: str, column: str, condition: str, value: str) -> str:
    """
    Filter Excel data based on a condition.
    
    Args:
        file_path: Path to the Excel file
        column: Column name to filter on
        condition: Condition operator (>, <, ==, !=, contains)
        value: Value to compare against
    
    Returns:
        Filtered data results
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"
        
        df = pd.read_excel(file_path)
        
        if column not in df.columns:
            return f"Error: Column '{column}' not found. Available: {', '.join(df.columns)}"
        
        # Apply filter based on condition
        if condition == ">":
            filtered_df = df[df[column] > float(value)]
        elif condition == "<":
            filtered_df = df[df[column] < float(value)]
        elif condition == "==":
            # Try numeric first, then string
            try:
                filtered_df = df[df[column] == float(value)]
            except:
                filtered_df = df[df[column] == value]
        elif condition == "!=":
            try:
                filtered_df = df[df[column] != float(value)]
            except:
                filtered_df = df[df[column] != value]
        elif condition == "contains":
            filtered_df = df[df[column].astype(str).str.contains(value, case=False)]
        else:
            return f"Error: Unknown condition '{condition}'. Use: >, <, ==, !=, contains"
        
        result = []
        result.append(f"Filter: {column} {condition} {value}")
        result.append(f"Matches found: {len(filtered_df)} rows")
        result.append(f"\nFiltered data:")
        result.append(filtered_df.to_string())
        
        return "\n".join(result)
        
    except Exception as e:
        return f"Error filtering data: {str(e)}"


@tool
def calculate_from_excel(file_path: str, operation: str, column: str) -> str:
    """
    Perform calculations on Excel data.
    
    Args:
        file_path: Path to the Excel file
        operation: Operation to perform (sum, average, max, min, count)
        column: Column name to operate on
    
    Returns:
        Calculation result
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"
        
        df = pd.read_excel(file_path)
        
        if column not in df.columns:
            return f"Error: Column '{column}' not found. Available: {', '.join(df.columns)}"
        
        operation_lower = operation.lower()
        
        if operation_lower == "sum":
            result = df[column].sum()
        elif operation_lower in ["average", "mean"]:
            result = df[column].mean()
        elif operation_lower == "max":
            result = df[column].max()
        elif operation_lower == "min":
            result = df[column].min()
        elif operation_lower == "count":
            result = df[column].count()
        else:
            return f"Error: Unknown operation '{operation}'. Use: sum, average, max, min, count"
        
        return f"{operation.capitalize()} of '{column}': {result}"
        
    except Exception as e:
        return f"Error calculating: {str(e)}"
