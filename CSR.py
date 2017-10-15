main_words = ['corporate', 'social', 'responsibility', 'corporate', 'conscience', 'csr', 'ethical', 'business', 'model']
key_words = ['ecomic', 'environmental', 'company', 'industry', 'self-regulation', 'standards', 'spirit', 'law',
             'enterprise', 'conglomorate']
key_issues = ['environmental', 'management', 'eco-efficiency', 'responsible', 'sourcing', 'stakeholders', 'engagement',
              'labour', 'standards', 'conditions',
              'employee', 'community', 'relations', 'enquiry', 'gender', 'balance', 'human', 'rights',
              'anti-corruption', ' measure'
                                 'governance']
key_benefits = ['improve', 'brand', 'image', 'enhance', 'customer', 'loyalty', 'better', 'decision', 'making']

list_of_lists = [main_words, key_words, key_issues, key_benefits]
main_words_points = 10
key_words_points = 5
key_issues_points = 3
key_benefits_points = 2


def csr(line):
    line.split()
    points = 0
    for i in range(len(line)):
        for j in list_of_lists:
            for k in j:
                if k == line[i]:
                    if list_of_lists[0]:
                        points = points + main_words_points
                    elif list_of_lists[1]:
                        points = points + key_words_points
                    elif list_of_lists[2]:
                        points = points + key_issues_points
                    elif list_of_lists[3]:
                        points = points + key_benefits_points
    return points
