from bs4 import BeautifulSoup
import requests
from lxml.etree import HTML
import re
import re
import json
import time
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
url='https://product.suning.com/0000000000/161937059.html'
res=requests.get(url).text
type=re.findall('型号</span> </div> </td> <td class="val">(.*?)</td>',res)[0]
print(type)