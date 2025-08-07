from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

User = get_user_model()

def test_login(request):
    """Test login view for debugging"""
    
    # Test direct authentication
    admin_user = authenticate(username='admin@cbt.com', password='admin123')
    student_user = authenticate(username='student@cbt.com', password='student123')
    
    response = f"""
    <h1>Authentication Test</h1>
    <h2>Backend Test Results:</h2>
    <p>Admin Auth: {'SUCCESS' if admin_user else 'FAILED'}</p>
    <p>Student Auth: {'SUCCESS' if student_user else 'FAILED'}</p>
    
    <h2>Database Users:</h2>
    """
    
    for user in User.objects.all():
        response += f"<p>{user.username} ({user.email}) - Active: {user.is_active}</p>"
    
    response += """
    <h2>Test Login Form:</h2>
    <form method="post">
        <p>
            <label>Email:</label><br>
            <input type="email" name="test_email" value="admin@cbt.com">
        </p>
        <p>
            <label>Password:</label><br>
            <input type="password" name="test_password" value="admin123">
        </p>
        <button type="submit">Test Login</button>
    </form>
    """
    
    if request.method == 'POST':
        test_email = request.POST.get('test_email')
        test_password = request.POST.get('test_password')
        test_user = authenticate(username=test_email, password=test_password)
        
        response += f"""
        <h3>Form Test Result:</h3>
        <p>Email: {test_email}</p>
        <p>Password: {'*' * len(test_password)}</p>
        <p>Result: {'SUCCESS' if test_user else 'FAILED'}</p>
        """
        
        if test_user:
            login(request, test_user)
            response += f"<p>Logged in as: {test_user.email}</p>"
    
    return HttpResponse(response)
