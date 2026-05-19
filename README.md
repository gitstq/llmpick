# 🎯 LLMPick - 智能本地LLM选型助手

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
</p>

**LLMPick** 是一款智能本地大语言模型（LLM）选型助手，能够根据您的硬件配置自动推荐最适合的本地LLM模型。针对中国用户优化，支持中文模型优先推荐。

## ✨ 核心特性

- 🔍 **自动硬件检测** - 智能识别GPU、CPU、内存配置
- 🎯 **智能模型推荐** - 基于硬件性能匹配最佳模型
- 🇨🇳 **中文优化** - 优先推荐中文能力优秀的模型
- ⚡ **速度估算** - 预估模型推理速度
- 📊 **多模型对比** - 直观对比不同模型特性
- 🖥️ **美观TUI** - 优雅的终端交互界面
- 🔧 **多后端支持** - 支持Ollama、LM Studio等运行方式

## 🚀 快速开始

### 安装

```bash
pip install llmpick
```

### 基础用法

```bash
# 检测硬件信息
llmpick detect

# 获取模型推荐
llmpick recommend

# 列出所有可用模型
llmpick list

# 查看模型详情
llmpick info qwen2.5-7b

# 对比多个模型
llmpick compare qwen2.5-7b llama-3.1-8b
```

## 📋 支持的模型

| 模型系列 | 参数量 | 中文优化 | 代码优化 |
|---------|--------|---------|---------|
| Qwen2.5 | 0.5B-32B | ✅ | ✅ |
| Llama 3.1/3.2 | 1B-8B | ⚪ | ✅ |
| Phi-4 | 14B | ⚪ | ✅ |
| DeepSeek | 6.7B-7B | ✅ | ✅ |
| Gemma 2 | 2B-9B | ⚪ | ⚪ |
| Mistral | 7B | ⚪ | ✅ |
| Yi-1.5 | 6B-9B | ✅ | ⚪ |

## 📄 开源协议

MIT License - 详见 [LICENSE](LICENSE) 文件
