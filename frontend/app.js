const API = "http://localhost:8000";

async function fetchStudents(q) {
  const url = q
    ? `${API}/students?q=${encodeURIComponent(q)}`
    : `${API}/students`;
  const res = await fetch(url);
  return res.json();
}

function renderTable(students) {
  const tbody = document.querySelector("#studentsTable tbody");
  tbody.innerHTML = "";
  students.forEach((s) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${s.student_id}</td><td>${s.name}</td><td>${s.major}</td><td>${s.gpa}</td><td><button data-id="${s.student_id}" class="edit">Edit</button> <button data-id="${s.student_id}" class="del">Delete</button></td>`;
    tbody.appendChild(tr);
  });
}

async function load(q) {
  const students = await fetchStudents(q);
  renderTable(students);
}

document.getElementById("btnRefresh").addEventListener("click", () => load());
document.getElementById("btnSearch").addEventListener("click", () => {
  const q = document.getElementById("search").value.trim();
  load(q);
});

document.getElementById("btnExport").addEventListener("click", () => {
  window.location = `${API}/export`;
});

document
  .querySelector("#studentsTable tbody")
  .addEventListener("click", async (e) => {
    if (e.target.classList.contains("edit")) {
      const id = e.target.dataset.id;
      const res = await fetch(`${API}/students/${id}`);
      const s = await res.json();
      document.getElementById("student_id").value = s.student_id;
      document.getElementById("student_id").disabled = true;
      document.getElementById("name").value = s.name;
      document.getElementById("birth_year").value = s.birth_year;
      document.getElementById("major").value = s.major;
      document.getElementById("gpa").value = s.gpa;
    }
    if (e.target.classList.contains("del")) {
      const id = e.target.dataset.id;
      if (confirm("Delete student " + id + "?")) {
        await fetch(`${API}/students/${id}`, { method: "DELETE" });
        load();
      }
    }
  });

document
  .getElementById("studentForm")
  .addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const student = {
      student_id: document.getElementById("student_id").value.trim(),
      name: document.getElementById("name").value.trim(),
      birth_year: parseInt(document.getElementById("birth_year").value, 10),
      major: document.getElementById("major").value.trim(),
      gpa: parseFloat(document.getElementById("gpa").value),
    };
    const idDisabled = document.getElementById("student_id").disabled;
    if (idDisabled) {
      // update
      await fetch(`${API}/students/${student.student_id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(student),
      });
      document.getElementById("student_id").disabled = false;
    } else {
      // create
      await fetch(`${API}/students`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(student),
      });
    }
    ev.target.reset();
    load();
  });

// initial load
load();
