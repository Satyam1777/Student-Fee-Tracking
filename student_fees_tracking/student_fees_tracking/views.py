from django.shortcuts import render 
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.http import HttpResponse
import pymysql

# def save_student_data(student_id, first_name, last_name, email, password, confirm_password):
#     # Database connection details
#     db_config = {
#         'host': 'localhost',
#         'user': 'root',      # Replace with your database username
#         'password': 'root',  # Replace with your database password
#         'database': 'sft',        # Replace with your database name
#     }
    
#     try:
#         connection = pymysql.connect(**db_config)
#         with connection.cursor() as cursor:
#             # SQL query to insert data into students table
#             students_sql = """
#             INSERT INTO students (student_id, first_name, last_name, email, password)
#             VALUES (%s, %s, %s, %s, %s)
#             """
#             cursor.execute(students_sql, (student_id, first_name, last_name, email, password))

#             # SQL query to insert data into login table
#             login_sql = """
#             INSERT INTO login (student_id, password)
#             VALUES (%s, %s)
#             """
#             cursor.execute(login_sql, (student_id, password))
        
#         # Commit the transaction
#         connection.commit()
#         print("Student and login data inserted successfully!")

#     except pymysql.MySQLError as e:
#         print(f"Error inserting data: {e}")

#     finally:
#         # Close the connection
#         if connection:
#             connection.close()

# # View to handle the form submission
# def signup(request):
#     if request.method == 'POST':
#         # Extract data from the form
#         student_id = request.POST.get('student_id')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')

#         # Check if passwords match
#         if password != confirm_password:
#             return HttpResponse("Passwords do not match!")

#         # Call the function to save data to the database
#         save_student_data(student_id, first_name, last_name, email, password, confirm_password)

#         # Redirect or send success response
#         return redirect('/')  # Redirect to home page or any other page
    
#     return render(request, 'signup.html')


def student_login(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')

        # Database connection details
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'root',
            'database': 'sft',
        }

        try:
            # Connect to the database
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                # Query to check if credentials match
                query = """
                SELECT * FROM login WHERE student_id = %s AND password = %s
                """
                cursor.execute(query, (student_id, password))
                result = cursor.fetchone()  # Fetch one result
                
                if result:
                    # Store student_id in session after successful login
                    request.session['student_id'] = student_id
                    return redirect('student_dashboard')
                else:
                    return render(request, 'studentloginpage.html', {'error': 'Invalid credentials'})

        except pymysql.MySQLError as e:
            print(f"Database Error: {e}")
            return HttpResponse("An error occurred while connecting to the database.")

        finally:
            if connection:
                connection.close()

    return render(request, 'studentloginpage.html')

# def student_dashboard(request):
#     # Ensure the student is logged in and their ID is in the session
#     student_id = request.session.get('student_id')  # Get the student_id from session
#     if not student_id:
#         return redirect('student_login')  # Redirect to login page if not logged in

#     # Database connection details
#     db_config = {
#         'host': 'localhost',
#         'user': 'root',
#         'password': 'root',
#         'database': 'sft',
#     }

#     try:
#         # Connect to the database
#         connection = pymysql.connect(**db_config)
#         with connection.cursor() as cursor:
#             # Fetch first_name, last_name, and email based on student_id
#             query = """
#             SELECT first_name, last_name, email FROM students WHERE student_id = %s
#             """
#             cursor.execute(query, (student_id,))
#             student_data = cursor.fetchone()

#             if student_data:
#                 # Combine first_name and last_name
#                 student_name = f"{student_data[0]} {student_data[1]}"
#                 student_email = student_data[2]

                
#                 # Pass data to the template
#                 context = {
#                     'student_name': student_name,
#                     'student_email': student_email,
#                 }

#                 return render(request, 'studentdashboard.html', context)  # Render the template
#             else:
#                 return HttpResponse("Student data not found.") 
#     except pymysql.MySQLError as e:
#         print(f"Database Error: {e}")  # Log the database error
#         return HttpResponse(f"Database Error: {e}")  # Show the error details on the page for now
#     except Exception as ex:
#         print(f"Unexpected Error: {ex}")  # Log the unexpected error
#         return HttpResponse(f"Unexpected Error: {ex}")  
#     finally:
#         if 'connection' in locals() and connection:
#             connection.close()  # Ensure the database connection is closed
# def student_dashboard(request):
#     # Ensure the student is logged in and their ID is in the session
#     student_id = request.session.get('student_id')  # Get the student_id from session
#     if not student_id:
#         return redirect('student_login')  # Redirect to login page if not logged in

