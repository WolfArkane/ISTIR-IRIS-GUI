const term = new Terminal({
  cursorBlink: true,
  theme: { background: "#0c0c0c" },
  convertEol: true
});
const fitAddon = new FitAddon.FitAddon();
term.loadAddon(fitAddon);
term.open(document.getElementById("terminal-container"));

window.term = term;
window.fitAddon = fitAddon;

function writeToTerminal(data) {
  term.write(data);
}

function getSafeColMargin() {
  const dpr = window.devicePixelRatio;
  return Number.isInteger(dpr) ? 0 : 2;
}

function flushPendingResize() {
  if (resizeTimeout) {
    clearTimeout(resizeTimeout);
    resizeTimeout = null;
    const margin = getSafeColMargin();
    const safeCols = Math.max(term.cols - margin, 10);
    window.pywebview.api.ssh_resize(safeCols, term.rows);
  }
}

term.onData((data) => {
  flushPendingResize();
  window.pywebview.api.ssh_send_input(data);
});

let resizeTimeout = null;
const terminalContainer = document.getElementById("terminal-container");

const resizeObserver = new ResizeObserver(() => {
  fitAddon.fit();

  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    const margin = getSafeColMargin();
    const safeCols = Math.max(term.cols - margin, 10);
    window.pywebview.api.ssh_resize(safeCols, term.rows);
    resizeTimeout = null;
  }, 400);
});
resizeObserver.observe(terminalContainer);