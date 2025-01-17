from datetime import datetime

from rich.console import Console

from chatgpt_tool_hub.chains.api import APIChain
from chatgpt_tool_hub.models import build_model_params
from chatgpt_tool_hub.models.model_factory import ModelFactory
from chatgpt_tool_hub.tools.all_tool_list import main_tool_register
from chatgpt_tool_hub.tools.base_tool import BaseTool
from chatgpt_tool_hub.tools.meteo.docs_prompt import OPEN_METEO_DOCS

default_tool_name = "meteo-weather"


class MeteoWeatherTool(BaseTool):
    name: str = default_tool_name
    description: str = (
        "当你想要获取天气信息时应该使用本工具。"
        "你需要分析用户想要哪些天气信息，严谨地用自然语言描述问题，然后将该问题传入本工具。"
        "你最好能在输入末尾添加返回天气信息的粒度，支持：按时 或 按天，查询某天的天气优先用按时"
    )
    api_chain: APIChain = None

    def __init__(self, console: Console = Console(), **tool_kwargs):
        super().__init__(console=console, return_direct=False)
        llm = ModelFactory().create_llm_model(**build_model_params(tool_kwargs))
        self.api_chain = APIChain.from_llm_and_api_docs(llm, OPEN_METEO_DOCS, console=console)

    def _run(self, query: str) -> str:
        """Use the tool."""
        if not query:
            return "the input of tool is empty"
        if not self.api_chain:
            return "the tool was not initialized"

        query += f"\nThe current time is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} in UTC+8."

        return self.api_chain.run(query)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("MeteoWeatherTool does not support async")


main_tool_register.register_tool(default_tool_name, lambda console, kwargs: MeteoWeatherTool(console, **kwargs), [])
