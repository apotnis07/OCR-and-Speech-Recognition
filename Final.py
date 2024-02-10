from PIL import Image
import pytesseract
import argparse
import cv2
import os
import string
import speech_recognition as sr

loop=True
while loop:
    print("1.Use image recognition")
    print("2.Use voice recognition(Enter any no of operands as long as the operations to be performed on them is the same)")
    print("3.Exit")
    ch=int(input("Enter the choice:"))
    if ch==1:
      a = []
      z = ''
      result = 0
      image = cv2.imread('C:/Users/Admin/PycharmProjects/aneesh/1556.png', 0)
      filename = "{}.png".format(os.getpid())
      cv2.imwrite(filename, image)
      text = pytesseract.image_to_string(Image.open(filename))
      x = len(text)

      print("1.For entering text to file")
      print("2.For calculations")
      print("3.For exiting the current option")
      ch1=int(input("Enter the choice:"))
      if ch1==1:
          text=str(text)
          with open('Proj.txt','w') as f:
              f.write(text)


      if ch1==2:
        for i in range(x):
            if text[i] == '-':
                a.append(text[0:i])
                a.append(text[i + 1:x + 1])
                result = int(a[0]) - int(a[1])
            elif text[i] == '+':
                a.append(text[0:i])
                a.append(text[i + 1:x + 1])
                result = int(a[0]) + int(a[1])
            elif text[i] == '/':
                a.append(text[0:i])
                a.append(text[i + 1:x + 1])
                d = int(a[1])
                if d == 0:
                    result = "Invalid"
                    break
                else:
                    result = int(a[0]) / int(a[1])
            elif text[i] == '*':
                a.append(text[0:i])
                a.append(text[i + 1:x + 1])
                result = int(a[0]) * int(a[1])
        print(a)

        print(result)
        os.remove(filename)
        cv2.imshow("Output", image)
        cv2.waitKey(0)
      if ch==3:
          continue

    elif ch==2:
     AUDIO_FILE = ("C:/Users/Admin/PycharmProjects/aneesh/3add.wav")

     r = sr.Recognizer()
     with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)
     try:
            print("audio file contains " + r.recognize_google(audio))
     except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
     except sr.RequestError:
            print("Couldn't get the results from Google SR")
     m = r.recognize_google(audio)


     print("1.For entering text to file")
     print("2.For calculations")
     print("3.For exiting the current option")
     ch2 = int(input("Enter your choice:"))
     if ch2==1:

         m = str(m)
         print(m)
         with open('Proj.txt', 'w') as f1:
             f1.write(m)


     if ch2==2:
        print(m)
        dict = {}
        dict1={}
        len=len(m)
        countp=0
        countm=0
        countx=0
        countd=0
        result=0
        i=0
        a=[]*0
        count1=0
        count2 = 0
        count3=0
        count4=0

        def check(m,i):
            z = i

            for i in range(z,len):
                if (m[i]=='+' ):
                    global count1
                    count1+=1
                    x=m.count('+' )
                    global countp
                    countp+=1
                    r=i

                    dict[countp]=m[z:r-1]

                    countp+=1
                    dict[countp]=m[r+1:len]


                    countp-=1


                    if count1==x:

                        dict.update({'No':countp+1})
                        dict.update({'op':'plus'})
                        return dict
                    else:
                        return check(m,r+1)

                elif m[i]=='-' :

                    global count2
                    count2+=1
                    y=m.count('-')
                    global countm
                    countm+=1
                    r=i


                    dict[countm]=m[z:r-1]



                    countm+=1
                    dict[countm]=m[r+1:len]

                    countm-=1

                    if count2==y:
                        dict.update({'No':countm+1})
                        dict.update({'op':'minus'})
                        return dict
                    else:
                        return check(m,r+1)
                elif m[i] == 'x':
                    global count3
                    count3 += 1
                    n = m.count('x')
                    global countx
                    countx += 1
                    r = i

                    dict[countx] = m[z:r - 1]

                    countx += 1
                    dict[countx] = m[r + 1:len]
                    countx -= 1

                    if count3 == n:
                        dict.update({'No': countx + 1})
                        dict.update({'op': 'multiply'})
                        return dict

                    else:
                        return check(m, r + 1)

                elif m[i] == '/':
                    global count4
                    count4+=1
                    d=m.count('/')
                    global countd
                    countd+=1
                    r=i

                    dict[countd]=m[z:r-1]

                    countd+=1
                    dict[countd]=m[r+1:len]
                    countd-=1
                    print(dict)
                    if count4==d:
                        dict.update({'No': countd + 1})
                        dict.update({'op': 'divide'})
                        return dict

                    else:
                        return check(m,r+1)


        dict=check(m,0)

        result=0

        if dict['op']=='plus':
            x=dict['No']
            for i in range(x):
                result=result+int(dict[i+1])
            print(result)

        if dict['op']=='multiply':
            x=dict['No']
            mult=1
            for i in range(x):
                mult=mult*int(dict[i+1])
            print(mult)

        if dict['op']=='divide':
            x=dict['No']
            div=1
            count=0
            div1 = int(dict[1])
            for i in range(x):
                count+=1
                if count==1:
                    div=1
                else:
                    div = int(dict[i + 1])
                div1=div1/div
            print(div1)


        if dict['op']=='minus':
            x=dict['No']

            count=0
            for i in range(1,x+1):
                dict[i]=int(dict[i])
                dict1[i]=dict[i]
                count+=1
            print(dict1)


            a=sorted(dict1.values(),reverse=True)
            print(a)

            result=a[0]
            for i in range(1,count):
                result=result-a[i]
            print(result)
    elif ch==3:
        print("You've exited")
        break

    else:
        print("Invalid Choice")