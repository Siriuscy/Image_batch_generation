const { app, BrowserWindow, protocol } = require('electron');
const path = require('path');

// 在应用准备就绪之前注册协议
app.whenReady().then(() => {
  protocol.registerFileProtocol('file', (request, callback) => {
    const pathname = decodeURI(request.url.replace('file:///', ''));
    callback(pathname);
  });
});

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      webSecurity: false,
      enableRemoteModule: true,
      additionalArguments: [`--app-path=${app.getAppPath()}`]
    }
  });

  // 开发环境使用相对路径，生产环境使用绝对路径
  if (process.env.NODE_ENV === 'development') {
    win.loadFile('index.html');
  } else {
    win.loadFile(path.join(app.getAppPath(), 'index.html'));
  }
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
