const { app, BrowserWindow } = require("electron");
const path = require("path");

const APP_URL = "http://nutrygym-uce-qa-alb-1894441400.us-east-1.elb.amazonaws.com/"; // tu web en AWS

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    show: true,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, "preload.js"), // opcional
    },
  });

  // Intenta cargar la web
  win.loadURL(APP_URL).catch(() => {
    // Si falla, carga página local
    win.loadFile(path.join(__dirname, "offline.html"));
  });

  // Si el render falla por caída de red, también caemos a offline
  win.webContents.on("did-fail-load", () => {
    win.loadFile(path.join(__dirname, "offline.html"));
  });
}

app.whenReady().then(() => {
  createWindow();
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
