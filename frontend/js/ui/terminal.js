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

// Appelée par Python via evaluate_js() - doit rester globale
function writeToTerminal(data) {
  term.write(data);
}

function getSafeColMargin() {
  const dpr = window.devicePixelRatio;
  return Number.isInteger(dpr) ? 0 : 2;
}

let resizeTimeout = null;

function sendResize() {
  const margin = getSafeColMargin();
  const safeCols = Math.max(term.cols - margin, 10);
  sshApi.resize(safeCols, term.rows);
}

function flushPendingResize() {
  if (resizeTimeout) {
    clearTimeout(resizeTimeout);
    resizeTimeout = null;
    sendResize();
  }
}

term.onData((data) => {
  flushPendingResize();
  sshApi.sendInput(data);
});

const terminalContainer = document.getElementById("terminal-container");

const resizeObserver = new ResizeObserver(() => {
  fitAddon.fit();

  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    sendResize();
    resizeTimeout = null;
  }, 400);
});
resizeObserver.observe(terminalContainer);