from flask import Flask, jsonify
from threading import Thread
import os, random

app = Flask('')


@app.route('/')
def home():
  return "I'm alive"


@app.route('/api/generate/<string:roomname>/<int:mode>')
def generate_number(roomname, mode):
  room_result = open(f'./DB/roomDB/{roomname}(number).txt', 'w')
  if mode == 1:
    room_result.write(str(random.randint(1, 25)))
  elif mode == 2:
    room_result.write(str(random.randint(1, 50)))
  elif mode == 3:
    room_result.write(str(random.randint(1, 100)))

  return jsonify({"result": "success!"})


@app.route('/api/number/<string:roomname>')
def number(roomname):
  room_result = open(f'./DB/roomDB/{roomname}(number).txt', 'r')
  number_file = room_result.readlines()
  number_list = []
  for line in number_file:
    line = line.strip()
    number_list.append(line)

  return jsonify({"number": number_list[0]})


@app.route('/api/makeroom/<string:roomname>/<string:roomps>/<string:nickname>')
def makeroom(roomname, roomps, nickname):
  if os.path.isfile(f"./DB/roomDB/{roomname}.txt") == True:
    return jsonify({"result": "Already exsisting room name"})
  room_player = open(f'./DB/roomDB/{roomname}.txt', 'w')
  room_player.write(roomps + '\n' + nickname + '\n')
  room_player.close()
  return jsonify({"result": "success!"})


@app.route('/api/joinroom/<string:roomname>/<string:roomps>/<string:nickname>')
def joinroom(roomname, roomps, nickname):
  if os.path.isfile(f"./DB/roomDB/{roomname}.txt") == False:
    return jsonify({"result": "Room does not exist"})
  room_player = open(f'./DB/roomDB/{roomname}.txt', 'r')
  players = room_player.readlines()
  player_list = []
  for line in players:
    line = line.strip()
    player_list.append(line)

  if player_list[0] == roomps:
    room_player.close()
    room_player = open(f'./DB/roomDB/{roomname}.txt', 'a')
    room_player.write('\n' + nickname)
    room_player.close()
    return jsonify({"result": "success!"})
  else:
    return jsonify({"result": "Wrong password"})


@app.route('/api/signup/<string:id>/<string:password>/<string:nickname>',
           methods=['GET'])
def signup(id, password, nickname):
  id_list = []
  id_file = open("./DB/id.txt", 'r')
  ids = id_file.readlines()
  for line in ids:
    line = line.strip()
    id_list.append(line)
  if id in id_list:
    return jsonify({"result": "Already existing ID"})
  else:
    id_file.close()
    id_file = open("./DB/id.txt", 'a')
    id_file.write(id + "\n")
    password_file = open("./DB/password.txt", 'a')
    password_file.write(password + "\n")
    user_file = open(f"./DB/userDB/{id}.txt", 'w')
    user_file.write(nickname + "\n" + "0\n" + "0")
    user_file.close()
    return jsonify({"result": "success!"})


@app.route('/api/login/<string:id>/<string:password>', methods=['GET'])
def login(id, password):
  id_list = []
  ps_list = []

  id_file = open("./DB/id.txt", 'r')
  ids = id_file.readlines()
  for line in ids:
    line = line.strip()
    id_list.append(line)

  password_file = open("./DB/password.txt", 'r')
  passwords = password_file.readlines()
  for line in passwords:
    line = line.strip()
    ps_list.append(line)
  detail_list = []
  user_file = open(f"./DB/userDB/{id}.txt", 'r')
  detail = user_file.readlines()
  for line in detail:
    line = line.strip()
    detail_list.append(line)
  id_wichi = id_list.index(id)
  try:
    ps_wichi = ps_list.index(password)
  except:
    return jsonify({"result": "Wrong password"})
  if id_wichi == ps_wichi:
    return jsonify({
      "result": "success!",
      "nickname": detail_list[0],
      "win": detail_list[1],
      "lose": detail_list[2]
    })


@app.route('/api/win/<string:id>/<string:nickname>/<string:roomname>',
           methods=['GET'])
def win(id, nickname, roomname):
  detail_list = []
  user_file = open(f"./DB/userDB/{id}.txt", 'r')
  detail = user_file.readlines()
  for line in detail:
    line = line.strip()
    detail_list.append(line)
  user_file.close()
  user_file = open(f"./DB/userDB/{id}.txt", 'w')
  win = int(detail_list[1]) + 1
  lose = int(detail_list[2])
  user_file.write(nickname + "\n" + f"{win}\n" + f"{lose}")
  player_file = open(f'./DB/roomDB/{roomname}.txt', 'w')
  player_file.write("done")
  player_file.close()
  return jsonify({"result": "success!!"})


@app.route('/api/lose/<string:id>/<string:nickname>/<string:roomname>',
           methods=['GET'])
def lose(id, nickname, roomname):
  detail_list = []
  user_file = open(f"./DB/userDB/{id}.txt", 'r')
  detail = user_file.readlines()
  for line in detail:
    line = line.strip()
    detail_list.append(line)
  user_file.close()
  user_file = open(f"./DB/userDB/{id}.txt", 'w')
  win = int(detail_list[1])
  lose = int(detail_list[2]) + 1
  user_file.write(nickname + "\n" + f"{win}\n" + f"{lose}")
  player_file = open(f'./DB/roomDB/{roomname}.txt', 'w')
  player_file.write("done")
  player_file.close()
  return jsonify({"result": "success!!"})


@app.route('/api/players/<string:roomname>/<string:roomps>')
def players(roomname, roomps):
  room_player = open(f'./DB/roomDB/{roomname}.txt', 'r')
  players = room_player.readlines()
  player_list = []
  for line in players:
    line = line.strip()
    player_list.append(line)
  player_list.remove(roomps)

  return jsonify({"result": player_list})


@app.route('/api/update/<float:version>')
def update(version):
  version_file = open('version.txt', 'r')
  version_file_read = version_file.readlines()
  version_list = []
  for line in version_file_read:
    line = line.strip()
    version_list.append(line)

  if float(version_list[0]) > float(version):
    return jsonify({"result": "There is a new update"})
  else:
    return jsonify({"result": "This is the lastest version"})


def run():
  app.run(host='0.0.0.0', port=7000)


t = Thread(target=run)
t.start()
