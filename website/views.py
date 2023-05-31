"""
Вюхи на класах
"""
#
#
# import openai
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm
# from .forms import SignUpForm
# from .models import Code
#
#
# class CodeProcessor:
#     OPENAI_API_KEY = "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"
#
#     def __init__(self):
#         self.lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'go', 'html', 'java', 'javascript',
#                           'markup',
#                           'markup-templating', 'matlab', 'objectivec', 'perl', 'php', 'powershell', 'python', 'r',
#                           'regex',
#                           'ruby', 'rust', 'sass', 'sql', 'swift', 'typescript']
#
#         self.openai_engine = 'text-davinci-003'
#
#     def get_openai_response(self, prompt):
#         openai.api_key = self.OPENAI_API_KEY
#         openai.Model.list()
#         response = openai.Completion.create(
#             engine=self.openai_engine,
#             prompt=prompt,
#             temperature=0,
#             max_tokens=1000,
#             top_p=1.0,
#             frequency_penalty=0.0,
#             presence_penalty=0.0,
#         )
#         return (response["choices"][0]["text"]).strip()
#
#     def process_code(self, request, template):
#         if request.method == "POST":
#             code = request.POST['code']
#             lang = request.POST['lang']
#
#             if lang == "Вибрати мову програмування":
#                 messages.success(request, "Будь ласка, виберіть мову програмування.")
#                 return render(request, template, {'lang_list': self.lang_list, 'code': code, 'lang': lang})
#
#             try:
#                 prompt = f"Respond only with code. Fix this {lang} code: {code}"
#                 response = self.get_openai_response(prompt)
#                 record = Code(question=code, code_answer=response, language=lang, user=request.user)
#                 record.save()
#                 return render(request, template,
#                               {'lang_list': self.lang_list, 'code': code, 'lang': lang, 'response': response})
#             except Exception as e:
#                 return render(request, template,
#                               {'lang_list': self.lang_list, 'code': code, 'lang': lang, 'response': e})
#
#         return render(request, template, {'lang_list': self.lang_list})
#
#
# class HomeView:
#     template_name = 'home.html'
#
#     def __init__(self):
#         self.code_processor = CodeProcessor()
#
#     def get(self, request):
#         return self.code_processor.process_code(request, self.template_name)
#
#     def post(self, request):
#         return self.code_processor.process_code(request, self.template_name)
#
#
# class SuggestView:
#     template_name = 'suggest.html'
#
#     def __init__(self):
#         self.code_processor = CodeProcessor()
#
#     def get(self, request):
#         return self.code_processor.process_code(request, self.template_name)
#
#     def post(self, request):
#         return self.code_processor.process_code(request, self.template_name)
#
#
# class LoginView:
#     def post(self, request):
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, "Ви увійшли у систему.")
#             return redirect('home')
#         else:
#             messages.success(request, "Помилка входу. Будь ласка спробуйте ще раз...")
#             return redirect('home')
#
#
# class LogoutView:
#     def get(self, request):
#         logout(request)
#         messages.success(request, "Ви вийшли з системи.")
#         return redirect('home')
#
#
# class RegisterView:
#     template_name = 'register.html'
#
#     def get(self, request):
#         form = SignUpForm()
#         return render(request, self.template_name, {"form": form})
#
#     def post(self, request):
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             messages.success(request, "Ви зареєструвалися!")
#             return redirect('home')
#         return render(request, self.template_name, {"form": form})
#
#
# class PastView:
#     template_name = 'past.html'
#
#     def get(self, request):
#         if request.user.is_authenticated:
#             code = Code.objects.filter(user_id=request.user.id)
#             return render(request, self.template_name, {"code": code})
#         else:
#             messages.success(request, "Ви маєте бути авторизованим, щоб побачити попередній код")
#             return redirect('home')
#
#
# class DeletePastView:
#     def get(self, request, Past_id):
#         past = Code.objects.get(pk=Past_id)
#         past.delete()
#         messages.success(request, "Успішно видалено")
#         return redirect('past')


