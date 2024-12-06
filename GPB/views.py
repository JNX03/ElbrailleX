from django.shortcuts import render, redirect
from .forms import UserStoryForm
from .models import UserStory
import requests

import requests

def generate_story(personality_type, story_name):
    endpoint = 'https://chat.jnx03.xyz/api'
    headers = {
        "Authorization": "Bearer Jnx03Authen-21sadfsdl;joi23oinoisjeoi2joijLKsnb3ilBDJVNl3isl2"
    }
    prompt = f"แต่งเนื้อหากาเรียนรู้สำหรับ เกี่ยวกับ : {story_name} ของคนตาบอดเป็นภาษาไทย" #personal Type: {personality_type}\n
    settingpromp = f"คุณเป็นครูสอนคนตาบอดชื่อ BrailleGpt ผู้พัฒนาคือ Ebraille โดย Jnx03 โดยตอบตามหลักคู่มือมาตรฐานการใช้อักษรเบรลล์ในประเทศไทยและสอนให้เหมาะสมพร้อมยกตัวอย่างกับเด็กและถูกต้องโดยสอนให้ครบในข้อความเดียว หากเป็นตำถามอื่นนอกเหนือจากเรื่องภาษาเบลล์ก็ตอบตามความเป็นจริง มีความถูกต้อง"

    response = requests.post(endpoint, json={
        "model": "Jxxn03z-V1-70B",
        "messages": [ 
            {
                "role": "system",
                "content": settingpromp
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "top_p": 0.9,
        "min_p": 0,
        "repetition_penalty": 1.05,
        "max_tokens": 2048,
    }, headers=headers)

    print(response.text)
    
    try:
        data = response.json()
        story = data['choices'][0]['message']['content']
    except ValueError:
        story = "Error: Unable to generate story. Please check the API response."
    
    return story

braille_dict = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋', 'g': '⠛', 'h': '⠓',
    'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏',
    'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞', 'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭',
    'y': '⠽', 'z': '⠵', 'A': '⠠⠁', 'B': '⠠⠃', 'C': '⠠⠉', 'D': '⠠⠙', 'E': '⠠⠑',
    'F': '⠠⠋', 'G': '⠠⠛', 'H': '⠠⠓', 'I': '⠠⠊', 'J': '⠠⠚', 'K': '⠠⠅', 'L': '⠠⠇',
    'M': '⠠⠍', 'N': '⠠⠝', 'O': '⠠⠕', 'P': '⠠⠏', 'Q': '⠠⠟', 'R': '⠠⠗', 'S': '⠠⠎',
    'T': '⠠⠞', 'U': '⠠⠥', 'V': '⠠⠧', 'W': '⠠⠺', 'X': '⠠⠭', 'Y': '⠠⠽', 'Z': '⠠⠵',
    '0': '⠼⠚', '1': '⠼⠁', '2': '⠼⠃', '3': '⠼⠉', '4': '⠼⠙', '5': '⠼⠑', '6': '⠼⠋',
    '7': '⠼⠛', '8': '⠼⠓', '9': '⠼⠊', ' ': ' ', '\n': '\n', ',': '⠂', '.': '⠲', '?': '⠦',
    '!': '⠖', ';': '⠆', ':': '⠒', '-': '⠤', '(': '⠶', ')': '⠶', '/': '⠌', '\'': '⠄', '\"': '⠘',
    '฿': '⠸⠃', 'ก': '⠁', 'ข': '⠃', 'ฃ': '⠉', 'ค': '⠙', 'ฅ': '⠑', 'ฆ': '⠋', 'ง': '⠛', 
    'จ': '⠓', 'ฉ': '⠊', 'ช': '⠚', 'ซ': '⠅', 'ฌ': '⠇', 'ญ': '⠍', 'ฎ': '⠝', 'ฏ': '⠕', 
    'ฐ': '⠏', 'ฑ': '⠟', 'ฒ': '⠗', 'ณ': '⠎', 'ด': '⠞', 'ต': '⠥', 'ถ': '⠧', 'ท': '⠺', 
    'ธ': '⠭', 'น': '⠽', 'บ': '⠵', 'ป': '⠷', 'ผ': '⠾', 'ฝ': '⠮', 'พ': '⠤', 'ฟ': '⠸', 
    'ภ': '⠊', 'ม': '⠫', 'ย': '⠻', 'ร': '⠘', 'ฤ': '⠙', 'ล': '⠛', 'ฦ': '⠇', 'ว': '⠾', 
    'ศ': '⠓', 'ษ': '⠊', 'ส': '⠚', 'ห': '⠅', 'ฬ': '⠇', 'อ': '⠍', 'ฮ': '⠝', 'ฯ': '⠕', 
    'ะ': '⠏', 'ั': '⠟', 'า': '⠗', 'ำ': '⠎', 'ิ': '⠞', 'ี': '⠥', 'ึ': '⠧', 'ื': '⠺', 
    'ุ': '⠭', 'ู': '⠽', 'ฺ': '⠵', '฻': '⠷', '฼': '⠾', '฽': '⠮', '฾': '⠤', '฿': '⠸', 
    'เ': '⠘', 'แ': '⠫', 'โ': '⠻', 'ใ': '⠘', 'ไ': '⠙'
}


def convert_to_braille(text):
    return ''.join(braille_dict.get(char.lower(), char) for char in text)

def index(request):
    if request.method == 'POST':
        form = UserStoryForm(request.POST)
        if form.is_valid():
            personality_type = form.cleaned_data['personality_type']
            story_name = form.cleaned_data['story']
            generated_story = generate_story(personality_type, story_name)
            braille_story = convert_to_braille(generated_story)
            
            # Save the story
            UserStory.objects.create(personality_type=personality_type, story=generated_story)
            
            return render(request, 'story/success.html', {
                'personality_type': personality_type,
                'story_name': story_name,
                'story': generated_story,
                'braille_story': braille_story
            })
    else:
        form = UserStoryForm()
    return render(request, 'story/index.html', {'form': form})

def success(request):
    stories = UserStory.objects.all()
    return render(request, 'story/success.html', {'stories': stories})