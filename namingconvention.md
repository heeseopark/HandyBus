# Django 프로젝트 명명 규칙 (GPT 추천)

## Python 파일

- **모델(Model)**: 클래스 이름은 카멜 케이스(CamelCase)를 사용하며 단수형을 사용합니다. 예: `UserProfile`, `BlogPost`
- **뷰(View)**: 함수 기반 뷰는 스네이크 케이스(snake_case)를 사용하며, 클래스 기반 뷰는 카멜 케이스(CamelCase)를 사용합니다. 예: `login_view`, `ProfileUpdateView`
- **폼(Form)**: 폼 클래스 이름은 카멜 케이스를 사용하며, 모델 이름 뒤에 `Form`을 붙입니다. 예: `UserCreationForm`, `BlogPostForm`
- **URLconf**: URL 패턴 이름은 스네이크 케이스를 사용하며, 가능한 명확하게 지어야 합니다. 예: `login`, `blog_post_detail`
- **템플릿(Template)**: 템플릿 파일 이름은 소문자와 언더스코어를 사용하며, 기능이나 앱 이름을 기반으로 명명합니다. 예: `login.html`, `blog_post_detail.html`

## HTML 파일

- **템플릿 파일**: HTML 템플릿 파일은 소문자와 언더스코어를 사용합니다. 기능이나 페이지의 이름을 반영합니다. 예: `user_profile.html`, `blog_list.html`
- **ID와 클래스 이름**: HTML 요소의 ID와 클래스 이름은 소문자와 하이픈을 사용하는 케밥 케이스(kebab-case)를 사용합니다. 예: `navbar`, `blog-post`

## JavaScript 파일

- **파일 이름**: JavaScript 파일 이름은 소문자와 언더스코어를 사용합니다. 기능이나 사용되는 페이지의 이름을 반영합니다. 예: `form_validation.js`, `blog_detail.js`
- **변수와 함수 이름**: 변수와 함수 이름은 소문자로 시작하며, 여러 단어를 연결할 때는 카멜 케이스(camelCase)를 사용합니다. 예: `validateForm`, `fetchUserData`
