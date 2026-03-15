const KEY = "recent_outputs_v1";
const MAX = 10;

function read() {
  try {
    const raw = localStorage.getItem(KEY);
    return raw ? JSON.parse(raw) : [];
  } catch { return []; }
}

// Add this to your recentOutputs.js
export function removeRecentOutput(id) {
  const prev = read();
  const next = prev.filter((o) => o.id !== id);
  write(next);
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
  
  // 1. Create the new entry with a GUARANTEED unique ID
  const newEntry = {
    id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`, // Truly unique
    created_at: entry.created_at || new Date().toISOString(),
    osf_url: entry.osf_url,
    input_preview: entry.input_preview || "Materials Combination",
  };

  // 2. Add it to the front
  const next = [newEntry, ...prev]
    // 3. Filter by ID (or remove filter entirely if you want to allow duplicates)
    .filter((x, idx, arr) => idx === arr.findIndex((y) => y.id === x.id))
    .slice(0, MAX);

  write(next);
}

export function getRecentOutputs() { return read(); }
export function clearRecentOutputs() { 
  localStorage.removeItem(KEY); 
  window.dispatchEvent(new Event("recent_outputs_updated"));
}