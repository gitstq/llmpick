<div align="center">

# 🎯 LLMPick

**智能本地LLM选型助手 | Intelligent Local LLM Selector**

<p align="center">
  <a href="#简体中文">简体中文</a> •
  <a href="#english">English</a>
</p>

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/gitstq/llmpick)

</div>

---

<a name="简体中文"></a>
## 🎉 项目介绍

**LLMPick** 是一款智能本地大语言模型（LLM）选型助手，专为中文用户优化。它能够自动检测您的硬件配置，并根据性能、显存、使用场景等多维度因素，智能推荐最适合的本地LLM模型。

### 💡 解决的痛点

- 🤔 **模型选择困难** - 面对数百个开源模型不知如何选择
- 💾 **硬件适配迷茫** - 不清楚自己的设备能运行什么模型
- 🌐 **中文支持不足** - 很多工具对中文模型支持不够友好
- ⚡ **性能预估缺失** - 无法预估模型运行速度和体验

### ✨ 自研差异化亮点

1. 🇨🇳 **中文优先** - 优先推荐中文能力优秀的模型（Qwen、DeepSeek、Yi等）
2. 🎯 **智能评分** - 基于Benchmark、量化质量、硬件适配度综合评分
3. 📊 **速度预估** - 智能估算模型推理速度（tokens/秒）
4. 🖥️ **美观TUI** - 基于Rich的优雅终端界面
5. 🔧 **多后端支持** - 一键生成Ollama/LM Studio/llama.cpp命令

---

## ✨ 核心特性

| 特性 | 描述 | 状态 |
|------|------|------|
| 🔍 **自动硬件检测** | 智能识别GPU、CPU、内存配置 | ✅ |
| 🎯 **智能模型推荐** | 基于硬件性能匹配最佳模型 | ✅ |
| 🇨🇳 **中文优化** | 优先推荐中文能力优秀的模型 | ✅ |
| ⚡ **速度估算** | 预估模型推理速度 | ✅ |
| 📊 **多模型对比** | 直观对比不同模型特性 | ✅ |
| 🖥️ **美观TUI** | 优雅的终端交互界面 | ✅ |
| 🔧 **多后端支持** | 支持Ollama、LM Studio等 | ✅ |
| 🏷️ **标签过滤** | 按中文/代码/多模态等过滤 | ✅ |

---

## 🚀 快速开始

### 环境要求

- **Python**: 3.9 或更高版本
- **操作系统**: Windows 10+ / macOS 10.15+ / Linux
- **可选**: NVIDIA GPU（CUDA）、Apple Silicon（Metal）

### 安装

```bash
# 使用 pip 安装
pip install llmpick

# 或使用 uv（推荐）
uv tool install llmpick
```

### 基础用法

```bash
# 🔍 检测硬件信息
llmpick detect

# 🎯 获取模型推荐（默认前5个）
llmpick recommend

# 🎯 获取前10个推荐，优先中文模型
llmpick recommend --top 10 --chinese

# 📋 列出所有可用模型
llmpick list

# 📋 仅列出中文优化模型
llmpick list --chinese-only

# ℹ️ 查看模型详情
llmpick info qwen2.5-7b

# 🔍 对比多个模型
llmpick compare qwen2.5-7b llama-3.1-8b phi-4
```

---

## 📖 详细使用指南

### 硬件检测

```bash
$ llmpick detect

╭────────────────────────╮
│ 🔍 正在检测硬件信息...  │
╰────────────────────────╯

CPU: Intel(R) Core(TM) i9-13900K
CPU核心数: 24
内存: 32.0 GB
磁盘可用: 500.0 GB
操作系统: Linux 6.5.0

GPU信息:
  [1] NVIDIA GeForce RTX 4090
      显存: 24.0 GB
      计算能力: 8.9

加速支持:
  CUDA: ✓
  Metal: ✗
  ROCm: ✗
```

### 模型推荐