#     # Database connection details
#     db_config = {
#         'host': 'localhost',
#         'user': 'root',
#         'password': 'root',
#         'database': 'sft',
#     }

#     try:
#         # Connect to the database
#         connection = pymysql.connect(**db_config)
#         with connection.cursor() as cursor:
#             # Fetch first_name, last_name, email, and fees based on student_id
#             query = """
#             SELECT first_name, last_name, email, fees FROM students WHERE student_id = %s
#             """
#             cursor.execute(query, (student_id,))
#             student_data = cursor.fetchone()

#             if student_data:
#                 # Combine first_name and last_name
#                 student_name = f"{student_data[0]} {student_data[1]}"
#                 student_email = student_data[2]
#                 fees_status = student_data[3]

#                 # Determine fees status
#                 fees_status_text = "Paid" if fees_status == 1 else "Unpaid"

#                 # Pass data to the template
#                 context = {
#                     'student_name': student_name,
#                     'student_email': student_email,
#                     'fees_status': fees_status_text,
#                     'show_pay_button': fees_status == 0,  # Show Pay Now button only if unpaid
#                 }

#                 return render(request, 'studentdashboard.html', context)  # Render the template
#             else:
#                 return HttpResponse("Student data not found.")
#     except pymysql.MySQLError as e:
#         print(f"Database Error: {e}")  # Log the database error
#         return HttpResponse(f"Database Error: {e}")  # Show the error details on the page for now
#     except Exception as ex:
#         print(f"Unexpected Error: {ex}")  # Log the unexpected error
#         return HttpResponse(f"Unexpected Error: {ex}")
#     finally:
#         if 'connection' in locals() and connection:
#             connection.close()

def student_dashboard(request):
    student_id = request.session.get('student_id')  # Ensure student is logged in
    if not student_id:
        return redirect('student_login')  # Redirect to login page if not logged in

    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'sft',
    }

    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # Fetch student details
            query = """
            SELECT first_name, last_name, email, fees FROM students WHERE student_id = %s
            """
            cursor.execute(query, (student_id,))
            student_data = cursor.fetchone()

            if student_data:
                student_name = f"{student_data[0]} {student_data[1]}"
                student_email = student_data[2]
                fees_status = "Paid" if student_data[3] == 1 else "Unpaid"

                context = {
                    'student_name': student_name,
                    'student_email': student_email,
                    'fees_status': fees_status,
                    'show_pay_button': student_data[3] == 0,  # Show Pay Now button if unpaid
                }

                return render(request, 'studentdashboard.html', context)
            else:
                return HttpResponse("Student not found.")
    except pymysql.MySQLError as e:
        print(f"Database Error: {e}")
        return HttpResponse("Database error.")
    finally:
        if 'connection' in locals() and connection:
            connection.close()
def pay(request):
    if request.method == "POST":
        # Ensure the student is logged in
        student_id = request.session.get('student_id')
        if not student_id:
            return redirect('student_login')  # Redirect to login page if not logged in

        # Database connection details
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'root',
            'database': 'sft',
        }

        try:
            # Connect to the database
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                # Update the fees status to Paid (1)
                update_query = """
                UPDATE students SET fees = 1 WHERE student_id = %s
                """
                cursor.execute(update_query, (student_id,))
                connection.commit()

            # Redirect to the dashboard or index page
            return redirect('student_dashboard')  # Replace 'student_dashboard' with your desired URL name
        except pymysql.MySQLError as e:
            print(f"Database Error: {e}")
            return JsonResponse({"error": "Database error"}, status=500)
        finally:
            if 'connection' in locals() and connection:
                connection.close()

    # Redirect to payment page if the request method is not POST
    return render(request, "pay.html")

    # Redirect to payment page if the request method is not POST
    return render(request, "pay.html")

def homepage(request):
    return render(request , "index.html" )


# def signup(request):
#     if request.method == 'POST':
#         form = StudentSignupForm(request.POST)
#         if form.is_valid():
#             # Save the student record
#             form.save()
#             messages.success(request, "Signup successful! You can now log in.")
#             return redirect('')  # Redirect to the homepage or login page
#         else:
#             messages.error(request, "There was an error with your signup.")
#     else:
#         form = StudentSignupForm()

    return render(request, 'signup.html', {'form': form})


