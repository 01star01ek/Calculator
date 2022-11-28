
from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import Profile,Lesson
from calapp.models import Graduate
from django.contrib import messages



def calculator(request):    
    current_user = request.user
    #user_id = user.id
    #userprofile = get_object_or_404(Profile,pk=user_id)
    user_profile = Profile.objects.get(user = current_user)
    gradu_major = user_profile.major
    gradu_ad_year = user_profile.ad_year
    gradu = Graduate.objects.get(major=gradu_major, ad_year=gradu_ad_year)


    choicemajor = Lesson.objects.filter(link = current_user, classkind='전공선택')
    needmajor   = Lesson.objects.filter(link = current_user, classkind='전공필수')
    
    special     = Lesson.objects.filter(link = current_user, classkind='특화교양')
    college     = Lesson.objects.filter(link = current_user, classkind='대학별교양')
    balance     = Lesson.objects.filter(link = current_user, classkind='균형교양')
    basic       = Lesson.objects.filter(link = current_user, classkind='기초교양')
    free        = Lesson.objects.filter(link = current_user, classkind='자유선택')
    teaching    = Lesson.objects.filter(link = current_user, classkind='교직이수')

    choicemajor = add_credit(choicemajor)
    deepmajor = 0
    needmajor = add_credit(needmajor)
    special = add_credit(special)
    college = add_credit(college)
    balance = add_credit(balance)
    basic = add_credit(basic)
    free = add_credit(free)
    teaching = add_credit(teaching)

    
    error_sum = 0

    flag = 0

    if(needmajor < gradu.needmajor):
        flag = 1
        messages.info(request,"전공 필수 학점이 부족합니다.")
    elif(needmajor > gradu.needmajor):
        choicemajor = choicemajor + (needmajor - gradu.needmajor)
        needmajor = gradu.needmajor
        messages.info(request,"전공 필수 학점이 초과되어 전공선택 학점에 추가되었습니다.")

    if(choicemajor < gradu.choicemajor):
        flag = 1
        messages.info(request,"전공 학점이 부족합니다.")
    else:
        deepmajor = choicemajor - gradu.choicemajor
        choicemajor = gradu.choicemajor
        if(deepmajor < gradu.deepmajor):
            flag = 1
            messages.info(request,"심화 전공 학점이 부족합니다.")
        elif(deepmajor > gradu.deepmajor):
            free = free + (deepmajor - gradu.deepmajor)
            deepmajor = gradu.deepmajor
            messages.info(request,"전공 학점이 초과되어 자유선택 학점에 추가되었습니다.")

    if(college < gradu.college):
        flag = 1
        messages.info(request,"대학별 교양 학점이 부족합니다.")
    elif(college > gradu.college):
        free = free + (college - gradu.college)
        error_sum = error_sum + (college - gradu.college)
        college = gradu.college
        messages.info(request,"대학별 교양 학점이 초과되어 자유선택 학점에 추가되었습니다.")

    if(basic < gradu.basic):
        flag = 1
        messages.info(request,"기초 교양 학점이 부족합니다.")
    elif(basic > gradu.basic):
        free = free + (basic - gradu.basic)
        error_sum = error_sum + (basic - gradu.basic)
        basic = gradu.basic
        messages.info(request,"기초 교양 학점이 초과되어 자유선택 학점에 추가되었습니다.")

    if(gradu.special):
        if(special < gradu.special):
            messages.info(request,"특화 교양 학점은 균형교양학점으로 대체됩니다.")
            if((balance+special) < (gradu.balance + gradu.special)):
                flag = 1
                messages.info(request,"균형교양 학점이 부족합니다.")
            elif((balance+special) > (gradu.balance + gradu.special)):
                free = free + (balance + special - gradu.balance - gradu.special)
                error_sum = error_sum + (balance + special - gradu.balance - gradu.special)
                balance = gradu.balance + gradu.special
                messages.info(request,"균형 교양 학점이 초과되어 자유선택 학점에 추가되었습니다.")

        elif(special > gradu.special):
            free = free + (special - gradu.special)
            error_sum = error_sum + (special - gradu.special)
            special = gradu.special
            messages.info(request,"특화 교양 학점이 초과되어 자유선택 학점에 추가되었습니다.")
            if(balance < gradu.balance):
                flag = 1
                messages.info(request,"균형교양 학점이 부족합니다.")
            elif(balance > gradu.balance):
                free = free + (balance - gradu.balance)
                error_sum = error_sum + (balance - gradu.balance)
                balance = gradu.balance
                messages.info(request,"균형 교양 학점이 초과되어 자유선택 학점에 추가되었습니다.")
        else:
            if(balance < gradu.balance):
                flag = 1
                messages.info(request,"균형교양 학점이 부족합니다.")
            elif(balance > gradu.balance):
                free = free + (balance - gradu.balance)
                error_sum = error_sum + (balance - gradu.balance)
                balance = gradu.balance
                messages.info(request,"균형 교양 학점이 초과되어 자유선택 학점에 추가되었습니다.")

    else:
        if(balance < gradu.balance):
            flag = 1
            messages.info(request,"균형교양 학점이 부족합니다.")
        elif(balance > gradu.balance):
            free = free + (balance - gradu.balance)
            error_sum = error_sum + (balance - gradu.balance)
            balance = gradu.balance
            messages.info(request,"균형 교양 학점이 초과되어 자유선택 학점에 추가되었습니다.")

    if(free < gradu.free):
        flag = 1
        messages.info(request,"자유 선택 학점이 부족합니다.")

    if(error_sum > 10):
        messages.info(request,"자유선택으로 인정되는 초과교양 학점은 10학점까지 인정됩니다. 초과 학점은 제외되었습니다.")
        free = free - (error_sum - 10)

    ge_Lessons = {
        '기초교양' : [basic,gradu.basic,gradu.basic-basic],
        '대학별교양' : [college,gradu.college,gradu.college-college],
        '균형교양' : [balance,gradu.balance,gradu.balance-balance],
        '특화교양' : [special,gradu.special,gradu.special-special],
        }


    free_Lessons = {
        '자유선택' : [free,gradu.free,gradu.free-free],
        '교직이수' : [teaching,gradu.teaching,gradu.teaching-teaching],
        }


    major_Lessons = {
        '전공선택' : [choicemajor,gradu.choicemajor,gradu.choicemajor-choicemajor],
        '심화전공' : [deepmajor,gradu.deepmajor,gradu.deepmajor-deepmajor],
        '전공필수' : [needmajor,gradu.needmajor,gradu.needmajor-needmajor],
        }
    
    Lessons = [
    choicemajor,
    deepmajor,
    needmajor,
    special,
    college,
    balance,
    basic,
    free,
    ]

    all_credits = 0
    for credit in Lessons:
        all_credits += credit
        
    remain = gradu.sum - all_credits

    if(flag):
        messages.info(request,"졸업이 불가능 합니다. 학점이 부족합니다.")
    else:
        messages.info(request,"고생하셨습니다. 졸업이 가능합니다.")
    
    
    return render(request,'result.html',{
        'user':current_user,'all':all_credits,'graduate':gradu,
        'ge_class':ge_Lessons,
        'major_class':major_Lessons,
        'free_class':free_Lessons,
        'remain':remain,
        'flag':flag
        })





def add_credit(credits):
    sum = 0
    for credit in credits:
        sum = sum + credit.classcredits
    return sum



def class_delete(request,class_id):
    delete_lesson = get_object_or_404(Lesson, pk=class_id) #수강한 과목 지우기
    delete_lesson.delete()
    return redirect('calculator')