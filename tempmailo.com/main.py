import requests

url = 'https://tempmailo.com/changemail'
params = {
    'tmail': 'pejutaqa@thetechnext.net',
    '_r': '0.5222617632121644'
}
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.6',
    'Cookie': '.AspNetCore.Antiforgery.dXyz_uFU2og=CfDJ8FIvWmWpDrJBnHLgyo7S7nEgtATD4_l_48NrgdCleZLhZng52uw1_wGLGzIjjT1QWhAtpRAKi8aWg9R46S7YQl7PmVp1GudRsgTsn7cOzedK_i4znMswMj7-MqOjcjxzMTc03EG79OPzV2acX0R_QJU; _ym_isad=1; cf_clearance=Y3wfxulAoBmYV7IGJQfHOiYC1oT6Q8miTsygDcRJ93A-1741968724-1.2.1.1-9WykTexvlN9mOVnTZZ8t1aMECZwBa_h7do.4sai8w7w2ykUgEB4yl43UmoRi39vYF2ivtXgPSKNNQV3qSZEjNnTPhAwkBh_momSsZv_ynQetP7_1UL3wUGRwWppA92E5logr1lxBcVo9tdnDYRatZ_hXCOrPIKRwkJPSbLHnx_P6Ho_zynq72XmZNWRYGPmZ03Y1ZGWyo8jPZU9QaD8ltuRlXZ_5GUosdHuaSXEnLgWoYYjvOgUoK_.rm1dD3Ds8405aYVcGqZ3mleBG72apseeT70YbKrL_d5D6e0MQFV5ePeSTGPcfNYGbMJUKKH7N0y4D2kDqbA0ZIq2BKv.hqiVZx5vfLug5BebI2CFqkXY',
    'priority': 'u=1, i',
    'referer': 'https://tempmailo.com/',
    'requestverificationtoken': 'CfDJ8FIvWmWpDrJBnHLgyo7S7nGB4-mXV5gADh2xlPpAA1SEtNjIzW7dRCZCXQCp6LcwBoAx_WCWIXaAoXRZtoE7hqGl6tB-pbCHmNI69Nbg3i3vBTDzYWeRn6FEktFk41EC4SnNRAT0-D-9UkcFC7yUBs4',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Brave";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

response = requests.get(url, params=params, headers=headers)
print(response.text)
