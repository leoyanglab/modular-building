# 模块建筑目录：代码结构与阅读顺序

## 从哪里开始

先读 `public/app.js` 的目录状态和事件，再看 `public/js/` 的具体交互。下载链路从 `src/worker.js` 进入 `pdf-response.js`，按清单读取资源分段。`npm run build` 负责恢复/验证资源，不会重新制作目录和 PDF。

## 目录职责

- `public/index.html`：页面语义结构；`public/style.css`：响应式样式。
- `public/app.js`：目录加载、筛选、搜索和分页入口（原生 ES module）。
- `public/js/product-dialog.js`：商品详情与选型弹窗。
- `public/js/project-brief.js`：项目描述表单与本地文件下载。
- `public/js/text.js`：HTML 转义与塞尔维亚语搜索规范化。
- `public/analytics.js`：有站点域名限制的统计脚本。
- `src/worker.js`：普通资源/PDF 请求分发。
- `src/pdf-response.js`：PDF 缓存协商、HEAD、Range 与分段流读取。
- `src/pdf-manifest.json`：PDF 分段元信息，由制作脚本生成。
- `assets/`：目录来源与已发布资源清单；`public/products.json`：浏览器目录数据。
- `scripts/restore-assets.mjs`：恢复并校验发布资源；`verify.cjs`：产品、PDF 与 JavaScript 检查。
- `scripts/*.py`：资料导入、图片生成与 PDF 制作；`tests/`：PDF 响应协议回归。

## 修改约定

- 页面入口负责组合，功能放在对应组件或模块；共享规则放到领域/状态层。
- 浏览器操作在事件或客户端初始化中执行，保证服务端渲染时可安全导入。
- 每个请求或应用实例保有自己的状态；不要引入跨用户的全局可变状态。
- 保持现有接口、持久化键、权限和业务行为；数据库变化新增迁移。
- 修改源码后运行 `npm run format`；提交前运行 `npm run format:check`、`npm run build` 和 `npm test`。
- 格式由 `.prettierrc.json` 与 `.editorconfig` 统一，生成资源不手工编辑。
