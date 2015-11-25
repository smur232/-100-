# 20
import json


def find_text_for_country(country, filename):
    for article in open(filename):
        j_article = json.loads(article)
        if country in j_article['title']:
            return j_article['text']

country_text = find_text_for_country(u'ポルトガル', 'jawiki-country.json')
print(' #20')
#print(country_text)

# 21


def find_category_line(country, country_text,  filename):
    country_text_by_line = country_text.split('\n')
    for line in country_text_by_line:
        if country in line and 'Category' in line:
            return line
print(' #21')
print(find_category_line(u'イギリス', country_text, 'jawiki-country.json'))

# 22

import re


def find_category(country_text):
    category = re.compile('\[\[Category:((?P<category>.*)\|+.*)\]\]')
    return category.search(country_text).group('category')
print(' #22')
print(find_category(country_text))

# 23

def section_levels(country_text):
    text_by_line = country_text.split("\n")
    section_list = [line for line in text_by_line if line.startswith("==")]
    return "\n".join([section + "\t" + str(section.count("=")//2-1) for section in section_list])
print(' #23')
print(section_levels(country_text))


# 24

def print_all_media(country_text):
    text_by_line = country_text.split("\n")
    for line in text_by_line:
        if line.startswith(u'[[ファイル:'):
            print(line)
print('\n   #24 All media files: ')
print_all_media(country_text)

# 25


def get_basic_info(country_text):
    basic_info_by_line = find_basic_info_from_list(re.split('\n{{|\n}}',country_text)).split('\n')
    all_basic_info = [info.strip('|') for info in basic_info_by_line if info.startswith('|')]
    return dict([tuple(line.split(' =')) for line in all_basic_info])


def find_basic_info_from_list(info_list):
    for info in info_list:
        if info.startswith(u'{{基礎情報') or info.startswith(u'基礎情報'):
            return info

print('\n   #25 Basic Information: ')
basic_info_dict = get_basic_info(country_text)
print(basic_info_dict)

# 26


def take_away_markup(basic_info_dict):
    return dict([(key, value.replace("'''''", "").replace("'''", "").replace("''", "")) for key, value in basic_info_dict.items()])

print('\n   #26 Without bold: ')
print(take_away_markup(basic_info_dict))


# 27
# 内部リンクは記事名のみを表示しております


def take_away_link_markup(basic_info_dict):
    without_bold = dict([(key, value.replace("'''''", "").replace("'''", "").replace("''", "")) for key, value in basic_info_dict.items()])
    return dict([(key, re.sub(r"\[\[.*\]\]", lambda x: x.group().replace("[[", "").replace("]]", "").split("|")[0].split("#")[0], value)) for key, value in without_bold.items()])

print('\n   #27 Without link:')
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

print('\n   #28 Without markup:')
basic_info_no_markup = take_away_markup(basic_info_dict)
print("\n".join([key+": "+basic_info_no_markup[key] for key in basic_info_no_markup.keys()]))

# 29

import urllib.request
import urllib.parse

def get_flag_image(basic_info_no_markup):
    url = "https://ja.wikipedia.org/w/api.php?format=json&action=query&titles=Image:{}&prop=imageinfo&iiprop=url".format(urllib.parse.quote_plus(basic_info_no_markup[u"国旗画像"]))
    response = urllib.request.urlopen(url).read().decode('utf-8')
    json_response = json.loads(response)
    try:
        return json_response['query']['pages']['-1']["imageinfo"][0]["url"]
    except KeyError:
         return '画像が見つかりませんでした、画像タイトルを再確認してください'

print('\n   #29 Image URL: ')
print(get_flag_image(basic_info_no_markup))
