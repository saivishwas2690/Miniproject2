from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import subprocess
import time, os, sys, re
import json

import google.generativeai as genai

@login_required(login_url ='accounts:login')
def modules(request):
    modules_list = [
        'Loops',
        'Array',
        'Recursion',
        'Hashing',
        'Dynamic-Programming',
        'Math'
    ]
    modules = []
    total = 0
    for module in modules_list:
        total_noof_problems = Problem.objects.filter(module=module).count()

        problem_queryset = Problem.objects.filter(module=module)

        total_noof_solves = Submission.objects.filter(
            user=request.user,
            problem__in=problem_queryset,
            status='Accepted'
        ).values('problem').distinct().count()

        accuracy = 0
        if total_noof_problems == 0:
            accuracy = 0
        else:
            accuracy = (total_noof_solves / total_noof_problems) * 100

        modules.append([module, total_noof_problems, total_noof_solves, accuracy])
    return render(request, 'problems/modules.html', {'modules':modules})

@login_required(login_url ='accounts:login')
def problems_list(request, string):
    problems = Problem.objects.filter(module=string)
    context = []
    total_solve = 0
    total_wrong = 0
    for problem in problems:
        total_noof_solves = Submission.objects.filter(
            problem=problem,
            status='Accepted',
        ).count()
        total_noof_attempts = Submission.objects.filter(
            problem=problem,
        ).count()

        if Submission.objects.filter(user=request.user, problem=problem, status='Accepted').exists():
            total_solve += 1
        elif Submission.objects.filter(user=request.user, problem=problem).exists():
            total_wrong += 1
    
        if total_noof_attempts == 0:
            accuracy = 0
        else:
            accuracy = (total_noof_solves / total_noof_attempts) * 100
        
        accuracy = round(accuracy, 1)
        if Submission.objects.filter(user=request.user, problem=problem, status='Accepted').exists():
            status = 'Accepted'
        elif Submission.objects.filter(user=request.user, problem=problem).exists():
            status = 'Wrong Answer'
        else:
            status = 'Not Attempted'

        context.append([problem, accuracy, status])

    total_not_attempted = Problem.objects.filter(module=string).count() - total_solve - total_wrong

    return render(request, 'problems/problems.html', {'context':context, 'total_solve':total_solve, 'total_wrong':total_wrong, 'total_not_attempted':total_not_attempted})

def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()

@login_required(login_url ='accounts:login')
def problem_detail(request, string, pk):
    problem = Problem.objects.get(pk=pk)
    submission_data = []
    all_submissions = Submission.objects.filter(problem=problem, status="Accepted").order_by('time_taken')
    for submission in all_submissions:
        submission_data.append([submission.user, submission.time_taken, submission.memory_taken, submission.id, submission.views])
    input_file1 = read_file(problem.input_file1.path)
    output_file1 = read_file(problem.output_file1.path)
    
    return render(request, 'problems/code.html', {'problem':problem, 
                                                  'input':input_file1, 
                                                  'output':output_file1, 
                                                  'submissions':submission_data})

