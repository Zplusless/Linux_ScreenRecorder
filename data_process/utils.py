import pickle
from functools import wraps
import os
import logging

def memorize(filename):
    """
    装饰器 保存函数运行结果
    :param filename: 缓存文件位置
    
    Example:
        @memorize('cache/square')
        def square(x):
            return x*x
    
    Todo:
        判断参数是否相同时有坑
    """

    def _memorize(func):
        @wraps(func)
        def memorized_function(*args, **kwargs):
            key = pickle.dumps(args[1:])

            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    cached = pickle.load(f)
                    f.close()
                    if isinstance(cached, dict) and cached.get('key') == key:
                        logging.info(
                            msg='Found cache:{0}, {1} does not have to run'.format(filename, func.__name__))
                        return cached['value']

            value = func(*args, **kwargs)
            with open(filename, 'wb') as f:
                cached = {'key': key, 'value': value}
                pickle.dump(cached, f)
                f.close()
            return value

        return memorized_function

    return _memorize