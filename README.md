# CatVault Server

CatVault 密码管理器的云端备份服务端。采用 FastAPI 构建，仅负责接收和存储**已加密**的 `.dat` 文件，永远不会接触用户的主密码或明文数据。

## 🛠️ 技术栈
- **Web 框架**：FastAPI
- **服务器**：Uvicorn
- **容器化**：Docker
- **存储**：本地文件系统（支持挂载持久化卷）

## 🚀 本地运行
建议在独立的虚拟环境中运行：
```bash
pip install -r requirements.txt
python -m uvicorn Server:app --reload
