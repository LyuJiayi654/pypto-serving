# PyPTO Serving 新增文档作用与 vLLM 文档目录对照

说明：用户问题中的“llvm”按上下文理解为 vLLM。本文中的 vLLM 指
<https://docs.vllm.ai/>。vLLM 目录依据 2026-09-07 读取到的
`https://docs.vllm.ai/en/stable/` 导航整理。

## 一、新增文档的作用概括

本次新增文档的目标不是复刻 vLLM 全站，而是把 PyPTO Serving 与 vLLM
之间的边界写清楚：哪些 vLLM/OpenAI serving 用法可以复用，哪些能力当前不
支持，哪些配置是 PyPTO Serving 在 Ascend NPU 环境下特有的。

### 1. `docs/user-guide/vllm-compatibility.md`

作用：作为“vLLM 兼容性说明”的入口页。

解决的问题：

- 明确 PyPTO Serving 不是完整 vLLM 替代品。
- 列出已支持的 HTTP endpoint：`/health`、`/v1/models`、
  `/v1/completions`、`/v1/chat/completions`、`/start_profile`、
  `/stop_profile`。
- 明确不支持 `/v1/responses`、`/v1/embeddings`、audio API、chat batch
  等 vLLM/OpenAI 扩展接口。
- 列出 completion/chat 请求字段，避免客户端带入 vLLM-only 参数后误判。
- 说明 generation 参数优先级：HTTP request > `--generate-config` >
  `GenerateConfig` 默认值。
- 给出 OpenAI Python client 的可用示例。

适合读者：正在把 vLLM client、vLLM benchmark、OpenAI client 接到
PyPTO Serving 的用户。

### 2. `docs/user-guide/model-support.md`

作用：作为模型和功能支持矩阵。

解决的问题：

- 把 Qwen3-14B 和 DeepSeek V4 Flash W8A8 的 checkpoint、设备数量、
  parallelism、offline、HTTP serving 支持状态放到一张表里。
- 用矩阵明确哪些 serving 功能支持，哪些不支持。
- 明确当前硬件范围只承诺 Ascend NPU + PyPTO kernels。
- 避免用户按照 vLLM 的 200+ 模型支持列表来理解本项目。

适合读者：准备选择模型、评估功能覆盖、判断是否能迁移 vLLM workload 的用户。

### 3. `docs/configuration/index.md`

作用：作为配置文档入口。

解决的问题：

- 把原来散落在 CLI、Profile、模型页里的配置说明集中起来。
- 说明 PyPTO Serving 的配置入口主要是 CLI 参数、HTTP request fields 和少量
  环境变量。
- 明确 vLLM 的大量 engine/server/plugin/LoRA/multimodal 配置不会自动适用。

适合读者：第一次配置服务，或需要知道“参数应该写在哪里”的用户。

### 4. `docs/configuration/runtime-capacity.md`

作用：解释运行时容量、调度和设备放置参数。

解决的问题：

- 解释 `--model`、`--device`、`--devices`、`--dp`、`--tp`、`--ep` 等放置参数。
- 解释 `--max-model-len`、`--max-num-seqs`、`--max-num-batched-tokens`、
  `--block-size` 等容量参数之间的关系。
- 说明 Qwen 的 replica placement 和 DeepSeek V4 的固定 8 卡 overlapped
  DP/EP placement。
- 解释 `--ring-*` 参数，替代旧的进程级 `PTO2_RING_*` 环境变量用法。

适合读者：需要调并发、KV cache、batching、DeepSeek V4 8 卡拓扑的用户。

### 5. `docs/configuration/env-vars.md`

作用：集中列出环境变量参考。

解决的问题：

- 统一说明 `PYPTO_LIB_ROOT`、`PYPTO_PROG_BUILD_DIR`、`PYPTO_STAGING_THREADS`、
  `PYPTO_WORKER_INIT_TIMEOUT`、`SERVING_WORKER_STEP_TIMEOUT`、
  `PYPTO_SERVING_GC_DEBUG`、`SA_PROFILE_OUTPUT`、`SA_PROFILE_LEVEL`、
  `PYPTO_RUNTIME_LOG`。
