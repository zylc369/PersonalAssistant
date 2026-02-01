# TTS一键式傻瓜工具

完全自动化的文本转语音工具，零配置、一键使用。

## 🚀 快速开始

### 方法1：Shell版本（推荐）
```bash
./tts_final.sh "Hello world"
./tts_final.sh "你好世界" -o my_audio.wav
```

### 方法2：Python版本
```bash
python3 tts_foolproof_fixed.py "Hello world"
python3 tts_foolproof_fixed.py "你好世界" -o my_audio.wav
```

## ✨ 特点

- ✅ **零配置**：自动检查Python、创建虚拟环境、安装依赖
- ✅ **一键运行**：一条命令完成所有操作  
- ✅ **智能错误处理**：自动修复常见兼容性问题
- ✅ **跨平台**：支持Windows、macOS、Linux
- ✅ **自动文件名**：智能生成音频文件名

## 📋 使用示例

```bash
# 基本使用
./tts_final.sh "Hello world"

# 指定输出文件
./tts_final.sh "你好世界" -o my_audio.wav

# 使用Python版本
python3 tts_foolproof_fixed.py "How are you today?"

# 指定模型
./tts_final.sh "Hello" --model-name tts_models/en/ljspeech/vits
```

## 🛠️ 自动化功能

脚本会自动完成以下操作：

1. **环境检查**：验证Python 3.8+版本
2. **虚拟环境**：创建`tts_venv`虚拟环境
3. **依赖安装**：安装TTS和相关依赖
4. **兼容性修复**：自动处理Python版本和库兼容问题
5. **模型管理**：自动下载和管理TTS模型
6. **警告消除**：自动解决常见的兼容性警告

## 📁 文件说明

- `tts_final.sh` - 推荐使用的Shell版本
- `tts_foolproof_fixed.py` - Python版本（功能相同）
- `tts_cli.py` - 核心CLI工具
- `requirements.txt` - 依赖配置
- `tts_venv/` - 自动创建的虚拟环境

## 💡 使用提示

- **首次运行**：需要几分钟下载依赖和模型
- **后续运行**：秒级响应
- **输出文件**：默认生成在当前目录
- **模型位置**：自动存储在系统默认位置

## 🎯 系统要求

- Python 3.8+
- 网络连接（首次安装时）
- 约2GB磁盘空间

## 📊 输出示例

```
🎵 TTS一键式傻瓜脚本 🎵
🎤 完全自动化的文本转语音工具
ℹ️ [步骤] 检查Python安装...
✅ 成功: Python 3.9 检测通过
ℹ️ [步骤] 设置虚拟环境...
✅ 成功: 虚拟环境已存在
ℹ️ [步骤] 检查TTS依赖...
✅ 成功: TTS依赖已就绪

🚀 开始语音生成...
ℹ️ [步骤] 生成语音: 'Hello world'
✅ 成功: 语音生成成功！
ℹ️ 信息: 生成文件: 📁 hello_world.wav
✅ 任务完成！享受你的语音文件吧！
```

## 🔧 故障排除

### Python版本问题
请安装Python 3.8+：
```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt update && sudo apt install python3
```

### 依赖安装失败
检查网络连接，然后重新运行脚本。

### 权限问题
确保当前目录有写权限。

---

**🎉 就这么简单！一条命令，搞定语音合成！**