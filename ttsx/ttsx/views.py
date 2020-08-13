from django.shortcuts import render,redirect,reverse

def base(reqeust):
    return render(reqeust,'base.html')
