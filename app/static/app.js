// OWC Consultant Copilot — minimal client for the capture API.

const state = { hospital: null, department: null, meeting: null };

const $ = (id) => document.getElementById(id);

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail || JSON.stringify(body);
    } catch (_) { /* ignore */ }
    throw new Error(`${res.status}: ${detail}`);
  }
  return res.json();
}

let toastTimer;
function toast(message, isError = false) {
  const el = $("toast");
  el.textContent = message;
  el.classList.remove("hidden", "error");
  if (isError) el.classList.add("error");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.add("hidden"), 2800);
}

// --- Hospitals ---
async function loadHospitals() {
  const list = $("hospital-list");
  const hospitals = await api("/hospitals");
  list.innerHTML = "";
  hospitals.forEach((h) => {
    const li = document.createElement("li");
    li.textContent = h.name;
    li.classList.toggle("selected", state.hospital && state.hospital.id === h.id);
    li.onclick = () => selectHospital(h);
    list.appendChild(li);
  });
}

async function selectHospital(h) {
  state.hospital = h;
  state.department = null;
  state.meeting = null;
  await loadHospitals();
  $("hospital-context").textContent = `— ${h.name}`;
  $("department-hint").classList.add("hidden");
  $("department-form").classList.remove("hidden");
  await loadDepartments();
  resetMeetingAndExtraction();
}

// --- Departments ---
async function loadDepartments() {
  const list = $("department-list");
  list.innerHTML = "";
  if (!state.hospital) return;
  const departments = await api(`/hospitals/${state.hospital.id}/departments`);
  departments.forEach((d) => {
    const li = document.createElement("li");
    li.textContent = d.name;
    li.classList.toggle("selected", state.department && state.department.id === d.id);
    li.onclick = () => selectDepartment(d);
    list.appendChild(li);
  });
}

async function selectDepartment(d) {
  state.department = d;
  state.meeting = null;
  await loadDepartments();
  $("department-context").textContent = `— ${d.name}`;
  $("meeting-hint").classList.add("hidden");
  $("meeting-form").classList.remove("hidden");
  await loadMeetings();
  resetExtraction();
}

// --- Meetings ---
async function loadMeetings() {
  const list = $("meeting-list");
  list.innerHTML = "";
  if (!state.department) return;
  const meetings = await api(`/departments/${state.department.id}/meetings`);
  meetings.forEach((m) => {
    const li = document.createElement("li");
    li.textContent = m.title;
    const sub = document.createElement("span");
    sub.className = "sub";
    sub.textContent = m.transcript ? m.transcript.slice(0, 80) : "(no transcript)";
    li.appendChild(sub);
    li.classList.toggle("selected", state.meeting && state.meeting.id === m.id);
    li.onclick = () => selectMeeting(m);
    list.appendChild(li);
  });
}

async function selectMeeting(m) {
  state.meeting = m;
  await loadMeetings();
  $("meeting-context").textContent = `— ${m.title}`;
  $("extraction-hint").classList.add("hidden");
  $("extraction-forms").classList.remove("hidden");
  await loadRecorded();
}

function resetMeetingAndExtraction() {
  $("meeting-context").textContent = "";
  $("meeting-hint").classList.remove("hidden");
  $("meeting-form").classList.add("hidden");
  $("meeting-list").innerHTML = "";
  resetExtraction();
}

function resetExtraction() {
  $("meeting-context").textContent = "";
  $("extraction-hint").classList.remove("hidden");
  $("extraction-forms").classList.add("hidden");
  $("recorded").innerHTML = "";
}

