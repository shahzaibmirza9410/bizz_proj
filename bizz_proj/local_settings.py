
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'CONN_MAX_AGE': 15,
        'NAME': 'biz_buy_data',
        'USER': 'biz_bu',
        'PASSWORD': 'Bizbuy123.',
        'HOST': '104.131.69.232',
        'PORT': '3306',
    },
}
ANYMAIL = {
"MAILGUN_API_KEY": "a78bc2107d26747682830f4d4e56e369-0920befd-e8e4072b",

}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"