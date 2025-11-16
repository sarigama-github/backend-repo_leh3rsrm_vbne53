import os
from typing import List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="ROQET API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Models ----------
class NewsItem(BaseModel):
    id: str
    title: str
    summary: str
    timeframe: str  # "short" | "long"
    tags: List[str] = []
    source: Optional[str] = None

class ToolItem(BaseModel):
    id: str
    name: str
    purpose: str
    when_to_use: str
    best_practices: List[str] = []
    level: str  # Launchpad, Pre-Launch, Ignition, Ascent, Orbit

class CourseLesson(BaseModel):
    id: str
    title: str
    objectives: List[str]
    level: str

class CourseStage(BaseModel):
    key: str
    title: str
    description: str
    lessons: List[CourseLesson]

# ---------- Root & Health ----------
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

# ---------- Sample Data Endpoints (static for prototype) ----------
@app.get("/api/news", response_model=List[NewsItem])
def get_news():
    return [
        NewsItem(
            id="n1",
            title="CPI prints inline; initial risk-on reaction fades",
            summary="Inflation meets expectations. Short-term relief rally, but trend depends on upcoming labor data.",
            timeframe="short",
            tags=["macro", "inflation", "usd"],
            source="ROQET Brief"
        ),
        NewsItem(
            id="n2",
            title="Central bank signals higher-for-longer stance",
            summary="Policy path suggests slower cuts. Watch yield curve and credit conditions over the next quarter.",
            timeframe="long",
            tags=["rates", "bonds"],
            source="ROQET Macro"
        ),
        NewsItem(
            id="n3",
            title="Earnings season: dispersion favors stock-pickers",
            summary="Mixed beats and margin pressures. Focus on relative strength and post-earnings drift.",
            timeframe="short",
            tags=["equities", "earnings"],
            source="ROQET Desk"
        ),
    ]

@app.get("/api/tools", response_model=List[ToolItem])
def get_tools():
    return [
        ToolItem(
            id="position-sizer",
            name="Position Sizer",
            purpose="Calculate position size based on account risk and stop distance.",
            when_to_use="Before placing any trade.",
            best_practices=[
                "Risk a fixed % per trade (e.g., 0.5%–1.0%).",
                "Recompute after equity changes.",
                "Use worst-case spread/slippage in stop distance.",
            ],
            level="Pre-Launch",
        ),
        ToolItem(
            id="trade-journal",
            name="Trade Journal",
            purpose="Log setups, context, execution, and outcomes to measure edge.",
            when_to_use="Immediately after each trade.",
            best_practices=[
                "Tag by setup and market regime.",
                "Record reasons for exit, not just P/L.",
                "Review weekly for patterns and mistakes.",
            ],
            level="Ascent",
        ),
        ToolItem(
            id="regime-scanner",
            name="Regime Scanner",
            purpose="Gauge trend/chop/volatility regime before selecting tactics.",
            when_to_use="Daily pre-market and before new positions.",
            best_practices=[
                "Match strategy to regime (don’t force trades).",
                "Recheck on major news days.",
                "Stand down in unclear signals.",
            ],
            level="Mission Control",
        ),
    ]

@app.get("/api/course-map", response_model=List[CourseStage])
def get_course_map():
    return [
        CourseStage(
            key="launchpad",
            title="Launchpad",
            description="Core concepts, platforms, and execution basics.",
            lessons=[
                CourseLesson(id="L1", title="Market Basics: How Prices Move", objectives=["Bid/ask, spread", "Order types: market/limit/stop"], level="Launchpad"),
                CourseLesson(id="L2", title="Platforms & Orders", objectives=["Placing orders correctly", "Fees and slippage"], level="Launchpad"),
            ],
        ),
        CourseStage(
            key="prelaunch",
            title="Pre-Launch Checks",
            description="Risk, psychology, and planning.",
            lessons=[
                CourseLesson(id="P1", title="Risk per Trade", objectives=["Fixed % risk", "Stop placement"], level="Pre-Launch"),
                CourseLesson(id="P2", title="Flight Plan: Trade Plan", objectives=["Criteria, invalidation", "Scenarios"], level="Pre-Launch"),
            ],
        ),
        CourseStage(
            key="ignition",
            title="Ignition",
            description="Starter strategies and first live trades.",
            lessons=[
                CourseLesson(id="I1", title="Breakout + Retest", objectives=["Context filter", "Execution checklist"], level="Ignition"),
                CourseLesson(id="I2", title="Mean Reversion in Range", objectives=["Identify range", "Risk control"], level="Ignition"),
            ],
        ),
        CourseStage(
            key="ascent",
            title="Ascent",
            description="System-building and backtesting.",
            lessons=[
                CourseLesson(id="A1", title="Building a Playbook", objectives=["Setup templates", "Criteria & invalidations"], level="Ascent"),
                CourseLesson(id="A2", title="Backtest Basics", objectives=["Sample size", "Bias control"], level="Ascent"),
            ],
        ),
        CourseStage(
            key="orbit",
            title="Orbit",
            description="Advanced consistency and scaling.",
            lessons=[
                CourseLesson(id="O1", title="Scaling Risk", objectives=["Risk scaling rules", "Drawdown limits"], level="Orbit"),
                CourseLesson(id="O2", title="Regime Detection", objectives=["Macro + micro filters", "Adaptation"], level="Orbit"),
            ],
        ),
    ]

# ---------- Database Connectivity Test (provided scaffold) ----------
@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        from database import db
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
