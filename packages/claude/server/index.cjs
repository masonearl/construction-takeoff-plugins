// The companion is installed separately by Construction Takeoff; no downloads occur here.
const { spawn } = require('node:child_process');
const { accessSync, constants } = require('node:fs');
const { homedir } = require('node:os');
const { join } = require('node:path');
if (process.platform !== 'darwin') {
  console.error('Construction Takeoff requires macOS and the separately installed Construction Takeoff companion.');
  process.exit(69);
}
const companion = join(homedir(), '.local', 'bin', 'takeoff-mcp');
try { accessSync(companion, constants.X_OK); } catch {
  console.error('Construction Takeoff companion missing. Export AI setup from Construction Takeoff > 3D Model > AI tools and install it first. Expected ~/.local/bin/takeoff-mcp.');
  process.exit(69);
}
const child = spawn(companion, [], {
  stdio: 'inherit',
  env: { ...process.env, TAKEOFF_MCP_ENABLE_LEGACY_WRITES: '0' }
});
child.on('error', (error) => { console.error('Cannot start Construction Takeoff companion:', error.message); process.exitCode = 69; });
child.on('exit', (code, signal) => { process.exitCode = code ?? (signal === 'SIGINT' ? 130 : 143); });
for (const signal of ['SIGINT', 'SIGTERM', 'SIGHUP']) {
  process.on(signal, () => child.kill(signal));
}
