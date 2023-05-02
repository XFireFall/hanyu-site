from django.shortcuts import render
from django.core.cache import cache
from . import terms_work

import random

def index(request):
    return render(request, "index.html")


def terms_list(request):
    terms = terms_work.get_terms_for_table()
    return render(request, "term_list.html", context={"terms": terms})


def add_term(request):
    return render(request, "term_add.html")


def send_term(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name", "")
        
        word = request.POST.get("word")
        pinyin = request.POST.get("pinyin").replace(";", ",")
        translation = request.POST.get("translation").replace(";", ",")
        example = request.POST.get("example", "").replace(";", ",")
        
        context = {"user": user_name}
        #if len(new_definition) == 0:
            #context["success"] = False
            #context["comment"] = "Описание должно быть не пустым"
        #elif len(new_term) == 0:
            #context["success"] = False
            #context["comment"] = "Термин должен быть не пустым"
        #else:
        if True:
            context["success"] = True
            context["comment"] = "Ваш термин принят"
            terms_work.write_term(word, pinyin, translation, example)

        if context["success"]:
            context["success-title"] = ""
        return render(request, "term_request.html", context)
    else:
        add_term(request)


def add_term_example(request):
    return render(request, "term_add_example.html")


def send_term_example(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name", "")
        
        word = request.POST.get("word")
        example = request.POST.get("example").replace(";", ",")
        
        context = {"user": user_name}
        
        if terms_work.update_term("word", word=word, example=example):
            context["success"] = True
            context["comment"] = "Пример употребления принят, распознанный ввод - иероглиф"
        elif terms_work.update_term("pinyin", pinyin=word, example=example):
            context["success"] = True
            context["comment"] = "Пример употребления принят, распознанный ввод - пиньинь"
        else:
            context["success"] = False
            context["comment"] = "Пример употребления отклонен, тип входных данных не был распознан или введенное слово не существет"

        if context["success"]:
            context["success-title"] = ""
        return render(request, "term_request.html", context)
    else:
        add_term_example(request)


def show_stats(request):
    stats: dict[str, float] = terms_work.get_terms_stats()
    
    print("stats =", stats)
    
    return render(request, "stats.html", stats)


def random_term(request):
    terms = terms_work.get_terms_for_table()
    i = random.randint(0, len(terms)-1)
    print(i)
    _, word, pinyin, translation, example = terms[i]
    return render(request, "term_random.html", context={
        "word": word,
        "pinyin": pinyin,
        "translation": translation,
        "example": example,
    })
