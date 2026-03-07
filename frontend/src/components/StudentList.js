import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function StudentList(){
  const [students, setStudents] = useState([]);

  const fetchStudents = async () => {
    const res = await axios.get('http://localhost:8000/students');
    setStudents(res.data);
  }

  useEffect(()=>{fetchStudents()},[]);

  const remove = async (id) => {
    if(!confirm('Delete student?')) return;
    await axios.delete(`http://localhost:8000/students/${id}`);
    fetchStudents();
  }

  const edit = async (s) => {
    const name = prompt('Name', s.name);
    if(name==null) return;
    const major = prompt('Major', s.major) || s.major;
    const birth_year = Number(prompt('Birth Year', s.birth_year) || s.birth_year);
    const gpa = Number(prompt('GPA', s.gpa) || s.gpa);
    await axios.put(`http://localhost:8000/students/${s.student_id}`, {student_id: s.student_id, name, birth_year, major, gpa});
    fetchStudents();
  }

  return (
    <table border="1" cellPadding="6">
      <thead>
        <tr><th>ID</th><th>Name</th><th>Major</th><th>GPA</th><th>Action</th></tr>
      </thead>
      <tbody>
        {students.map(s=> (
          <tr key={s.student_id}>
            <td>{s.student_id}</td>
            <td>{s.name}</td>
            <td>{s.major}</td>
            <td>{s.gpa}</td>
            <td>
              <button onClick={()=>edit(s)}>Edit</button>
              <button onClick={()=>remove(s.student_id)}>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
