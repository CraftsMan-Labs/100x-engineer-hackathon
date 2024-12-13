from src.app.routers.customer_discovery import CustomerDiscoverer

async def get_customer_discoverer(topic:str):
    cd = CustomerDiscoverer(topic)
    rp = cd.discover()
    return rp.ideal_customer_profile["insights"]