"""MAIN 2.0"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from dotenv import load_dotenv
from .forms import SignUpForm
from .models import Code
import os
import openai

from django.urls import reverse

# Load environment variables from .env file
load_dotenv()

# Create your views here.

KEY = os.getenv('API_KEY')

LANGUAGES = [
    'c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'go', 'html', 'java',
    'javascript', 'markup', 'markup-templating', 'matlab', 'objectivec', 'perl',
    'php', 'powershell', 'python', 'r', 'regex', 'ruby', 'rust', 'sass', 'sql',
    'swift', 'typescript'
]


def check_language(request, lang, code):
    if lang == "Вибрати мову програмування":
        messages.success(request, "Будь ласка, виберіть мову програмування.")
        return render(request, 'home.html', {'lang_list': LANGUAGES, 'code': code, 'lang': lang})
    return None


# def process_request(request, template_name, prompt, code, lang):
def process_request(request, template_name, prompt, code, lang, explain=False):
    try:
        openai.api_key = KEY
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            temperature=0,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        if explain:
            response = response.replace('\n', '<br>')

        response = response.choices[0].text.strip()

        record = Code(question=code, code_answer=response, language=lang, user=request.user)
        record.save()

        share_url = request.build_absolute_uri(reverse('share', args=[record.id]))

        # return render(request, template_name, {'lang_list': LANGUAGES, 'response': response, 'lang': lang})
        return render(request, template_name,
                      {'lang_list': LANGUAGES, 'response': response, 'lang': lang, 'share_url': share_url})


    except Exception as e:
        return render(request, template_name, {'lang_list': LANGUAGES, 'response': e, 'lang': lang})


def home(request):
    if request.method == "POST":
        code = request.POST.get('code')
        lang = request.POST.get('lang')

        error_response = check_language(request, lang, code)
        if error_response:
            return error_response

        prompt = f"Respond only with code. Fix this {lang} code: {code}"
        return process_request(request, 'home.html', prompt, code, lang)

    return render(request, 'home.html', {'lang_list': LANGUAGES})


def suggest(request):
    if request.method == "POST":
        code = request.POST.get('code')
        lang = request.POST.get('lang')

        error_response = check_language(request, lang, code)
        if error_response:
            return error_response

        prompt = f"Respond only with code. {code}"
        return process_request(request, 'suggest.html', prompt, code, lang)

    return render(request, 'suggest.html', {'lang_list': LANGUAGES})


def explain_code(request):
    if request.method == "POST":
        code = request.POST.get('code')
        lang = request.POST.get('lang')

        error_response = check_language(request, lang, code)
        if error_response:
            return error_response

        prompt = f"Поясни наступний {lang} код: \n {code}"
        return process_request(request, 'explain.html', prompt, code, lang)

    return render(request, 'explain.html', {'lang_list': LANGUAGES})


def share(request, record_id):
    record = Code.objects.get(pk=record_id)

    share_url = request.build_absolute_uri(reverse('share', args=[record_id]))

    return render(request, 'share.html', {'record': record, 'share_url': share_url})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Ви увійшли у систему.")
            return redirect('welcome')
        else:
            messages.success(request, "Помилка входу. Будь ласка спробуйте ще раз...")
            return redirect('home')
    else:
        return render(request, 'home.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "Ви вийшли з системи.")
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Ви зареєструвалися!  ")
            return redirect('welcome')

    else:
        form = SignUpForm()

    return render(request, 'register.html', {"form": form})


def past(request):
    if request.user.is_authenticated:
        code = Code.objects.filter(user_id=request.user.id)
        return render(request, 'past.html', {"code": code})
    else:
        messages.success(request, "Ви маєте бути авторизованим, щоб побачити попередній код")
        return redirect('home')


def delete_past(request, Past_id):
    past = Code.objects.get(pk=Past_id)
    past.delete()
    messages.success(request, "Успішно видалено")
    return redirect('past')


def delete_all_past(request):
    if request.user.is_authenticated:
        Code.objects.filter(user_id=request.user.id).delete()
        messages.success(request, "Успішно видалено всю історію")
    else:
        messages.success(request, "Ви маєте бути авторизованим, щоб видалити історію")
    return redirect('past')


def welcome(request):
    return render(request, 'welcome.html')
