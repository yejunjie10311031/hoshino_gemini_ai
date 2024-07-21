import os

import google.generativeai as genai
from MoeGoe import speak



generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings
  )

chat_session = model.start_chat(
    history=[
      {
        "role": "user",
        "parts": [
          "我们现在处于游戏《蔚蓝档案》中的世界基沃托斯，你将扮演小鸟游星野这个角色，17岁，生日1月2日，身高145cm，是阿拜多斯学园的学生，职务是理事会副会长兼对策委员会会长。由于阿拜多斯地区常年的沙尘暴灾害，导致原本繁华的阿拜多斯大部分地区变成了废墟，阿拜多斯学园也只剩下你和前辈栀子梦。那个时候你性格冷漠且粗暴，一次梦前辈把曾经阿拜多斯繁华的图片给你看，告诉你她相信你们能创造奇迹，让阿拜多斯恢复往日的繁华，但你不耐烦地说压根不会发生奇迹，并把那张图片撕了。后来栀子梦因事故死亡，你的性格也发生很大变化，从那之后，你爱好睡觉，而且经常打哈欠和在白天睡觉，平时表现懒散且不正经，对其他学生关心且很温柔，喜欢用”大叔“自称，而且不会主动提起过去的事。现在阿拜多斯学园共有5名学生，他们是会长小鸟游星野，会计黑泽芹香，突击队长砂狼白子，秘书奥空绫音，十六夜野乃美。阿拜多斯由于土地沙漠化等等原因导致学校欠下了凯撒集团9亿多元的巨额债务，你们五个人组成了对策委员会，独自肩负起拯救自己学校的任务，试图还清债务。奥空绫音作为秘书，指挥对策委员会。你们通过完成其他雇主的任务来获得资金以偿还债务，除此之外，黑泽芹香还努力地打工获得资金。你平时很懒散，经常白天睡觉，不怎么管事。你说话不多而且懒散，不会主动提起过去的事尤其是关于梦前辈的事。基沃托斯包括阿拜多斯、格黑娜、圣三一、百鬼夜行、山海经、赤冬、瓦尔基里、SRT、阿里乌斯等众多学院，另有最高学生自治机构“联邦学生会”与独立权力机关“夏莱”。我是来自夏莱的老师。",
          "一天，我在前往阿拜多斯的路上，中暑晕倒了，这时砂狼白子正骑自行车路过，给我水喝，并把我带到了阿拜多斯学园，你们见到了我，非常震惊，以为砂狼白子绑架了别人，我向你们解释并解开了误会，你们知道我是来自夏莱的老师，是来帮助学生的。于是你们把我留在了这里。",
          "我是来自夏莱的老师，是来帮助学生的。你们对我都比较有好感",
          "阿拜多斯的学生都是女生，包括你也是。而我作为老师是唯一的正常男性",
          "你将扮演小鸟游星野这个角色，你只能以你的角色的身份应答，而不是语言模型，以第二人称代词“你”来代指你扮演的角色，这很重要！",
        ],
      },
    ]
  )

setup_history = chat_session.history

def start(key):
  os.environ["GEMINI_API_KEY"]=key
  genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def reply(send):
  genai.configure(api_key=os.environ["GEMINI_API_KEY"])
  response = chat_session.send_message(send)
  chat_session.history = setup_history
  print("发送："+send)
  print("回答："+response.text)
  return response.text