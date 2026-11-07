// Render lớp đồ hoạ trong suốt từ overlay.html thành chuỗi PNG.
//   node render.js <overlay.html> <outdir> <fps> <fromFrame> <toFrame>
//   node render.js <overlay.html> <outdir> times 2.5,11,16.9     (xem thử vài thời điểm)
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [html, out, a, b, c] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.resolve(html));
  await page.evaluate(() => document.fonts.ready);
  const shot = async (t, file) => {
    await page.evaluate(t => window.setT(t), t);
    await page.screenshot({ path: file, omitBackground: true });
  };
  if (a === 'times') {
    for (const t of b.split(',').map(Number)) await shot(t, path.join(out, `t_${t.toFixed(2)}.png`));
  } else {
    const fps = +a;
    for (let i = +b; i < +c; i++) await shot(i / fps, path.join(out, `f_${String(i).padStart(5, '0')}.png`));
  }
  await browser.close();
})();
