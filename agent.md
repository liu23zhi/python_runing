# Agent 接手说明

本文件用于记录本仓库已经踩过的坑、稳定约定和后续 Agent 必须继续补充的经验。每次完成一个值得复用的修复、排查出真实根因、或用户明确指出同类问题重复出现时，都要更新本文件。

## 基本工作规则

- 开始改动前先看 `git status --short`，确认是否有用户或上一轮 Agent 留下的改动；不要回滚无关改动。
- 一件事完成并验证后就立即 commit，不要把多个已完成任务堆在一起。
- 中文任务使用中文提交信息，提交信息直接说明修复内容。
- 前端可见行为变化必须更新 `version.json`，`version` 使用日期加随机字母数字后缀，例如 `20260728-P4xL8v`；不要用纯时间戳后缀或特殊字符。
- 修改 `version.json` 时同步更新 `build_time` 为当前实际时间。
- 有值得学习的地方就写入本文件，不要只把经验留在对话里。

## 地图供应商相关入口

- 非高德地图的真实前端渲染主要在 `scripts/main.new.js` 的 `initProviderMap()`、`ensureSingleMap()`、`initMap(AMap)` 相关链路，不要只看 `index.html` 的静态容器。
- 地图供应商前端运行时的重点测试是 `tests/map_provider_frontend_runtime.test.mjs`。
- 后端供应商路线规划合同主要看 `tests/test_map_provider_business_execution_contract.py`、`tests/test_map_provider_backend_contract.py`、`tests/test_map_provider_runtime_guards.py`。
- 地图控件、SDK 加载、右键拖动、3D 视角这类问题，自动化测试通过后，尽量再直接加载真实地图验证；用户截图反复指出的问题不能只靠静态代码判断。

## 腾讯地图控件踩坑

- `showControl: false` 不能作为唯一保障。真实 Tencent SDK 仍可能显示默认缩放、旋转、比例尺控件；需要用官方 `removeControl()` 移除 `TMap.constants.DEFAULT_CONTROL_ID.SCALE`、`ZOOM`、`ROTATION`。
- 应用自绘控件必须挂在外层地图容器上，不能挂在 SDK surface 里，否则会被 SDK 自己的 DOM 层级影响。
- 右上角缩放等级不能写死为 `17`。腾讯地图要用 `getZoom()` 读取真实缩放，并监听官方 `zoom` 事件刷新标签。
- 腾讯缩放按钮优先走 `getZoom()` + `setZoom()`，这样按钮点击后能立即同步显示数值；不要只调用 `zoomBy()` 后等待未知的 SDK 状态。
- 左上角 3D/复位视角控件不只百度需要，腾讯也需要。点击后应调用统一的 `applyProviderMapDefaultOrientation()`，腾讯恢复 `pitch:55`、`rotation:0`。

## 百度和天地图控件踩坑

- 百度地图必须使用 BMapGL/WebGL 版本，加载 URL 要带 WebGL 类型，初始化时保留 3D 能力。
- 百度原生 3D 控件和应用左上角 3D 按钮是两个层次：原生控件可用于 SDK 能力，应用按钮用于和其它供应商保持一致。
- 天地图缺少右键拖动时，需要在 SDK surface 上自定义右键拖动并调用 `panBy()`，同时阻止浏览器默认右键菜单。
- 天地图标记点必须显式显示点名称，不能只画图标，否则会和百度、高德表现不一致。

## 坐标转换踩坑

- `wandergis/coordtransform` 是常见坐标系互转工具，不是高精度增强库；它的 `gcj02towgs84` 是一次近似反推，不应替换当前迭代逆解。
- 当前前端 `gcj02ToWgs84()` 使用迭代逆解，目标是让 `WGS84 -> GCJ02` 回环误差进入厘米级。
- 后端天地图路线运行时也要保持同样的 GCJ02 -> WGS84 精确逆解，避免前后端坐标基准不一致。
- 高德官方 `AMap.convertFrom(points, "gps")` 可用于验证或提升 `WGS84/GPS -> GCJ02` 正向转换，但它不提供 `GCJ02 -> WGS84`。
- 如果问题是路径偏离道路，优先使用各供应商自己的步行路线规划返回 path，不要指望坐标转换后直接连线能吸附道路。

## 路线与标记显示规则

- 能用步行路线规划就用步行路线规划。
- Tencent WebService 返回的道路 path 可能缺少原始起点、终点或中间检查点；绘制前要补齐路径显示，但不能修改 `currentRunData.target_points` 或真实执行坐标。
- 进度颜色不能只依赖 `target_sequence` 或 `checked_targets_count`。执行进度可能滞后，应该从 `current_point_index` 或 `current_position` 对 `run_coords` 推断。
- 已完成段用灰色，当前检查点用蓝色，未完成检查点用绿色，剩余路线用活动色；这套语义应对高德、腾讯、百度、天地图保持一致。

## 验证清单

- 修改 `scripts/main.new.js` 后至少运行 `node --check scripts/main.new.js`。
- 地图供应商前端改动运行 `node --test tests/map_provider_frontend_runtime.test.mjs`。
- 后端路线规划或供应商配置改动运行：
  - `python -m pytest tests/test_map_provider_business_execution_contract.py`
  - `python -m pytest tests/test_map_provider_backend_contract.py`
  - `python -m pytest tests/test_map_provider_runtime_guards.py`
- 提交前运行 `git diff --check`。Windows 下 LF/CRLF 提示不是失败，但真正的 whitespace error 不能忽略。
- 提交前确认 `git diff --stat` 和 `git status --short`，只提交当前任务相关文件。

## 后续更新方式

当以后又踩到坑时，在对应章节追加：

- 症状：用户看到或测试暴露的问题。
- 根因：最终确认的真实原因。
- 正确做法：以后应该怎么写、怎么验证。
- 相关测试：能防止回归的测试文件或命令。
