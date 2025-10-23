from django import template
register = template.Library()  # Djangoのテンプレートタグ用ライブラリに登録するための準備

@register.filter  # カスタムフィルタとして登録（テンプレート内で使用可能になる）
def get_item(dictionary, key):
  
    return dictionary.get(key, [])
