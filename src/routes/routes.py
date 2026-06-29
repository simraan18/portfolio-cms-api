from fastapi import APIRouter


from src.routes import home_route, experience_route, card_category_route, card_route, profile_route, social_link_route

app_routes = APIRouter()

app_routes.include_router(home_route.route)
app_routes.include_router(experience_route.route)
app_routes.include_router(card_category_route.route)
app_routes.include_router(card_route.route)
app_routes.include_router(profile_route.route)
app_routes.include_router(social_link_route.route)