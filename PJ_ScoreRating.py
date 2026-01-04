import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import csv
import datetime as dt
dtn=dt.datetime.now()


root=tk.Tk()
root.title("プロセカ達成率計算ソフト")
root.geometry("640x360")
root.configure(bg="#E4F7F7")
root.option_add("*Label.background", "#E4F7F7")


def calc(per, gre, goo, bad, mis,title):
    score=per*3+gre*2+goo
    theo=(per+gre+goo+bad+mis)*3
    # print(f"Rate: {score/theo*100 }")
    return score/theo*100

def clear_fields():
    txt0.delete(0, tk.END)
    txt1.delete(0, tk.END)
    txt2.delete(0, tk.END)
    txt3.delete(0, tk.END)
    txt4.delete(0, tk.END)
    txt5.delete(0, tk.END)





def main(): #旧getcalc
    diff = combobox.get()
    title = txt0.get().strip()
    if not title:
        messagebox.showerror("入力エラー", "曲名を入力してください")
        return
    try:
        per = int(txt1.get() or 0)
        gre = int(txt2.get()or 0)
        goo = int(txt3.get()or 0)
        bad = int(txt4.get()or 0)
        mis = int(txt5.get()or 0)
        if goo == 0 and bad == 0 and mis == 0:
            if gre==0:
                fcap.config(text="APしました！")
            else:
                fcap.config(text="FCしました！")
        else:
           fcap.config(text="")

    except ValueError:
        messagebox.showerror("入力エラー", "数値をすべて入力してください")
        return
    
    # lb6.config(text=f"楽曲：{title}")
    lb6.config(text="記録しました")
    lb7.config(text=f"達成率：{calc(per, gre, goo, bad, mis,title):.4f}%")
    

    #以下DB保存
    dtn = dt.datetime.now()
    today = dtn.strftime("%Y/%m/%d %H:%M")
    new_rate = calc(per, gre, goo, bad, mis, title)
    old_best=None

    try:
        with open("scores.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)

            same = [
            row for row in reader
            if len(row) >= 3 and row[1] == title and row[2] == diff
            ]

            if same:
                old_best = max(float(row[3]) for row in same)

    except FileNotFoundError:
        pass
    lb_update.config(text="")

    if old_best is not None and new_rate > old_best:
        diff_rate = new_rate - old_best
        lb_update.config(text=f"{diff_rate:.4f}%更新しました！")



    
    with open("scores.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)


        #保存内容の更新はこちらから
        writer.writerow([today,title, diff,calc(per, gre, goo, bad, mis,title)])

#DB検索
def search_score():
    title = txt8.get().strip()
    diff = combobox2.get()

    if not title:
        messagebox.showerror("入力エラー", "検索する曲名を入力してください")
        return

    try:
        with open("scores.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)

            records = [row for row in reader if row[1] == title and row[2] == diff]

            if not records:
                lb9.config(text="前回記録日：なし")
                lb11.config(text="達成率：なし")
                messagebox.showinfo("検索結果", "その楽曲の達成率はまだ記録されていません")
                return

            best = max(records, key=lambda row: float(row[3]))   # 最良の行

            date = best[0]
            diff2=best[2]
            rate = float(best[3])

            lb9.config(text=f"前回記録日：{date}")
            lb10.config(text=f"難易度：{diff2}")
            lb11.config(text=f"達成率：{rate:.4f}%")

    except FileNotFoundError:
        messagebox.showerror("エラー", "まだ記録ファイルがありません")
        return


#musictitle
lb0=tk.Label(text="曲名：")
lb0.place(x=30,y=30)
txt0=tk.Entry(width=20)
txt0.place(x=90,y=30)

#difficulty
lb0_1=tk.Label(text="難易度：")
lb0_1.place(x=30,y=55)
combobox = ttk.Combobox(root, height=3,values=["APPEND", "MASTER", "EXPERT","HARD","NORMAL", "EASY"],state="readonly")
combobox.place(x=90, y=55)   
combobox.current(0)

#perfect
lb1 = tk.Label(text='Perfect：')
lb1.place(x=30, y=80)
txt1= tk.Entry(width=20)
txt1.place(x=90, y=80)

#great
lb2=tk.Label(text='Great：')
lb2.place(x=30,y=100)
txt2=tk.Entry(width=20)
txt2.place(x=90, y=100)

#good
lb3=tk.Label(text='Good：')
lb3.place(x=30,y=120)
txt3=tk.Entry(width=20)
txt3.place(x=90, y=120)

#bad
lb4=tk.Label(text='Bad：')
lb4.place(x=30,y=140)
txt4=tk.Entry(width=20)
txt4.place(x=90, y=140)

#miss
lb5=tk.Label(text='Miss：')
lb5.place(x=30,y=160)
txt5=tk.Entry(width=20)
txt5.place(x=90, y=160)

bt1=tk.Button(text="計算",command=main)
bt1.place(x=90,y=185)

bt2=tk.Button(text="クリア",command=clear_fields)
bt2.place(x=177,y=185)


#以下結果表示

lb6 = tk.Label(text="楽曲：")
lb6.place(x=30, y=220)

lb7 = tk.Label(text="達成率：")
lb7.place(x=30, y=240)

lb_update = tk.Label(text="")
lb_update.place(x=30, y=260)

fcap=tk.Label(text="")
fcap.place(x=30,y=280)


#以下DB検索
lb8=tk.Label(text="楽曲を検索：")
lb8.place(x=270,y=50)
txt8=tk.Entry(width=20)
txt8.place(x=350,y=50)

lb8_1=tk.Label(text="難易度：")
lb8_1.place(x=270,y=75)
combobox2 = ttk.Combobox(root, height=3,values=["APPEND", "MASTER", "EXPERT","HARD","NORMAL", "EASY"],state="readonly")
combobox2.place(x=330, y=75)   
combobox2.current(0)



lb9=tk.Label(text="前回記録日：")
lb9.place(x=270,y=100)

lb10=tk.Label(text="難易度：")
lb10.place(x=270,y=120)

lb11=tk.Label(text="達成率：")
lb11.place(x=270,y=140)

bt3=tk.Button(text="検索",command=search_score)
bt3.place(x=480,y=45)

lb11=tk.Label(text="※楽曲名は完全一致でのみヒットするので打ち間違いにご注意ください",bg="#E4F7F7")
lb11.place(x=270, y=25)


root.mainloop()
