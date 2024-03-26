Django에서 URL에 로그인 페이지를 추가하여 사용자가 특정 페이지에 접근하기 전에 로그인하도록 강제하려면, `login_required` 데코레이터를 사용하거나 미들웨어를 사용하는 방법이 있습니다. 여기서는 `login_required` 데코레이터를 사용하는 방법을 설명하겠습니다.

### `login_required` 데코레이터 사용하기

`login_required` 데코레이터는 사용자가 로그인한 상태에서만 특정 뷰에 접근할 수 있도록 제한합니다. 사용자가 로그인하지 않은 상태에서 접근하려고 하면, 설정된 로그인 URL로 리디렉션됩니다.

먼저, `login_required` 데코레이터를 사용하기 위해 필요한 모듈을 임포트합니다.

```python
from django.contrib.auth.decorators import login_required
```

그런 다음, `login_required` 데코레이터를 각 뷰 함수에 적용합니다. 함수 기반 뷰의 경우 데코레이터를 직접 적용할 수 있지만, 클래스 기반 뷰의 경우 `LoginRequiredMixin`을 사용하거나 `method_decorator`를 사용하여 데코레이터를 적용할 수 있습니다.

여기서는 함수 기반 뷰를 예시로 들겠습니다.

```python
# adminviews.py 내의 각 뷰 함수에 login_required 적용

@login_required
def concert(request):
    # 뷰 로직
    pass

@login_required
def addconcert(request):
    # 뷰 로직
    pass

@login_required
def privacyConsent(request):
    # 뷰 로직
    pass

@login_required
def gatheringPlace(request, name):
    # 뷰 로직
    pass

@login_required
def pricing(request, name):
    # 뷰 로직
    pass
```

이렇게 `login_required` 데코레이터를 적용하면, 사용자가 로그인하지 않은 상태에서 이러한 URL에 접근하려고 할 때 로그인 페이지로 리디렉션됩니다.

### 로그인 URL 설정

`login_required` 데코레이터가 리디렉션하는 로그인 페이지의 URL은 `settings.py` 파일에서 `LOGIN_URL` 설정을 통해 지정할 수 있습니다.

```python
# settings.py

LOGIN_URL = '/your_login_url/'
```

`/your_login_url/` 부분을 실제 로그인 페이지의 URL로 변경하세요. 이 설정을 통해 사용자가 로그인이 필요한 페이지에 접근하려 할 때 설정된 로그인 URL로 리디렉션됩니다.

---

Django에서 login_required 데코레이터나 LoginRequiredMixin을 사용할 때, Django의 기본 인증 시스템이 세션 및 사용자 인증을 처리합니다. 사용자가 로그인할 때, Django는 사용자의 세션을 생성하고 관리하며, 이 세션을 통해 사용자가 로그인한 상태인지 판단합니다. 따라서 별도로 세션 또는 토큰 관리를 구현할 필요가 없습니다.

사용자 인증 처리
Django의 기본 인증 시스템은 사용자 ID와 비밀번호를 기반으로 인증을 처리합니다. Django의 User 모델을 사용하여 사용자 정보를 저장하고 관리할 수 있습니다. 사용자가 로그인할 때는 주로 authenticate와 login 함수를 사용합니다.

사용자 인증 예시
다음은 사용자가 로그인 폼을 통해 ID와 비밀번호를 입력하고 로그인하는 과정의 예시입니다.

```python
from django.contrib.auth import authenticate, login

def my_login_view(request):
    if request.method == 'POST':
        # 로그인 폼으로부터 'username'과 'password'를 받아옵니다.
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # authenticate 함수를 사용하여 사용자 인증을 시도합니다.
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # 사용자가 존재하고 비밀번호가 맞다면 로그인 처리를 합니다.
            login(request, user)
            # 성공적으로 로그인 처리 후 리디렉션할 페이지로 이동합니다.
            return redirect('desired_page_after_login')
        else:
            # 인증 실패 시, 로그인 폼으로 다시 리디렉션하고 오류 메시지를 표시할 수 있습니다.
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
```
이 예시에서는 사용자가 로그인 폼을 통해 제출한 ID와 비밀번호를 받아 authenticate 함수를 사용해 인증을 시도합니다. 인증에 성공하면 login 함수를 호출하여 사용자를 로그인 시키고, 원하는 페이지로 리디렉션합니다. 인증에 실패하면 에러 메시지와 함께 로그인 페이지를 다시 보여줄 수 있습니다.

---

Django의 인증 시스템은 `django.contrib.auth.models`에 있는 `User` 모델을 사용하여 사용자 정보를 관리합니다. `User` 모델은 Django에서 제공하는 기본 사용자 모델로, 사용자의 계정 정보와 관련된 다양한 필드를 포함하고 있습니다. 여기에는 사용자의 ID, 비밀번호, 이메일 주소, 이름 등이 포함됩니다.

### `User` 모델의 주요 필드:

- **`username`**: 사용자의 고유한 식별자로 사용되는 필드입니다. 일반적으로 사용자 이름이 이 필드에 저장됩니다.
- **`password`**: 사용자의 비밀번호를 저장하는 필드입니다. Django는 비밀번호를 평문으로 저장하지 않고, 안전한 해시 알고리즘을 사용하여 해시된 형태로 저장합니다.
- **`email`**: 사용자의 이메일 주소를 저장하는 필드입니다.
- **`first_name`** 및 **`last_name`**: 사용자의 이름을 저장하는 필드입니다. 이들은 필수가 아닌 선택적 필드입니다.
- **`is_active`**, **`is_staff`**, **`is_superuser`**: 사용자의 계정 상태와 권한을 관리하는 데 사용되는 불리언(Boolean) 필드입니다. 예를 들어, `is_superuser`가 `True`인 사용자는 관리자 권한을 가지며, Django의 관리 사이트에 접근할 수 있습니다.

### 비밀번호 관리:

Django는 사용자의 비밀번호를 안전하게 관리하기 위해 비밀번호 해싱을 사용합니다. 이는 사용자의 비밀번호를 평문으로 저장하는 대신, 해시 함수를 사용하여 변환된 값을 저장함을 의미합니다. 해싱은 단방향 프로세스이므로, 저장된 해시값으로부터 원본 비밀번호를 복구하는 것은 계산상 불가능합니다.

Django는 `set_password` 메서드를 사용하여 비밀번호를 해싱하고 저장합니다. 사용자 객체를 생성하거나 비밀번호를 변경할 때 이 메서드를 사용하여 비밀번호를 안전하게 처리해야 합니다.

```python
from django.contrib.auth.models import User

# 사용자 객체 생성
user = User.objects.create_user(username='myusername', email='myemail@example.com')
user.set_password('mypassword')  # 비밀번호를 해싱하여 저장
user.save()
```

### 사용자 인증:

Django는 `authenticate` 함수를 사용하여 사용자 인증을 처리합니다. 이 함수는 사용자 이름과 비밀번호를 인자로 받아, 해당 사용자가 유효한지 확인합니다. 유효한 사용자인 경우 `User` 객체를 반환하고, 그렇지 않은 경우 `None`을 반환합니다.

```python
from django.contrib.auth import authenticate

# 사용자 인증 시도
user = authenticate(username='myusername', password='mypassword')
if user is not None:
    # 인증 성공: user 객체 사용
    pass
else:
    # 인증 실패 처리
    pass
```

Django의 인증 시스템을 사용하면 사용자 계정 관리와 비밀번호 보안을 손쉽게 처리할 수 있으며, 이는 웹 애플리케이션의 보안을 강화하는 데 기여합니다.