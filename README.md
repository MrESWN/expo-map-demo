# 展会地图 Demo

移动端展会地图原型：地理围栏解锁、实时定位、朝向箭头、展会底图叠加、路径规划占位、页面可见性控制。

纯静态单文件，零后端，零构建。

## 快速预览

```bash
# 任意静态服务器即可，不要直接双击打开（file:// 下浏览器拒绝定位）
python -m http.server 8123
# 浏览器访问 http://127.0.0.1:8123
```

## 部署到 GitHub Pages

1. 在 GitHub 新建仓库，例如 `expo-map-demo`（Public）
2. 本地执行：

```bash
git remote add origin https://github.com/<你的用户名>/expo-map-demo.git
git branch -M main
git push -u origin main
```

3. 仓库 **Settings → Pages → Build and deployment → Source** 选 **GitHub Actions**
4. 等 Actions 跑完，访问 `https://<你的用户名>.github.io/expo-map-demo/`

此后每次 `git push` 都会自动重新部署，大约 30 秒生效。地址永久固定。

> 国内网络访问 `github.com` 可能需要代理。`github.io` 域名通常可以直连。

## 部署到其他平台（同样零配置）

- **Vercel**：导入仓库 → Framework 选 Other → Deploy
- **Netlify**：拖拽整个目录到 Netlify Drop
- **任意服务器**：把 `index.html` 放到站点根目录即可

## 配置项

全部集中在 `index.html` 顶部的 `CONFIG`：

```js
venues: [
  { id:'necc', name:'国家会展中心', lat: 31.1937, lng: 121.3058, radius: 1200 },
  { id:'demo', name:'上海凯德国正中心', lat: 31.3109033, lng: 121.5015148, radius: 800 }
],
activeVenue: 'demo',          // 默认场地；正式上线改成 'necc'
window:     { start:'2026-10-29T00:00:00+08:00', end:'2026-11-01T00:00:00+08:00' },
overlayUrl: '',               // 展会平面图地址，留空则用内置示例图
overlaySpanMeters: 520,       // 底图覆盖边长（米）
lockShowsSelf: true           // 未解锁时是否显示灰色自身点位
```

## 关于展会底图

当前使用内置 SVG 示例图。替换方式：

1. 把平面图放到仓库里，例如 `assets/floorplan.png`
2. 设置 `CONFIG.overlayUrl = 'assets/floorplan.png'`
3. 调整 `overlaySpanMeters` 让图片覆盖范围与实际场馆一致

目前是矩形 bbox 拉伸对齐。如果平面图不是正南正北，需要改成四角点透视对齐（尚未实现）。

## 与现有能力的对接点

页面不包含真实路径规划，预留了钩子：

```js
window.ExpoMap_RoutePlan = function ({ from, to }) {
  // from: { lat, lng, acc }   to: { lat, lng, name }
  // 在这里调用已有的路径规划能力，拿到折线后替换地图上的占位连线
};
```

## 技术要点

- 地图瓦片：高德（GCJ-02），失败自动降级 OpenStreetMap（WGS84）
- 坐标转换：内置 WGS84 ⇄ GCJ-02 双向转换，避免国内地图偏移
- 罗盘：`webkitCompassHeading` / `alpha+beta+gamma` 倾角补偿 / 屏幕方向补偿
- 定位：`watchPosition`，页面不可见时主动 `clearWatch`，回到页面自动恢复
- 无第三方地图 SDK，仅约 800 行原生 JS

## 已知限制

- 桌面浏览器无方向传感器，箭头不显示（仅手机可用）
- iOS 需要用户手势触发方向权限（首次触摸时申请）
- 室内 GPS 精度差，围栏判定可能不准，调试时可点「模拟进入」
