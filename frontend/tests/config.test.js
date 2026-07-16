const fs = require('fs');
const path = require('path');
const assert = require('assert');

const configJs = fs.readFileSync(path.join(__dirname, '..', 'assets/js/config.js'), 'utf8');

try {
  assert.ok(configJs.includes('["127.0.0.1", "localhost"].includes(window.location.hostname)'), 'config should detect local dev hosts');
  assert.ok(configJs.includes('"http://127.0.0.1:8000"'), 'config should default local API origin to backend port 8000');
  console.log('config test passed');
} catch (error) {
  console.error(`config test failed: ${error.message}`);
  process.exit(1);
}
