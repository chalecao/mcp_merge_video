from setuptools import setup, find_packages

setup(
    name="mcp_merge_video",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mcp"
    ],
    author="chalecao",
    author_email="chh_exe@163.com",
    description="合成视频 MCP 服务",
    keywords="merge, video, mcp",
    python_requires=">=3.10",
)