def execute_python_script(code_to_run, input_data):
    try:
        cpu_time_start = time.process_time()
        process = subprocess.Popen(['python', '-c', code_to_run],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        stdout, stderr = process.communicate(input=input_data.encode(), timeout=5)

        cpu_time_end = time.process_time()
        cpu_time = cpu_time_end - cpu_time_start

        
        if process.returncode != 0:
            error = stderr.decode().strip() if stderr else "Unknown error"
            return f"Script execution failed: {error}", cpu_time
        else:
            return stdout.decode().strip(), cpu_time

    except subprocess.TimeoutExpired:
        process.kill()
        return "Time Limit Exceeded", 5 
    except Exception as e:
        return f"Error: {str(e)}", None

@login_required(login_url ='accounts:login')
def simple_run_code(request):
    code = request.POST.get('code')
    inputstring = request.POST.get('input')
    output, runtime = execute_python_script(code, inputstring)
    return JsonResponse({'output': output, 'runtime': runtime})

def run_code(code_to_run, input_file_path, correct_output_file_path, timelimit):
    with open(input_file_path, 'r') as input_file:
        input_data = input_file.read()

    try:
        start_time = time.process_time()
        process = subprocess.Popen(['python', '-c', code_to_run],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=input_data.encode(), timeout=1)

    except subprocess.TimeoutExpired:
        return ["Time Limit Exceeded", timelimit]
    

    encoding = "utf-8"
    stdout = stdout.decode(encoding).strip().split("\r\n")


    trimmed_stdout = []
    for i in stdout:
        if i != "":
            trimmed_stdout.append(i) 

    end_time = time.process_time()
    runtime = end_time - start_time
    runtime = round(runtime, 4)

    process.kill()

    if stderr:
        print(stderr.decode(encoding).strip())
        return ["RunTime Error", runtime]
    
    with open(correct_output_file_path, 'r') as correct_output_file:
        correct_output_data = correct_output_file.read().strip().split("\n")

    trimmed_correct_output_data = []
    for i in correct_output_data:
        if i != "":
            trimmed_correct_output_data.append(i)

    print(trimmed_stdout, trimmed_correct_output_data)

    if trimmed_stdout == trimmed_correct_output_data:
        return ["Accepted", runtime]
    else:
        return ["Wrong Answer", runtime]

def test_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        id = request.POST.get('id')
        problem = Problem.objects.get(pk=id)

        tests = []
        if problem.input_file1 :
            tests.append([problem.input_file1.path, problem.output_file1.path])
        if problem.input_file2 :
            tests.append([problem.input_file2.path, problem.output_file2.path])
        if problem.input_file3 :
            tests.append([problem.input_file3.path, problem.output_file3.path])
        if problem.input_file4 :
            tests.append([problem.input_file4.path, problem.output_file4.path])
        if problem.input_file5 :
            tests.append([problem.input_file5.path, problem.output_file5.path])

        data = {}
        maximum_runtime = 0

        for i in range(len(tests)):
            test_number = i + 1
            input_path = tests[i][0]
            output_path = tests[i][1]

            result, runtime = run_code(code, input_path, output_path, problem.time_limit)
            maximum_runtime = max(maximum_runtime, runtime)
            data.update({"TestCase"+str(test_number):{"runtime": runtime, "verdict": result}})
            if result != "Accepted":
                Submission.objects.create(
                    user = request.user,
                    problem = problem,
                    status = result,
                    code = code,
                    failed_test_case = test_number,
                    time_taken = maximum_runtime,
                    memory_taken = 0
                )
                for j in range(test_number, len(tests)):
                    data.update({"TestCase"+str(j+1):{"runtime": "skipped", "verdict": "skipped"}})
                return JsonResponse(data, safe = False)
            
        Submission.objects.create(
            user = request.user,
            problem = problem,
            status = "Accepted",
            code = code,
            failed_test_case = -1,
            time_taken = maximum_runtime,
            memory_taken = 0
        )
        
        return JsonResponse(data, safe=False)
        
    return render(request, 'problems/test.html')

def suggestions(request):
    code = request.POST.get('code')
    genai.configure(api_key="AIzaSyBr1TAYwytCe8yMlihD2604ph1YzlGb5i8")
    suggestions_template = f''' this is the ```{code}``` user has written. give exactly five prompt suggestions for the user for next query based on the code.
                    give suggestions like:
                    1.what this particular method from the code does?
                    2.what is the time complexity and space complexity of the code?
                    3.why this logic works?
                    4.How to optmize the code?
                    5.How to make the code more readable?
                    6.what are the errors in the code?
                    7.suggest modifications?
                    each suggestions sholud be only 5 to 6 words long.
                    response should be strictly in this format only.
                    $$suggestion1
                    $$suggestion2
                    $$suggestion3
                    $$suggestion4
                    $$suggestion5      
                    '''
    prompt = suggestions_template.format(code=code)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content(prompt)
    suggestions = [suggestion.strip() for suggestion in response.text.split('$$') if suggestion.strip()]

    data = {}
    for i in range (len(suggestions)):
        print(suggestions[i])
        data.update({str(i+1): suggestions[i]})
    
    return JsonResponse(data, safe=False)

def getcode(request):
    id = request.POST.get('id')
    submission = Submission.objects.get(pk=id, status='Accepted')
    submission.views += 1
    submission.save()
    data = {}
    data['code'] = submission.code
    return JsonResponse(data, safe=False)