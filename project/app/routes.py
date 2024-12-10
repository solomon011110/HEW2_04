from flask import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from app.models import db, User, Inventory, Contact, Product, Sale, Review, Post
from flask_login import current_user, LoginManager, UserMixin, login_user, logout_user, login_required
from functools import wraps
from app import mail, socketio
from flask_socketio import *

bp = Blueprint('main', __name__)

admin_credentials = {
    'username': '1@1',
    'password': '1'
}


def generate_verification_code():
    return str(1)


@bp.route('/')
def index():
    return render_template('home.html')

# 商品----------------------------------------------


@bp.route('/store/<int:id>')
def store(id):
    product = Product.query.get_or_404(id)
    image_url = url_for('static', filename=f'img/product/{product.id}.jpg')
    reviews = Review.query.filter(id == Review.product_id).all()
    return render_template('store.html', product=product, image_url=image_url, reviews=reviews)

@bp.route('/store/<int:product_id>/review', methods=['POST'])
@login_required
def add_review(product_id):
    title = request.form.get("title")  # カートに追加する数量を取得
    describe = request.form.get("describe")
    star = request.form.get("star")
    name = session.get('name')
    product_id_str = str(product_id)  # 商品IDを文字列として統一

    new_Review = Review(
        product_id = product_id_str,
        title = title,
        star = star,
        describe = describe,
        name = name
    )
    db.session.add(new_Review)
    db.session.commit()

    return redirect(url_for('main.store',id=product_id))


@bp.route('/search', methods=['GET', 'POST'])
def search_products():

    query = request.form.get('query')  # 検索キーワード
    category = request.form.get('category')  # カテゴリフィルタ

    # クエリを構築
    products = Product.query

    if query:  # 商品名で検索
        products = products.filter(Product.name.like(f"%{query}%"))

    if category:  # カテゴリでフィルタリング
        products = products.filter_by(category=category)

    # クエリ実行
    products = products.all()

    return render_template('kensaku.html', products=products)


@bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))  # カートに追加する数量を取得
    product = Product.query.get_or_404(product_id)  # 商品をデータベースから取得

    # セッション内のカートを取得
    cart = session.get('cart', {})

    # カートに商品を追加
    product_id_str = str(product_id)  # 商品IDを文字列として統一
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += quantity  # すでにカートに商品があれば数量を増やす
    else:
        cart[product_id_str] = {
            'product_id': product_id,
            'name': product.name,
            'price': float(product.sale_price),
            'quantity': quantity
        }  # 商品を新規追加

    session['cart'] = cart  # セッションにカート情報を保存
    flash(f"{product.name} をカートに追加しました。")
    return redirect(url_for('main.cart'))


@bp.route('/cart')
def cart():
    cart = session.get('cart', {})
    total_price = sum(float(item['price']) * item['quantity']
                      for item in cart.values())

    # カートのアイテムをテンプレート用にリスト化
    products = [
        {
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            # 小数点2位で丸める
            'total': round(float(item['price']) * item['quantity'], 2)
        }
        for item in cart.values()
    ]

    return render_template('cart.html', products=products, total_price=round(total_price, 2))


