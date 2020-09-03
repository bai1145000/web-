from django.shortcuts import render,redirect,reverse

def static(reqeust,html):
    print(reqeust.url)

    return render(reqeust,'static_index.html')
