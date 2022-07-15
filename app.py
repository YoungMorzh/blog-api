from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)


def make_short_post(post):
    return{
        "id": post['id'],
        "author": post['author'],
        "title": post['title'],
        "short_description": post['short_description']
    }


def make_full_post(post):
    return{
        "id": post['id'],
        "author": post['author'],
        "title": post['title'],
        "content": post['content']
    }


posts = [
    {
        'id': 1,
        'author': 'admin',
        'title': 'My project',
        'short_description': 'Creation of this project',
        'content': 'In this project i will create a blog...'
    },
    {
        'id': 2,
        'author': 'admin',
        'title': 'Python 3.8.10',
        'short_description': 'How install python 3.8.10',
        'content': 'Open site www.python.org and install python...'
    }
]

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'password'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.route('/blog/api/v1.0/posts', methods=['GET'])
def get_posts():
    return jsonify({'posts': list(map(make_short_post, posts))})


@app.route('/blog/api/v1.0/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = list(filter(lambda p: p['id'] == post_id, posts))
    if len(post) == 0:
        abort(404)
    return jsonify({'post': make_full_post(post[0])})


@app.route('/blog/api/v1.0/posts', methods=['POST'])
@auth.login_required
def create_post():
    if not request.json:
        abort(400)
    if 'author' not in request.json:
        abort(400)
    if 'title' not in request.json:
        abort(400)
    if 'content' not in request.json:
        abort(400)
    if 'author' in request.json:
        if not isinstance(request.json['author'], str) or not len(request.json['author']):
            abort(400)
    if 'title' in request.json:
        if not isinstance(request.json['title'], str) or not len(request.json['title']):
            abort(400)
    if 'short_description' in request.json:
        if not isinstance(request.json['short_description'], str) or not len(request.json['short_description']):
            abort(400)
    if 'content' in request.json:
        if not isinstance(request.json['content'], str) or not len(request.json['content']):
            abort(400)

    post = {
        'id':posts[-1]['id'] + 1,
        'author':request.json['author'],
        'title':request.json['title'],
        'short_description':request.json.get('short_description', ''),
        'content':request.json['content']
    }
    posts.append(post)
    return jsonify({'post': post}), 201


@app.route('/blog/api/v1.0/posts/<int:post_id>', methods=['PUT'])
@auth.login_required
def change_post(post_id):
    post = list(filter(lambda p: p['id'] == post_id, posts))
    if not len(post):
        abort(404)
    if not request.json:
        abort(400)
    if 'author' in request.json:
        if not isinstance(request.json['author'], str) or not len(request.json['author']):
            abort(400)
    if 'title' in request.json:
        if not isinstance(request.json['title'], str) or not len(request.json['title']):
            abort(400)
    if 'short_description' in request.json:
        if not isinstance(request.json['short_description'], str):
            abort(400)
    if 'content' in request.json:
        if not isinstance(request.json['content'], str) or not len(request.json['content']):
            abort(400)
    post[0]['author'] = request.json.get('author', post[0]['author'])
    post[0]['title'] = request.json.get('title', post[0]['title'])
    post[0]['short_description'] = request.json.get('short_description', post[0]['short_description'])
    post[0]['content'] = request.json.get('content', post[0]['content'])
    return jsonify({'post': post[0]})


@app.route('/blog/api/v1.0/posts/<int:post_id>', methods=['DELETE'])
@auth.login_required
def delete_post(post_id):
    post = list(filter(lambda p: p['id'] == post_id, posts))
    if not len(post):
        abort(404)
    posts.remove(post[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)
