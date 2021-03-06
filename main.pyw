# -*- coding: utf-8 -*-
"""
Version:1.2.1.1
Changes:优化结果显示
"""
import tkinter as tk
from tkinter import StringVar
import webbrowser as wb
import os
import pyperclip
VERSION='1.2.1.1'
class fact():
    def runWindow(self):
        self._window=tk.Tk()
        window=self._window
        window.title('十字相乘计算器')
        window.geometry('400x150')
        window.resizable(0,0)
        #%%menu
        menubar=tk.Menu(window)
        #rootmenu
        rootmenu=tk.Menu(window,tearoff=False)
        rootmenu.add_command(label = "关于", command = self._about)
        rootmenu.add_command(accelerator='Ctrl+Q',label = "退出",command=self._quit)
        #resultmenu
        resultMenu=tk.Menu(window,tearoff=False)
        resultMenu.add_command(accelerator='Ctrl+C',label='复制结果',command=self._copy)
        #menubar
        menubar.add_cascade(label="十字相乘计算器",menu=rootmenu)
        menubar.add_cascade(label="结果",menu=resultMenu)
        menubar.add_command(label="帮助",command=self._help)
        window.config(menu = menubar)
        #%%bindings
        window.bind_all('<Control-q>',self._quit)
        window.bind_all('<Return>',self._submit)
        window.bind_all('<Control-c>',self._copy)
        #%%other
        tk.Label(window,text='ax²+bx+c => (x+m)(x+n)').place(x=50,y=0)
        tk.Label(window,text='a:').place(x=50,y=30)
        self._var_a=StringVar()
        tk.Entry(window,textvariable=self._var_a,width=3).place(x=70,y=30)
        tk.Label(window,text='b:').place(x=50,y=60)
        self._var_b=StringVar()
        tk.Entry(window,textvariable=self._var_b,width=3).place(x=70,y=60)
        tk.Label(window,text='c:').place(x=50,y=90)
        self._var_c=StringVar()
        tk.Entry(window,textvariable=self._var_c,width=3).place(x=70,y=90)
        tk.Button(window,text='确定',command=self._submit).place(x=150,y=30)
        self._can_or_not=StringVar()
        tk.Label(window,textvariable=self._can_or_not).place(x=230,y=20)
        self._result=StringVar()
        tk.Label(window,textvariable=self._result).place(x=230,y=50)
        window.mainloop()
    #%%menu function
    def _quit(self,event=None):
        self._window.destroy()
    def _about(self):
        top=tk.Toplevel()
        top.title('关于')
        top.geometry('200x60')
        top.resizable(0,0)
        tk.Label(top,text="版本号："+VERSION).pack()
        tk.Label(top,text='制作者：元素周期表').pack()
        tk.Label(top,text='本项目仅供学习交流使用').pack()
        top.mainloop()
    def _help(self,event=None):
        wb.open(os.path.join(os.getcwd(),'Help.html'))
    def _submit(self,event=None):
        a=self._var_a.get()
        b=self._var_b.get()
        c=self._var_c.get()
        returns=self.factorize(a,b,c)
        if returns[0]:
            PF=returns[2]
            if PF==1:
                PF=''
            factors=returns[1]
            self._can_or_not.set('可以分解因式')
            paren= lambda x:str(x)if x>0 else '('+str(x)+')'
            d=factors[0][0]
            e=paren(factors[0][1])
            f=factors[1][0]
            g=paren(factors[1][1])
            self._result.set('%s(%sx+%s)*(%sx+%s)'%(PF,d,
                             e,f,g))
        elif not returns[0]:
            self._can_or_not.set('不能分解因式')
            self._result.set('')
    def _copy(self,event=None):
        contence=self._result.get()
        pyperclip.copy(contence)
    #%%core function
    def Decompose(self,num):
        nums=list()
        num=int(num)
        for rounds in range(round(abs(num)**0.5)+1):
            for suspected in range(2,abs(num)+1):
                if num % suspected == 0:  #可以整除
                    nums.append(suspected)
                    num = num // suspected
                    break
        nums.sort()
        return nums
    def findFactor(self,num):
        factors=list()
        for suspected in range(-abs(num),abs(num)+1):
            if suspected==0:
                pass
            else:
                other=num%suspected
                if other==0:
                    factors.append([suspected,round(num/suspected)])
        return factors[::-1]
    def factorize(self,a,b,c):
        '''ax^2+bx+c
        returns ints
        '''
        try:
            a=int(a)
            b=int(b)
            c=int(c)
        except ValueError:
            return [False]
        if (b**2)-(4*a*c)<0:
            return [False]
        PFMax=1
        PF_a=self.Decompose(a)
        PF_b=self.Decompose(b)
        PF_c=self.Decompose(c)
        for PF in PF_a:
            if ((PF in PF_b) and (PF in PF_c)):
                PFMax*=PF
                PF_a.remove(PF)
                PF_b.remove(PF)
                PF_c.remove(PF)
                a=round(a/PF)
                b=round(b/PF)
                c=round(c/PF)
        factor_a=self.findFactor(a)
        factor_c=self.findFactor(c)
        for numbers_a in factor_a:
            for numbers_c in factor_c:
                d=numbers_a[0]
                e=numbers_a[1]
                f=numbers_c[0]
                g=numbers_c[1]
                pn=lambda x,y:[abs(x),abs(y),True] if x<0 and y<0 else [x,y,False]
                sy=lambda bol,num:int('-'+str(num)) if bol else num
                if d*g+e*f==b:
                    Symbol=pn(d,f)
                    d=Symbol[0]
                    f=Symbol[1]
                    bol1=Symbol[2]
                    Symbol=pn(e,g)
                    e=Symbol[0]
                    g=Symbol[1]
                    bol2=Symbol[2]
                    PFMax=sy((bol1 ^ bol2),PFMax)
                    return [True,[[d,f],[e,g]],PFMax]
                elif d*f+e*g==b:
                    Symbol=pn(d,g)
                    d=Symbol[0]
                    g=Symbol[1]
                    bol1=Symbol[2]
                    Symbol=pn(e,f)
                    e=Symbol[0]
                    f=Symbol[1]
                    bol2=Symbol[2]
                    PFMax=sy((bol1 ^ bol2),PFMax)
                    return [True,[[d,g],[e,f]],PFMax]
        return [False,[]]
#%%running
def main():
    f=fact()
    f.runWindow()
if __name__=='__main__':
    main()
