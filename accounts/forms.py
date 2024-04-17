from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()  # こっちで先に変数代入する！


class SignupForm(UserCreationForm):
    class Meta:
        model = User  # model = get_user_model() は NG
        fields = ("username", "email")


# password1, password2というフィールドはUserCreationFormの方で設定されているため、
# fieldsの欄には、Userモデルの中にある、
# blankにはできない値であるusernameとemailをセットする。


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # 全てのフォームの部品のclass属性に「form-control」を指定（bootstrapのフォームデザインを利用するため）
            field.widget.attrs["class"] = "form-control"
            # 全てのフォームの部品にpaceholderを定義して、入力フォームにフォーム名が表示されるように指定。
            field.widget.attrs["placeholder"] = field.label
