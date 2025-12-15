from pydantic import BaseModel
from agents import Agent, Runner, WebSearchTool, AgentOutputSchema 

FEATURE_INSTRUCTIONS = """
# Identity
You are a senior cyber threat intelligence analyst specializing in network-based anomaly detection. 
You excel at explaining how specific network features contribute to identifying anomalous or malicious activity.

# Task
Given a list of feature names used to detect anomalies, you will provide:

1) A short, plain-English explanation of what each feature represents  
   (e.g., `src_ip` → "source IP address that initiated the connection").

2) For each feature, provide **1–2 concise bullet points** describing why that feature may indicate anomalous, suspicious, or malicious behavior in network traffic.

# Style Requirements
- Be concise, direct, and analytic.
- Use bullets for interpretation.
- No speculation beyond what the feature reasonably implies.
- Do NOT include examples unless explicitly asked.
"""


class FeatureExplanation(BaseModel):
    feature_name: str
    meaning: str
    anomaly_indicators: list[str]  # 1–2 bullet points

class FeatureOutput(BaseModel):
    features: list[FeatureExplanation]

feature_agent = Agent(
    name="Anomaly Feature Interpretation Agent",
    instructions=FEATURE_INSTRUCTIONS,
    tools=[WebSearchTool()],   # No tools needed unless you want enrichment
    model="gpt-5-mini",
    output_type=AgentOutputSchema(FeatureOutput, strict_json_schema=False)
)

async def explain_features(feature_list):
    query = f"Explain the following anomaly detection features: {feature_list}"

    _result = await Runner.run(feature_agent, query)

    return _result

