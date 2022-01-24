from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from api.forms import MaterialForm
from .models import Level, Material, QuestionAttempt, QuizAttempt, QuizPack, Student, StudentProgress, User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from . import utils
from autolearn_japanese import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator

# Create your views here.
error_code = {
    1:'Wrong password. Please reenter your password',
    2:'New password and old password cannot match',
    3:'New password and resubmitted password did not match',
    4:'Password contains at least 6 characters',
}

def main(request):
    if request.user.is_authenticated:
        return redirect('home_student') 
    else:
        return render(request, 'app_screen.html')

@login_required(login_url='/login')
def home_student(request):
    if not Student.objects.filter(user=request.user):
        try:
            student = Student(user = request.user)
            student.save()
        except Exception:
            messages.error(request, Exception)
            
    #get all quizzes
    quizzes = QuizPack.objects.all()
    total = len(quizzes)
    
    #get all beginner quizzes
    beginner = Level.objects.get(level = 'Beginner')
    beginnerQuizzes = QuizPack.objects.filter(level=beginner)
    totalBeginner = len(beginnerQuizzes)
    
    #get all intermediate quizzes
    intermediate = Level.objects.get(level = 'Intermediate')
    intermediateQuizzes = QuizPack.objects.filter(level=intermediate)
    totalIntermediate = len(intermediateQuizzes)
    
    #get all advanced quizzes
    advanced = Level.objects.get(level = 'Advanced')
    advancedQuizzes = QuizPack.objects.filter(level=advanced)
    totalAdvanced = len(advancedQuizzes)
    
    student = Student.objects.get(pk=request.user)
    if StudentProgress.objects.filter(pk= student):
        studentProgress = StudentProgress.objects.get(pk= student)
        
        #get all completed quizzes
        quizCompleted = studentProgress.quizCompleted.all()
        completed = len(quizCompleted)
        
        #get beginner completed quizzes
        beginnerCompleted = studentProgress.quizCompleted.filter(level=beginner)
        beginnerDone = len(beginnerCompleted)
        
        #get intermediate completed quizzes
        intermediateCompleted = studentProgress.quizCompleted.filter(level=intermediate)
        intermediateDone = len(intermediateCompleted)
        
        #get advanced completed quizzes
        advancedCompleted = studentProgress.quizCompleted.filter(level=advanced)
        advancedDone = len(advancedCompleted)
    else:
        completed = 0
        beginnerDone = 0
        intermediateDone = 0
        advancedDone = 0
    percent = get_percent_check_zero(completed, total)
    percentBeginner = get_percent_check_zero(beginnerDone, totalBeginner)
    percentIntermediate = get_percent_check_zero(intermediateDone, totalIntermediate)
    percentAdvanced = get_percent_check_zero(advancedDone, totalAdvanced)
    return render(request, "home_student.html", 
            {'completed':completed, 'total':total, 'percent':percent, 
            'beginnerDone':beginnerDone, 'totalBeginner':totalBeginner, 'percentBeginner':percentBeginner,
            'intermediateDone':intermediateDone, 'totalIntermediate':totalIntermediate, 'percentIntermediate':percentIntermediate,
            'advancedDone':advancedDone, 'totalAdvanced':totalAdvanced, 'percentAdvanced':percentAdvanced})
    
def get_percent_check_zero(divisor, divided):
    if divided == 0: 
        return 100.0
    else:
        return  round(divisor/divided * 100,2)

@login_required(login_url='/login')
def student_letter(request, chart):
    return render(request, "letters_screen.html", {'chart': chart})

@login_required(login_url='/login')
def letter_detail(request, chart, letter):
    return render(request, "letters_screen.html", {'chart': chart, 'letter':letter})

def log_in(request):
    login_url = 'login.html'
    if request.method == "POST":
        if 'sign_up' in request.POST:
            username = request.POST.get('username')
            email = request.POST.get('email')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')

            if any(not c.isalnum() for c in username):
                messages.error(request, "Username cannot contain special characters!")
                return render(request, login_url)
            
            if User.objects.filter(username=username):
                messages.error(request, "User name already taken!")
                return render(request, login_url)

            if utils.validate_email(email) is False:
                messages.error(request, "Email not valid!")
                return render(request, login_url)

            if User.objects.filter(email=email):
                messages.error(request, "Email already taken!")
                return render(request, login_url)

            if pass1 != pass2:
                messages.error(request, "Password verification does not match password!")
                return render(request, login_url)

            myuser = User.objects.create_user(username, email, pass2)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            student = Student(user=myuser)
            student.save()
            messages.success(request, "Your account has been successfully created")
            return render(request, login_url)

        elif 'sign_in' in request.POST:
            username = request.POST['username']
            passwd = request.POST['pass']

            user = authenticate(username=username, password=passwd)

            if user is not None:
                login(request, user)
                # user_type = "Undefined"
                # if user.is_student:
                #     user_type = 'Student'
                # elif user.is_admin:
                #     user_type = 'Admin'
                return redirect('home_student')
            else:
                messages.error(request, "Invalid user!")
                return render(request, login_url)

    return render(request, login_url)

@login_required(login_url='/login')
def signout(request):
    logout(request)
    # messages.success(request, "Logged Out Successfully")
    return redirect('main')


def forget_passwd(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user= User.objects.get(username=username, email=email)
            new_password = '123456'
            user.set_password(new_password)
            user.save()

            # Send Reset-Password Email
            subject = "Reset Password"
            message = "Dear " + user.first_name + ",\nYour new password is: " + new_password + "\n\n\n\nPlease don't reply this email.\nAuto Learn System - http://127.0.0.1:8000/"
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]
            send_mail(subject, message, from_email, to_list, fail_silently=False)

            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "User invalid!")
            return render(request, 'forget_passwd.html')

    return render(request, 'forget_passwd.html')

