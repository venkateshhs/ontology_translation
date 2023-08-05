import urllib

import wikipedia

wikipedia.set_lang('en')

link = 'https://en.wikipedia.org/wiki/OpenAI'

page_title = urllib.parse.unquote(link.split("/")[-1])
page = wikipedia.page(page_title)
print(page.title)

page_summary = wikipedia.summary(page_title)

print(page_summary)
