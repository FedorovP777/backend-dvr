from typing import Callable


class ApiAuthMiddleware:
    async def handle(self, request: object, next_step: Callable[[object], None]) -> None:
        """Handle incoming HTTP request.

        Args:
            request: object
            next_step: Callable[[object], None]
        """
        next_step(request)
