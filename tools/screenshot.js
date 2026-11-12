// Screenshot an HTML page at 1280x720 (thumbnails). Usage: node screenshot.js <page.html> <out.jpg>
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
  await p.goto('file://' + process.argv[2]); await p.waitForTimeout(500);
  await p.screenshot({ path: process.argv[3], type: 'jpeg', quality: 92 }); await b.close();
})();
