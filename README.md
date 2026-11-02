# Modularni prostori

塞语拉丁字母模块化建筑网站，部署于 https://modular.bool.win 。

## 本地与部署

`npm ci`，`npm run build`，`npm run dev`，打开 http://localhost:4174 。
`npm run deploy` 使用已登录的 Cloudflare 账号发布 Worker `modularni-prostori-rs`。

## 内容与生成

四份供应商资料共整理 219 个独立型号/概念，分为 11 个系列；双层集装箱 SC-01 至 SC-52 完整收录。跨资料重复型号合并，尺寸或面积冲突保留说明，不推算缺失参数。图片保留原资料水印，未标为塞尔维亚落地案例。

- `assets/catalog-products.json`：产品数据源；修改型号在此进行。
- `assets/source-coverage.json`：四份来源文档页码覆盖记录。
- `assets/source/`：原资料图片。
- `scripts/build.py`：生成网站图片、图库和 public/products.json。
- `scripts/brochure.py`：生成 output/pdf 下电子、印刷两版 PDF。
- `scripts/package_pdfs.py`：拆分 PDF 静态资源并更新 src/pdf-manifest.json。
- `src/worker.js`：通过原下载地址输出完整 PDF，支持范围请求与浏览器阅读。

依次运行上述三个 Python 脚本，再部署。Python 需要 Pillow、ReportLab；审核另用 pypdf、pypdfium2。

## 画册

两版均为 244 页 A4 纵向、单页顺序；219 款独立展示页、11 个系列扉页及重点细节页。字体嵌入，目录可点击。电子版压缩图片，印刷版保留更高分辨率；实际清晰度受供应商源图限制。未做拼版、出血、PDF/X 或 CMYK 转换。

## 验证

`node scripts/check.cjs` 检查本地桌面/手机、219 款搜索筛选与详情、画册完整内容校验及跨分块范围请求。
`RANGE_ONLY=1 SITE_URL=https://modular.bool.win node scripts/check.cjs` 用于线上检查。
`python scripts/review_pdf.py` 检查两版页数、文字一致性及全部型号代码，并生成整册视觉审核图。

## 待业务信息确认

品牌与公开联系方式仍待定。询价表仅下载需求文本，不实际发送；没有编造价格、认证、保修或投资回报。当前保留 noindex，正式品牌、联系渠道与商业服务范围确认后再开放搜索收录。

## GitHub 与自动部署

仓库：https://github.com/leoyanglab/modular-building 。

网站：https://modular.bool.win 。本地项目：`/Users/leo/Project/redbook/modular-building`。

Cloudflare Workers 已连接此仓库，仅授权 `leoyanglab/modular-building`；生产分支为 `main`。推送后由 Git 事件自动触发 Cloudflare 构建：安装依赖，执行 `npm run build` 补齐发布素材并校验 219 个产品与两版 PDF 的 SHA-256，再执行 `npx wrangler deploy`。

同时配置了 Cloudflare Deploy Hook `github-main-push`，目标为 `main`。可通过 POST 请求触发同一构建流程。Hook 地址含触发凭据，不提交到仓库；可在 Cloudflare Worker 的「设置 → 构建 → 部署挂钩」查看。无需在 GitHub 中保存 Cloudflare API 令牌。

GitHub Actions 的 `Check catalog` 工作流在 `main` push 和 PR 时执行独立数据校验。本机也可用已有 Cloudflare 登录执行 `npm run deploy`。

仓库包含完整页面源码、产品数据、Worker、生成脚本和资源 SHA-256 清单。约 164 MB 的已发布图片和 PDF 分块不直接纳入 Git，构建时依据 `assets/published-assets.json` 从现有发布站点补齐，逐个校验长度和 SHA-256；已有正确文件则跳过。可通过 `ASSET_BASE_URL` 指定相同资源的备份镜像。构建恢复依赖资源源站或备份可访问；首次发布到全新环境前请先准备素材备份。

原始供应商图片 `assets/source/`、生成的完整 PDF `output/pdf/*.pdf`、已发布素材 `public/images/` 和 `public/_pdf/` 均完整保留在本机并被 Git 忽略。修改素材后应先在本地重新生成、校验与发布，再更新资源清单中的哈希。CI 无需重新制作 244 页画册。

## 访问统计

爱站独立统计站点 ID：`226859`，主地址为 `https://modular.bool.win/`。`public/analytics.js` 仅在 `modular.bool.win` 和 `modular.dht.so` 加载官方异步代码，本地调试和 Worker 预览不计入统计。旧域名当前未解析，恢复到同一站点后兼容统计。

CSP 仅额外放行该站点的统计节点 `https://node92.aizhantj.com:21233`；使用独立 JS 文件加载，不启用 `unsafe-inline` 或 `unsafe-eval`。统计采用平台默认页面访问行为，不额外采集询价表单内容。产品详情弹窗、搜索筛选不额外手工计入 PV，PDF 请求不执行页面统计。

报表：https://tongji.aizhan.com/analysis/index/index/?siteId=226859 。新配置同步和报表入库可能有延迟，需在后台确认实际访问数据。
