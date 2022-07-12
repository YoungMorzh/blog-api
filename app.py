from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)


posts = [
    {
        'id': 1,
        'author': 'admin',
        'title': 'My project',
        'short description': 'Creation of this project',
        'content': 'In this project i will create a blog...'
    },
    {
        'id': 2,
        'author': 'admin',
        'title': 'Python 3.8.10',
        'short description': 'How install python 3.8.10',
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
    return jsonify({'posts': posts})


@app.route('/blog/api/v1.0/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = list(filter(lambda p: p['id'] == post_id, posts))
    if len(post) == 0:
        abort(404)
    return jsonify({'post': post[0]})


@app.route('/blog/api/v1.0/posts', methods=['POST'])
@auth.login_required
def create_post():
    if not request.json or 'author' not in request.json:
        abort(400)
    if not isinstance(request.json['author'], str) or not len(request.json['author']):
        abort(400)
    if not isinstance(request.json['title'], str) or not len(request.json['title']):
        abort(400)
    if not isinstance(request.json['short description'], str) or not len(request.json['short description']):
        abort(400)
    if not isinstance(request.json['content'], str) or not len(request.json['content']):
        abort(400)

    post = {
        'id': posts[-1]['id'] + 1,
        'author': request.json['author'],
        'title': request.json['title'],
        'short description': request.json['short description'],
        'content': request.json['content']
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
    if not isinstance(request.json['title'], str) or not len(request.json['title']):
        abort(400)
    if not isinstance(request.json['short description'], str) or not len(request.json['short description']):
        abort(400)
    if not isinstance(request.json['content'], str) or not len(request.json['content']):
        abort(400)
    post[0]['title'] = request.json.get('title', post[0]['title'])
    post[0]['short description'] = request.json.get('short description', post[0]['short description'])
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