- 解释 compile cache 的使用条件和风险。
- 解释 pypto-lib discovery、profiling 环境变量、worker timeout 的使用方式。
- 说明旧 `PTO2_RING_*` 变量在 serving 路径下应优先替换成 CLI `--ring-*` 参数。

适合读者：维护运行环境、排查启动慢、排查找不到 kernel、配置 profiling 的用户。

### 6. `docs/deployment/local-ascend.md`

作用：作为当前项目的部署/运行手册。

解决的问题：

- 没有照搬 vLLM 的 Docker/Kubernetes/生产栈文档，而是聚焦当前实际支持的
  本地 Ascend NPU 运行方式。
- 给出 host checklist、source checkout、`task-submit` 验证命令。
- 给出 Qwen 单卡服务、Qwen 多卡 DP 服务、DeepSeek V4 8 卡服务示例。
- 说明网络绑定、启动成本、compile cache、DeepSeek prepacked sidecar 和
  shutdown/profiling merge。

适合读者：在 Ascend 机器上实际启动服务、做 smoke test、跑长服务的用户。

### 7. `docs/user-guide/troubleshooting.md`

作用：作为排障入口。

解决的问题：

- 按失败边界组织常见问题：CLI 缺失、HTTP 依赖缺失、kernel 找不到、首次启动慢、
  worker init timeout、HTTP 400、vLLM client 传了 unsupported fields、
  chat template 失败、DeepSeek V4 启动失败、streaming client hang、
  profile trace 没有 kernel events。
- 将排障动作指向对应配置页、兼容性页和模型页。

适合读者：遇到启动、请求、streaming、profiling、DeepSeek V4 拓扑问题的用户。

### 8. 配套修改

- `docs/user-guide/online-serving.md`：补充 `seed`、`reasoning_effort`，并把
  `Responses` 小节改名为 `Response Schema`，避免被误解成 OpenAI
  `/v1/responses` API。
- `docs/user-guide/benchmarking.md`：补充 vLLM benchmark client 使用限制。
- `docs/cli-reference/pypto-serving.md`：补充 `seed`。
- `mkdocs.yml`：新增 `Configuration` 和 `Deployment` 顶层导航，并把
  vLLM 兼容性和模型支持矩阵放入 User Guide。
- `tests/lint/check_docs_api_reference.py`：新增文档覆盖校验，防止 HTTP routes、
  request fields、`GenerateConfig` 字段更新后文档漏改。

## 二、增加文档后的当前项目文档目录

下面是 PyPTO Serving 当前 MkDocs 导航意义上的目录结构。

```text
PyPTO Serving
├── Home
│   └── docs/index.md
├── User Guide
│   ├── Getting Started
│   │   ├── Installation
│   │   │   └── docs/get-started/installation.md
│   │   └── Quickstart
│   │       └── docs/get-started/quickstart.md
│   ├── Inference and Serving
│   │   ├── Offline Inference
│   │   │   └── docs/user-guide/offline-inference.md
│   │   ├── Online Serving
│   │   │   └── docs/user-guide/online-serving.md
│   │   ├── vLLM Compatibility
│   │   │   └── docs/user-guide/vllm-compatibility.md
│   │   ├── Parallelism and Scaling
│   │   │   └── docs/user-guide/parallel.md
│   │   ├── Benchmarking
│   │   │   └── docs/user-guide/benchmarking.md
│   │   └── Profiling
│   │       └── docs/user-guide/profile.md
│   └── Models
│       ├── Model Support Matrix
│       │   └── docs/user-guide/model-support.md
│       ├── Qwen3-14B
│       │   └── docs/user-guide/qwen.md
│       └── DeepSeek V4
│           └── docs/user-guide/deepseek-v4.md
├── Configuration
│   ├── Overview
│   │   └── docs/configuration/index.md
│   ├── Runtime Capacity
│   │   └── docs/configuration/runtime-capacity.md
│   └── Environment Variables
│       └── docs/configuration/env-vars.md
├── Deployment
│   ├── Local Ascend Runs
│   │   └── docs/deployment/local-ascend.md
│   └── Troubleshooting
│       └── docs/user-guide/troubleshooting.md
├── CLI Reference
│   ├── Overview
│   │   └── docs/cli-reference/index.md
│   ├── pypto-serving
│   │   └── docs/cli-reference/pypto-serving.md
│   ├── DeepSeek V4 Conversion
│   │   └── docs/cli-reference/deepseek-v4-conversion.md
│   └── pypto-prepack-deepseek-v4
│       └── docs/cli-reference/pypto-prepack-deepseek-v4.md
└── Developer Guide
    ├── Architecture
    │   └── docs/developer-guide/architecture.md
    ├── Model Integration
    │   └── docs/developer-guide/model-integration.md
    ├── Weight Staging
    │   └── docs/developer-guide/weight-staging.md
    └── DeepSeek V4 Runtime
        └── docs/developer-guide/deepseek-v4-runtime.md
```

