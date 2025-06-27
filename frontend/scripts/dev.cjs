if (process.platform !== 'win32') {
  console.error('本脚本仅支持Windows系统（需netsh命令）');
  process.exit(1);
}

const { execSync, spawn } = require('child_process');
const net = require('net');
const path = require('path');

// 检查netsh命令可用性
let hasNetsh = true;
try {
  execSync('where netsh', { stdio: 'ignore' });
} catch {
  hasNetsh = false;
  console.warn('【警告】未检测到netsh命令，未自动开放防火墙端口。请确保内网可访问此端口，或手动配置防火墙。');
}

// 生成随机五位端口
function getRandomPort() {
  return Math.floor(Math.random() * (65535 - 10000 + 1)) + 10000;
}

// 检查端口是否可用
function checkPort(port) {
  return new Promise((resolve) => {
    const server = net.createServer();
    server.once('error', () => resolve(false));
    server.once('listening', () => {
      server.close(() => resolve(true));
    });
    server.listen(port, '0.0.0.0');
  });
}

async function findAvailablePort() {
  for (let i = 0; i < 20; i++) {
    const port = getRandomPort();
    if (await checkPort(port)) return port;
  }
  throw new Error('未找到可用端口');
}

async function main() {
  const port = await findAvailablePort();
  const ruleName = `vite-dev-${port}`;
  if (hasNetsh) {
    try {
      execSync(`netsh advfirewall firewall add rule name="${ruleName}" dir=in action=allow protocol=TCP localport=${port}`);
      console.log(`已开放防火墙端口: ${port}`);
    } catch (e) {
      console.error('开放防火墙端口失败', e);
    }
  }
  // 启动Vite
  const vite = spawn('npx', ['vite', '--port', port, '--host'], {
    stdio: 'inherit',
    cwd: path.resolve(__dirname, '..'),
    shell: true,
    env: { ...process.env, VITE_PORT: port }
  });
  vite.on('exit', (code) => {
    if (hasNetsh) {
      try {
        execSync(`netsh advfirewall firewall delete rule name="${ruleName}"`);
        console.log(`已关闭防火墙端口: ${port}`);
      } catch (e) {
        console.error('关闭防火墙端口失败', e);
      }
    }
    process.exit(code);
  });
  process.on('SIGINT', () => vite.kill('SIGINT'));
  process.on('SIGTERM', () => vite.kill('SIGTERM'));
}

main(); 