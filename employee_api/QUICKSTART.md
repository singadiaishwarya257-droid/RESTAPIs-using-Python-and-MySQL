# 🚀 Quick Start Guide - 5 Minutes

Get the Employee Management REST API running in 5 minutes!

---

## Prerequisites ✅

- Python 3.8+ installed
- MySQL Server running
- Terminal/PowerShell open

---

## Step 1: Navigate to Project (30 seconds)

```bash
cd c:\Users\PC\RESTAPIs-using-Python-and-MySQL\employee_api
```

---

## Step 2: Activate Virtual Environment (30 seconds)

```bash
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` in your terminal prompt.

---

## Step 3: Set Database Credentials (1 minute)

Edit `.env` file:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password  ← CHANGE THIS
DB_NAME=employee_management
DB_PORT=3306
```

Save the file.

---

## Step 4: Create Database (1 minute)

```bash
mysql -u root -p < setup_database.sql
```

Type your MySQL password when prompted.

---

## Step 5: Run Server (30 seconds)

```bash
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## Step 6: Test API (1 minute)

Open your browser and visit:

### Option A: Auto-Generated Documentation
```
http://localhost:8000/docs
```
You'll see all 40+ endpoints with a UI to test them!

### Option B: Test in Postman
1. Import `postman_collection.json` into Postman
2. All endpoints ready to test

### Option C: Test in Terminal

```bash
# Health check
curl http://localhost:8000/health

# Get all employees
curl http://localhost:8000/employees

# Create employee
curl -X POST "http://localhost:8000/employees?name=John%20Doe&email=john@company.com&department=IT&salary=75000"

# Get employee
curl http://localhost:8000/employees/1
```

---

## 🎉 You're Done!

API is running with:
✅ 40+ endpoints
✅ MySQL database
✅ File handling
✅ CSV/JSON support
✅ Auto-generated docs

---

## Next Steps

### Learn
- Read `README.md` for complete documentation
- Read `LEARNING_GUIDE.md` for interview questions

### Test
- Use Swagger UI at `/docs`
- Import Postman collection
- Try example requests

### Extend
- Add more fields to employees table
- Create new endpoints
- Add authentication

### Deploy
- Deploy to Heroku
- Use Docker
- Set up CI/CD

---

## 📞 Common Issues

### "Cannot connect to MySQL"
```bash
# Check MySQL is running and credentials in .env are correct
mysql -u root -p
```

### "Port 8000 already in use"
```bash
# Use different port
uvicorn main:app --reload --port 8001
```

### "ModuleNotFoundError: fastapi"
```bash
# Activate venv first
.\venv\Scripts\Activate.ps1
```

### "Database does not exist"
```bash
# Recreate database
mysql -u root -p < setup_database.sql
```

---

## 📡 Quick API Examples

### Create Employee
```bash
curl -X POST "http://localhost:8000/employees?name=Jane&email=jane@company.com&department=HR&salary=65000"
```

### Get All Employees
```bash
curl http://localhost:8000/employees
```

### Search by Department
```bash
curl "http://localhost:8000/employees/search/department?value=IT"
```

### Export to CSV
```bash
curl -X POST "http://localhost:8000/files/csv/export?filename=employees.csv"
```

### Export to JSON
```bash
curl -X POST "http://localhost:8000/files/json/export?filename=employees.json"
```

---

## 📁 Project Files

```
employee_api/
├── main.py              # FastAPI app (40+ endpoints)
├── database.py          # MySQL connection
├── employee_queries.py  # SQL functions
├── file_operations.py   # File handling
├── setup_database.sql   # Database init
├── README.md            # Full documentation
├── LEARNING_GUIDE.md    # Interview questions
├── QUICKSTART.md        # This file
└── postman_collection.json  # API tests
```

---

## ✨ Features

✅ **Employee CRUD**
- Add, get, update, delete employees
- Search by name/department
- Salary statistics

✅ **File Operations**
- Text file create/read/write/delete
- CSV import/export
- JSON import/export
- File upload/download

✅ **Error Handling**
- Input validation
- Meaningful error messages
- Proper HTTP status codes

✅ **Documentation**
- Auto-generated API docs
- Postman collection
- 700+ lines of README
- Learning guide with 10 Q&A

---

## 🎓 Learning

Understand every line of code:

1. **Read Code**
   - Start with `main.py`
   - See how endpoints work
   - Understand decorators

2. **Study Concepts**
   - Read `LEARNING_GUIDE.md`
   - 10 interview questions
   - 4 practice tasks

3. **Test & Experiment**
   - Modify endpoints
   - Add new features
   - Break things (safely!)

4. **Deploy**
   - Prepare for production
   - Add authentication
   - Deploy to cloud

---

**Happy Coding!** 🚀

For detailed docs, see `README.md`
For learning, see `LEARNING_GUIDE.md`
