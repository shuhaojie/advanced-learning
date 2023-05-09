# docker

## 一、安装docker

一定要采用docker官方文档提供的方法来安装, 否则后面可能会有问题

### 1.配置源

```Bash
 1. sudo apt-get update
 2. sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
3. curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
4. echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 2.docker国内源

采用上面的配置,在下一步安装docker的时候,可能速度非常慢,可以配置国内源

```Bash
1. 配置 apt-get 可以使用 https 库
$ sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

2. 添加 Docker 使用的公钥
$ curl -fsSL https://mirrors.cloud.tencent.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -

3. 添加 Docker 远程仓库
$ sudo add-apt-repository "deb [arch=amd64] https://mirrors.cloud.tencent.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
$ sudo apt-get update

4. 配置docker镜像加速
{
    "registry-mirrors": [
     "https://mirror.ccs.tencentyun.com"
    ]
}
配置文件在 /etc/docker/daemon.json
```

### 3.安装docker

```Bash
 sudo apt-get update
 sudo apt-get install docker-ce docker-ce-cli containerd.io
```

完成安装后测试一下`sudo docker run hello-world`, 后面可以用`sudo chmod 666 /var/run/docker.sock`来去掉sudo.

### 4. 安装docker-compose

```Bash
1.安装 
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

2.修改权限
sudo chmod +x /usr/local/bin/docker-compose

3.测试
docker-compose --version
```

### 5. 添加当前用户到docker用户组

```Bash
1.groups  # 列出自己的用户组，确认自己在不在 docker 组中

2.sudo groupadd docker  # 没有则新增docker组

3.sudo gpasswd -a ${USER} docker  # 把当前用户加入到docker组中

4.
  # 重启docker服务
```

## 二、镜像, 容器和仓库

### 1. 镜像

#### （1）基本概念

操作系统环境, image可以重复建立container, 就像印钞机可以一直印钞票

#### （2）常用命令

- docker images: 查看本机所有镜像

```bash
REPOSITORY            TAG       IMAGE ID       CREATED          SIZE
shuhaojie/stackdemo   latest    3f4ec02bf9d8   40 minutes ago   84.6MB
redis                 alpine    0b405767398c   8 days ago       29.9MB
```

这里的REPOSITORY+TAG就是镜像的名称，可以在docker ps中看到

```bash
CONTAINER ID   IMAGE                        COMMAND                  CREATED       STATUS       PORTS                                       NAMES
275e359c08cb   redis:alpine                 "docker-entrypoint.s…"   4 hours ago   Up 4 hours   6379/tcp                                    stackdemo_redis_1
99883979b298   shuhaojie/stackdemo:latest   "python app.py"          4 hours ago   Up 4 hours   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   stackdemo_web
```

**当我们在build镜像的时候，通过这个名称来判断本地是否存在这个镜像，如果存在就用本地的**

- docker run：创建一个容器并启动容器。**docker run = docker create + docker start**

- docker build: 通过Dockerfile来制作镜像。

  ```bash
  docker build -t koa-demo:1.0 . # .表示Dockerfile相对路径
  ```

- docker push：将镜像推送到仓库。**在推送之前，仓库上一定要创建对应的REPOSITORY**，例如上面的shuhaojie/stackdemo:latest，需要创建stackdemo这个仓库。

  <img src="/Users/shuhaojie/Library/Application Support/typora-user-images/image-20230426144225630.png" alt="image-20230426144225630" style="zoom:50%;" />

- docker rmi <image_id>: 删除镜像. 删除所有镜像: docker rmi -f $(docker images -aq)

- docker commit: 容器转化为镜像. 假设一个容器没有vim, 但希望安装vim后, 即使重启容器也会有vim, 下面是主要步骤

  ```bash
  docker exec -it container_id bash # 在终端: 进入容器
  yum install vim -y  # 在容器内: 安装vim
  docker commit container_id image  # 在终端: 容器转镜像   
  ```

- docker save: 将镜像制作为tar文件
- docker load: 导入使用docker save出的镜像

### 2. 容器

#### （1）基本概念

docker利用的正是container来运行程序

#### （2）常用命令

- docker start: 启动已经存在的容器
- docker exec: 进入已经启动的容器
- docker ps -a: 所有容器列表
- docker ps: 所有运行中的容器
- docker rm container_id: 删除容器. 删除所有容器:docker rm $(docker ps -a -q)
- docker stop: 停止一个已经启动的容器(容器只有停止在停止状态才可以删除)
- 停止所有容器：docker kill $(docker ps -q)

### 3. 仓库

#### （1）基本概念

docker的registry和git概念一样, 可以从registry上传或下载images.

#### （2）常用命令

- docker push：将本地的镜像上传到镜像仓库

## 三、Dockerfile

### 1. Dockerfile简介

Dockerfile是一个用来构建镜像的文本文件, 文本内容包含了一条条构建镜像所需的指令和说明. Dockerfile中有三个常见的命令

* FROM: 定制的镜像都是基于FROM的镜像, 后续的操作都是基于该镜像做的操作

* RUN: 用于执行后面跟着的命令行命令, 有两种格式

    1. shell格式

    ```Bash
    RUN <命令行命令>   # 命令行命令 等同于在终端操作的shell命令
    ```

    2. exec格式

    ```Bash
    RUN ["可执行文件", "参数1", "参数2"]
    ```

> 注意，在RUN命令中有路径时，指的是容器外的相对路径，而不是容器内的路径
> 此外，要注意的是，执行`pip install -r requirements.txt`前，需要先执行`COPY requirements.txt .`

* CMD: **在镜像构建好，用镜像启动容器时(docker run)会执行的命令**

> 注意: 当docker-compose启动容器时，**它并不会去执行Dockerfile中的CMD**，而是会去执行docker-compose中的command

### 2. 构建镜像

在Dockerfile文件的存放目录下, 执行构建动作

```Bash
# 1. nginx表示镜像名称， v3表示版本
# 2. 最后的.表示Dockerfile相对终端执行环境的相对路径
docker build -t nginx:v3 .  
```

### 3. 文件实例

```Bash
FROM centos
RUN yum install wget
RUN wget -O redis.tar.gz "http://download.redis.io/releases/redis-5.0.3.tar.gz"
RUN tar -xvf redis.tar.gz
```

以上执行会创建 3 层镜像, 可简化为以下格式:

```Bash
FROM centos
RUN yum install wget \
    && wget -O redis.tar.gz "http://download.redis.io/releases/redis-5.0.3.tar.gz" \
    && tar -xvf redis.tar.gz
