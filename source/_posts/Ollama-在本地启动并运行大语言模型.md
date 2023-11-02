---
layout: layout
title: 一键部署: Ollama在本地启动并运行大语言模型
date: 2023-11-02 15:13:38
tags:
---

```
> docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

```
Unable to find image 'ollama/ollama:latest' locally
latest: Pulling from ollama/ollama
aece8493d397: Pull complete
4eca1ad9be6c: Pull complete
fcd9fc6db2c0: Pull complete
Digest: sha256:871505ffb1050381f75875a645e7b24c37e1436fc51b915fd91a8ed202583e3b
Status: Downloaded newer image for ollama/ollama:latest
e8291c35ef1f8414f9b8ab008bc3c3523cb7881ad96ccf60745fffb5916e2d9e
> docker exec -it ollama ollama run llama2
pulling manifest
pulling 22f7f8ef5f4c... 100% |█████████████████████████████████| (3.8/3.8 GB, 29 MB/s)
pulling 8c17c2ebb0ea... 100% |███████████████████████████████████| (7.0/7.0 kB, 3.2 kB/s)
pulling 7c23fb36d801... 100% |███████████████████████████████████| (4.8/4.8 kB, 2.0 kB/s)
pulling 2e0493f67d0c... 100% |████████████████████████████████████████| (59/59 B, 27 B/s)
pulling 2759286baa87... 100% |██████████████████████████████████████| (105/105 B, 45 B/s)
pulling 5407e3188df9... 100% |█████████████████████████████████████| (529/529 B, 163 B/s)
verifying sha256 digest
writing manifest
removing any unused layers
success
```

> what's your name?

I'm just an AI, I don't have a personal name. My purpose is to assist and provide information to users like you through text-based conversations. How may I help you today?

> 你叫什么？

I'm just an AI, I don't have a personal name. My purpose is to assist and provide information to users like you through text-based conversations. How may I help you today?

> 请帮我写一段自我介绍，我是一个python     后端程序员

Sure, here's a simple self-introduction for a Python developer:

"Hi there! My name is [Your Name], and I'm a Python developer with [Number of Years] years of experience. I specialize in developing web applications, data analysis, and machine learning models using Python. I'm passionate about solving complex problems and creating innovative solutions using my technical skills. In my free time, I enjoy learning new technologies and sharing knowledge with the developer community. Let's connect and work together on exciting projects!"

>  /?

Available Commands:
  /set         Set session variables
  /show        Show model information
  /bye         Exit
  /?, /help    Help for a command

Use `"""` to begin a multi-line message.

> /show

Available Commands:
  /show license      Show model license
  /show modelfile    Show Modelfile for this model
  /show parameters   Show parameters for this model
  /show system       Show system prompt
  /show template     Show prompt template

>  我现在是在命令 行进行输入，怎么才能 输入多行呢？

Great, you want to input multiple lines of text! In the command line, you can input multiple lines by pressing the `Enter` key after each line. For example:

1. `My name is John.`
2. `I'm a Python developer with 5 years of experience.`
3. `I specialize in developing web applications and data analysis using Python.`
4. `In my free time, I enjoy learning new technologies and sharing knowledge with the developer community.`

After each line, press the `Enter` key to move on to the next line. When you're finished, you can press `Ctrl+D` to exit the command prompt.

> 可以帮我写一个python的冒泡排序吗？`

Of course! Here is an example of a simple bubble sort algorithm written in Python:
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
```
This algorithm takes an array as input and sorts it using the bubble sort algorithm. It works by repeatedly iterating over the array, comparing adjacent elements, and swapping them if they are in the wrong order. The `range()` function is used to generate the loop indices for the iteration.

Here's an example of how you could use this function:
```python
arr = [5, 2, 7, 3, 1, 4]
print(bubble_sort(arr))
```
This would output the sorted array `[1, 2, 3, 4, 5, 7]`.

Keep in mind that this is a very basic implementation of bubble sort, and it has a time complexity of O(n^2), which means it can take a long time to sort large arrays. There are more efficient algorithms for sorting large arrays, such as quicksort or mergesort.

> 你可以用中文回答我吗？

Of course! I can answer in Chinese if you'd like. Here is the same information in Chinese:
```python
def 泡沫排序(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
```
请使用以上函数来排序一个数组。例如：
```python
arr = [5, 2, 7, 3, 1, 4]
print(泡沫排序(arr))
```
这将输出排序后的数组 `[1, 2, 3, 4, 5, 7]`.

