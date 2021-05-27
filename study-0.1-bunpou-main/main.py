# STEP1
name1 = "ねずこ"
name2 = "ぜんいつ"
print(f'{name1}と{name2}は仲間です')

# STEP2
name2 = "むざん"

if name2 == "むざん":
    print('仲間ではありません')

# STEP3
name = ["たんじろう","ぎゆう","ねずこ","むざん"]
name.append("ぜんいつ")

# STEP4
for i in name:
    print(i)

# STEP5
def func():
    print(name1)
func()

# STEP6
def test(hikisuu):
    if hikisuu in name:
        print(f'{hikisuu}は含まれます')

name3 = "ぎゆう"
test(name3)
