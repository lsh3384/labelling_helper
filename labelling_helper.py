from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import os
import glob
import shutil

class Labelling:
    def __init__(self):

        #변수 선언
        self.prev_path = ""
        self.new_path = ""

        #--화면 UI 설정--
        self.root = Tk()
        self.root.title("Labelling")
        self.root.geometry("540x250+100+100")
        self.root.resizable(False, False)

        self.lbl0 = Label(self.root, text="---------------------- 사용법 ----------------------")
        self.lbl0.pack()

        self.lbl1 = Label(self.root, text="라벨링 텍스트 파일이 있는 곳을 지정하고 시작버튼을 누르세요.")
        self.lbl1.pack(pady=10)


        #이전 폴더 선택 버튼
        self.frame1 = Frame(self.root)                      # frame 생성
        self.frame1.pack(fill=X)

        self.btn1 = Button(self.frame1, text="기존데이터 위치", command=self.ask_previous_path, width=20)    # 버튼 생성
        self.btn1.pack(side=LEFT, padx=10, pady=5)

        self.txt1 = Label(self.frame1, bg="white")          # 주소 표시될 라벨 설정(배경 흰색으로)
        self.txt1.pack(fill=X, padx=10, expand=True)


        #저장할 폴더 선택 버튼
        self.frame2 = Frame(self.root)                      # frame 생성
        self.frame2.pack(fill=X)

        self.btn2 = Button(self.frame2, text="저장위치(numerate경우)", command=self.ask_new_path, width=20)         # 버튼 생성
        self.btn2.pack(side=LEFT, padx=10, pady=5)

        self.txt2 = Label(self.frame2, bg="white")          # 주소 표시될 라벨 설정(배경 흰색으로)
        self.txt2.pack(fill=X, padx=10, expand=True)


        # 콤보박스
        self.str = StringVar()
        self.Combo1 = ttk.Combobox(textvariable=self.str, width=20)
        self.Combo1['value'] = ("annotation", "numerate")
        self.Combo1.current(0)
        self.Combo1.pack(pady=10)

        # annotation, numerate 버튼
        self.Click_button = Button(text="시작", command=self.button_click)
        self.Click_button.pack(pady=10)

        self.root.mainloop()


    def button_click(self):
        print(self.str.get())
        if (self.str.get() == "annotation"):
            print("라벨링 텍스트 수정")
            self.annotation_modify()
        elif(self.str.get() == "numerate"):
            print("파일 순번 정리")
            self.numerate()
        else:
            print("콤보박스를 정해주세요.")


    def ask_previous_path(self):
        # self.root.dirName = filedialog.askdirectory()
        self.prev_path = filedialog.askdirectory()
        # root.file = filedialog.askopenfile(initialdir='path', title='select file', filetypes=(('jpeg files', '*.jgp'), ('all files', '*.*')))
        print(self.prev_path)
        # print(self.root.dirName)
        self.txt1.configure(text=self.prev_path)

    def ask_new_path(self):
        # self.root.dirName = filedialog.askdirectory()
        self.new_path = filedialog.askdirectory()
        # root.file = filedialog.askopenfile(initialdir='path', title='select file', filetypes=(('jpeg files', '*.jgp'), ('all files', '*.*')))
        print(self.new_path)
        # print(self.root.dirName)
        self.txt2.configure(text=self.new_path)

    def annotation_modify(self):
        if (self.prev_path == ""):
            print("폴더 위치를 지정하세요.")
            messagebox.showinfo("Error!", "폴더 위치를 지정하세요.")
            return
        annotation_txt_files = glob.glob(f"{self.prev_path}/*.txt")
        for i in annotation_txt_files:
            f = open(i, "r")                    #텍스트 파일을 연다
            content = f.readline()              #텍스트 파일 내용을 읽어온다
            content_split = content.split(" ")  #텍스트파일을 스페이스를 기준으로 나눠서 리스트로 만든다
            content_split[0] = "0"              #클래스로 지정하는 첫번째 값이 15로 되어있는 것을 0으로 바꾼다
            print(content_split)                #내용이 잘 들어갔는지 프린트해본다
            f2 = open(i, "w")                   #같은 이름으로 파일을 만든다
            f2.write(" ".join(content_split))   #빈칸을 기준으로 파일 내용을 넣는다
            print(" ".join(content_split))      #내용을 프린트해본다.

    def numerate(self):
        if (self.prev_path=="" or self.new_path == ""):
            if(self.prev_path==""):
                print("폴더 위치를 지정하세요.")
                messagebox.showinfo("error", "이전 폴더 위치를 지정하세요.")
                return
            elif(self.new_path==""):
                print("폴더 위치를 지정하세요.")
                messagebox.showinfo("error", "새로운 폴더 위치를 지정하세요.")
                return
        images_list = glob.glob(f"{self.prev_path}/*.jpg")     #폴더의 이미지들만 추출해서 리스트를 만든다
        print("hello")
        oldPath = self.prev_path                              #이미지 경로를 지정한다.
        length = int(len(os.listdir(oldPath)) / 2)                  #이미지의 갯수를 저장한다.
        # newPath = "C:/labelling/2021.11.16 images/new/"             #번호를 바꿔서 저장할 새로운 폴더를 지정한다.

        for n, i in enumerate(images_list):
            print("hello")
            filename_split = os.path.splitext(i)                               #파일이름과 확장자를 나눠서 리스트로 만든다.
            # basename = os.path.basename(i)
            if os.path.exists(filename_split[0] + '.txt'):                      #이미지 파일과 이름이 같은 txt파일이 있는지 검사
                print('both exsists')
                # 이미지 숫자붙여서 새로운 폴더로 복사
                shutil.copy(filename_split[0] + '.jpg', self.new_path + '/' + str(length + n + 1) + '.jpg')
                # 텍스트파일 숫자 붙여서 새로운 폴더로 복사
                shutil.copy(filename_split[0] + '.txt', self.new_path + '/' + str(length + n + 1) + '.txt')
            else:
                print('only jpg' + i + 'exists')

lb = Labelling()