from django.db import models


def test_case_upload_path1(instance, filename):
    return f'tcs/{instance.id}/tc1/{filename}'

def test_case_upload_path2(instance, filename):
    return f'tcs/{instance.id}/tc2/{filename}'

def test_case_upload_path3(instance, filename):
    return f'tcs/{instance.id}/tc3/{filename}'

def test_case_upload_path4(instance, filename):
    return f'tcs/{instance.id}/tc4/{filename}'

def test_case_upload_path5(instance, filename):
    return f'tcs/{instance.id}/tc5/{filename}'

class Problem(models.Model):
    TAG_CHOICES = [
        ('Array', 'Array'),
        ('String', 'String'),
        ('Bit Manipulation', 'Bit Manipulation'),
        ('Binary Search', 'Binary Search'),
        ('Greedy', 'Greedy'),
        ('Sorting', 'Sorting'),
        ('Hashing', 'Hashing'),
        ('Two Pointers', 'Two Pointers'),
        ('Dynamic Programming', 'Dynamic Programming'),
    ]

    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'), 
        ('Medium', 'Medium'), 
        ('Hard', 'Hard')
    ]

    MODULE_CHOICES = [
        ('Loops', 'Loops'),
        ('Array', 'Array'),
        ('Recursion', 'Recursion'),
        ('Hashing', 'Hashing'),
        ('Dynamic-Programming', 'Dynamic-Programming'),
        ('Math', 'Math')
    ]

    title = models.CharField(max_length=100, unique=True)
    time_limit = models.IntegerField(default=1)
    hint = models.TextField(default="No hints in the Database")
    module = models.CharField(max_length=100, choices=MODULE_CHOICES, default='Array', blank=False)
    noof_solves = models.IntegerField(default=0)
    noof_attempts = models.IntegerField(default=0)
    problem_statement = models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()

    input_file1 = models.FileField(upload_to=test_case_upload_path1, blank=True, default = None)
    output_file1 = models.FileField(upload_to=test_case_upload_path1, blank=True)

    input_file2 = models.FileField(upload_to=test_case_upload_path2, blank=True, default=None)
    output_file2 = models.FileField(upload_to=test_case_upload_path2, blank=True)
    
    input_file3 = models.FileField(upload_to=test_case_upload_path3, blank=True, default=None)
    output_file3 = models.FileField(upload_to=test_case_upload_path3, blank=True)
    
    input_file4 = models.FileField(upload_to=test_case_upload_path4, blank=True, default = None)
    output_file4 = models.FileField(upload_to=test_case_upload_path4, blank=True)
    
    input_file5 = models.FileField(upload_to=test_case_upload_path5, blank=True, default = None)
    output_file5 = models.FileField(upload_to=test_case_upload_path5, blank=True)
    
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Easy')
    tags = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.title

class Submission(models.Model):
    STATUS_CHOICES = [
        ('Accepted', 'Accepted'),
        ('Wrong Answer', 'Wrong Answer'),
        ('Time Limit Exceeded', 'Time Limit Exceeded'),
        ('Runtime Error', 'Runtime Error'),
        ('Compilation Error', 'Compilation Error'),
    ]

    user = models.ForeignKey('accounts.ProPyUser', on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Wrong Answer')
    code = models.TextField()
    failed_test_case = models.IntegerField(default=1)
    views = models.IntegerField(default=0)
    time_taken = models.FloatField()
    memory_taken = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} | {self.problem.title} | {self.status}'