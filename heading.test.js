const PI = Math.PI;

function rotateToWorld(alpha, beta, gamma, v){
  const a = alpha * PI / 180, b = beta * PI / 180, g = gamma * PI / 180;
  const ca = Math.cos(a), sa = Math.sin(a);
  const cb = Math.cos(b), sb = Math.sin(b);
  const cg = Math.cos(g), sg = Math.sin(g);
  let x = v[0] * cg + v[2] * sg;
  let y = v[1];
  let z = -v[0] * sg + v[2] * cg;
  const y2 = y * cb - z * sb;
  const z2 = y * sb + z * cb;
  y = y2; z = z2;
  const x3 = x * ca - y * sa;
  const y3 = x * sa + y * ca;
  return [x3, y3, z];
}
function azimuthOf(vec){
  let d = Math.atan2(vec[0], vec[1]) * 180 / PI;
  if (d < 0) d += 360;
  return d;
}
let lastTopZ = 0;
function headingFromOrientation(alpha, beta, gamma){
  const top = rotateToWorld(alpha, beta, gamma, [0, 1, 0]);
  const back = rotateToWorld(alpha, beta, gamma, [0, 0, -1]);
  lastTopZ = top[2];
  const topAz = azimuthOf(top), backAz = azimuthOf(back);
  const wBack = Math.max(0, Math.min(1, 1 - Math.abs(back[2])));
  const wTop = 1 - wBack;
  const rad = PI / 180;
  const x = wTop * Math.sin(topAz * rad) + wBack * Math.sin(backAz * rad);
  const y = wTop * Math.cos(topAz * rad) + wBack * Math.cos(backAz * rad);
  let h;
  if (Math.hypot(x, y) < 0.25) h = Math.abs(top[2]) < Math.abs(back[2]) ? backAz : topAz;
  else h = (Math.atan2(x, y) * 180 / PI + 360) % 360;
  if (top[2] < -0.7) h = (h + 180) % 360;
  return h;
}

const cases = [
  [0,   0,  0,   '平放，顶部朝北', 0],
  [270, 0,  0,   '平放，顶部朝东', 90],
  [180, 0,  0,   '平放，顶部朝南', 180],
  [90,  0,  0,   '平放，顶部朝西', 270],
  [270, 90, 0,   '立起，镜头朝东', 90],
  [180, 90, 0,   '立起，镜头朝南', 180],
  [0,   90, 0,   '立起，镜头朝北', 0],
  [90,  90, 0,   '立起，镜头朝西', 270],
  [0,   45, 0,   '倾斜45°，朝北', 0],
  [270, 45, 0,   '倾斜45°，朝东', 90],
  [0,   60, 0,   '倾斜60°，朝北', 0],
  [270, 60, 0,   '倾斜60°，朝东', 90],
  [0,   30, 0,   '倾斜30°，朝北', 0],
  [0,   88, 0,   '近垂直，朝北', 0],
  [0,   2,  0,   '近水平，朝北', 0],
  [0,   90, 20,  '立起+绕竖轴偏20°，朝北', 340],
  [0,  -90, 0,   '倾角符号反向（iQOO 场景）', 0],
  [270,-90, 0,   '倾角反向且朝东', 90],
];

let bad = 0;
for (const [a, b, g, label, expect] of cases){
  const got = headingFromOrientation(a, b, g);
  const diff = Math.abs(((got - expect + 540) % 360) - 180);
  const ok = diff < 1.5;
  if (!ok) bad++;
  console.log(
    (ok ? 'PASS' : 'FAIL') + '  ' + label.padEnd(22) +
    ' a=' + String(a).padStart(3) + ' b=' + String(b).padStart(2) + ' g=' + String(g).padStart(2) +
    '  -> ' + got.toFixed(1) + '°  (期望 ' + expect + '°)'
  );
}
console.log('\n失败数: ' + bad);

/* ---------- 连续性检查：倾角扫过临界区不应出现跳变 ---------- */
function scan(gamma){
  let maxStep = 0, at = null, prev = null;
  for (let b = 0; b <= 90; b += 0.5){
    const h = headingFromOrientation(0, b, gamma);
    if (prev !== null){
      const d = Math.abs(((h - prev + 540) % 360) - 180);
      if (d > maxStep){ maxStep = d; at = b; }
    }
    prev = h;
  }
  console.log(`倾角 0→90 (γ=${gamma}) 单步最大跳变 ${maxStep.toFixed(2)}°  @β=${at}`);
  return maxStep;
}
console.log('');
scan(0); scan(-20); scan(20); scan(-40);