@bp.route('/kounyu', methods=['GET', 'POST'])
def kounyu():
    # セッションからカートを取得
    cart = session.get('cart', {})
    total_price = sum(float(item['price']) * item['quantity']
                      for item in cart.values())

    # カートのアイテムをテンプレート用にリスト化
    products = [
        {
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'total': round(total_price, 2)  # 小数点2位で丸める
        }
        for item in cart.values()
    ]

    if request.method == 'POST':
        email = current_user.email

        # メール本文の作成
        cart_contents = "\n".join(
            [f"""{item['name']} - {item['quantity']} 個 - 合計: {item['price']
                                                              * item['quantity']}円""" for item in cart.values()]
        )
        cart_rows = "".join(
            f"""
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd; text-align: left;">{item['name']}</td>
                <td style="padding: 10px; border: 1px solid #ddd; text-align: center;">{item['quantity']} 個</td>
                <td style="padding: 10px; border: 1px solid #ddd; text-align: right;">¥{item['price'] * item['quantity']}</td>
            </tr>
            """ for item in cart.values()
        )

        email_html = f"""
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
        </head>
        <body>
        <table style="width: 100%; border: 0; border-spacing: 0; padding: 0;">
            <tr>
                <td style="padding: 10px; background-color: #f4f4f4;">
                    <h1 style="font-family: Arial, sans-serif; color: #333;">購入確定のお知らせ</h1>
                </td>
            </tr>
            <tr>
                <td style="padding: 20px; background-color: #ffffff;">
                    <p>ご注文いただき、ありがとうございます。以下の内容でご注文が確定しました。</p>
                    <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                        <thead>
                            <tr>
                                <th style="padding: 10px; border: 1px solid #ddd; background-color: #f4f4f4; text-align: left;">商品名</th>
                                <th style="padding: 10px; border: 1px solid #ddd; background-color: #f4f4f4; text-align: center;">数量</th>
                                <th style="padding: 10px; border: 1px solid #ddd; background-color: #f4f4f4; text-align: right;">合計</th>
                            </tr>
                        </thead>
                        <tbody>
                            {cart_rows}
                        </tbody>
                    </table>
                    <p style="margin-top: 20px; font-size: 16px; font-weight: bold;">総合計: ¥{round(total_price, 2)}</p >
                </td>
            </tr>
        </table>
        </body>
        </html>
        """

        # 商品ごとに処理
        for product_key, item in cart.items():
            product_id = int(product_key)  # セッションから取得したproduct_id (キーとして使用)
            quantity = item['quantity']  # カート情報から数量を取得
            price = item['price']  # カート情報から価格を取得
            user = User.query.filter_by(email=email).first()

            # Sale レコードを追加
            new_sale = Sale(
                product_id=product_id,
                user_id=user.id,
                quantity=int(quantity),
                price=float(price)
            )
            db.session.add(new_sale)

        # コミットして変更を確定
        db.session.commit()

        # メール送信
        msg = Message(
            '注文内容確認',
            sender='hewgroup040@gmail.com',
            recipients=[email],
            html=email_html
        )
        mail.send(msg)

        # カートを空にする
        session.pop('cart', None)

        # 購入完了メッセージ
        flash('購入が完了しました！メールで注文内容を確認してください。')
        return redirect(url_for('main.index'))

    return render_template('kounyu.html', products=products, total_price=round(total_price, 2))


@bp.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    product_id_str = str(product_id)  # 商品IDを文字列として統一
    if product_id_str in cart:
        del cart[product_id_str]  # カートから商品を削除
        session['cart'] = cart
        flash('商品をカートから削除しました。')
    return redirect(url_for('main.cart'))


# ----------------------------------------------商品


# 一般アカウント----------------------------------------------


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        # Userテーブルからemailに一致するユーザを取得
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/profile')
        else:
            flash('ユーザー名またはパスワードが間違っています。')
            return redirect('/login')
    return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(
            request.form['password'], method='pbkdf2:sha256')
        # 認証コード生成
        verification_code = generate_verification_code()

        # セッションに認証コードを保存
        session['verification_code'] = verification_code
        session['email'] = email
        session['password'] = password

        # 認証コードをメールで送信
        msg = Message('Your Verification Code',
                      sender='hewgroup040@gmail.com', recipients=[email])
        msg.body = f'Your verification code is: {verification_code}'
        mail.send(msg)

        flash('認証コードがメールに送信されました。')
        return redirect(url_for('main.verify'))

    return render_template('register.html')


