from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any
import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

app = FastAPI(title="Trading Agents API", version="1.0.0")

# Initialize the trading graph
trading_graph = None

def get_trading_graph():
    """Get or create the trading graph instance."""
    global trading_graph
    if trading_graph is None:
        trading_graph = TradingAgentsGraph(config=DEFAULT_CONFIG)
    return trading_graph

class DebateLog(BaseModel):
    """Model for individual debate log entries."""
    round: int
    type: str  # 'bull', 'bear', or 'general'
    message: str

class AnalystReports(BaseModel):
    """Model for analyst reports."""
    market_report: str
    news_report: str
    sentiment_report: str
    technical_report: str

class RiskManagement(BaseModel):
    """Model for risk management data."""
    risky_summary: str
    safe_summary: str
    neutral_summary: str
    judge_decision: str
    final_recommendation: str

class TradingResponse(BaseModel):
    """Response model for trading decisions."""
    ticker: str
    date: str
    recommendation: str
    confidence: Optional[str] = None
    reasoning: str
    processed_signal: str
    
    # Extended fields
    analyst_reports: AnalystReports
    debate_logs: List[DebateLog]
    risk_management: RiskManagement
    
    # Individual risk summaries for backward compatibility
    risky_summary: str
    safe_summary: str
    neutral_summary: str

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Trading Agents API is running"}

@app.get("/trade", response_model=TradingResponse)
async def get_trade(
    ticker: str,
    date: str,
    deep_think_model: Optional[str] = Query(None),
    quick_think_model: Optional[str] = Query(None),
    debate_rounds: Optional[int] = Query(None),
):
    """
    Get trading decision for a given ticker and date, with optional model/round overrides.
    """
    try:
        # Validate date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        ta = get_trading_graph()
        result = ta.propagate(
            ticker,
            date,
            deep_think_model=deep_think_model,
            quick_think_model=quick_think_model,
            debate_rounds=debate_rounds,
        )
        
        # Create response using the extended result structure
        response = TradingResponse(
            ticker=ticker,
            date=date,
            recommendation=result.get("recommendation", ""),
            confidence=result.get("confidence", "Medium"),
            reasoning=result.get("reasoning", ""),
            processed_signal=result.get("processed_signal", ""),
            
            # Extended fields
            analyst_reports=AnalystReports(**result.get("analyst_reports", {
                "market_report": "",
                "news_report": "", 
                "sentiment_report": "",
                "technical_report": ""
            })),
            debate_logs=[DebateLog(**log) for log in result.get("debate_logs", [])],
            risk_management=RiskManagement(**result.get("risk_management", {
                "risky_summary": "",
                "safe_summary": "",
                "neutral_summary": "",
                "judge_decision": "",
                "final_recommendation": ""
            })),
            
            # Individual risk summaries for backward compatibility
            risky_summary=result.get("risky_summary", ""),
            safe_summary=result.get("safe_summary", ""),
            neutral_summary=result.get("neutral_summary", "")
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing trade decision: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Trading Agents API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)