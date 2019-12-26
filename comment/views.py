from django.shortcuts import render,redirect
from .models import comments
from .forms import CommentForm
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.http import JsonResponse

# Create your views here.
def news(request,pincode):
    pass
    print("pincode",pincode)
    comment = comments.objects.filter(pincode=pincode, reply=None).order_by('-id')
    comment_form = CommentForm(request.POST)
    if request.method == 'POST':
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('i_id')
            comment_qs = None
            if reply_id:
                comment_qs = comments.objects.get(id = reply_id)
            comments_a = comments.objects.create(user = request.user,pincode = pincode,content = content, reply = comment_qs)
            comments_a.save()
            x = "http://127.0.0.1:8000/news/" + str(pincode)
            return redirect(x)
        else:
            comment_form = CommentForm()
    return render(request,'home_comment.html',{'comment':comment,'comment_form':comment_form,"pincode":pincode})






@require_POST
@ajax_required
def write_problem(request):
    if request.method == 'POST':
        pincode = int(request.user.address1.pincode)

        comment_come = request.POST.get('comment')

        user_dn = str(request.user)
        try:
            comment_create = comments.objects.create(
            user = request.user,
            pincode = pincode,
            content = comment_come,
            )
        except:
            print("e")
        print("Nit")
        user_m = {'id':comment_create.id,'user_dn':user_dn,'content':comment_create.content}
        data = {
        'status' : 'ok',
        'user_m':user_m
        }
        return JsonResponse(data)
    return JsonResponse({'status' : 'ko'})



@require_POST
@ajax_required
def write_reply(request):
    if request.method == 'POST':
        #try:
        problem_id = request.POST.get('problem_id')
        print(problem_id)
        pincode = int(request.user.address1.pincode)
        reply_come = request.POST.get('reply')
        print(reply_come)

        a_reply_to = comments.objects.get(id=problem_id)
        a_reply = comments.objects.get(id=problem_id).id

        user_dn = str(request.user)
        reply_use_for_ajax = comments.objects.create(
        user = request.user,
        pincode = pincode,
        reply = a_reply_to,
        content = reply_come,
        )
        user_p_r = {'id':reply_use_for_ajax.id,'user_dn':user_dn,'reply_use_id':a_reply,'content':reply_use_for_ajax.content}
        data = {
        'status' : 'ok',
        'reply':reply_come,
        'user_p_r':user_p_r
        }
        return JsonResponse(data)
    return JsonResponse({'status' : 'ko'})