```bash
$ llmpick recommend

╭─────────────────────────────────────╮
│ 🎯 正在分析硬件并推荐最佳LLM模型...  │
╰─────────────────────────────────────╯

                                                  🎯 推荐模型列表
╭──────┬──────────────────────┬──────────┬──────────┬──────────┬────────────┬──────────────┬──────────────────────────╮
│ 排名 │ 模型                 │  参数量  │     大小 │     评分 │   适配度   │ 预估速度     │ 推荐理由                 │
├──────┼──────────────────────┼──────────┼──────────┼──────────┼────────────┼──────────────┼──────────────────────────┤
│  1   │ Qwen2.5-14B [CN]     │   14B    │    9.0GB │     76.0 │    良好    │     45.0 t/s │ 良好适配；中文优化       │
│  2   │ Qwen2.5-7B [CN]      │    7B    │    4.5GB │     70.0 │    完美    │     85.0 t/s │ 完美适配；中文优化       │
│  3   │ Llama 3.1 8B         │    8B    │    5.0GB │     68.0 │    完美    │     80.0 t/s │ 完美适配                 │
╰──────┴──────────────────────┴──────────┴──────────┴──────────┴────────────┴──────────────┴──────────────────────────╯
```

### 模型对比

```bash
$ llmpick compare qwen2.5-7b llama-3.1-8b phi-4

╭──────────────────────────────────────────────────────────────╮
│ 🔍 模型对比                                                   │
├─────────────┬─────────────────┬─────────────────┬────────────┤
│ 属性        │ Qwen2.5-7B      │ Llama 3.1 8B    │ Phi-4      │
├─────────────┼─────────────────┼─────────────────┼────────────┤
│ 参数量      │ 7B              │ 8B              │ 14B        │
│ 模型大小    │ 4.5GB           │ 5.0GB           │ 8.0GB      │
│ 量化        │ Q4_K_M          │ Q4_K_M          │ Q4_K_M     │
│ 上下文      │ 32K             │ 128K            │ 16K        │
│ 中文优化    │ ✓               │ ✗               │ ✗          │
│ 代码优化    │ ✓               │ ✓               │ ✓          │
│ 多模态      │ ✗               │ ✗               │ ✗          │
│ 评分        │ 70.0            │ 68.0            │ 75.0       │
╰─────────────┴─────────────────┴─────────────────┴────────────╯
```

---

## 📋 支持的模型

### 中文优化模型

| 模型 | 参数量 | 大小 | 上下文 | 特点 |
|------|--------|------|--------|------|
| Qwen2.5 | 0.5B-32B | 0.4-20GB | 32K | 阿里巴巴，中文最强 |
| DeepSeek | 6.7B-7B | 4.0-4.5GB | 16K | 深度求索，代码优秀 |
| Yi-1.5 | 6B-9B | 3.8-5.8GB | 4K | 零一万物，中文对话 |

### 国际主流模型

| 模型 | 参数量 | 大小 | 上下文 | 特点 |
|------|--------|------|--------|------|
| Llama 3.1/3.2 | 1B-8B | 0.7-5GB | 128K | Meta，多语言 |
| Phi-4 | 14B | 8GB | 16K | 微软，小巧高效 |
| Gemma 2 | 2B-9B | 1.6-6GB | 8K | Google，知识丰富 |
| Mistral | 7B | 4.5GB | 32K | Mistral AI，推理强 |

---

## 💡 设计思路与迭代规划

### 技术选型原因

- **Python 3.9+**: 兼顾兼容性与现代特性
- **Typer**: 类型安全的CLI框架，自动生成帮助文档
- **Rich**: 强大的终端美化库，支持表格、面板、进度条
- **Pydantic**: 数据验证和序列化
- **HuggingFace**: 模型数据来源

### 评分算法

```
最终评分 = Benchmark分数 × 量化质量系数 × 适配度系数

其中:
- 量化质量: Q4_K_M=1.0, Q5_K_M=1.05, Q8_0=1.10
- 适配度: 完美=1.0, 良好=0.95, 部分=0.85, 紧张=0.75, CPU=0.60
```

### 后续迭代计划

- [ ] 支持更多模型（GLM-4、Baichuan等）
- [ ] 添加模型下载进度显示
- [ ] 支持自定义模型配置
- [ ] 集成更多推理后端（vLLM、TGI等）
- [ ] Web UI界面
- [ ] 模型性能实测数据

---

## 📦 打包与部署指南

### 开发安装

