from typing import Callable


class PrepareQueryParams:
    async def handle(self, request: object, next_step: Callable[[object], None]) -> None:
        """Handle incoming HTTP request.

        Args:
            request: object
            next_step: Callable[[object], None]
        """
        result = {}
        for key, value in request.query_arguments.items():
            if isinstance(value, list) and len(value) == 1:
                result[key] = value[0]
        request.query = result
        next_step(request)
