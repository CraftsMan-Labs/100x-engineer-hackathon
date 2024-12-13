from src.app.routers.market_analysis import MarketAnalyzer
import base64
from io import BytesIO
from PIL import Image

# convert base64 to image
def base64_to_image(base64_string):
    imgdata = base64.b64decode(base64_string)
    return BytesIO(imgdata)

async def get_market_report(analysis_topic:str):
    ma = MarketAnalyzer()
    res = ma.breakdown_problem(analysis_topic)
    tg = await ma.generate_trend_visualization()
    img_tg = ma.visualize_trend(tg)
    
    #Get Image
    img = base64_to_image(img_tg['img'])
    # display image
    
    ma.perform_analysis()
    report = ma.compile_comprehensive_report()
    final_report = ma.get_report()
    return final_report.comprehensive_report, img