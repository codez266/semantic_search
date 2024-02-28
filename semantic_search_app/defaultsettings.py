from semantic_search_app.config import CONFIG

class AppConfig:
    SECRET_KEY = CONFIG.get('app', 'secret_key')
    MODEL_PATH = CONFIG.get('app', 'model_path')
    CACHE_TYPE = CONFIG.get('app', 'cache_type')
    # CACHE_DEFAULT_TIMEOUT = CONFIG.get('app', 'cache_default_timeout')
    # POLICY_ID = CONFIG.get('app', 'policy_id')
    # INFERENCE = True if int(CONFIG.get('app', 'run_inference')) == 1 else False

class DevelopmentConfig(AppConfig):
    DEBUG = True
    TESTING = True
    DATABASE = 'agent.db'
    TEMPLATES_AUTO_RELOAD = True

class TestingConfig(AppConfig):
    #DEBUG = True
    TESTING = True
    DATABASE = ':memory:'
    SECRET_KEY = 'test_key'

class ProductionConfig(AppConfig):
    TEMPLATES_AUTO_RELOAD = True
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}