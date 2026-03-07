import React, { useState } from 'react';
import axios from 'axios';

export default function AddStudent(){
  const [student, setStudent] = useState({student_id:'', name:'', birth_year:'', major:'', gpa:''});

  const onChange = e => setStudent({...student, [e.target.name]: e.target.value});

  const onSubmit = async e => {
    e.preventDefault();
    try{
      await axios.post('http://localhost:8000/students', {
        student_id: student.student_id,
        name: student.name,
        birth_year: Number(student.birth_year),
        major: student.major,
        gpa: Number(student.gpa)
      });
      window.location.reload();
    }catch(err){
      alert(err.response?.data?.detail || 'Error');
    }
  }

  return (
    <form onSubmit={onSubmit} style={{marginBottom:20}}>
      <div>
        <label>Student ID:</label>
        <input name="student_id" value={student.student_id} onChange={onChange} required />
      </div>
      <div>
        <label>Name:</label>
        <input name="name" value={student.name} onChange={onChange} required />
      </div>
      <div>
        <label>Birth Year:</label>
        <input name="birth_year" value={student.birth_year} onChange={onChange} required />
      </div>
      <div>
        <label>Major:</label>
        <input name="major" value={student.major} onChange={onChange} required />
      </div>
      <div>
        <label>GPA:</label>
        <input name="gpa" value={student.gpa} onChange={onChange} required />
      </div>
      <button type="submit">Add Student</button>
    </form>
  )
}
