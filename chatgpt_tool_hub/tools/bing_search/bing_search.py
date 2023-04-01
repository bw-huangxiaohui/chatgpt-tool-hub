"""Tool for the Bing search API."""

from chatgpt_tool_hub.tools.base_tool import BaseTool
from chatgpt_tool_hub.tools.bing_search.wrapper import BingSearchAPIWrapper


class BingSearch(BaseTool):
    """Tool that adds the capability to query the Bing search API.

    In order to set this up, follow instructions at:
    https://levelup.gitconnected.com/api-tutorial-how-to-use-bing-web-search-api-in-python-4165d5592a7e
    """

    name = "Bing Search"
    description = (
        "A wrapper around Bing Search. "
        "Useful for when you need to answer questions about current events. "
        "Input should be a search query."
    )
    api_wrapper: BingSearchAPIWrapper

    def _run(self, query: str) -> str:
        """Use the tool."""
        return self.api_wrapper.run(query)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("BingSearch does not support async")
