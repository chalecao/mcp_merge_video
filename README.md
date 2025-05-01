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