```bash
git clone https://github.com/gitstq/llmpick.git
cd llmpick
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest tests/ -v
```

### 构建发布

```bash
# 构建 wheel
python -m build

# 上传到 PyPI
python -m twine upload dist/*
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 提交规范

- `feat:` 新增功能
- `fix:` 修复问题
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

<div align="center">

**Made with ❤️ by LLMPick Team**

如果这个项目对您有帮助，请给个 ⭐ Star！

</div>

---

<a name="english"></a>
## 🎉 Introduction (English)

**LLMPick** is an intelligent local Large Language Model (LLM) selector optimized for Chinese users. It automatically detects your hardware configuration and intelligently recommends the most suitable local LLM models based on multiple dimensions such as performance, VRAM, and usage scenarios.

### ✨ Key Features

- 🔍 **Automatic Hardware Detection** - Intelligently identify GPU, CPU, and memory configurations
- 🎯 **Smart Model Recommendation** - Match the best model based on hardware performance
- 🇨🇳 **Chinese Optimized** - Prioritize models with excellent Chinese capabilities
- ⚡ **Speed Estimation** - Estimate model inference speed
- 📊 **Multi-Model Comparison** - Intuitively compare different model features
- 🖥️ **Beautiful TUI** - Elegant terminal interface based on Rich
- 🔧 **Multi-Backend Support** - Support Ollama, LM Studio, etc.

---

## 🚀 Quick Start

### Requirements

- **Python**: 3.9 or higher
- **OS**: Windows 10+ / macOS 10.15+ / Linux
- **Optional**: NVIDIA GPU (CUDA), Apple Silicon (Metal)

### Installation

```bash
# Using pip
pip install llmpick

# Or using uv (recommended)
uv tool install llmpick
```

### Basic Usage

```bash
# 🔍 Detect hardware info
llmpick detect

# 🎯 Get model recommendations (default top 5)
llmpick recommend

# 🎯 Get top 10 recommendations, prioritize Chinese models
llmpick recommend --top 10 --chinese

# 📋 List all available models
llmpick list

# 📋 List only Chinese-optimized models
llmpick list --chinese-only

# ℹ️ View model details
llmpick info qwen2.5-7b

# 🔍 Compare multiple models
llmpick compare qwen2.5-7b llama-3.1-8b phi-4
```

---

## 📋 Supported Models

### Chinese-Optimized Models

| Model | Parameters | Size | Context | Features |
|-------|------------|------|---------|----------|
| Qwen2.5 | 0.5B-32B | 0.4-20GB | 32K | Alibaba, Best Chinese |
| DeepSeek | 6.7B-7B | 4.0-4.5GB | 16K | DeepSeek, Code Expert |
| Yi-1.5 | 6B-9B | 3.8-5.8GB | 4K | 01.AI, Chinese Chat |

### International Models

| Model | Parameters | Size | Context | Features |
|-------|------------|------|---------|----------|
| Llama 3.1/3.2 | 1B-8B | 0.7-5GB | 128K | Meta, Multilingual |
| Phi-4 | 14B | 8GB | 16K | Microsoft, Efficient |
| Gemma 2 | 2B-9B | 1.6-6GB | 8K | Google, Knowledge Rich |
| Mistral | 7B | 4.5GB | 32K | Mistral AI, Strong Reasoning |

---

## 💡 Design Philosophy

### Scoring Algorithm

```
Final Score = Benchmark Score × Quantization Quality × Fit Factor

Where:
- Quantization: Q4_K_M=1.0, Q5_K_M=1.05, Q8_0=1.10
- Fit: Perfect=1.0, Good=0.95, Partial=0.85, Tight=0.75, CPU=0.60
```

### Roadmap

- [ ] Support more models (GLM-4, Baichuan, etc.)
- [ ] Add model download progress display
- [ ] Support custom model configuration
- [ ] Integrate more inference backends (vLLM, TGI, etc.)
- [ ] Web UI interface
- [ ] Real model performance benchmark data

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

### Commit Convention

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation update
- `refactor:` Code refactoring
- `test:` Test related

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**Made with ❤️ by LLMPick Team**

If this project helps you, please give it a ⭐ Star!

</div>