@bp.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        input_code = request.form['verification_code']
        stored_code = session.get('verification_code')

        if input_code == stored_code:
            flash('認証に成功しました！登録が完了しました。')
            id = session.get('id')
            email = session.get('email')
            password = session.get('password')
            # Userのインスタンスを作成
            user = User(id=id, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect("login")
        else:
            flash('認証コードが正しくありません。再試行してください。')

    return render_template('verify.html')


@bp.route('/profile')
@login_required
def profile():

    sales = db.session.query(Sale).filter(
        Sale.user_id == current_user.id).all()
    
    return render_template('profile.html', sales=sales,user=current_user)
# ----------------------------------------------一般アカウント


@bp.route('/faq', methods=['GET', 'POST'])
def faq():
    # 要DB追加
    faqs = "hoge"
    return render_template('faq.html', faqs=faqs)


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        text = request.form['text']

        contact = Contact(email=email, name=name, text=text)
        db.session.add(contact)
        db.session.commit()

        flash('お問い合わせが送信されました。')
        return redirect(url_for('home.html'))
    return render_template('contact.html')


# admin--------------------------------------------------------------
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in as an admin to access this page.')
            return redirect(url_for('main.admin_login'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 認証チェック
        if username == admin_credentials['username'] and password == admin_credentials['password']:
            session['admin_logged_in'] = True  # セッションにログイン状態を保持
            login_user(User.query.filter_by(email=username).first())
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash('Invalid username or password')  # 誤ったログイン情報でフラッシュメッセージ

    return render_template('admin_login.html')


@bp.route('/admin_logout', methods=['GET', 'POST'])
@admin_required
def admin_logout():
    session['admin_logged_in'] = False


@bp.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    # ユーザーと在庫データを取得
    users = User.query.all()
    inventories = Inventory.query.all()
    product = Product.query.all()
    sales = Sale.query.all()
    return render_template('admin_dashboard.html', name=current_user.email, users=users, inventories=inventories, product=product, sales=sales)


@bp.route('/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    if current_user.email != admin_credentials["username"]:  # 管理者のみアクセス許可
        return "アクセス権がありません", 403

    user = User.query.get(user_id)
    if user and user_id != 1:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('main.admin_dashboard'))
    return "ユーザーが見つかりません", 404


# 商品追加
@bp.route('/add_product', methods=['POST'])
@admin_required
def add_product():
    product_name = request.form.get('product_name')
    product_price = request.form.get('product_price')

    # 種類を追加
    new_product = Product(
        name=product_name,
        sale_price=product_price
    )
    db.session.add(new_product)
    db.session.commit()
    flash("商品が追加されました。")
    return redirect(url_for('main.admin_dashboard'))


# 商品更新
@bp.route('/update_product/<int:product_id>', methods=['POST'])
@admin_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        flash("指定された商品が見つかりません。")
        return redirect(url_for('main.admin_dashboard'))

    # 新しい数量を取得して更新
    new_product_name = request.form.get('new_product_name')
    new_product_price = request.form.get('new_product_price')
    # new_product_quantity = request.form.get('new_product_quantity')

    if (new_product_name):
        product.name = new_product_name
    if (new_product_price):
        product.sale_price = new_product_price
    # if(new_product_quantity):
    #     product.quantity = new_product_quantity
    db.session.commit()
    flash("商品が更新されました。")
    return redirect(url_for('main.admin_dashboard'))


# 在庫追加
@bp.route('/add_inventory', methods=['POST'])
@admin_required
def add_inventory():
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity')

    # 商品が存在するか確認
    product = Product.query.get(product_id)
    if not product:
        flash("指定された商品IDが存在しません。")
        return redirect(url_for('main.admin_dashboard'))

    # 在庫を追加
    new_inventory = Inventory(
        product_id=product_id,
        quantity=quantity,)

    db.session.add(new_inventory)
    db.session.commit()
    flash("在庫が追加されました。")
    return redirect(url_for('main.admin_dashboard'))


# 在庫削除
@bp.route('/delete_inventory/<int:inventory_id>', methods=['POST'])
@admin_required
def delete_inventory(inventory_id):
    inventory = Inventory.query.get(inventory_id)
    if not inventory:
        flash("指定された在庫が見つかりません。")
        return redirect(url_for('main.admin_dashboard'))

    db.session.delete(inventory)
    db.session.commit()
    flash("在庫が削除されました。")
    return redirect(url_for('main.admin_dashboard'))


# 在庫更新
@bp.route('/update_inventory/<int:inventory_id>', methods=['POST'])
@admin_required
def update_inventory(inventory_id):
    inventory = Inventory.query.get(inventory_id)
    if not inventory:
        flash("指定された在庫が見つかりません。")
        return redirect(url_for('main.admin_dashboard'))

    # 新しい数量を取得して更新
    new_quantity = request.form.get('quantity')
    inventory.quantity = new_quantity
    db.session.commit()
    flash("在庫が更新されました。")
    return redirect(url_for('main.admin_dashboard'))
# --------------------------------------------------------------admin






@socketio.on('new_message')
def handle_new_message(data):
    # メッセージが新しく投稿された場合の処理
    print("New message received: ", data)
    # クライアントにメッセージをブロードキャスト
    emit('message_received', data, broadcast=True)


@bp.route('/board', methods=['GET'])
def board():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('board.html', posts=posts)

# 投稿を受け取るルート
@bp.route('/post', methods=['POST'])
def post_message():
    device_id = request.cookies.get('device_id')
    content = request.form.get('content')
    if content and device_id:
        new_post = Post(device_id=device_id, content=content)
        db.session.add(new_post)
        db.session.commit()
        # 新しい投稿をSocketIOでクライアントに送信
        socketio.emit('new_message', {'content': content, 'timestamp': new_post.timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'device_id': device_id}, broadcast=True)
    return redirect('/board')

# ソケットイベント：新しいメッセージが送信された場合
@socketio.on('new_message')
def handle_new_message(data):
    # クライアントにメッセージをブロードキャスト
    emit('message_received', data, broadcast=True)
