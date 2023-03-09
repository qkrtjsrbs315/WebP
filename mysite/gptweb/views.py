from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
import openai
from .models import User

API_KEY = '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'


# Create your views here.

def Index(request):
    return render(request, 'index.html')


def Search(request):
    if request.user.is_authenticated:
        print("INDEX로그인이 성공되었습니다" + str(request.user))
        if request.method == "GET":
            return render(request, 'search.html')
        elif request.method == "POST":
            q = request.POST['question']
            print("질문 : " + q)
            answer = ChatGPT(question=q)
            #       User.save()
            # AI_LIST = openai.Model.list()
            # print("AI_LIST="+str(AI_LIST))
            request.session['answer'] = answer
            print(request.session['answer'])
            return redirect('result')
    else:
        return HttpResponse(
            "<script>alert('올바르지 않은 접근입니다. 로그인 페이지로 돌아갑니다.');location.href='/login';</script>")


def AnswerPage(request):
    answer = request.session['answer']
    print("AnswerPage" + answer)
    return render(request, 'result.html', {'answer': answer})


def Register(request):
    if request.method == "GET":
        return render(request, 'register.html')

    elif request.method == "POST":
        id = request.POST['userid']
        pw = request.POST['userpw']
        print("id = " + id + "pw = " + pw)
        user = User.objects.create_user(username=id, password=pw)
        user.save()
        if user:
            return redirect('login')


def Login(request):
    if request.method == "GET":
        return render(request, 'login.html')

    elif request.method == "POST":
        id = request.POST['userid']
        pw = request.POST['userpw']

        result = authenticate(username=id, password=pw)
        print(result)
        print("id = " + id + "pw = " + pw)
        if result != None:
            print("로그인이 성공되었습니다" + str(request.user))
            # return HttpResponse('<script>alert("로그인이 성공되었습니다.") location.href="http://127.0.0.1:8000/search"</script>')
            return redirect('search')
        else:
            print('fail!')
            return HttpResponse('<script>alert("로그인이 실패되었습니다.")</script>')


def ChatGPT(question):
    final = ''
    openai.api_key = API_KEY
    prompt = question
    result = openai.Completion.create(
        prompt=prompt,
        model='text-davinci-003',
        max_tokens=2048,
        temperature=0,
        n=1,
        # stop=['\n']
    )

    print(result)
    for result in result.choices:
        final = result.text

    b = final.replace('\n', '')
    print(b)
    return b
