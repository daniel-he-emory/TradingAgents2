from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json


def create_market_analyst(llm, toolkit):

    def market_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]

        if toolkit.config["online_tools"]:
            tools = [
                toolkit.get_YFin_data_online,
                toolkit.get_stockstats_indicators_report_online,
            ]
        else:
            tools = [
                toolkit.get_YFin_data,
                toolkit.get_stockstats_indicators_report,
            ]

        system_message = (
            """You're a market analyst at an investment bank. Make it PUNCHY and VISUAL. Max 100-120 words.

**Format**:
📊 **The Story**: [1 sentence - what's happening with price]

**Signals** (3 only):
• 📈 **Trend**: Up/Down/Sideways + why in 3 words
• 🎯 **Entry**: Price level + why
• ⚠️ **Risk**: What could go wrong in 5 words

**Data Table** (REQUIRED):
| Metric | Value | Signal |
|--------|-------|--------|
| Price | $XXX | ✅/⚠️/🚨 |
| RSI | XX | ✅/⚠️/🚨 |
| 50MA | $XXX | ✅/⚠️/🚨 |

**Bottom Line**: [1 sentence - BUY/HOLD/SELL why]

**Rules**:
- Use emojis heavily (📈📉✅⚠️🚨💰)
- Numbers only, no explanations
- Investment banker pitch style
- Make it POP visually

Call get_YFin_data then get_stockstats_indicators_report_online."""
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to progress towards answering the question."
                    " If you are unable to fully answer, that's OK; another assistant with different tools"
                    " will help where you left off. Execute what you can to make progress."
                    " If you or any other assistant has the FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** or deliverable,"
                    " prefix your response with FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** so the team knows to stop."
                    " You have access to the following tools: {tool_names}.\n{system_message}"
                    "For your reference, the current date is {current_date}. The company we want to look at is {ticker}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(ticker=ticker)

        chain = prompt | llm.bind_tools(tools)

        result = chain.invoke(state["messages"])

        report = ""

        if len(result.tool_calls) == 0:
            report = result.content
       
        return {
            "messages": [result],
            "market_report": report,
        }

    return market_analyst_node
