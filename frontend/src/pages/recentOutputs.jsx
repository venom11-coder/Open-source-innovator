const KEY = "recent_outputs_v1";
const MAX = 10;

function read() {
  try {
    const raw = localStorage.getItem(KEY);
    return raw ? JSON.parse(raw) : [];
  } catch { return []; }
}

function write(arr) {
  localStorage.setItem(KEY, JSON.stringify(arr));
  // Wrapping in a 0ms timeout pushes the event to the end of the 
  // execution stack, ensuring the component is ready to hear it.
  setTimeout(() => {
    window.dispatchEvent(new Event("recent_outputs_updated"));
  }, 0);
}

export function addRecentOutput(entry) {
  if (!entry?.osf_url) return;
  const prev = read();
  const next = [
    {
      id: entry.id || `${Date.now()}`,
      created_at: entry.created_at || new Date().toISOString(),
      osf_url: entry.osf_url,
      input_preview: entry.input_preview || "Materials Combination",
    },
    ...prev,
  ]
  .filter((x, idx, arr) => idx === arr.findIndex((y) => y.osf_url === x.osf_url))
  .slice(0, MAX);

  write(next);
}

export function getRecentOutputs() { return read(); }
export function clearRecentOutputs() { 
  localStorage.removeItem(KEY); 
  window.dispatchEvent(new Event("recent_outputs_updated"));
}