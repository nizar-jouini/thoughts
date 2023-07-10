from flask_app.config.mysqlconnection import connectToMySQL, DB
from flask import flash
from flask_app.models.user import User

class Post:

    def __init__(self, data):
        self.id = data['id']
        self.post = data['post']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.users_who_liked = []
        self.user_ids_who_liked = []

    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM posts JOIN users AS creators ON posts.user_id = creators.id
        LEFT JOIN likes ON posts.id = likes.post_id
        LEFT JOIN users AS users_who_liked ON users_who_liked.id = likes.user_id
        ORDER BY posts.id;
        """

        results = connectToMySQL(DB).query_db(query)
        
        posts = []
        for row in results:
            new_post = True
            users_who_liked_dict = {
                'id': row['users_who_liked.id'],
                'first_name': row['users_who_liked.first_name'],
                'last_name': row['users_who_liked.last_name'],
                'email': row['users_who_liked.email'],
                'password': row['users_who_liked.password'],
                'created_at': row['users_who_liked.created_at'],
                'updated_at': row['users_who_liked.updated_at'],
            }
            
            number_of_posts = len(posts)

            if number_of_posts > 0:
                last_post = posts[number_of_posts - 1]
                if last_post.id == row['id']:
                    last_post.users_who_liked.append(User(users_who_liked_dict))
                    last_post.user_ids_who_liked.append(users_who_liked_dict['id'])
                    new_post = False

            if new_post:
                post = cls(row)
                user_dict = {
                    'id': row['creators.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['creators.created_at'],
                    'updated_at': row['creators.updated_at'],
                }
                post.user = User(user_dict)
                if row['users_who_liked.id']:
                    post.users_who_liked.append(User(users_who_liked_dict))
                    post.user_ids_who_liked.append(users_who_liked_dict['id'])
                posts.append(post)
            
        return posts
    
    @classmethod 
    def get_by_id(cls, data):
        query = "SELECT * FROM posts JOIN users ON users.id = posts.user_id WHERE users.id = %(id)s;"
        
        results = connectToMySQL(DB).query_db(query, data)
       
        posts = []
        for row in results:
            post = cls(row)
            user_dict = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
            post.user = User(user_dict)
            posts.append(post)
        return posts

    @classmethod
    def create(cls, data):
        query = "INSERT INTO posts (post, user_id) VALUES (%(post)s, %(user_id)s);"
        results = connectToMySQL(DB).query_db(query , data)
        return results
    
    @classmethod 
    def delete(cls, data):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def get_likes(cls, data):
        query = "SELECT COUNT(*) AS likes FROM likes WHERE post_id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        print(results[0]['likes'])
        return results[0]['likes']

    @staticmethod
    def validation(post):
        is_valid = True
        if len(post['post']) < 5:
            flash("name must be at least 5 characters!","post")
            is_valid = False
        return is_valid
    
    @classmethod 
    def delete_like(cls, data):
        query1 = "SELECT * FROM likes WHERE post_id = %(post_id)s"
        result = connectToMySQL(DB).query_db(query1, data)
        print('--'*50)
        print(result[0])
        data = {
            'user_id' : result[0]['user_id'],
            'post_id' : result[0]['post_id']
        }
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND post_id = %(post_id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def add_like(cls, data):
        query = "INSERT INTO likes (user_id, post_id) VALUES (%(user_id)s, %(post_id)s);"
        results = connectToMySQL(DB).query_db(query, data)
        return results