```

如上, 以 && 符号连接命令, 这样执行后只会创建1层镜像

### 4. 构建并启动容器

针对单个容器, 可以先通过`docker build`来构建镜像，并通过`docker run`来创建并启动容器。**如果涉及多个容器，就可以通过docker-compose来实现**。

## 四、docker-compose

### 1.简介

用于构建和启动多容器工具, 通过`docker-compose.yml`来配置项目需要的所有服务, 然后`docker-compose up`启动所有服务

### 2.文件实例

```Bash
version: '2.2'
services:  
  web:  # 服务名称, docker-compose中一个服务可以有多个容器
    container_name: aiplatform  # 容器名称
    image: aiplatform:v3  # 如果本地有镜像, 直接用本地镜像; 如果没有, 采用repository的; 如果没有指定repository, 就是用Docker Hub的.
    ports:
      - 8001:8000  # 端口映射
    depends_on:
      - db  # 依赖的服务
    environment:
      - DEBUG=1
    volumes:
      - aiplatform_data:/data  # volume
      - ${PROJECTDIR}/backend:/workspaces # bind mount, 没有workspaces的话，会自己创建
      - ${PROJECTDIR}/logs:/logs
    command: bash -c "sleep 10 && bash /workspaces/start.sh && tail -f /dev/null"  # 启动docker时候的命令

volumes:
  postgres_data:
    name: postgres_data
  redis_data:
    name: redis_data
```

#### (1) service

关于service，有如下几点要注意

1. service name和container name: 例如上面的例子, 这里的web实际上指的是一个服务，而不是一个容器，一个服务可以包含多个容器。在docker-compose中，必须有service name，而不必有container name，如果没有container name，那么container name=`当前工作路径名>_<service name>_<sequence number>`，这里的sequence number是从1开始的

2. 非常重要的一点: service name 可以广泛的被应用

* 在nginx中，可以看到`proxy_pass http://web:8000;`这样的表示式，这里的web就是指的service name
* 在django的settings中，可以看到数据的配置如下，这里的`db`指的也是service name

