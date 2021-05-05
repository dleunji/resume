# Resume Generator
[![Run on Ainize](https://ainize.ai/images/run_on_ainize_button.svg)](https://master-resume-dleunji.endpoint.ainize.ai/)<br>

![resumes](https://user-images.githubusercontent.com/46207836/117151072-af060e80-adf3-11eb-9ccd-ddf585fe8c1a.jpg)
만약 취업이나 이직을 준비하고 계시다면 **résumé** 쓰기는 피할 수 없습니다. résumé에는 지금까지의 자신만의 이력과 성취에 대해서 단 한 장에 간결하게 설명해야 합니다. 지금까지 코드와 고군분투하며 살아왔지만, 막상 résumé를 쓰려면 무얼, 어떻게 쓸지 막막해지기 쉽습니다.

이처럼 코드 짜기보다 자신을 소개하는 글쓰기가 더 어려운 개발자들을 위해, **Teachable NLP**를 통해 résumé를 편리하게 생성하는 모델을 만들었습니다. 실제로 단 몇 분만에 제 résumé는 다음과 같이 완성되었습니다. 

```
- Creating Web RESTful API
- Web Frontend with HTML, CSS
- Taking part in preprocessing steps of machine learning mainly missing value treatment, outlier detection, encoding, scaling, feature selection.
- Testing machine learn algorithms in python. optimizing of existing algorithms.
```

막상 처음부터 이러한 웹 서비스를 만드려고 하면 막막한 경우가 많습니다. 사실 많은 기능이 필요한 것이 아니라, 입력에 따른 출력만 나오는 간단한 웹 페이지 하나면 충분한데 말이죠.

그러한 분들을 위한 오픈소스 **Opyrator**를 소개해드립니다. 🥳

```
What is Opyrator?
Turns your machine learning code into microservices with web API, interactive GUI, and more.
🦾  Turn functions into production-ready services within seconds.
🔌  Auto-generated HTTP API based on **FastAPI**.
🌅  Auto-generated Web UI based on **Streamlit**.
📦  Save and share as self-contained executable file or Docker image.
🧩  Reuse pre-defined components & combine with existing Opyrators.
📈  Instantly deploy and scale for production usage.
```

[Opyrator](https://github.com/ml-tooling/opyrator)는 단 몇 줄로 이루어진 Python functions를 통해 단번에 간단한 서비스로 변신시켜줍니다. 이는 API를 매우 빠르게 빌드하는 강점을 지닌 **[FASTAPI](https://fastapi.tiangolo.com/)** 와 Machine Learning에 특화되어 시각적으로 편리하게 보여주는 **[Streamlit](https://streamlit.io/)** 기반으로 구성된 오픈소스입니다.

<img width="1552" alt="_2021-04-30__5 42 57" src="https://user-images.githubusercontent.com/46207836/116836686-7226f580-ac02-11eb-8489-281f799bbeb7.png">

게다가 FastAPI는 별도로 Swagger를 작성하지 않아도 API documentation를 Swagger UI 형식으로 자동으로 생성해냅니다.

![index-03-swagger-02](https://user-images.githubusercontent.com/46207836/116836726-9f73a380-ac02-11eb-866f-07796c93df22.png)

이처럼 놀라운 기능을 지닌 두 프레임워크를 합친 Opyrator는 어떻게 작동하는지 상세히 알아보겠습니다.

## 1. Brainstorming

저는 기존에 Teachable NLP로 만든 모델 [Résumé For SW Developer](https://forum.ainetwork.ai/t/teachable-nlp-resume-for-sw-developers/89/2) 을 활용하여 서비스를 만들어 보고자 합니다. text와 원하는 출력 길이를 입력하면 해당 text를 중심으로 3개의 후보 문장이 출력되어, 그 중 마음에 드는 문장을 고를 수 있도록 합니다.

<img width="1552" alt="_2021-05-01__7 58 11" src="https://user-images.githubusercontent.com/46207836/116836762-c92cca80-ac02-11eb-9cb9-44a700af596f.png">

## 2. Installation

```bash
pip install opyrator
```

위 명령을 통해 opyrator에 필요한 fastapi, streamlit 이외에 머신러닝에 주로 사용되는 많은 패키지가 자동 다운로드 됩니다. 이 점을 감안하여 **가상환경을 구축**한 후 위 명령어를 실행할 것을 추천드립니다.

## 3. Directory

단 하나의 Python 파일로, 하나의 함수로 구성되어있기 때문에 구조는 아래와 같이 간단합니다.

```
├────resume
    ├ app.py
    ├ requirements.txt
    ├ .dockerignore
    ├ .gitignore
    ├ Dockerfile
```

## 4. Models

Opyrator는 FastAPI를 기반에 두고, FastAPI는 Pydantic Model에 기반을 두어서 [Pydantic](https://pydantic-docs.helpmanual.io)  모델과 유사한  형식으로 입력과 출력을 관리합니다. Pydantic은 파이썬 3.6 이상에서 지원되고, Type Hints를 사용함으로써 코드에 자료형을 명시하고, 데이터 유효성 검사를 가능케 합니다. 모든 모델은 Pydantic의 BaseModel을 상속하고, 기본적으로 아래와 같이 사용됩니다.

```python
from pydantic import BaseModel

class Foo(BaseModel):
    count: int
    size: float = None

class Bar(BaseModel):
    apple = 'x'
    banana = 'y'
```

Opyrator에서는 이 점을 활용하여 입력과 출력에 대한 class를 만들 수 있습니다. 저는 text_input 1개와 출력하고 싶은 길이인 length를 입력받아, text 3개를 출력하고자 하여 아래와 같이 작성하였습니다.  아래의 사항들에 주의를 기울이며 코드를 작성합니다.

✅ 별도의 Field function의 title을 명시하지 않는 이상 변수명이 자동으로 필드명으로 설정됩니다.

✅ 만약, title필드를 별도로 지정하지 않아 변수명이 필드명으로 부여될 경우에는 변수명의 가장 첫 문자는 대문자로 나타납니다.

✅ 띄어쓰기는 _(under bar)로 구현 가능합니다.

```python
from pydantic import BaseModel, Field

class TextGenerationInput(BaseModel):
    text_input : str = Field(
        ...,
        title = "Text Input"
        description = "The input text to use as basis to generate resume.",
        max_length = 30,
    )
    length : int = Field(
        10,
        title = "Length"
        description="The length of the sequence to be generated.",
        ge=5,
        le=50,
    )

class TextGenerationOutput(BaseModel):
    output_1 : str
    output_2 : str
    output_3 : str
```

TextGenerationInput을 통해 입력을, TextGenerationOutput을 통해 출력을 정의하였습니다. 그 중 [Field](https://pydantic-docs.helpmanual.io/usage/schema/#field-customisation) function으로 더 세부적으로 데이터를 지정할 수 있습니다. 위의 모델의 필드에 대해 간단히 설명드리자면,

- **...** (ellipsis) :  해당 필드가 필수적(required)
- **title** : 필드명을 지정해준다. 만약 생략되면 `field_name.title()` 이 사용됩니다.
- **description** : description을 별도로 지정하면, opyrator에서 물음표 아이콘을 통해 해당 필드에 대한 안내를 제공
- **max_length** : 텍스트의 최대 길이를 지정
- **ge** : 해당 값의 최대값
- **le** : 해당 값의 최소값
- **default**  : 초기값

![요소](https://user-images.githubusercontent.com/46207836/116836845-127d1a00-ac03-11eb-8485-deca3e3e9776.png)

![field](https://user-images.githubusercontent.com/46207836/116836850-232d9000-ac03-11eb-9c41-37823f3e076e.png)

해당 입력들을 통하여 아래와 같이 세 텍스트가 출력됩니다.

<img width="802" alt="_2021-05-01__7 47 04" src="https://user-images.githubusercontent.com/46207836/116836880-422c2200-ac03-11eb-8671-b5bd28c5cafe.png">

## 5. Function

generate_resume의 함수로 위의 Models를 연결합니다. `parameter`로 input Model을 명시하고, `→`으로 output Model을 명시합니다. 이 때, dot(.)으로 각 모델의 필드에 접근할 수 있습니다. (e.g. input.text_input,  input.length) 그 과정에 쓰이는 Text Generation API는 [여기](https://www.notion.so/GPT2-Ghostwriter-Kant-d4dc01c4cfad4a70a12c11083a3666ef)를 참고하시길 바랍니다.

![diagram](https://user-images.githubusercontent.com/46207836/116836904-57a14c00-ac03-11eb-99da-1f648adc1dc3.png)

```python
def generate_resume(input: TextGenerationInput)-> TextGenerationOutput:
    """Generate Résumé based on a given prompt. And choose one of the best sentences. """
    encoded = autoTokenizer.encode(input.text_input)
    data = {
        'text' : encoded,
        'length' : input.length,
        'num_samples' : 3
    }
    response = requests.post(url, data = json.dumps(data) , headers = {"Content-Type":'application/json; charset=utf-8'})
    if response.status_code == 200:
        text = dict()
        res = response.json()
        for idx, output in enumerate(res):
            text[idx] = autoTokenizer.decode(res[idx], skip_special_tokens = True)
        return TextGenerationOutput(output_1 = text[0], output_2 = text[1], output_3 = text[2])
    else:
        return TextGenerationOutput(output_1 = response.status_code)
```



## 5. Docker

위 과정을 거쳐 서비스는 모두 만들었으니 이를 배포하기 위해 Dockerfile만으로 웹 서비스를 배포할 수 있는 [ainize](https://ainize.ai/dleunji/resume?branch=master)를 활용하고자 합니다. ainize에 업로드하기 전 Dockefile을 아래와 같이 제작하였습니다.

```docker
FROM tensorflow/tensorflow:1.15.5-gpu-py3
RUN mkdir -p /app
WORKDIR /app
COPY . .
RUN apt-get update && \\
    apt-get install -y
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["opyrator", "launch-ui", "app:generate_resume"]
```

- `FROM` : ainize는 GPU환경을 제공하므로 빠른 문장 생성을 위해 GPU 환경의 tensorflow를 base image로 사용합니다.

- `RUN` : requirements.txt에 언급된 대로 pip 패키지를 설치합니다.

  문장 생성에 필요한 requests, transformers와 opyrator, watchdog을 설치하였습니다.

- `EXPOSE` : opyrator는 8501 port를 default로 사용하기 때문입니다.

- `CMD` : opyrator run 명령어입니다. 구조는 `opyrator launch-ui 실행파일명:실행함수` 입니다.

  - 만약 swagger UI를 위한 페이지로 접근하기 위해서는 `opyrator launch-api 실행파일명:실행함수` 를 실행합니다.

Dockerfile을 모두 작성했다면 Dockerfile을 Build하고 Run합니다.

- `Build` : docker build -t resume(image)
- `Run` : docker run -it -p 8501:8501 resume:latest(image)

Chrome 브라우저에서 `0.0.0.0:8501` 로 접속하면 아래와 같이 성공적으로 opyrator가 작동하는 것을 볼 수 있습니다.

- Safari 등 타 브라우저에서는 작동되지 않을 수 있습니다.

<img width="1552" alt="_2021-05-01__7 58 11" src="https://user-images.githubusercontent.com/46207836/116836762-c92cca80-ac02-11eb-9cb9-44a700af596f.png">

## 6. Swagger

ainize에 업로드할 경우 해당 사이트의 API를 업로드하여 브라우저에 상관없이 resume 생성 서비스를 체험하고, 해당 API로 또다른 서비스를 창출해낼 수 있습니다.

이를 위해선 아까와 다르게 `launch-ui`가 아니라 `launch-api`로 run해야 합니다.

(만약 가상환경을 docker container로 하셨다면 `EXPOSE 8080`으로 변경해야합니다.)

```bash
opyrator launch-api app:generate_resume
```

아래와 같은 화면에서 API를 직접 테스트하고, `./openapi.jso` 을 클릭하면 Swagger 원문을 확인할 수 있습니다.

![_2021-05-03__11 16 34](https://user-images.githubusercontent.com/46207836/116836976-96370680-ac03-11eb-800c-1e97f9f14dc1.png)

아래 내용을 swagger.json으로 저장 후 ainize에 업로드한다면, 위와 동일하게 API를 [ainize](https://ainize.ai/dleunji/resume?branch=master)에서도 테스트하실 수 있습니다. 

![_2021-05-03__11 20 43](https://user-images.githubusercontent.com/46207836/116837006-b1097b00-ac03-11eb-8fe1-cb0b008f7c3d.png)

## 7. Wrap Up

[opyrator](https://github.com/ml-tooling/opyrator)는 그동안 본인만의 API를 개발하고, 서비스를 개발하여도 웹사이트를 만들어야 한다는 부담감에 망설였던 개발자들에게 매우 유용한 오픈소스라고 생각합니다. 현재 opyrator 개발자께 직접 여쭤본 결과 꾸준히 기능을 추가하고 계시다고 하니, 앞으로 더욱 유용해질 것이라 기대됩니다.

저처럼 Teachable NLP와 ainize로 서비스를 간단하게 만들어, [포럼](https://forum.ainetwork.ai/c/ai-showcase/11)에서 여러분의 아이디어와 실력보여주세요:)

![_2021-05-03__10 12 40](https://user-images.githubusercontent.com/46207836/116837045-ced6e000-ac03-11eb-8788-871899cde0ef.png)

