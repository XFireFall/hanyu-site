from collections import defaultdict


def get_terms_for_table():
    terms = []
    with open("./data/terms.csv", "r", encoding="utf-8") as f:
        cnt = 1
        for line in f.readlines()[1:]:
            word, pinyin, translation, example, source = line.split(";")
            terms.append([cnt, word, pinyin, translation, example])
            cnt += 1
    
    print(terms)
    
    return terms


def update_term(search_key, **kwargs):
    with open("./data/terms.csv", "r", encoding="utf-8") as f:
        title, *terms_data = [l.strip("\n") for l in f.readlines()]
    
    keys = title.split(';')
    
    terms = [
        {key: value for key, value in zip(keys, term_data.split(';'))}
        for term_data in terms_data
    ]
    
    print(terms)
    
    print(search_key, kwargs)
    
    search_value = kwargs[search_key]
    for term in terms:
        if term[search_key] == search_value:
            print(term)
            for key, value in kwargs.items():
                term[key] = value
            print(term)
            break
    else:
        return False
    
    lines = [title] + [
        "{word};{pinyin};{translation};{example};{source}".format(**term)
        for term in terms
    ]
    with open("./data/terms.csv", "w", encoding="utf-8") as f:
        f.write('\n'.join(lines))
    return True

def write_term(word, pinyin, translation, example):
    new_term_line = f"{word};{pinyin};{translation};{example};user"
    with open("./data/terms.csv", "r", encoding="utf-8") as f:
        existing_terms = [l.strip("\n") for l in f.readlines()]
        title = existing_terms[0]
        old_terms = existing_terms[1:]
        
        print(title)
        
    terms_sorted = old_terms + [new_term_line]
    terms_sorted.sort()
    new_terms = [title] + terms_sorted
    with open("./data/terms.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(new_terms))


def get_terms_stats():
    db_terms = 0
    user_terms = 0
    defin_len = []
    
    cnt_words = 0
    cnt_phrases = 0
    words_by_len = defaultdict(int)
    missing_example = 0
    
    with open("./data/terms.csv", "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            word, pinyin, translation, example, source = line.split(";")
            
            is_word = len(pinyin.split()) == 1
            
            if is_word:
                cnt_words += 1
            else:
                cnt_phrases += 1
            
            words_by_len[len(word)] += 1
            
            if not example:
                missing_example += 1
            
            if "user" in source:
                user_terms += 1
            elif "db" in source:
                db_terms += 1
    stats = {
        "terms_all": db_terms + user_terms,
        "terms_own": db_terms,
        "terms_added": user_terms,
        
        "words": cnt_words,
        "phrases": cnt_phrases,
        
        "words_by_len": words_by_len.items(),
        
        "missing_example": missing_example,
    }
    return stats
