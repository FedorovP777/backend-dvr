from app.main.middleware.prepare_query_params import PrepareQueryParams
from app.main.middleware.validate_country_middleware import ValidateCountryMiddleware
from app.main.middleware.api_auth_middleware import ApiAuthMiddleware

middleware = {
    'api_auth': ApiAuthMiddleware,
    'validate_country': ValidateCountryMiddleware,
    'prepare_query_params': PrepareQueryParams,
}
middleware_group = {'web': [
    PrepareQueryParams
], 'api': [
    PrepareQueryParams
]}
