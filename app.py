from flask import Flask, render_template, request, redirect, flash
import oracledb
 
app = Flask(__name__)
app.secret_key = "theneuralstriker@biswojit" 
 
oracledb.init_oracle_client(lib_dir= r"C:\oracle\instantclient_23_9")
# Oracle THIN Mode Connection
connection = oracledb.connect(
    user="your user name",
    password="your password",
    host="hostname",
    port=1521,
    sid="sis"
)

# Fetch Employee data
@app.route('/')
def index():
    cursor = connection.cursor()
    cursor.execute("SELECT T.EMP_ID, T.EMP_NAME, T.EMP_SAL, T.DEPT_ID, T1.DEPT_NAME,  CAST(TRUNC(DOB) AS DATE) as DOB, T.AADHAAR, T.ACTIVE_STATUS  FROM EMPLOYEE T, DEPARTMENT T1 WHERE T.DEPT_ID=T1.DEPT_ID order by emp_id desc")
    employees = cursor.fetchall()
    return render_template('index.html', employees=employees)

 # Add Employee data
@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        sal = request.form['salary']
        deptid = request.form['deptid']
        dob = request.form['dob']
        aadhaar = request.form['aadhaar']
        activestatus = request.form['activestatus']
        bssal = request.form['bssal']
        hra = request.form['hra']
        lta = request.form['lta']
        pa = request.form['pa']
        ca = request.form['ca']
        pp = request.form['pp']
        ts = request.form['ts']
        cursor = connection.cursor()
        cursor.execute("INSERT INTO EMPLOYEE (EMP_ID, EMP_NAME, EMP_SAL, DEPT_ID, DOB, AADHAAR, ACTIVE_STATUS) VALUES (EMP_SEQ.NEXTVAL, :1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5, :6)", (name, sal, deptid, dob, aadhaar, activestatus))
        # generated_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO employee_salary_details (EMP_ID, BASIC_SAL, HR_ALWC, LT_ALWC, PER_ALWC, CITY_ALWC, PERF_PAY, TOTAL) VALUES (EMP_SEQ.CURRVAL,:1, :2, :3, :4, :5, :6, :7)", ( bssal, hra, lta, pa, ca, pp, ts))
        connection.commit()
        return redirect('/')
    return render_template('add.html')

 # Edit Employee data
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    cursor = connection.cursor()
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        sal = request.form['salary']
        deptid = request.form['deptid']
        dob = request.form['dob']
        aadhaar = request.form['aadhaar']
        activestatus = request.form['activestatus']
        bssal = request.form['bssal']
        hra = request.form['hra']
        lta = request.form['lta']
        pa = request.form['pa']
        ca = request.form['ca']
        pp = request.form['pp']
        ts = request.form['ts']
        cursor.execute("UPDATE EMPLOYEE SET EMP_ID =:1, EMP_NAME=:2, EMP_SAL=:3, DEPT_ID=:4, DOB=TO_DATE(:5, 'YYYY-MM-DD'), AADHAAR=:6, ACTIVE_STATUS=:7  WHERE EMP_ID=:8", (id, name, ts, deptid, dob, aadhaar, activestatus, id))
        cursor.execute("UPDATE employee_salary_details SET Basic_sal =:1, HR_Alwc =:2, lt_Alwc =:3, Per_Alwc =:4, City_alwc =:5, perf_Pay =:6, Total =:7 WHERE EMP_ID=:8", (bssal, hra, lta, pa, ca, pp, ts, id))
        # cursor.execute("UPDATE EMPLOYEE SET EMP_SAL=:1 WHERE EMP_ID=:2", (ts, id))
        connection.commit()
        return redirect('/')
    cursor.execute("select t1.EMP_ID, t1.EMP_NAME, t1.EMP_SAL, t1.DEPT_ID, t1.DOB, t1.AADHAAR, t1.ACTIVE_STATUS, t.Basic_sal, t.HR_Alwc, t.lt_Alwc, t.Per_Alwc, t.City_alwc, t.perf_Pay , t.Total from employee_salary_details t, employee t1 where t.emp_id=t1.emp_id and t1.EMP_ID=:1", [id])
    employee = cursor.fetchone()
    return render_template('edit.html', employee=employee, emp_id=id)


 # Delete Employee data
@app.route('/delete/<int:id>')
def delete_employee(id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM EMPLOYEE WHERE EMP_ID=:1", [id])
    connection.commit()
    return redirect('/')

# Fetch Department
@app.route('/department')
def department():
    cursor = connection.cursor()
    cursor.execute("SELECT dept_id, dept_name FROM DEPARTMENT order by dept_id asc")
    department = cursor.fetchall()
    return render_template('department.html', department=department)

# Add Department
@app.route('/addDepartment', methods=['GET', 'POST'])
def add_department():
    if request.method == 'POST':
        deptid = request.form['deptid']
        deptname = request.form['deptname']
        cursor = connection.cursor()
        cursor.execute("INSERT INTO DEPARTMENT (DEPT_ID, DEPT_NAME) VALUES (:1, :2)", (deptid,deptname))
        connection.commit()
        flash("Employee added successfully", "success")
        return redirect('/department')
    return render_template('addDepartment.html')

# Edit Department
@app.route('/editdept/<int:deptid>', methods=['GET', 'POST'])
def edit_dept(deptid):
    cursor = connection.cursor()
    if request.method == 'POST':
        depid = request.form['depid']
        deptname = request.form['deptname']
        cursor.execute("UPDATE DEPARTMENT SET DEPT_ID=:1, DEPT_NAME=:2 WHERE DEPT_ID=:3", (depid, deptname, deptid))
        connection.commit()
        return redirect('/department')
    cursor.execute("SELECT dept_id, dept_name FROM DEPARTMENT WHERE DEPT_ID=:1", [deptid])
    department = cursor.fetchone()
    return render_template('editdept.html', department=department, deptid=deptid)

# Delete Department
@app.route('/deletedept/<int:deptid>')
def delete_department(deptid):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM DEPARTMENT WHERE DEPT_ID=:1", [deptid])
    connection.commit()
    return redirect('/department')
 
if __name__ == '__main__':
    app.run(debug=True)
