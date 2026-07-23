const fs = require('fs');
const path = require('path');
const assert = require('assert');

const frontendRoot = path.join(__dirname, '..');
const appJs = fs.readFileSync(path.join(frontendRoot, 'assets/js/app.js'), 'utf8');
const clientJs = fs.readFileSync(path.join(frontendRoot, 'assets/js/api/client.js'), 'utf8');

function functionBody(source, functionName) {
  const start = source.indexOf(`async function ${functionName}`);
  assert.ok(start >= 0, `missing function ${functionName}`);
  const end = source.indexOf('\n}\n', start);
  assert.ok(end > start, `missing function end for ${functionName}`);
  return source.slice(start, end);
}

try {
  const subtitleSubmitBody = functionBody(appJs, 'handleSubtitleSubmit');
  const burnSubmitBody = functionBody(appJs, 'handleBurnSubmit');
  const compressSubmitBody = functionBody(appJs, 'handleToolSubmit');
  const loginSubmitBody = functionBody(appJs, 'handleLoginSubmit');
  const registerSubmitBody = functionBody(appJs, 'handleRegisterSubmit');

  assert.ok(
    subtitleSubmitBody.includes('await loadToolRuns();'),
    'subtitle submit should refresh tool run history after completion',
  );
  assert.ok(
    burnSubmitBody.includes('await loadToolRuns();'),
    'burn submit should refresh tool run history after completion',
  );
  assert.ok(
    compressSubmitBody.includes('await loadToolRuns();'),
    'video compress submit should refresh tool run history after completion',
  );
  assert.ok(
    appJs.includes('run.errorMessage'),
    'tool run history should render failure messages when present',
  );
  assert.ok(
    appJs.includes('toUserMessage(error'),
    'page actions should convert request errors into user-facing messages',
  );
  assert.ok(
    loginSubmitBody.includes('toUserMessage(error'),
    'login submit should use user-facing error messages',
  );
  assert.ok(
    registerSubmitBody.includes('toUserMessage(error'),
    'register submit should use user-facing error messages',
  );
  assert.ok(
    !compressSubmitBody.includes('error.message || "Please try again later"'),
    'video compress submit should not expose raw error.message fallback',
  );
  assert.ok(
    !subtitleSubmitBody.includes('error.message || "Please try again later"'),
    'subtitle submit should not expose raw error.message fallback',
  );
  assert.ok(
    !burnSubmitBody.includes('error.message || "Please try again later"'),
    'burn submit should not expose raw error.message fallback',
  );
  assert.ok(
    clientJs.includes('buildApiError'),
    'api client should normalize server failures before surfacing them',
  );
  assert.ok(
    !clientJs.includes('throw new Error(payload.detail || JSON.stringify(payload));'),
    'api client should not throw raw FastAPI detail payloads',
  );
  console.log('tool history and error handling test passed');
} catch (error) {
  console.error(`tool history and error handling test failed: ${error.message}`);
  process.exit(1);
}
