import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import flask_cors
import re  # Regex modülü

app = Flask(__name__)

# CORS'u uygulamaya dahil ediyoruz
flask_cors.CORS(app)  # Bu şekilde tüm domainlere izin verir. Belirli domainler için de yapılandırılabilir.

bcrypt = Bcrypt(app)

# MySQL veritabanı bağlantısı
db_config = {
    'host': 'localhost',
    'user': 'root',  # Veritabanı kullanıcı adınızı yazın
    'password': '1234',  # Veritabanı şifrenizi yazın
    'database': 'login_service'
}

# Veritabanı bağlantısı
try:
    connection = mysql.connector.connect(**db_config)
    print("Veritabanına başarıyla bağlanıldı!")
    connection.close()
except mysql.connector.Error as err:
    print(f"Veritabanına bağlanılamadı: {err}")

# JWT için gizli anahtar
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
jwt = JWTManager(app)


# Ana Sayfa Endpoint
@app.route('/')
def home():
    return 'Welcome to the Login Microservice!'


# Kullanıcı Kaydı Endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    emailaddress = data.get('emailaddress')

    if not username or not password or not emailaddress:
        return jsonify({'message': 'Kullanıcı adı, şifre ve e-posta adresi gereklidir!'}), 400

    # E-posta regex doğrulaması
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, emailaddress):
        return jsonify({'message': 'Geçersiz e-posta adresi formatı!'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    connection = None
    cursor = None  # Başlangıçta None olarak tanımlayın
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Kullanıcı adı kontrolü
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            return jsonify({'message': 'Bu kullanıcı adı zaten alınmış!'}), 409

        # E-posta adresi kontrolü
        cursor.execute("SELECT * FROM users WHERE emailaddress = %s", (emailaddress,))
        user_email = cursor.fetchone()
        if user_email:
            return jsonify({'message': 'Bu e-posta adresi zaten kullanılıyor!'}), 409

        # Yeni kullanıcıyı ekle
        cursor.execute(
            "INSERT INTO users (username, password, emailaddress) VALUES (%s, %s, %s)",
            (username, hashed_password, emailaddress)
        )
        connection.commit()
        return jsonify({'message': 'Kullanıcı başarıyla kaydedildi!'}), 201

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

    finally:
        # Eğer cursor veya connection None değilse, kapatmaya çalışın
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Kullanıcı Giriş Endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Kullanıcı adı ve şifre gereklidir!'}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        print(user)

        if not user or not bcrypt.check_password_hash(user['PASSWORD'], password):
            return jsonify({'message': 'Geçersiz kullanıcı adı veya şifre!'}), 401

        access_token = create_access_token(identity={'username': username})
        return jsonify({'access_token': access_token}), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route('/getUserID', methods=['POST'])
def getUserID():
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({'message': 'Kullanıcı gereklidir!'}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        print(user)

        return jsonify({'userID': user}), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

        @app.route('/getUserID', methods=['POST'])
        def getUserID():
            data = request.json
            username = data.get('username')

            if not username:
                return jsonify({'message': 'Kullanıcı gereklidir!'}), 400

            try:
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                print(user)

                return jsonify({'userID': user}), 200

            except mysql.connector.Error as err:
                return jsonify({'error': str(err)}), 500
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

@app.route('/getUsername', methods=['POST'])
def getUsername():
    data = request.json
    userID = data.get('userID')

    if not userID:
        return jsonify({'message': 'Kullanıcı gereklidir!'}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT username FROM users WHERE id = %s", (userID,))
        user = cursor.fetchone()
        print(user)

        return jsonify({'userName': user}), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

        # Korunan Endpoint (JWT gerektirir)


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({'message': 'Bu korunan bir endpointtir!'})


if __name__ == '__main__':
    app.run(debug=True)
