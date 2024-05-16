from bevyframe import Request, Page, Widget, Response, redirect
from TheProtocols import ID, CredentialsDidntWorked


def post(request: Request) -> (Page, Response):
    try:
        ID(request.form['email'], request.form['password'])
        resp: Response = redirect('/')
        resp.login(request.form['email'], request.form['password'])
        return resp
    except CredentialsDidntWorked:
        return get(request, 'Credentials Didn\'t Worked')


def get(request: Request, message: str = None) -> (Page, Response):
    if request.email.split('@')[0] != 'Guest':
        return redirect('/')
    else:
        return Page(
            title='Login - SelfDict',
            description='An app to track all words learned in a language. Made as a companion to language learners.',
            selector='body_blank',
            childs=[
                Widget(
                    'div',
                    selector='the_box',
                    style={
                        'margin': 'auto',
                        'width': 'max-content',
                        'text-align': 'center',
                        'margin-top': 'calc(50vh - 225px)'
                    },
                    childs=[
                        Widget('h1', innertext='Login'),
                        Widget(
                            'form',
                            method='POST',
                            childs=[
                                Widget('p', childs=[i])
                                for i in [
                                    Widget(
                                        'input',
                                        type='email',
                                        name='email',
                                        selector='textbox',
                                        placeholder='Email Address'
                                    ),
                                    Widget(
                                        'input',
                                        type='password',
                                        name='password',
                                        selector='textbox',
                                        placeholder='Password'
                                    ),
                                ] + [('' if message is None else message)] + [
                                    Widget(
                                        'input',
                                        type='submit',
                                        selector='button',
                                        value='Login'
                                    )
                                ]
                            ]
                        )
                    ]
                )
            ]
        )
