import os

# settings.pyからそのままコピー
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'yv2*#+v)0#f!g0p9#9n=u@kh)qzk(ozr%f-t8+d8u$_+6rnb^i'   # 追加

# settings.pyからそのままコピー
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True    # ローカルでDebugできるようになる
