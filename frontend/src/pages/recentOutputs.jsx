// src/pages/recentOutputs.js

const KEY = "recent_outputs_v1";
const MAX = 10;

// Safe parse
function read() {
  try {
    const raw = localStorage.getItem(KEY);
    const arr = raw ? JSON.parse(raw) : [];
    return Array.isArray(arr) ? arr : [];
  } catch {
    return [];
  }
}

function write(arr) {
  localStorage.setItem(KEY, JSON.stringify(arr));
}

// Add newest at top, keep only last 10
export function addRecentOutput(entry) {
  if (!entry?.osf_url) return;

  const prev = read();

  const next = [
    {
      id: entry.id || `${Date.now()}_${Math.random().toString(16).slice(2)}`,
      created_at: entry.created_at || new Date().toISOString(),
      osf_url: entry.osf_url,
      input_preview: entry.input_preview || "",
    },
    ...prev,
  ]
    // remove duplicates by osf_url (keep the newest)
    .filter(
      (x, idx, arr) => idx === arr.findIndex((y) => y.osf_url === x.osf_url)
    )
    .slice(0, MAX);

  write(next);
}

export function getRecentOutputs() {
  return read();
}

export function clearRecentOutputs() {
  localStorage.removeItem(KEY);
}