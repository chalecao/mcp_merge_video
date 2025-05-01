## mcp_merge_video
合成视频tool, 先读取主图和音乐，将他们合成，然后在读取GIF图片，支持多个gif图按照先后叠加，循环播放，这里面需要设置每个gif的循环时间。

具体教程：https://mp.weixin.qq.com/s/8hgI0ahxDjPztxljKVRlyg (微信公众号：mcp-sdk)

## 安装

```bash
git clone https://github.com/chalecao/mcp_merge_video.git
cd mcp_merge_video
pip install mcp
pip install .
```
## 配置信息

stdio模式：

```bash
{
  "mcpServers": {
    "merge-video-mcp": {
      "command": "path-to-your-python",
      "args": [
        "-m",
        "mcp_merge_video"
      ],
      "env": {
        "MERGE_VIDEO_WORKING_DIR": "/Users/xyz/account"
      }
    }
  }
} 
```

sse模式：

```bash
{
  "mcpServers": {
    "merge-video-mcp": {
      "url": "http://127.0.0.1:9000/sse",
      "env": {
        "MERGE_VIDEO_WORKING_DIR": "/Users/xyz/account"
      }
    }
  }
} 
```