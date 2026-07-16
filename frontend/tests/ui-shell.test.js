const fs = require('fs');
const path = require('path');
const assert = require('assert');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const frontendRoot = path.join(__dirname, '..');
const appJs = fs.readFileSync(path.join(frontendRoot, 'assets/js/app.js'), 'utf8');
const i18nJs = fs.readFileSync(path.join(frontendRoot, 'assets/js/i18n/index.js'), 'utf8');

function expectIncludes(fragment, message) {
  assert.ok(html.includes(fragment), message);
}

function expectAppIncludes(fragment, message) {
  assert.ok(appJs.includes(fragment), message);
}

function expectFile(relativePath, message) {
  assert.ok(fs.existsSync(path.join(frontendRoot, relativePath)), message);
}

function expectI18nIncludes(fragment, message) {
  assert.ok(i18nJs.includes(fragment), message);
}

try {
  expectIncludes('id="themeSwitcher"', 'missing theme switcher mount point');
  expectIncludes('id="languageSwitcher"', 'missing language switcher mount point');
  expectIncludes('id="userMenuButton"', 'missing user menu button');
  expectIncludes('id="userMenu"', 'missing user menu panel');
  expectIncludes('id="adminSettingsEntry"', 'missing admin settings entry mount');
  expectAppIncludes('openStoragePolicyPanel', 'missing storage policy panel opener');
  expectAppIncludes('loadStoragePolicySettings', 'missing storage policy loader');
  expectAppIncludes('saveStoragePolicySettings', 'missing storage policy save handler');
  expectAppIncludes('runManualStorageCleanup', 'missing manual cleanup handler');
  expectAppIncludes('isAdminUser', 'missing admin role gate');
  expectIncludes('id="storagePolicyPanel"', 'missing storage policy panel');
  expectIncludes('存储与清理策略', 'missing storage policy copy');
  expectIncludes('最近清理记录', 'missing cleanup activity summary');
  expectIncludes('id="modalRoot"', 'missing modal root container');
  expectIncludes('id="view"', 'missing view mount');
  expectIncludes('assets/css/base.css', 'missing base stylesheet');
  expectIncludes('assets/css/layout.css', 'missing layout stylesheet');
  expectIncludes('assets/css/components.css', 'missing components stylesheet');
  expectIncludes('assets/js/app.js', 'missing app module entry');
  expectIncludes('type="module"', 'index should load module entry');
  expectFile('assets/css/base.css', 'missing base stylesheet file');
  expectFile('assets/css/layout.css', 'missing layout stylesheet file');
  expectFile('assets/css/components.css', 'missing components stylesheet file');
  expectFile('assets/js/app.js', 'missing app module file');
  expectFile('assets/js/config.js', 'missing config module file');
  expectFile('assets/js/i18n/index.js', 'missing i18n index module file');
  expectFile('assets/js/i18n/messages.js', 'missing i18n messages module file');
  expectFile('assets/js/state/store.js', 'missing store module file');
  expectFile('assets/js/api/client.js', 'missing api client module file');
  expectFile('assets/js/api/tools.js', 'missing tools api module file');
  expectFile('assets/js/api/admin.js', 'missing admin api module file');
  expectFile('assets/js/components/modal.js', 'missing modal component module file');
  expectFile('assets/js/components/toast.js', 'missing toast component module file');
  expectFile('assets/js/components/theme-switcher.js', 'missing theme switcher module file');
  expectFile('assets/js/components/user-menu.js', 'missing user menu module file');
  expectFile('assets/js/components/storage-policy-panel.js', 'missing storage policy panel module file');
  expectFile('assets/js/views/dashboard.js', 'missing dashboard view module file');
  expectFile('assets/js/views/auth.js', 'missing auth view module file');
  expectFile('assets/js/views/tools.js', 'missing tools view module file');
  expectFile('assets/js/views/nodes.js', 'missing nodes view module file');
  expectFile('assets/js/views/graph.js', 'missing graph view module file');
  expectFile('assets/js/views/roadmaps.js', 'missing roadmaps view module file');
  expectFile('assets/js/tools/video-compress.js', 'missing video tool module file');
  expectFile('assets/js/tools/vtt-subtitle.js', 'missing subtitle tool module file');
  expectFile('assets/js/tools/video-subtitle-burn.js', 'missing burn tool module file');
  expectFile('assets/js/utils/format.js', 'missing format util module file');
  expectFile('assets/js/utils/router.js', 'missing router util module file');
  expectAppIncludes('show("login")', 'missing login route handling');
  expectAppIncludes('show("register")', 'missing register route handling');
  expectAppIncludes('renderLanguageSwitcher', 'missing language switcher renderer');
  expectAppIncludes('setLocale(', 'missing locale setter wiring');
  expectI18nIncludes('hagsyn_locale', 'missing locale persistence key usage');
  expectAppIncludes('/api/auth/me', 'missing current-user auth check');
  assert.ok(!html.includes('生成示例数据'), 'demo seed entry should be removed');
  assert.ok(!html.includes('普通用户也可见存储与清理策略'), 'regular users should not see admin storage policy copy');
  console.log('ui shell test passed');
} catch (error) {
  console.error(`ui shell test failed: ${error.message}`);
  process.exit(1);
}
