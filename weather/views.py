from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def get_html_content(paysville):  
    import requests
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0"
    #LANGUAGE = "en-US,en;q=0.9"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    #session.headers['Accept-Language'] = LANGUAGE
    #session.headers['Content-Language'] = LANGUAGE
    paysville = paysville.replace(' ','+')
    headers = {'Accept-Language': 'fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5'}
    html_content = session.get('https://www.google.com/search?q=weather+in'+paysville, headers=headers).text
    return html_content

def home(request):
    weather_data = None
    if 'paysville' in request.GET:
        #Fetch weacther data
        paysville = request.GET.get("paysville")
        html_content = get_html_content(paysville)
        #print(html_content)
        from bs4 import BeautifulSoup 
        soup = BeautifulSoup(html_content, 'html.parser')
        weather_data = dict() 
        weather_data['region']=soup.find('div', attrs={'id':'wob_loc'}).text 
        weather_data['daytime'] = soup.find('div', attrs={'id':'wob_dts'}).text 
        weather_data['status'] = soup.find('span', attrs={'id':'wob_dc'}).text 
        weather_data['temp'] = soup.find('span', attrs={'id':'wob_tm'}).text 
        
        #print(region)
        
    return render(request,"weather/home.html", {'weather': weather_data})
    