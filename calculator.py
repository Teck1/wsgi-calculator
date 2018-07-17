"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
#import traceback


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    try:
        total = sum(list(map(int, args)))
    except ValueError:
        return "Please enter numeric values for the calculation."
    return str(total)

def divide(*args):
    """ Returns a STRING with the first arg in the list divided by the second arg"""
    try:
        total = int(args[0]) / int(args[1])
    except ValueError:
        return "Please enter numeric values for the calculation."
    except ZeroDivisionError:
        return "Nice try. No dividing by zero. You know the rules."
    return str(total)

def multiply(*args):
    """ Returns a STRING with the first arg in the list multiplied by the second arg"""
    try:
        total = int(args[0]) * int(args[1])
    except ValueError:
        return "Please enter numeric values for the calculation."
    return str(total)

def subtract(*args):
    try:
        total = int(args[0]) - sum(list(map(int, args[1:])))
    except ValueError:
        return "Please enter numeric values for the calculation."
    return str(total)


def instruct(*args):
    page = """
    <h1>Simple Calculator</h1><br>
    <p><b>Usage:</b><br><br>
        ADD: takes a list of operands <br>
            &emsp;http://host:port/add/&ltop1&gt/&ltop2&gt/.../&ltopn&gt <br>
            &emsp;ex: <br>
            &emsp;http://host:8080/add/5/4/3/2/1 <br>
            &emsp;returns 15 <br><br>
        SUBTRACT: takes a list of operands <br>
            &emsp;http://host:port/subtract/&ltop1&gt/&ltop2&gt/.../&ltopn&gt <br>
            &emsp;ex: <br>
            &emsp;http://host:8080/subtract/10/5/4/4 <br>
            &emsp;returns -3 <br><br>
        MULTIPLY: takes only 2 operands <br>
            &emsp;http://host:port/multipy/&ltop1&gt/&ltop2&gt <br>
            &emsp;ex: <br>
            &emsp;http://host:8080/multiply/10/2 <br>
            &emsp;returns 20 <br><br>
        DIVIDE: takes only 2 operands <br>
            &emsp;http://host:port/divide/&ltop1&gt/&ltop2&gt <br>
            &emsp;ex: <br>
            &emsp;http://host:8080/divide/10/5 <br>
            &emsp;returns 2.0 <br><br>
    </p>
    """
    return page

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {
        '': instruct,
        'add': add,
        'subtract': subtract,
        'divide': divide,
        'multiply': multiply,
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    if not len(args) >= 2:
        func = funcs['']

    return func, args


def application(environ, start_response):

    headers = [('Content-type', 'text/html')]
    body = ""
    status = ""
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
        # print(traceback.format_exc())
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>"
        # print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
