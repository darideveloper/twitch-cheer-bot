<div><a href='https://github.com/darideveloper/twitch-cheer-bot/blob/master/LICENSE' target='_blank'>
            <img src='https://img.shields.io/github/license/darideveloper/twitch-cheer-bot.svg?style=for-the-badge' alt='MIT License' height='30px'/>
        </a><a href='https://www.linkedin.com/in/francisco-dari-hernandez-6456b6181/' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=LinkedIn&color=0A66C2&logo=LinkedIn&logoColor=FFFFFF&label=' alt='Linkedin' height='30px'/>
            </a><a href='https://t.me/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Telegram&color=26A5E4&logo=Telegram&logoColor=FFFFFF&label=' alt='Telegram' height='30px'/>
            </a><a href='https://github.com/darideveloper' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=GitHub&color=181717&logo=GitHub&logoColor=FFFFFF&label=' alt='Github' height='30px'/>
            </a><a href='https://www.fiverr.com/darideveloper?up_rollout=true' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Fiverr&color=222222&logo=Fiverr&logoColor=1DBF73&label=' alt='Fiverr' height='30px'/>
            </a><a href='https://discord.com/users/992019836811083826' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Discord&color=5865F2&logo=Discord&logoColor=FFFFFF&label=' alt='Discord' height='30px'/>
            </a><a href='mailto:darideveloper@gmail.com?subject=Hello Dari Developer' target='_blank'>
                <img src='https://img.shields.io/static/v1?style=for-the-badge&message=Gmail&color=EA4335&logo=Gmail&logoColor=FFFFFF&label=' alt='Gmail' height='30px'/>
            </a></div><div align='center'><br><br><img src='https://github.com/darideveloper/twitch-cheer-bot/blob/master/logo.png?raw=true' alt='Twitch Cheer Bot' height='80px'/>

# Twitch Cheer Bot

Submit bits to streamers with twitch accounts

Project type: **client**

</div><br><details>
            <summary>Table of Contents</summary>
            <ol>
<li><a href='#buildwith'>Build With</a></li>
<li><a href='#relatedprojects'>Related Projects</a></li>
<li><a href='#media'>Media</a></li>
<li><a href='#details'>Details</a></li>
<li><a href='#roadmap'>Roadmap</a></li></ol>
        </details><br>

# Build with

<div align='center'><a href='https://www.python.org/' target='_blank'> <img src='https://cdn.svgporn.com/logos/python.svg' alt='Python' title='Python' height='50px'/> </a><a href='https://requests.readthedocs.io/en/latest/' target='_blank'> <img src='https://requests.readthedocs.io/en/latest/_static/requests-sidebar.png' alt='Requests' title='Requests' height='50px'/> </a><a href='https://github.com/marty90/PyChromeDevTools' target='_blank'> <img src='https://cdn.svgporn.com/logos/chrome.svg' alt='PyChromeDevTools' title='PyChromeDevTools' height='50px'/> </a></div>

# Related projects

<div align='center'><a href='https://github.com/darideveloper/comunidad-mc' target='_blank'> <img src='https://github.com/darideveloper/comunidad-mc/blob/master/app/static/app/imgs/logo_white.png?raw=true' alt='Comunidad MC' title='Comunidad MC' height='50px'/> </a><a href='https://github.com/darideveloper/twitch-viwer-bot' target='_blank'> <img src='https://github.com/darideveloper/twitch-viwer-bot/blob/master/logo.png?raw=true' alt='Twitch Viwer Bot' title='Twitch Viwer Bot' height='50px'/> </a><a href='https://github.com/darideveloper/twitch-cookies-getter/tree/master' target='_blank'> <img src='https://github.com/darideveloper/twitch-cookies-getter/blob/master/logo.png?raw=true' alt='Twitch Cookies Getter' title='Twitch Cookies Getter' height='50px'/> </a></div>

# Media

![cheers](https://github.com/darideveloper/twitch-cheer-bot/blob/master/screenshots/cheers.png?raw=true)

![dashboard bots form](https://github.com/darideveloper/twitch-cheer-bot/blob/master/screenshots/dashboard-bots-form.png?raw=true)

![dashboard bots list](https://github.com/darideveloper/twitch-cheer-bot/blob/master/screenshots/dashboard-bots-list.png?raw=true)

![dashboard donations form](https://github.com/darideveloper/twitch-cheer-bot/blob/master/screenshots/dashboard-donations-form.png?raw=true)

![dashboard donations list](https://github.com/darideveloper/twitch-cheer-bot/blob/master/screenshots/dashboard-donations-list.png?raw=true)

![terminal](https://github.com/darideveloper/twitch-cheer-bot/blob/master/screenshots/termina.png?raw=true)

# Details

The bot manage a single chrome window
It don't login with the accounts, instead of that, the bot use cookies already saved in a Backend service. 
All information required, like users, streams to cheer, comments, amounts, etc; its provided from a Django private app backend.

## Features

* Login with cookies
* Cheer at specific time 
	* Use custom message to cheer
	* Use custom donation to cheer
* Manage donations
* Manage bots / users to donate
* Mark donations already sent
* Disable bots / users with timeout cookies

# Roadmap

* [x] Proxies
* [x] Get donation from backend
* [x] Submit cheers to specific stream
* [x] Manage multiple donation with threading
* [x] Project status for not overlap donations
* [x] Update donation status in backend
* [x] Disable users with time out cookies
* [x] Auto open and close chrome
* [x] Change proxy in each donation

