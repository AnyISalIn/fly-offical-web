import os

from pathlib import Path
from markdown2 import Markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from bs4 import BeautifulSoup


class Article(object):

    def __init__(self, article_title, article_content, article_link):
        self.title = article_title
        self.content = article_content
        self.link = article_link


def remove_title(content):
    bs_obj = BeautifulSoup(content, 'lxml')
    title = bs_obj.h1.text
    bs_obj.find('h1').decompose()
    return title, str(bs_obj)

def get_loader(template_path):
    return Environment(
        loader=FileSystemLoader(template_path),
        autoescape=select_autoescape(['html', 'xml'])
    )


class FlyTemplate(object):
    article_templates = {
        'detail_page': 'detail.html',
        'custom_page': 'customer_center.html'
    }
    article_path = 'data/articles'
    article_render_path = 'articles'

    def __init__(self, template_path, template_name, render_path):
        self._loader = get_loader(template_path)
        self.template = self._loader.get_template(template_name)
        if self.is_article:
            self.render_path = os.path.join(
                render_path, self.article_render_path)
        else:
            self.render_path = render_path

    @staticmethod
    def _render_markdown(file_path):
        with open(file_path, 'r') as f:
            m = Markdown()
            return m.convert(f.read())

    @property
    def is_article(self):
        return True if self.template.name == self.article_templates['detail_page'] else False

    @property
    def is_custom(self):
        return True if self.template.name == self.article_templates['custom_page'] else False

    def render(self):
        def simpe_render(context={}):
            with open(os.path.join(self.render_path, self.template.name), 'w') as f:
                f.write(self.template.render(context))
                print('Write to {}'.format(f.name))

        def generate_path(article_name):
            return os.path.join(self.render_path, '{}.{}'.format(article.name.split('.md')[0], 'html'))

        if not self.is_article and not self.is_custom:
            simpe_render()
        else:
            p = Path(self.article_path)
            articles = [item for item in p.iterdir() if item.name.endswith('md')]

            summary = []
            for article in articles:
                title, content = remove_title(self._render_markdown(article))
                context = dict(
                    article_title=title,
                    article_content=content,
                    article_link='/{}'.format(os.path.join(self.article_render_path, article.name.split('.md')[0] + '.html'))
                )
                print(context)
                summary.append(Article(**context))
                if not self.is_custom:
                    with open(generate_path(article.name), 'w') as f:
                        f.write(self.template.render(context))
                        print('Write to {}'.format(f.name))
                else:
                    simpe_render({'articles': summary})



def main():
    loader = get_loader('src/templates')
    for template in loader.list_templates():
        f = FlyTemplate('src/templates', template, 'public')
        f.render()

if __name__ == '__main__':
    main()
