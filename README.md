# 晨报易

> 晨报处理更容易XD

## Dependency

Frontend: React + ant design (pro)

Backend: Django

## How to run

Assume that you have a good developing environment...

**If you'd like to deploy on local:**

```sh
cd chenbao_service
sh start.sh
```
Then view the website in browser: localhost:8012

**If you'd like to deploy on a server:**

There is no Nginx supported, so only a stupid way is provided.

Firstly modify the host and port configurations in chenbao_frontend/src/components/config.js

Then build the react project. 

```sh
npm run build
```
Next, copy the contents in build folder into chenbao_service/chenbao/templates/ except the static folder. The static folder should be copied to chenbao_service/chenbao/

Then modify the PORT variable in chenbao_service/start.sh

Finally copy the entire chenbao_service folder to your server, and run start.sh to start.

URL may be your_host:your_port

**If you'd like to modify frontend:**

It's the same procedure as above. Build, copy and restart.

**If you'd like to modify backend:**

Just restart after modification.

**If you don't like the cumbersome procedure:**

I don't care and I don't want to spend more time on this project.

Maybe I would optimize it when I have a good mood one day.