// --- Extraction summary ---
async function loadRecorded() {
  const el = $("recorded");
  el.innerHTML = "";
  if (!state.meeting) return;
  const mid = state.meeting.id;
  const did = state.department.id;
  const [workflows, problems, risks, stakeholders] = await Promise.all([
    api(`/departments/${did}/workflows`),
    api(`/departments/${did}/problems`),
    api(`/departments/${did}/adoption-risks`),
    api(`/meetings/${mid}/stakeholders`),
  ]);
  const tags = [];
  workflows.forEach((w) => tags.push(`Workflow: ${w.description.slice(0, 60)}`));
  problems.forEach((p) => tags.push(`Problem: ${p.title}`));
  risks.forEach((r) => tags.push(`Risk: ${r.title}`));
  stakeholders.forEach((s) => tags.push(`Stakeholder: ${s.name}`));
  el.innerHTML = tags.map((t) => `<span class="tag">${t}</span>`).join("") ||
    '<span class="muted">Nothing recorded yet.</span>';
}

// --- Form handlers ---
$("hospital-form").onsubmit = async (e) => {
  e.preventDefault();
  const input = $("hospital-name");
  try {
    const h = await api("/hospitals", { method: "POST", body: JSON.stringify({ name: input.value }) });
    input.value = "";
    toast(`Hospital "${h.name}" added`);
    await loadHospitals();
    selectHospital(h);
  } catch (err) { toast(err.message, true); }
};

$("department-form").onsubmit = async (e) => {
  e.preventDefault();
  const input = $("department-name");
  try {
    const d = await api(`/hospitals/${state.hospital.id}/departments`, {
      method: "POST", body: JSON.stringify({ name: input.value }),
    });
    input.value = "";
    toast(`Department "${d.name}" added`);
    await loadDepartments();
    selectDepartment(d);
  } catch (err) { toast(err.message, true); }
};

$("meeting-form").onsubmit = async (e) => {
  e.preventDefault();
  try {
    const m = await api(`/departments/${state.department.id}/meetings`, {
      method: "POST",
      body: JSON.stringify({ title: $("meeting-title").value, transcript: $("meeting-transcript").value }),
    });
    $("meeting-title").value = "";
    $("meeting-transcript").value = "";
    toast(`Meeting "${m.title}" recorded`);
    await loadMeetings();
    selectMeeting(m);
  } catch (err) { toast(err.message, true); }
};

$("workflow-form").onsubmit = async (e) => {
  e.preventDefault();
  try {
    await api(`/meetings/${state.meeting.id}/workflows`, {
      method: "POST", body: JSON.stringify({ description: $("workflow-description").value }),
    });
    $("workflow-description").value = "";
    toast("Workflow added");
    await loadRecorded();
  } catch (err) { toast(err.message, true); }
};

$("problem-form").onsubmit = async (e) => {
  e.preventDefault();
  try {
    await api(`/meetings/${state.meeting.id}/problems`, {
      method: "POST",
      body: JSON.stringify({ title: $("problem-title").value, description: $("problem-description").value }),
    });
    $("problem-title").value = "";
    $("problem-description").value = "";
    toast("Problem added");
    await loadRecorded();
  } catch (err) { toast(err.message, true); }
};

$("risk-form").onsubmit = async (e) => {
  e.preventDefault();
  try {
    await api(`/meetings/${state.meeting.id}/adoption-risks`, {
      method: "POST",
      body: JSON.stringify({ title: $("risk-title").value, description: $("risk-description").value }),
    });
    $("risk-title").value = "";
    $("risk-description").value = "";
    toast("Adoption risk added");
    await loadRecorded();
  } catch (err) { toast(err.message, true); }
};

$("stakeholder-form").onsubmit = async (e) => {
  e.preventDefault();
  try {
    const s = await api(`/departments/${state.department.id}/stakeholders`, {
      method: "POST",
      body: JSON.stringify({ name: $("stakeholder-name").value, role: $("stakeholder-role").value }),
    });
    await api(`/meetings/${state.meeting.id}/stakeholders`, {
      method: "POST", body: JSON.stringify({ stakeholder_id: s.id }),
    });
    $("stakeholder-name").value = "";
    $("stakeholder-role").value = "";
    toast(`Stakeholder "${s.name}" added & linked`);
    await loadRecorded();
  } catch (err) { toast(err.message, true); }
};

// --- Boot ---
loadHospitals().catch((err) => toast(err.message, true));
