# Hagsyn Graph Deployment

## 1. 目标形态

当前项目推荐采用以下部署形态：

- `caddy` 提供前端静态资源
- `caddy` 反向代理 `/api/*` 到本机 `uvicorn`
- `systemd` 守护后端服务
- 本地通过 `deploy/deploy.sh` 直接 CLI 发布

默认部署目标：

- 前端站点：`http://<server>:9999/`
- 后端健康检查：`http://<server>:9999/api/health`

## 2. 当前服务器默认值

当前已验证服务器：

- Host: `159.75.81.13`
- Port: `22`
- User: `ubuntu`
- OS: `Ubuntu 24.04.4 LTS`
- 80 端口已有 `caddy`
- 已安装：`python3`、`ffmpeg`、`systemctl`

## 3. 首次准备

### 3.0 放行云安全组 / 防火墙

如果服务器在云厂商上，必须先放行公网入站规则：

- `22/tcp`：SSH
- `9999/tcp`：当前应用入口
- `443/tcp`：HTTPS（后续绑定域名时建议一起放行）

这一步不做，本机服务即使正常，公网也会一直超时。

### 3.1 准备服务器环境变量

推荐在本地创建：

`backend/.env.server`

可从 [`/Users/hagsyn/ai/workspace/Hagsyn-Graph/backend/.env.server.example`](/Users/hagsyn/ai/workspace/Hagsyn-Graph/backend/.env.server.example) 复制。

至少需要改：

- `FRONTEND_ORIGIN`
- `AUTH_USERNAME`
- `AUTH_PASSWORD`
- `AUTH_TOKEN`

### 3.2 应用登录凭据说明

`AUTH_USERNAME` / `AUTH_PASSWORD` 不是服务器 SSH 登录账号，也不是 Linux 系统用户密码。

它们是 **Hagsyn 应用自己的后台登录凭据**，用于：

- `POST /api/auth/login`
- 前端登录后换取 Bearer Token
- 受保护的 `/api/*` 业务接口访问

如果首发部署时用了临时生成的账号密码，后续应尽快替换成正式值，并重启后端服务：

```bash
sudo systemctl restart hagsyn.service
```

## 4. 一键发布

本地执行：

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph
chmod +x deploy/deploy.sh

SERVER_HOST=159.75.81.13 \
SERVER_USER=ubuntu \
SERVER_PORT=22 \
DEPLOY_DIR=/opt/hagsyn/Hagsyn-Graph \
SITE_ADDRESS=http://159.75.81.13:9999 \
SERVICE_NAME=hagsyn \
APP_USER=ubuntu \
APP_GROUP=ubuntu \
DATA_DIR=/opt/hagsyn/data \
DEPLOY_SSH_PASSWORD='your-ssh-password' \
ENV_SOURCE_FILE=/Users/hagsyn/ai/workspace/Hagsyn-Graph/backend/.env.server \
./deploy/deploy.sh
```

## 5. 脚本做了什么

`deploy/deploy.sh` 会：

1. 创建远端部署目录和数据目录
2. `rsync` 当前仓库到服务器
3. 上传 `backend/.env`
4. 渲染并安装 `systemd` service
5. 渲染并安装 `Caddyfile`
6. 在服务器上创建 `.venv`
7. 安装 `requirements.txt`
8. 启动 / 重启 `hagsyn.service`
9. 重启 `caddy`
10. 本机校验远端 `api/health`

## 6. 部署后的运维命令

### 后端状态

```bash
ssh ubuntu@159.75.81.13
sudo systemctl status hagsyn.service
```

### 后端日志

```bash
sudo journalctl -u hagsyn.service -n 200 --no-pager
```

### Caddy 状态

```bash
sudo systemctl status caddy
```

### Caddy 配置检查

```bash
sudo caddy validate --config /etc/caddy/Caddyfile
```

## 7. 回滚方式

当前脚本属于“覆盖式发布”。如果需要回滚：

1. 在本地切回目标版本
2. 重新运行同一条 `deploy/deploy.sh`

如果要升级成保留历史版本的回滚体系，后续可以再改成：

- `releases/<timestamp>/`
- `current -> releases/...` 软链接切换

## 8. 注意事项

1. 当前前端默认已支持“同源 API”，部署后不再强依赖 `127.0.0.1:8000`
2. 当前默认是 HTTP + IP + `9999` 端口访问，所以 `SITE_ADDRESS` 应写成 `http://159.75.81.13:9999`
3. 如果后续绑定域名，可把 `SITE_ADDRESS` 改成裸域名，例如 `app.example.com`，并把入口端口调整回 `80/443`，交给 `caddy` 自动接 HTTPS
4. 如果服务器要跑字幕功能，请确认 `faster-whisper` 依赖安装成功，并留意模型首次下载时间
5. `backend/storage/` 和本地 SQLite 文件不会被直接 rsync 上线，服务器使用的是部署目录自己的运行态与 `DATA_DIR`
6. 如果服务器内 `curl http://127.0.0.1/` 正常、`curl http://127.0.0.1:8000/api/health` 正常，但公网访问 `http://<公网IP>/` 超时，优先检查云安全组 / 防火墙，而不是先怀疑应用代码
