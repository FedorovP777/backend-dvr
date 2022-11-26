import copy
from typing import TypeVar, Sequence

T = TypeVar('T')


async def handle_middleware(request: T,
                            processing_middleware: Sequence[callable],
                            middleware_registry: dict,
                            middleware_groups_registry: dict) -> T:
    """Iterate over middleware sequence and run it.

    Args:
        processing_middleware:
        middleware_groups_registry:
        middleware_registry:
        request: T

    Returns:
        T
    """
    final_request = copy.copy(request)

    def set_request(modified_request: T) -> None:
        nonlocal final_request
        final_request = modified_request

    for middleware_alias in processing_middleware:
        if middleware_alias in middleware_groups_registry:
            for cls in middleware_groups_registry[middleware_alias]:
                await cls().handle(final_request, set_request)

        if middleware_alias in middleware_registry:
            cls = middleware_registry[middleware_alias]
            await cls().handle(final_request, set_request)
    return final_request