构建辅助文件：

```text
docs/
├── requirements.txt
└── _hooks/
    ├── __init__.py
    └── repo_links.py
```

## 三、vLLM 官方文档目录概览

vLLM 的官方文档是完整通用 serving 平台文档，范围远大于 PyPTO Serving。
下面按官方导航归纳主要目录，不展开 2000 多个自动生成的 API reference 页面。

```text
vLLM
├── Home
├── User Guide
│   ├── Getting Started
│   │   ├── Quickstart
│   │   └── Installation
│   │       ├── GPU
│   │       ├── CPU
│   │       └── TPU
│   ├── Examples
│   │   ├── Applications
│   │   │   ├── API Server
│   │   │   ├── Chatbot
│   │   │   └── RAG
│   │   ├── Basic
│   │   │   ├── Offline Inference
│   │   │   └── Online Serving
│   │   ├── Deployment
│   │   │   ├── Async LLM Streaming
│   │   │   ├── Helm Charts
│   │   │   ├── LLM Engine Example
│   │   │   └── Sagemaker Entrypoint
│   │   ├── Disaggregated
│   │   │   ├── Disaggregated Encoder
│   │   │   ├── Disaggregated Serving
│   │   │   ├── FlexKV Connector
│   │   │   ├── LMCache Examples
│   │   │   └── Mooncake Connector
│   │   ├── Features
│   │   │   ├── Automatic Prefix Caching
│   │   │   ├── Batch Invariance
│   │   │   ├── Context Extension
│   │   │   ├── Data Parallel
│   │   │   ├── KV Events
│   │   │   ├── LoRA
│   │   │   ├── OpenAI Batch file format
│   │   │   ├── Prompt Embed
│   │   │   ├── Speculative Decoding
│   │   │   ├── Structured Outputs
│   │   │   └── Torchrun
│   │   ├── Generate
│   │   │   ├── Batched Chat Completions Online
│   │   │   ├── Multimodal
│   │   │   └── Qwen 1M Offline
│   │   ├── Observability
│   │   │   ├── Monitoring Dashboards
│   │   │   ├── Metrics
│   │   │   ├── OpenTelemetry
│   │   │   └── Prometheus and Grafana
│   │   ├── Pooling
│   │   │   ├── Classify
│   │   │   ├── Embed
│   │   │   ├── Reward
│   │   │   ├── Score
│   │   │   ├── Token Classify
│   │   │   └── Token Embed
│   │   ├── Ray Serving
│   │   │   ├── Batch LLM Inference
│   │   │   ├── Elastic EP
│   │   │   ├── Multi-Node Serving
│   │   │   ├── Ray Serve DeepSeek
│   │   │   └── Run Cluster
│   │   ├── Reasoning
│   │   │   ├── Chat Completion Tool Calls With Reasoning
│   │   │   ├── Chat Completion With Reasoning
│   │   │   ├── Reasoning Streaming
│   │   │   └── Responses Client
│   │   ├── RL
│   │   │   ├── RLHF Async APIs
│   │   │   ├── RLHF HTTP IPC
│   │   │   ├── RLHF HTTP NCCL
│   │   │   └── Routed Experts E2E
│   │   ├── Scale Out
│   │   │   ├── Example MM Serve
│   │   │   └── Token Generation Client
│   │   ├── Speech To Text
│   │   │   ├── Language Identification
│   │   │   ├── OpenAI
│   │   │   └── Realtime
│   │   └── Tool Calling
│   │       ├── Chat With Tools Offline
│   │       ├── Chat Completion Client With Tools
│   │       ├── Required Tools
│   │       ├── xLAM Tool Calling
│   │       └── Responses Client With Tools
│   ├── vLLM V1
│   ├── Frequently Asked Questions
│   ├── Production Metrics
│   ├── Reproducibility
│   ├── Security
│   ├── Troubleshooting
│   └── Usage Stats Collection
├── Serving
│   ├── Offline Inference
│   ├── Online Serving
│   │   ├── Derenderer APIs
│   │   ├── Generative Scoring
│   │   ├── OpenAI-Compatible Server
│   │   ├── Renderer APIs
│   │   └── Speech to Text APIs
│   ├── Context Parallel Deployment
│   ├── Data Parallel Deployment
│   ├── Troubleshooting Distributed Deployments
│   ├── Expert Parallel Deployment
│   ├── Parallelism and Scaling
│   └── Integrations
│       ├── Claude Code
│       ├── Codex
│       ├── LangChain
│       └── LlamaIndex
├── Deployment
│   ├── Using Docker
│   ├── Using Kubernetes
│   ├── Using Nginx
│   ├── Frameworks
│   │   ├── Anyscale
│   │   ├── AnythingLLM
│   │   ├── AutoGen
│   │   ├── BentoML
│   │   ├── Cerebrium
│   │   ├── Chatbox
│   │   ├── Crusoe
│   │   ├── Dify
│   │   ├── dstack
│   │   ├── Haystack
│   │   ├── Helm
│   │   ├── Hugging Face Inference Endpoints
│   │   ├── LiteLLM
│   │   ├── Lobe Chat
│   │   ├── Modal
│   │   ├── Open WebUI
│   │   ├── Retrieval-Augmented Generation
│   │   ├── RunPod
│   │   ├── SkyPilot
│   │   ├── Streamlit
│   │   └── NVIDIA Triton
│   └── Integrations
│       ├── AIBrix
│       ├── NVIDIA Dynamo
│       ├── KServe
│       ├── KubeAI
│       ├── KubeRay
│       ├── Llama Stack
│       ├── llm-d
│       ├── llmaz
│       └── Production stack
├── Training
│   ├── Async Reinforcement Learning
│   ├── Layerwise Reloading
│   ├── RLHF
│   ├── Sampling Mask
│   ├── Transformers RL
│   └── Weight Transfer
│       ├── Base Classes and Custom Engines
│       ├── IPC Engine
│       └── NCCL Engine
├── Configuration
│   ├── Conserving Memory
│   ├── Engine Arguments
│   ├── Environment Variables
│   ├── Model Resolution
│   ├── Optimization and Tuning
│   └── Server Arguments
├── Models
│   ├── Supported Models
│   ├── Generative Models
│   ├── Pooling Models
│   │   ├── Classification Usages
│   │   ├── Embedding Usages
│   │   ├── Reward Usages
│   │   ├── Scoring Usages
│   │   ├── Specific Model Examples
│   │   ├── Token Classification Usages
│   │   └── Token Embedding Usages
│   ├── Weight Loading Extensions
│   │   ├── fastsafetensors
│   │   ├── InstantTensor
│   │   ├── Run:ai Model Streamer
│   │   └── Tensorizer
│   └── Hardware Supported Models
│       ├── CPU - Intel Xeon
│       └── XPU - Intel GPUs
├── Features
│   ├── Compatibility Matrix
│   ├── Automatic Prefix Caching
│   ├── Batch Invariance
│   ├── Context Extension
│   ├── Custom Arguments
│   ├── Custom Logits Processors
│   ├── Disaggregated Encoder
│   ├── Disaggregated Prefilling
│   ├── IndexCache
│   ├── Interleaved Thinking
│   ├── KV Offloading
│   ├── LoRA Adapters
│   ├── Multimodal Inputs
│   ├── Per-Request Metrics
│   ├── Prompt Embedding Inputs
│   ├── Reasoning Outputs
│   ├── Sleep Mode
│   ├── Structured Outputs
│   ├── Tool Calling
│   ├── Quantization
│   │   ├── AutoAWQ
│   │   ├── BitsAndBytes
│   │   ├── GGUF
│   │   ├── GPTQModel
│   │   ├── ModelOpt
│   │   ├── Quantized KV Cache
│   │   ├── TorchAO
│   │   └── LLM Compressor
│   └── Speculative Decoding
│       ├── Adaptive Verification
│       ├── Draft Models
│       ├── Dynamic Speculative Decoding
│       ├── EAGLE
│       ├── MTP
│       ├── N-Gram
│       ├── Parallel Draft Models
│       └── Suffix Decoding
├── Developer Guide
│   ├── Deprecation Policy
│   ├── Dockerfile
│   ├── Editing Agent Instructions
│   ├── Incremental Compilation Workflow
│   ├── Profiling vLLM
│   ├── Vulnerability Management
│   ├── Model Implementation
│   │   ├── Basic Model
│   │   ├── Registering a Model
│   │   ├── Unit Testing
│   │   ├── Multi-Modal Support
│   │   └── Speech-to-Text Support
│   └── CI
│       ├── CI Failures
│       ├── Nightly Builds
│       └── Update PyTorch Version
├── Benchmarking
│   ├── Benchmark CLI
│   ├── Parameter Sweeps
│   └── Performance Dashboard
├── API Reference
│   └── 自动生成的 `vllm` Python API 页面约 2105 个导航项
├── CLI Reference
│   ├── chat
│   ├── complete
│   ├── run-batch
│   ├── serve
│   ├── bench
│   │   ├── latency
│   │   ├── serve
│   │   ├── startup
│   │   ├── throughput
│   │   └── sweep
│   └── launch
└── Community
    ├── Contact Us
    ├── Meetups
    ├── Sponsors
    └── Governance / Blog / Forum / Slack
```