@login_required(login_url='/login')
def student_reference(request):
    if not request.method=='POST':
        form = MaterialForm()
        records = Material.objects.all()
        target = ''
    else:
        target = request.POST['target']
        skill = get_multiple_object_field(request, 'skill')
        level = get_multiple_object_field(request, 'level')
        language = get_multiple_object_field(request, 'language')
        form = MaterialForm(initial={'skill':skill,'level':level, 'language':language})
        if skill and level and language:
            records = Material.objects.filter(title__icontains=target, level=level, skill=skill, language=language)
        elif skill:
            records = Material.objects.filter(title__icontains=target, skill=skill)
        elif level:
            records = Material.objects.filter(title__icontains=target, level=level) 
        elif language:
            records = Material.objects.filter(title__icontains=target, language=language)
        elif skill and level:
            records = Material.objects.filter(title__icontains=target, level=level, skill=skill)
        elif skill and language:
            records = Material.objects.filter(title__icontains=target, skill=skill, language=language)
        elif level and language:
            records = Material.objects.filter(title__icontains=target, level=level, language=language)     
        else:
            records = Material.objects.filter(title__icontains=target)
    paginator = Paginator(records, 25) # Show 25 records per page.

    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'reference_screen.html', {'page':page_obj, 'target':target, 'form':form})

def get_multiple_object_field(request, field):
    try:
        return request.POST[field]
    except Exception:
        return None

@login_required(login_url='/login')
def reference_detail(request, id):
    book = Material.objects.get(pk=id)
    topics = book.topic.all()
    skills = book.skill.all()
    languages = book.language.all()
    return render(request, 'reference_detail.html', {'book':book, 'topics':topics, 'skills':skills, 'languages':languages})

@login_required(login_url='/login')
def student_quiz(request, level):
    levelModel = Level.objects.get(level = level)
    quizzes = QuizPack.objects.filter(level = levelModel)
    student = Student.objects.get(pk=request.user)
    if StudentProgress.objects.filter(pk= student):
        studentProgress = StudentProgress.objects.get(pk= student)
        quizCompleted = studentProgress.quizCompleted.all()
    else:
        quizCompleted = None
    return render(request, 'quiz_screen.html',{'Quizzes':quizzes, 'quizCompleted':quizCompleted})

@login_required(login_url='/login')
def quiz_detail(request, id):
    quiz = QuizPack.objects.get(pk=id)
    student = Student.objects.get(pk=request.user)
    if StudentProgress.objects.filter(pk= student):
        studentProgress = StudentProgress.objects.get(pk= student)
        quizCompleted = studentProgress.quizCompleted.all()
    else:
        quizCompleted = None
    questions = quiz.questions.all()
    score = 0
    total = len(questions)
    if request.method == 'POST':
        new_attempt = QuizAttempt(student=request.user)
        new_attempt.save()
        for q in questions:
            chosen_op = request.POST[q.question]
            if chosen_op == 'A':
                ans = q.op1
            elif chosen_op == 'B':
                ans = q.op2
            elif chosen_op == 'C':
                ans = q.op3
            else:
                ans = q.op4
            new_quest = QuestionAttempt(quizAttempt=new_attempt, question = q.question, answer = ans, status=(q.ans == chosen_op))
            new_quest.save()
            if q.ans == chosen_op:
                score +=1
        
        percent = round(score/total *100 ,2)
        questionAttempts = new_attempt.questionattempt_set.all()
        context = {
            'score':score,
            'time': request.POST['timer'],
            'percent':percent,
            'total':total,
            'questionAttempts': questionAttempts,
            'quizId':id
        }
        if (quizCompleted==None or quiz not in quizCompleted) and score==total:
            newQuizCompleted = StudentProgress(student = student)
            newQuizCompleted.save()
            newQuizCompleted.quizCompleted.add(quiz)
        return render(request,'quiz_result.html',context)
    else:
        return render(request, 'quiz_detail.html',{'quiz':quiz,'questions':questions})

@login_required(login_url='/login')
def edit_profile(request):
    current_user = request.user
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        current_user.last_name = lname
        current_user.first_name = fname
        current_user.save()
    messages.success(request, 'Info updated!')
    return render(request, 'edit_profile.html')

@login_required(login_url='/login')
def change_passwd(request):
    if request.method == 'POST':
        current_user = request.user        
        old_pass = request.POST['old_pass']
        new_pass = request.POST['new_pass']
        new_pass2 = request.POST['new_pass2']
        code = validatePasswordChange(current_user, old_pass, new_pass, new_pass2)
        if code==0:
            current_user.set_password(new_pass2)
            current_user.save()
            update_session_auth_hash(request, current_user)  # Important!
            messages.success(request, 'Mật khẩu cập nhật thành công!')
            # Send Reset-Password Email
            subject = "Change Password"
            message = "Dear " + current_user.first_name + ",\nYour new password is: " + new_pass2 + "\n\n\n\nPlease don't reply this email.\nCOVID Prevention System - http://127.0.0.1:8000/"
            from_email = settings.EMAIL_HOST_USER
            to_list = [current_user.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
        else:
            messages.error(request, error_code[code])
            
    return render(request, 'change_pass.html')
    
def validatePasswordChange(current_user, old_pass, new_pass, new_pass2):
    current_pass = current_user.password
    check_pass = check_password(old_pass, current_pass)
    if not check_pass:
        return 1
    if old_pass == new_pass:
        return 2
    if new_pass != new_pass2:
        return 3
    if len(new_pass2) < 6: 
        return 4 
    return 0

