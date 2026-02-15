const OUTPUTS_KEY = "recent_outputs_v1";
const MAX_OUTPUTS = 10;

function loadRecentOutputs() {
  try {
    const raw = localStorage.getItem(OUTPUTS_KEY);
    const arr = raw ? JSON.parse(raw) : [];
    return Array.isArray(arr) ? arr : [];
  } catch {
    return [];
  }
}

function saveRecentOutputs(list) {
  localStorage.setItem(OUTPUTS_KEY, JSON.stringify(list));
}

// Call this when backend returns { created_at, osf_url }
export function addRecentOutput({ created_at, osf_url }) {
  if (!created_at || !osf_url) return;

  const prev = loadRecentOutputs();

  // de-dupe by URL (or by created_at+url)
  const filtered = prev.filter((x) => x?.osf_url !== osf_url);

  const next = [{ created_at, osf_url }, ...filtered].slice(0, MAX_OUTPUTS);

  saveRecentOutputs(next);
  return next;
}

export function getRecentOutputs() {
  // optional: ensure sorted newest-first
  return loadRecentOutputs().sort(
    (a, b) => new Date(b.created_at) - new Date(a.created_at)
  );
}

export function clearRecentOutputs() {
  localStorage.removeItem(OUTPUTS_KEY);
}
