import React from 'react';
import StudentList from './components/StudentList';
import AddStudent from './components/AddStudent';

export default function App(){
  return (
    <div style={{padding:20}}>
      <h1>Student Management</h1>
      <AddStudent />
      <hr />
      <StudentList />
    </div>
  )
}
