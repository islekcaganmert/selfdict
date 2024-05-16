from bevyframe import Frame, Page, Widget, Request, Response
from TheProtocols import ID
import requests

app = Frame(
    package='dev.islekcaganmert.selfdict',
    developer='islekcaganmert@hereus.net',
    administrator=True,
    secret='457a91c6727a5243ef762102d42c',
    style=requests.get('https://github.com/hereus-pbc/HereUS-UI-3.1/raw/master/HereUS-UI-3.1.json').json(),
    icon='/favicon.png',
    keywords=["Education", "Dictionary", "Decentralized"]
)


@app.route('/Languages/<language>')
def index(request: Request, language: str) -> Page:
    session: ID = ID(request.email, request.password)
    widgets = []
    dictionary = {}
    for pair in session.data.dev.islekcaganmert.selfdict()['db']:
        if pair['language'] == language:
            dictionary.update({pair['word']: pair['meaning']})
    c_letter = ''
    for word in {k: dictionary[k] for k in sorted(dictionary)}:
        if word[:1] != c_letter:
            c_letter = word[:1]
            widgets.append(Widget('h1', innertext=c_letter))
        widgets.append(Widget('p', childs=[Widget('b', innertext=f'{word}: '), dictionary[word]]))
    return Page(
        title='SelfDict',
        description='An app to track all words learned in a language. Made as a companion to language learners.',
        selector=f'body_{session.id.settings.theme_color}',
        childs=[] + widgets + [
            Widget('h1', innertext='Add a New Word'),
            Widget(
                'form',
                method='POST',
                action='/',
                childs=[
                    Widget('p', childs=[i])
                    for i in [
                        Widget(
                            'input',
                            type='text',
                            name='language',
                            style={'visibility': 'hidden', 'height': '0px', 'width': '0px'},
                            value=language
                        ),
                        Widget(
                            'input',
                            selector='textbox',
                            type='text',
                            placeholder='Word',
                            name='word',
                            style={'width': '100%'}
                        ),
                        Widget(
                            'input',
                            selector='textbox',
                            type='text',
                            placeholder='Meaning',
                            name='meaning',
                            style={'width': '100%'}
                        ),
                        Widget(
                            'input',
                            selector='button',
                            type='submit',
                            value='Add'
                        )
                    ]
                ]
            )
        ]
    )


app.run('0.0.0.0', 8000, True)