## 四、目录差异总结

| 维度 | PyPTO Serving 当前文档 | vLLM 官方文档 |
| --- | --- | --- |
| 项目定位 | Ascend NPU + PyPTO kernels 的小型本地 serving 栈 | 通用 LLM inference/serving 平台 |
| 模型范围 | Qwen3-14B、DeepSeek V4 Flash W8A8 | 大量 text、multimodal、pooling、speech 模型 |
| API 范围 | OpenAI completions/chat completions 子集 | OpenAI-compatible server、Responses、Embeddings、Audio、更多扩展参数 |
| 配置范围 | CLI、HTTP request fields、少量环境变量 | engine/server/env/model/hardware/plugin 大量参数 |
| 部署范围 | 本地 Ascend、`task-submit`、单机多卡 | Docker、Kubernetes、Nginx、云平台、框架集成、生产栈 |
| 特性范围 | continuous batching、paged KV、chunked prefill、prefix cache、DeepSeek MTP | LoRA、structured outputs、tool calling、multimodal、quantization 矩阵、spec decode 全家桶等 |
| API Reference | 无自动生成 Python API 站点 | 自动生成 `vllm` Python API，导航项非常多 |
| 当前补文档策略 | 写清楚边界、减少误用、服务 Ascend 实际运行 | 平台级完整文档 |

