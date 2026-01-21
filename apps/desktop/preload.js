/**
 * preload.js
 * Capa segura entre el renderer (web) y Electron.
 * Para la app NutryGym Desktop (informativa).
 */

window.addEventListener("DOMContentLoaded", () => {
  // Puedes exponer solo información básica si lo deseas
  const info = {
    appName: "NutryGym Desktop",
    platform: process.platform,
    version: process.versions.electron,
  };

  // Exponer datos de solo lectura al frontend (opcional)
  window.__NUTRYGYM__ = Object.freeze(info);
});