```Python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'orthanc',
        'HOST': 'db',
        'PORT': 5432,
        'USER': 'haojie',
        'PASSWORD': '4a53e4f5c42fd5a31890860b204472c5'
    }
}
```

* 同样的还有celery broker的配置，这里的host指的也是service name

```Python
redis_passwd = '4a53e4f5c42fd5a31890860b204472c5'
redis_host = 'redis'
redis_port = "6379"
redis_db = "1"

CELERY_BROKER_URL = f'redis://:{redis_passwd}@{redis_host}:{redis_port}/{redis_db}'
```

#### (2) image和build

image和build都是用来构建、启动容器用的镜像

* image: **如果本地有镜像, 直接用本地镜像**; 如果没有, 采用repository的; 如果没有指定repository, 就是用Docker Hub的.
* build: 是指通过Dockerfile来构建。

```docker-compose
version: "3.7"
services:
  webapp:
    build:
      context: ./dir  # Dockerfile的路径
      dockerfile: Dockerfile-alternate  # Dockerfile的名字
      args:
        buildno: 1  # Dockerfile构建镜像时候的参数，在构建时候的环境变量
```

#### (3) ports

* port: 8001:8000，当外部访问主机的8001端口时，主机将8001端口映射到容器的8000端口

* expose: expose暴露端口给link(下面会解释)到当前容器的容器

#### (4) depends_on

* depends_on: 定义服务之间的依赖关系，上面的例子中db服务启动顺序要优先于web服务
* links: 当我们链接(links)容器时，docker会创建环境变量并将容器添加到已知主机列表中

#### (5) environment

environment变量可以在构建镜像过程中，在Dockerfile中去使用。也可以在已构建好的镜像制作出的容器中使用，在容器的终端中输入`env`即可查找到所有的环境变量。可以用如下的python代码拿到具体的环境变量。

```Python
import os
os.environ.get('DEBUG')
```

#### (6) volume

docker的挂载主要有两种方式

* bind mount(全路径的主机目录): 将主机的目录mount到container中，这种方式`主机的目录路径必须为全路径，否则docker会将其当做volume处理`。这种方式有一个不好的地方: windows和linux的目录结构不一样，那么此时我们是没法在不同的系统去写一个主机的目录来兼容的。
* volume(非全路径的主机目录): volume和bind mount不同之处在于，volume的主机目录是被docker管理的，都在主机的`/var/lib/docker/volumes`目录下，这个目录的权限非常严格，即使是用`sudo`都不能打开(`cd`)。将my-volume挂载到container中的/mydata目录: `docker run -it -v my-volume:/mydata alpine sh`，它会在主机下创建`/var/lib/docker/volumes/my-volume/_data`目录，如果该目录不存在，那么docker会先创建然后再挂载。

#### (7) command

基本和`docker run`的`CMD`差不多，都是启动docker时执行的命令

## 五、docker swarm

### 1. swarm 

#### （1）简介

Swarm(群)，由多个docker主机组成，包括manager和worker。

**服务(service)是docker swarm的操作单位，而不是容器**。当创建服务时，我们会定义其最佳状态（例如副本数）， docker 致力于维护所需的状态。例如，如果工作节点变得不可用，Docker 会在其他节点上安排该节点的任务(Task)。

**任务(Task)是一个正在运行的容器**，它是swarm服务的一部分，由swarm管理器管理，而不是一个独立的容器。

#### （2）作用

- swarm最大的优势是可以修改服务的配置，包括它所连接的网络和卷，而无需手动重启服务

#### （3）swarm, stack, service, task, node

- Dockerfile是用来构建镜像的，一个Dockerfile只能构建一个镜像

- docker compose可以在单机上构建一组任务，可以管理多个容器
- swarm是用来构建集群
- stack是在集群的基础上管理容器，他可以操作多个service

- service是一组任务，包含多个镜像和容器，通常用于在集群的基础上管理容器
- task是swarm中的原子调度单元，对应运行在一个service中的单个container

- node是swarm中的节点概念，一个节点对应一台服务器。

### 2. service

