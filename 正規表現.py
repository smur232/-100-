# 20
import json


def find_text_for_country(country, filename):
    for article in open(filename):
        j_article = json.loads(article)
        if country in j_article['title']:
            return j_article['text']

country_text = find_text_for_country(u'イギリス', 'jawiki-country.json')
#print(country_text)

# 21


def find_category_line(country, country_text,  filename):
    country_text_by_line = country_text.split('\n')
    for line in country_text_by_line:
        if country in line and 'Category' in line:
            return line

print(find_category_line(u'イギリス', country_text, 'jawiki-country.json'))

# 22

import re


def find_category(country_text):
    category = re.compile('\[\[Category:((?P<category>.*)\|+.*)\]\]')
    return category.search(country_text).group('category')

print(find_category(country_text))

# 23

def section_levels(country_text):
    text_by_line = country_text.split("\n")
    section_list = [line for line in text_by_line if line.startswith("==")]
    return "\n".join([section + "\t" + str(section.count("=")//2-1) for section in section_list])

print(section_levels(country_text))


# 24

def extract_all_media(country_text):
    text_by_line = country_text.split("\n")
    for line in text_by_line:
        if line.startswith(u'[[ファイル:'):
            print(line)
print('\nAll media files: ')
extract_all_media(country_text)

# 25

def get_basic_info(country_text):
    basic_info_line = country_text.split("}}\n")[1].split('\n')
    all_basic_info = [info.strip('|') for info in basic_info_line if info.startswith('|')]
    return dict(tuple(line.split(' = ')) for line in all_basic_info)

print('\nBasic Information: ')
basic_info_dict = get_basic_info(country_text)
print(basic_info_dict)
# def basic(country_text):
#     basic_info_line = country_text.split("}}\n")[1].split('\n')
#     all_basic_info = [info for info in basic_info_line if info.startswith('|')]
#     return dict(tuple(line.split(' = ')) for line in all_basic_info)
# print(basic(country_text))

# 26

def take_away_markup(basic_info_dict):
    return dict([(key, value.replace("'''''", "").replace("'''", "").replace("''", "")) for key, value in basic_info_dict.items()])

print('\nWithout bold: ')
print(take_away_markup(basic_info_dict))


# 27
# 内部リンクは記事名のみを表示しております


def take_away_link_markup(basic_info_dict):
    without_bold = dict([(key, value.replace("'''''", "").replace("'''", "").replace("''", "")) for key, value in basic_info_dict.items()])
    return dict([(key, re.sub(r"\[\[.*\]\]", lambda x: x.group().replace("[[", "").replace("]]", "").split("|")[0].split("#")[0], value)) for key, value in without_bold.items()])

print('\nWithout link:')
print(take_away_link_markup(basic_info_dict))

# 28
# スピードを早くするには以下の4つのステップを一回で全てのマークアップを取り除くのが良いと思いました
# 今回は読みやすさのために、新しい辞書を４つ作りました


def take_away_markup(basic_info_dict):
    without_bold = dict([(key, value.replace("'''''", "").replace("'''", "")
                        .replace("''", "")) for key, value in basic_info_dict.items()])

    without_links = dict([(key, re.sub(r"\[\[.*\]\]", lambda x: x.group().replace("[[", "")
                        .replace("]]", "").split("|")[0].split("#")[0], value)) for key, value in without_bold.items()])

    without_template = dict([(key, re.sub(r"{{.*}}", lambda x: x.group().replace("{{", "")
                        .replace("}}", ""), value)) for key, value in without_links.items()])

    without_HTML = dict([(key, re.sub(r"<.*>", "", value)) for key, value in without_template.items()])
    return without_HTML

print('\nWithout markup:')
basic_info_no_markup = take_away_markup(basic_info_dict)
print("\n".join([key+": "+basic_info_no_markup[key] for key in basic_info_no_markup.keys()]))

# 29

import urllib.request
import urllib.parse

def get_flag_image(basic_info_no_markup):
    url = "https://ja.wikipedia.org/w/api.php?format=json&action=query&titles=Image:{}&prop=imageinfo&iiprop=url".format(urllib.parse.quote_plus(basic_info_no_markup[u"国旗画像"]))
    response = urllib.request.urlopen(url).read().decode('utf-8')
    json_response = json.loads(response)
    return json_response['query']['pages']['-1']["imageinfo"][0]["url"]

print('\nImage URL: ')
print(get_flag_image(basic_info_no_markup))
