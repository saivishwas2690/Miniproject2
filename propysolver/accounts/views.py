from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json
from .models import *
from problems.models import Submission, Problem
from django.shortcuts import redirect
import google.generativeai as genai
import os

def home(request):
    if request.user.is_authenticated:
        return redirect('/problems/modules/')
    return render(request,'accounts/home.html')

def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/problems/modules/')
        else:
            return JsonResponse({'message':'Invalid credentials'})
        
    return render(request,'accounts/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if ProPyUser.objects.filter(username=username).exists():
            return JsonResponse({'message':'Username already exists'})
        if ProPyUser.objects.filter(email=email).exists():
            return JsonResponse({'message':'Email already exists'})
        
        user = ProPyUser.objects.create_user(username=username, email=email, password=password)
        user.save()
        profile = Profile.objects.create(user=user, bio = "No bio")
        login(request, user)

        return redirect('/problems/modules/')
    
def logoutuser(request):
    logout(request)
    return redirect('/login/')

def profile(request):
    tags = ['Two Pointers', 'Greedy', 'Math', 'Binary Search', 'DP', 'Divide and Conquer', 'Sorting', 'Data Structures']
    tag_count = []
    
    for tag in tags:
        all_problems_tag = Problem.objects.filter(tags__icontains=tag)
        submissions_queryset = Submission.objects.filter(problem__in=all_problems_tag, user=request.user, status='Accepted')
        tag_count.append(submissions_queryset.filter(problem__tags__icontains=tag,user=request.user).count())


    modules_list = [
        'Loops',
        'Array',
        'Recursion',
        'Hashing',
        'Dynamic Programming',
        'Math'
    ]
    module_count = []
    for module in modules_list:
        module_name = module
        problems_queryset = Problem.objects.filter(module=module)
        submissions_queryset = Submission.objects.filter(problem__in=problems_queryset, user=request.user)
        all_problems = submissions_queryset
        solves = all_problems.filter(status='Accepted', user=request.user).values('problem').distinct().count()
        percentage = round((solves / problems_queryset.count()) * 100 , 1)if solves != 0 else 0
        module_count.append([module_name, solves, percentage])
    
    problems_queryset = Problem.objects.all()
    submissions_queryset = Submission.objects.filter(problem__in=problems_queryset, user=request.user, status='Accepted').count()

    wrong_answers = Submission.objects.filter(problem__in=problems_queryset, user=request.user, status='Wrong Answer').count()
    accepted = Submission.objects.filter(problem__in=problems_queryset, user=request.user, status='Accepted').count()
    noof_problems = Problem.objects.count()
    not_attempted = noof_problems - wrong_answers - accepted
    overall_percentage = round((accepted / noof_problems) * 100, 1) if noof_problems != 0 else 0

    context = {
        'tag_count':tag_count,
        'module_count':module_count,
        'wrong_answers':wrong_answers,
        'accepted':accepted,
        'not_attempted':not_attempted,
        'overall_percentage':overall_percentage,
        'noof_problems':noof_problems
    }

    
    return render(request,'accounts/profile.html', context)

def advise(request):
    modules_list = [
        'Loops',
        'Array',
        'Math'
        'Hashing',
        'Recursion',
        'Dynamic Programming',
    ]
    genai.configure(api_key="AIzaSyBr1TAYwytCe8yMlihD2604ph1YzlGb5i8")
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    
    problem_queryset = Problem.objects.filter(module='Loops')
    submissions_queryset = Submission.objects.filter(problem__in=problem_queryset, user=request.user)
    
    loops = submissions_queryset
    loops_easy_attempted = loops.filter(problem__difficulty='Easy').count()
    loops_easy_solved = loops.filter(status='Accepted', problem__difficulty='Easy').count()
    loops_easy_wrong = loops.filter(status='Wrong Answer', problem__difficulty='Easy').count()
    loops_medium_attempted = loops.filter(problem__difficulty='Medium').count()
    loops_medium_solved = loops.filter(status='Accepted', problem__difficulty='Medium').count()
    loops_medium_wrong = loops.filter(status='Wrong Answer', problem__difficulty='Medium').count()
    loops_hard_attempted = loops.filter(problem__difficulty='Hard').count()
    loops_hard_solved = loops.filter(status='Accepted', problem__difficulty='Hard').count()
    loops_hard_wrong = loops.filter(status='Wrong Answer', problem__difficulty='Hard').count()

    problem_queryset = Problem.objects.filter(module='Arrays')
    submissions_queryset = Submission.objects.filter(problem__in=problem_queryset, user=request.user)
    
    arrays = submissions_queryset
    arrays_easy_attempted = arrays.filter(problem__difficulty='Easy').count()
    arrays_easy_solved = arrays.filter(status='Accepted', problem__difficulty='Easy').count()
    arrays_easy_wrong = arrays.filter(status='Wrong Answer', problem__difficulty='Easy').count()
    arrays_medium_attempted = arrays.filter(problem__difficulty='Medium').count()
    arrays_medium_solved = arrays.filter(status='Accepted', problem__difficulty='Medium').count()
    arrays_medium_wrong = arrays.filter(status='Wrong Answer', problem__difficulty='Medium').count()
    arrays_hard_attempted = arrays.filter(problem__difficulty='Hard').count()
    arrays_hard_solved = arrays.filter(status='Accepted', problem__difficulty='Hard').count()
    arrays_hard_wrong = arrays.filter(status='Wrong Answer', problem__difficulty='Hard').count()

    problem_queryset = Problem.objects.filter(module='Math')
    submissions_queryset = Submission.objects.filter(problem__in=problem_queryset, user=request.user)

    
    math = submissions_queryset
    math_easy_attempted = math.filter(problem__difficulty='Easy').count()
    math_easy_solved = math.filter(status='Accepted', problem__difficulty='Easy').count()
    math_easy_wrong = math.filter(status='Wrong Answer', problem__difficulty='Easy').count()
    math_medium_attempted = math.filter(problem__difficulty='Medium').count()
    math_medium_solved = math.filter(status='Accepted', problem__difficulty='Medium').count()
    math_medium_wrong = math.filter(status='Wrong Answer', problem__difficulty='Medium').count()
    math_hard_attempted = math.filter(problem__difficulty='Hard').count()
    math_hard_solved = math.filter(status='Accepted', problem__difficulty='Hard').count()
    math_hard_wrong = math.filter(status='Wrong Answer', problem__difficulty='Hard').count()

    problem_queryset = Problem.objects.filter(module='Hashing')
    submissions_queryset = Submission.objects.filter(problem__in=problem_queryset, user=request.user)

    hashing = submissions_queryset
    hashing_easy_attempted = hashing.filter(problem__difficulty='Easy').count()
    hashing_easy_solved = hashing.filter(status='Accepted', problem__difficulty='Easy').count()
    hashing_easy_wrong = hashing.filter(status='Wrong Answer', problem__difficulty='Easy').count()
    hashing_medium_attempted = hashing.filter(problem__difficulty='Medium').count()
    hashing_medium_solved = hashing.filter(status='Accepted', problem__difficulty='Medium').count()
    hashing_medium_wrong = hashing.filter(status='Wrong Answer', problem__difficulty='Medium').count()
    hashing_hard_attempted = hashing.filter(problem__difficulty='Hard').count()
    hashing_hard_solved = hashing.filter(status='Accepted', problem__difficulty='Hard').count()
    hashing_hard_wrong = hashing.filter(status='Wrong Answer', problem__difficulty='Hard').count()

    problem_queryset = Problem.objects.filter(module='Recursion')
    submissions_queryset = Submission.objects.filter(problem__in=problem_queryset, user=request.user)
    
    recursion = submissions_queryset
    recursion_easy_attempted = recursion.filter(problem__difficulty='Easy').count()
    recursion_easy_solved = recursion.filter(status='Accepted', problem__difficulty='Easy').count()    
    recursion_easy_wrong = recursion.filter(status='Wrong Answer', problem__difficulty='Easy').count()
    recursion_medium_attempted = recursion.filter(problem__difficulty='Medium').count()
    recursion_medium_solved = recursion.filter(status='Accepted', problem__difficulty='Medium').count()
    recursion_medium_wrong = recursion.filter(status='Wrong Answer', problem__difficulty='Medium').count()
    recursion_hard_attempted = recursion.filter(problem__difficulty='Hard').count()
    recursion_hard_solved = recursion.filter(status='Accepted', problem__difficulty='Hard').count()
    recursion_hard_wrong = recursion.filter(status='Wrong Answer', problem__difficulty='Hard').count()

    problem_queryset = Problem.objects.filter(module='Dynamic Programming')
    submissions_queryset = Submission.objects.filter(problem__in=problem_queryset, user=request.user)
    
    dp = submissions_queryset
    dp_easy_attempted = dp.filter(problem__difficulty='Easy').count()
    dp_easy_solved = dp.filter(status='Accepted', problem__difficulty='Easy').count()
    dp_easy_wrong = dp.filter(status='Wrong Answer', problem__difficulty='Easy').count()
    dp_medium_attempted = dp.filter(problem__difficulty='Medium').count()
    dp_medium_solved = dp.filter(status='Accepted', problem__difficulty='Medium').count()
    dp_medium_wrong = dp.filter(status='Wrong Answer', problem__difficulty='Medium').count()
    dp_hard_attempted = dp.filter(problem__difficulty='Hard').count()
    dp_hard_solved = dp.filter(status='Accepted', problem__difficulty='Hard').count()
    dp_hard_wrong = dp.filter(status='Wrong Answer', problem__difficulty='Hard').count()
    

    prompt = f"""
            Based on the following problem-solving statistics and the specified learning path, analyze the my performance and provide suggestions  on which topics should i practice next.

            My Problem-Solving Stats:

            Module: Loops
            - Easy Problems: {loops_easy_attempted} attempted, {loops_easy_solved} solved (AC), {loops_easy_wrong} incorrect (WA)
            - Medium Problems: {loops_medium_attempted} attempted, {loops_medium_solved} solved (AC), {loops_medium_wrong} incorrect (WA)
            - Hard Problems: {loops_hard_attempted} attempted, {loops_hard_solved} solved (AC), {loops_hard_wrong} incorrect (WA)

            Module: Arrays
            - Easy Problems: {arrays_easy_attempted} attempted, {arrays_easy_solved} solved (AC), {arrays_easy_wrong} incorrect (WA)
            - Medium Problems: {arrays_medium_attempted} attempted, {arrays_medium_solved} solved (AC), {arrays_medium_wrong} incorrect (WA)
            - Hard Problems: {arrays_hard_attempted} attempted, {arrays_hard_solved} solved (AC), {arrays_hard_wrong} incorrect (WA)

            Module: Math
            - Easy Problems: {math_easy_attempted} attempted, {math_easy_solved} solved (AC), {math_easy_wrong} incorrect (WA)
            - Medium Problems: {math_medium_attempted} attempted, {math_medium_solved} solved (AC), {math_medium_wrong} incorrect (WA)
            - Hard Problems: {math_hard_attempted} attempted, {math_hard_solved} solved (AC), {math_hard_wrong} incorrect (WA)

            Module: Hashing
            - Easy Problems: {hashing_easy_attempted} attempted, {hashing_easy_solved} solved (AC), {hashing_easy_wrong} incorrect (WA)
            - Medium Problems: {hashing_medium_attempted} attempted, {hashing_medium_solved} solved (AC), {hashing_medium_wrong} incorrect (WA)
            - Hard Problems: {hashing_hard_attempted} attempted, {hashing_hard_solved} solved (AC), {hashing_hard_wrong} incorrect (WA)

            Module: Recursion
            - Easy Problems: {recursion_easy_attempted} attempted, {recursion_easy_solved} solved (AC), {recursion_easy_wrong} incorrect (WA)
            - Medium Problems: {recursion_medium_attempted} attempted, {recursion_medium_solved} solved (AC), {recursion_medium_wrong} incorrect (WA)
            - Hard Problems: {recursion_hard_attempted} attempted, {recursion_hard_solved} solved (AC), {recursion_hard_wrong} incorrect (WA)

            Module: Dynamic Programming
            - Easy Problems: {dp_easy_attempted} attempted, {dp_easy_solved} solved (AC), {dp_easy_wrong} incorrect (WA)
            - Medium Problems: {dp_medium_attempted} attempted, {dp_medium_solved} solved (AC), {dp_medium_wrong} incorrect (WA)
            - Hard Problems: {dp_hard_attempted} attempted, {dp_hard_solved} solved (AC), {dp_hard_wrong} incorrect (WA)

            Learning Path:
            1. Loops
            2. Arrays
            3. Math
            4. Hashing
            5. Recursion
            6. Dynamic Programming

            Instructions:
            1. Identify modules where the I demonstrates strong problem-solving skills.
            2. Highlight modules where the I need improvement, particularly focusing on higher difficulty levels.
            3. Recommend specific modules and problem difficulties I should practice next, ensuring the suggestions align with the learning path from basic to advanced topics.
            4. Ouput everything covered in a single paragraph.

            Example Output:
            Based on your problem-solving statistics and our learning path, you have shown strong proficiency in Loops, excelling in both Easy and Medium difficulty levels. 
            In Arrays, your performance is commendable in Easy problems, although there is room for improvement in Medium and Hard challenges. 
            However, you faced difficulties in Math, particularly with Medium and Hard problems, indicating a need for more focused practice. 
            Similarly, Recursion also shows potential for improvement, especially in Medium and Hard problems. To optimize your learning journey, we recommend continuing to practice Medium and Hard problems in Arrays to reinforce your skills, concentrating on Medium problems in Math to strengthen your foundational understanding, and then advancing to Easy and Medium challenges in Hashing to progress steadily along our structured curriculum.
            """
    
    response = model.generate_content(prompt)
    response = response.text
    print(response)

    return JsonResponse({'response':response})