![image-20230421210912517](/Users/haojie/Library/Application Support/typora-user-images/image-20230421210912517.png)

应用程序的不同部分，称之为服务。**服务定义了一个镜像该如何运行的方法，如端口数，容器的个数(replicas)**，例如上图中service1，在节点1中需要两个image1，在节点2中需要一个image1。

#### （1）部署服务

```bash
docker service create --replicas 1 --name helloworld alpine ping docker.com
```

- docker service create: 创建服务
- --name：服务名称
- --replicas：运行实例个数。一个服务可以有多个运行实例。
- alpine ping docker.com：将服务定义为执行`ping docker.com`命令的Alpine Linux容器

#### （2）查看服务

```bash
docker service ls # 查看所有服务
docker service inspect --pretty helloworld  # 查看某个服务的细节，不加--pretty会返回json格式
docker service ps helloworld  # 查看哪些节点在运行服务，有可能不在当前节点运行服务，此时需要ssh到对应机器上通过docker ps查看
```

#### （3）扩展服务

```bash
docker service scale helloworld=5  # 将服务扩展为5个，其实就是有5个运行的容器
```

#### （4）删除服务

```bash
docker service rm helloworld
```

### 3. docker-compose VS docker stack

- docker stack和docker-compose一样，**都能操纵 compose.yml文件**，定义 services、volumes 、networks
- docker-compose在单个docker引擎上编排服务，docker stack可以在多个docker引擎上编排服务
- docker stack必须是在docker swarm模式中执行，并且只能在manager节点上执行。而如果开启了docker swarm模式，此时不建议用docker-compose。

### 4. 使用docker swarm部署项目

参考官方文档https://docs.docker.com/engine/swarm/stack-deploy/

#### （1）开启swarm模式

```
docker swarm init
# 开放端口
firewall-cmd --add-port=2377/tcp --permanent
firewall-cmd --reload
# 重启机器
```

#### （2）文件准备

- app.py

  ```python
  from flask import Flask
  from redis import Redis
  
  app = Flask(__name__)
  redis = Redis(host='redis', port=6379)
  
  @app.route('/')
  def hello():
      count = redis.incr('hits')
      return 'Hello World! I have been seen {} times.\n'.format(count)
  
  if __name__ == "__main__":
      app.run(host="0.0.0.0", port=8000, debug=True)
  ```

  - Dockerfile

    ```dockerfile
    # syntax=docker/dockerfile:1
    FROM python:3.4-alpine
    ADD . /code
    WORKDIR /code
    RUN pip install -r requirements.txt
    CMD ["python", "app.py"]
    ```

  - requirements.txt

    ```txt
    flask
    redis
    ```

  - docker-compose.yml

    ```yml
    version: "3.9"
    
    services:
      web:
        image: shuhaojie/stackdemo:latest
        build: .
        ports:
          - "8000:8000"
      redis:
        image: redis:alpine
    ```

#### （3）构建镜像

- 构建镜像，`docker-compose up -d`: **既会构建镜像，也会去启动容器**。
- 查看镜像状态，`docker-compose ps`
- 关闭`compose`, `docker-compose down --volumes`

- 将构建好的镜像推到临时仓库：`docker-compose push`

#### （4）构建栈

- 创建docker stack(栈)：`docker stack deploy --compose-file docker-compose.yml stackdemo`，最后一个参数是栈的名称。
- 查看栈中的服务状态：`docker stack services stackdemo`，查看由stackdemo这个栈创建的服务

- 测试manager节点：`curl http://localhost:8000`

#### （5）加入worker节点

- 首先确保可以从虚拟机ssh到mac，需要在mac上开启允许ssh，详情<https://support.apple.com/zh-sg/guide/mac-help/mchlp1066/mac>

- 用mac作为从节点，下面具体的命令在`docker swarm join-token worker`，可以看到如下命令

  ```bash
  docker swarm join --token SWMTKN-1-0k7mff4t95pbe8lzn08omjfs66d1xrgu733vxa8bhsicp3e6v0-cyyjmzydwmzwsmiwuk7831uon 172.16.94.129:2377
  ```

- 查看所有节点：`docker node ls`

- 在虚拟机上给mac发HTTP请求，`curl http://address-of-other-node:8000`

> 目前报错 - curl: (52) Empty reply from server
