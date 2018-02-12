### Prepare development environment 

1. Build Python-Nose docker to run test
```bash
docker build -t python_gilded_rose .
```

2. When image is ready to run attach working directory and run docker container
```bash
docker run -v "$(pwd)":/usr/src/app -i -t python_gilded_rose /bin/bash
```

#### Running test

In docker container, run the nose test
```bash
nosetests
```

#### Running text test fixture

In docker container, run the nose test
```bash
python texttest_fixture.py
```