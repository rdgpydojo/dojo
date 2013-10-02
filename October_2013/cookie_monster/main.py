from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

import requests
# import ipdb
from bs4 import BeautifulSoup

javascript = '''window.setInterval((function nomify(){var shapes={"w_rect":["cookiemonstercrumbypicturesopen-o.gif","tumblr_mohxt1V6a91svhqpoo1_500.gif","tumblr_md0q05wMJb1rxis0k.gif","tumblr_ml0nmjWpX41snjjivo1_500.gif","cookie4.gif"],"t_rect":["CookieMonster-Sitting.jpg","487961_10150955894571587_1215263686_n.jpg","534767_10151516100086587_1790492047_n.jpg","patientmonster.png"],"square":["cookie_monster.jpg","935823_10151502554911587_1547641144_n.jpg","902502_10151355606796587_45192127_o.jpg","cookie-monster.jpg"]},img_path="http://downloads.cdn.sesame.org/sw/OmNomNomify/";function chooseImg(shape){return img_path+shapes[shape][Math.floor(Math.random()*shapes[shape].length)]}function getShape(h,w){return h===w?"square":h>w?"t_rect":"w_rect"}var imgs=document.getElementsByTagName("img"),img,h,w,shape;for(var i=0,len=imgs.length;i<len;i++){img=imgs[i],h=img.height,w=img.width,s=getShape(h,w);img.setAttribute("height",h);img.setAttribute("width",w);img.src=chooseImg(s)};return void 0;}), 10000)'''
bad_headers = {'connection', 'keep-alive', 'proxy-authenticate', 'proxy-authorization', 'te',
    'trailers', 'transfer-encoding', 'upgrade', 'content-length', 'content-encoding'}

def app(environ, start_response):
    # ipdb.set_trace()
    url = environ['RAW_URI']

    r = requests.get(url)
    status_message = requests.status_codes._codes[r.status_code][0].replace('_', ' ').upper()
    status_message = '{code} {message}'.format(
        code=r.status_code,
        message=status_message)

    sanitised_headers = [(name, value) for name, value in r.headers.items() if name not in bad_headers]
    start_response(status_message, sanitised_headers)

    if 'html' not in r.headers['content-type']:
        return r.content

    bs = BeautifulSoup(r.content, "html5lib")
    script = bs.new_tag('script')
    script.append(javascript)

    bs.head.append(script)

    return str(bs)

if __name__ == '__main__':
    httpd = make_server('', 8000, app)
    print "Serving on port 8000..."
    httpd.serve_forever()
