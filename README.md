# Sebastyan
Discord bot for moderation, listening to music from youtube, linking accounts (FACEIT, Steam, VK)
1. [Commands for playing music](#music)
2. [Commands for moderation](#mod)
3. [Commands for modifying account data](#data)
4. [Instructions for complete work](#instal)

### Image
__________________________________

![image](https://user-images.githubusercontent.com/70542011/128198969-7df22347-2fec-47c6-bcc7-95d6bde7628f.png)
![image](https://user-images.githubusercontent.com/70542011/128199128-179a9c80-6a70-4d85-ac34-78ceb9e5c621.png)

### Instructions for complete work <a name="instal"></a>
__________________________________
Create TOKEN.py file and fill in as written below
```python
vk = "TEXT" #vk api
ds = "TEXT" #discord api
faceit_api = "TEXT" #faceit api
```
Modules
```
pip install discord.py
pip install discord-components
pip install youtube_dl
pip install youtube-search
pip install requests
```
### Commands for playing music <a name="music"></a>
__________________________________
| Command | Argument | Operation |
|----------------|:---------:|----------------:|
| .play | `name(url)` | Play music (name or url) |
| .oldplay | `name(url)` | Playing music (longer than ".play") |
| .stop | --- | Stops the music |
| .pause | --- | Pause music |
| .resume | --- | Keeps playing music |
| .leave | --- | Kicks the bot out of the channel |

### Commands for moderation<a name="mod"></a>
__________________________________
| Command | Argument | Operation |
|----------------|:---------:|----------------:|
| .ban | `member nickname` and `reason` | Excludes user from server |

### Commands for modifying account data<a name="data"></a>
__________________________________
| Command | Argument | Operation |
|----------------|:---------:|----------------:|
| .add | service(`faceit,steam,vk`) | Add your info |
| .account | --- | Print your info |
| .faceit | `*` or `nickname` | Print your stats(CS:GO) |

