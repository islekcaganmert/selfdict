from bevyframe import Request, Page, Widget, Response, redirect
from TheProtocols import ID


def post(request: Request) -> Response:
    session: ID = ID(request.email, request.password)
    db = session.data.dev.islekcaganmert.selfdict
    new_pair = {'language': request.form['language'], 'word': request.form['word'], 'meaning': request.form['meaning']}
    mirr: dict[str, list] = db()
    if new_pair not in mirr['db']:
        mirr['db'].append(new_pair)
        db(mirr)
    return redirect(f'/Languages/{request.form['language']}')


def get(request: Request) -> (Page, Response):
    if request.email.split('@')[0] == 'Guest':
        return redirect('/Login.py')
    else:
        session: ID = ID(request.email, request.password)
        languages = []
        db = session.data.dev.islekcaganmert.selfdict
        if db() == {}:
            db({'db': []})
        for pair in db()['db']:
            if pair['language'] not in languages:
                languages.append(pair['language'])
        return Page(
            title='SelfDict',
            description='An app to track all words learned in a language. Made as a companion to language learners.',
            selector=f'body_{session.id.settings.theme_color}',
            childs=[
                Widget('p', childs=[i])
                for i in [
                    Widget(
                        'div',
                        childs=[
                            Widget('img', src=session.id.profile_photo, style={
                                'height': '50px',
                                'border-radius': '50%',
                                'float': 'right'
                            })
                        ]
                    )
                ] + [
                    Widget(
                        'a',
                        href=f'/Languages/{i}',
                        childs=[
                            Widget(
                                'button',
                                selector='button',
                                innertext=i
                            )
                        ]
                    )
                    for i in languages
                ] + [
                    Widget('h1', innertext='Add a New Language'),
                    Widget(
                        'form',
                        method='POST',
                        childs=[
                            Widget('p', childs=[i])
                            for i in [
                                Widget(
                                    'input',
                                    selector='textbox',
                                    type='text',
                                    placeholder='Language',
                                    name='language',
                                    style={'width': '100%'}
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
            ]
        )
