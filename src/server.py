from fastmcp import FastMCP
from moviepy import ImageClip, AudioFileClip, VideoFileClip, CompositeVideoClip
from moviepy.video.fx.Loop import Loop
from moviepy.video.fx.Resize import Resize
from typing import Optional, Union, List
from os import listdir
from os.path import isfile, join
import logging
import json
from os.path import basename, splitext

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = {
    "log_level": "DEBUG"
}

mcp = FastMCP(
    "merge-video-mcp",log_level="ERROR", settings=settings
)

@mcp.tool()
def generate_video(
    image_path: Optional[str],
    gif_path: Optional[str],  # 改为逗号分隔的字符串
    audio_path: Optional[str],
    output_path: Optional[str],
    duration: Optional[float] = None,
    need_crop: Optional[bool] = False,
    gif_position: Optional[str] = "center,center",
    gif_sequential: Optional[bool] = True  # 新增参数：True为顺序展示，False为同时展示
) -> str:
    """
    将图片和MP3音频合成为视频
    
    参数:
        image_path: 图片文件路径
        gif_path: 动效贴图图片文件路径, 多个路径用逗号分隔
        audio_path: 音频文件路径
        output_path: 输出视频路径(默认为 图片名.mp4)
        duration: 视频时长(秒)，如果为None则使用音频时长
        need_crop: 是否需要裁剪图片(默认为False)
        gif_position: GIF位置(格式:"x,y"，如"center,center")
    返回:
        output_path: 生成的视频文件路径
    """
    audio_name = splitext(basename(image_path))[0]
    # 拼接完整输出路径
    output_file = join(output_path, f"{audio_name}.mp4")
    # 加载音频
    audio = AudioFileClip(audio_path)
    
    # 设置视频时长
    video_duration = duration if duration is not None else audio.duration
    
    # 创建图片剪辑并设置音频
    video = ImageClip(image_path, duration=video_duration)
    video = video.with_duration(video_duration)  # 显式设置时长
    
    # 修改：根据need_crop参数决定是否裁剪
    if need_crop:
        video = video.resized(width=975).cropped(
            x_center=video.w/2,
            y_center=550/2,
            width=975,
            height=550
        )
    
     # 将音频与视频组合
    clips = [video.with_audio(audio)]
    
    # 修改：处理单个或多个GIF路径
    if gif_path:
        gif_paths = [path.strip() for path in gif_path.split(',')]  # 分割字符串为列表
        
        if gif_sequential:  # 顺序展示
            gif_duration = video_duration / len(gif_paths)
            for i, path in enumerate(gif_paths):
                gif_clip = VideoFileClip(path, has_mask=True)
                if need_crop:
                    gif_clip = Resize(width=975).apply(gif_clip)
                else:
                    img_width = video.w
                    gif_clip = Resize(width=img_width).apply(gif_clip)
                
                # 修正：设置GIF的持续时间和时间段
                # gif_clip = gif_clip.with_duration(gif_duration)  # 先设置持续时间
                gif_clip = Loop(n=None, duration=gif_duration).apply(gif_clip)
                gif_clip = gif_clip.with_start(i * gif_duration)  # 再设置开始时间
                
                x_pos, y_pos = gif_position.split(',')
                gif_clip = gif_clip.with_position((x_pos.strip(), y_pos.strip()))
                clips.append(gif_clip)
        else:  # 同时展示
            for path in gif_paths:
                gif_clip = VideoFileClip(path, has_mask=True)
                if need_crop:
                    gif_clip = Resize(width=975).apply(gif_clip)
                else:
                    img_width = video.w
                    gif_clip = Resize(width=img_width).apply(gif_clip)
                
                # 设置每个GIF的显示时间段
                gif_clip = Loop(n=None, duration=video_duration).apply(gif_clip)
                x_pos, y_pos = gif_position.split(',')
                gif_clip = gif_clip.with_position((x_pos.strip(), y_pos.strip()))
                clips.append(gif_clip)
    
    # 将音频与视频组合
    final_clip = CompositeVideoClip(clips)
    
    # 输出视频
    final_clip.write_videofile(output_file, 
            fps=24,             
            codec="libx264",
            audio_codec="aac",  # Mac系统必须添加此参数
            threads=4,          # 多线程加速处理
            logger=None         # 关闭冗余日志
    )
    # 开发者只需返回字符串，FastMCP自动生成协议层报文
    return json.dumps({
            "output_file_path" : output_file
        }, ensure_ascii=False)

@mcp.tool()
def getFileList(
    dir_path: Optional[str] = "pic",
    file_ext: Optional[str] = None
) -> List[str]:
    """
    获取指定目录下的文件列表(SSE模式)
    
    参数:
        dir_path: 目录路径
        file_ext: 文件扩展名过滤(可选)
        
    返回:
        文件路径列表(每行一个文件路径)
    """
    # 过滤隐藏文件和目录
    files = [f for f in listdir(dir_path) if isfile(join(dir_path, f)) and not f.startswith('.')]
    if file_ext:
        files = [f for f in files if f.lower().endswith(file_ext.lower())]
    
    file_list = [join(dir_path, f) for f in files]
    return json.dumps({"file_list": file_list}, ensure_ascii=False)

def run_server():
    """运行 MCP 服务器"""
    print("=== Merge Video MCP 服务启动 ===")
    logging.info("Merge Video MCP 服务启动")
    print(f"当前工作目录: {os.getcwd()}")

    mcp.run(transport='sse') # 启动SSE服务器
    # mcp.run(transport='stdio') # 启动stdio服务器