def admin_login(request):
    if request.method == 'POST':
        admin_id = request.POST.get('admin_id')
        password = request.POST.get('password')

        # Database connection details
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'root',
            'database': 'sft',
        }

        try:
            # Connect to the database
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                # Query to check if admin credentials match
                query = """
                SELECT * FROM admin_login WHERE admin_id = %s AND password = %s
                """
                cursor.execute(query, (admin_id, password))
                result = cursor.fetchone()  # Fetch one result

                if result:
                    # If credentials match, redirect to custom admin dashboard
                    return redirect('admin_dashboard')
                else:
                    # If credentials do not match, show error message
                    return render(request, 'adminlogin.html', {'error': 'Invalid credentials'})

        except pymysql.MySQLError as e:
            print(f"Database Error: {e}")
            return HttpResponse("An error occurred while connecting to the database.")

        finally:
            if connection:
                connection.close()

    # Render the admin login page for GET requests
    return render(request, 'adminlogin.html')

def admin_dashboard(request):
    students = []

    if request.method == 'POST':
        # Debug: Check if form data is received
        print("Form data received:", request.POST)

        # Extract form data
        student_id = request.POST.get('student_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        fees = 1 if request.POST.get('fees') else 0  # Convert checkbox to boolean

        # Debug: Check extracted data
        print("Extracted data:", student_id, first_name, last_name, email, password, fees)

        # Validate passwords
        if password != confirm_password:
            return HttpResponse("Passwords do not match!")

        # Save student data
        save_student_data(student_id, first_name, last_name, email, password, fees)
        print("Student data saved successfully.")

        # Redirect to refresh the page
        return redirect('admin_dashboard')

    # Fetch students from database
    try:
        with connection.cursor() as cursor:
            query = "SELECT student_id, first_name, last_name, email, password, fees FROM students"
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            students = [dict(zip(columns, row)) for row in cursor.fetchall()]
            print("Fetched students:", students)  # Debug: Check fetched data
    except Exception as e:
        print(f"Error fetching student data: {e}")

    # Render the dashboard
    return render(request, 'admindashboard.html', {'students': students})




def save_student_data(student_id, first_name, last_name, email, password, fees):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'sft',
    }

    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            students_sql = """
            INSERT INTO students (student_id, first_name, last_name, email, password, fees)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            login_sql = """
            INSERT INTO login (student_id, password)
            VALUES (%s, %s)
            """
            cursor.execute(login_sql, (student_id, password))
            cursor.execute(students_sql, (student_id, first_name, last_name, email, password, fees))
            connection.commit()
            print("Student inserted:", student_id, first_name, last_name, email, password, fees)  # Debug
    except pymysql.MySQLError as e:
        print(f"Error inserting data: {e}")
    finally:
        if connection:
            connection.close()

# View to handle the form submission
def signup(request):
    if request.method == 'POST':
        # Extract form data
        student_id = request.POST.get('student_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        fees = 1 if request.POST.get('fees') else 0  # Handle fees as boolean

        # Check if passwords match
        if password != confirm_password:
            return HttpResponse("Passwords do not match!")

        # Call the function to save the student data to the database
        save_student_data(student_id, first_name, last_name, email, password, fees)

        # Redirect to the admin dashboard or any other page after successful registration
        return redirect('student_login')  

    # If GET request, just render the form
    return render(request, 'signup.html')  # If you have a dedicated signup template




















# def update_admin_settings(request):
#     if request.method == 'POST':
#         new_password = request.POST.get('new_password')
#         confirm_password = request.POST.get('confirm_password')

#         if new_password != confirm_password:
#             messages.error(request, "Passwords do not match!")
#             return redirect('admin_dashboard')

#         user = User.objects.get(username=request.user.username)
#         user.set_password(new_password)
#         user.save()
#         messages.success(request, "Password updated successfully!")
#         return redirect('admin_dashboard')
# def manage_student(request, student_id):
#     student = get_object_or_404(Student, id=student_id)
#     if request.method == 'POST':
#         # Handle student edits or deletion
#         student.delete()
#         messages.success(request, "Student deleted successfully.")
#         return redirect('admin_dashboard')
#     return render(request, 'manage_student.html', {'student': student})

# def admin_login(request):
#     if request.method == 'POST':
#         admin_id = request.POST.get('admin_id')
#         password = request.POST.get('password')

#         # Authenticate the admin
#         admin = authenticate(request, username=admin_id, password=password)
        
#         if admin is not None:
#             login(request, admin)
#             messages.success(request, 'Welcome back, Admin!')
#             return redirect('admin_dashboard')  # Redirect to the admin dashboard after login
#         else:
#             messages.error(request, 'Invalid Admin ID or Password.')
#             return render(request, 'adminlogin.html')
    
#     return render(request, 'adminlogin.html')   