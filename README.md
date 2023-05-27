# CI/CD Architecture

![architecture](https://github.com/ohjinseo/wihao-bot/assets/62508156/2c25801f-bdad-411e-866c-153934519f2a)

> 1. Github Actions을 사용하여 Docker Image 빌드 및 S3에 업로드
>
> - Github master 브랜치에 코드가 push되면, Github Actions 워크 플로우가 트리거 된다.
> - 이 워크 플로우에서는 Docker 이미지를 빌드하고, 이미지 전송을 위해 tar 파일로 저장한다.
> - tar 파일을 S3 버킷에 업로드 한다. <br /> <br />
>
> 2. AWS Lambda와 AWS IoT Core
>
> - 새 Docker 이미지가 S3에 업로드되면, AWS Lambda 함수가 트리거 된다.
> - Lambda 함수에서는 AWS IoT Core MQTT 프로토콜을 이용해 NAT 환경의 라즈베리파이에게 메시지를 보낸다. <br /><br />
>
> 3. 라즈베리파이에서의 실행
>
> - 라즈베리파이는 AWS IoT Core에서 메시지를 받는다.
> - 메시지를 받으면, S3에서 새 Docker Image를 받고 이 이미지를 로드하고 컨테이너를 실행한다.
