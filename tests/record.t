type StudentRecord : record
    name : string
    age : int
    grade : real
end record

var student1 : StudentRecord

% Assign values to the record fields
student1.name := "Alice"
student1.age := 20
student1.grade := 92.5

% Display the record fields
put "Student Name: ", student1.name
put "Age: ", student1.age
put "Grade: ", student1.grade
