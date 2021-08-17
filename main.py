import os
from  tkinter import *
from tkinter.ttk import Combobox
from Process import *

'''
Areen Abu Caf 212654719
Fadi Amon 212472542
Rasheed Abu Mdeagm 212555650
'''


window=Tk()
window.title('Data Project')
width =1250
height = 750
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
window.geometry("%dx%d+%d+%d" % (width, height, x, y-35))

Path = StringVar()
Discretization = StringVar()
NumOFBins = StringVar()
NumOfNeighbors = StringVar()
Algorithm = StringVar()

def MainFrame():
    '''
    This function is responsible for building the main frame, and takes all the needed inputs from the user.
    '''
    global FirstFrame, result_label,BinsEntry,NumOfNeighbors_entry,NumOfNeighbors_label
    FirstFrame = Frame(window)
    FirstFrame['bg'] = "#D79771"
    FirstFrame.place(x=0, y=0, width=width, height=height)

    Title = Label(FirstFrame, text="Please fill all the required fields",bg="#D79771",font=("times", 25))
    Title.place(x=300,y=50)

    PathLabel = Label(FirstFrame, text="Path :",bg="#D79771", font=("times", 20))
    PathLabel.place(x=135,y=150)

    PathEntry = Entry(FirstFrame, textvariable=Path,width=25,font=('times', 20))
    PathEntry.place(x=600,y=150)

    DiscretizationLabel = Label(FirstFrame, text="Discretization type :", bg="#D79771", font=("times", 20) )
    DiscretizationLabel.place(x=135,y=220)

    Discretization_values=['Equal frequency','Equal width','Based entropy']
    Discretization_Combo = Combobox(FirstFrame,values=Discretization_values, textvariable=Discretization, font=('times', 20), width=24,state="readonly")
    Discretization_Combo.place(x=600,y=220)
    Discretization_Combo.current(0)
    Discretization_Combo.bind("<<ComboboxSelected>>")

    BinsLabel = Label(FirstFrame,text="Number of bins :",bg="#D79771",font=('times', 20))
    BinsLabel.place(x=135,y=290)

    BinsEntry= Entry(FirstFrame, font=('times', 20), textvariable=NumOFBins, width=25)
    BinsEntry.place(x=600,y=290)

    Algorithm_label = Label(FirstFrame, text="The Algorithm :",bg="#D79771", font=('times', 20))
    Algorithm_label.place(x=135,y=360)

    Algorithm_values=['naive bayes classifier','naive bayes classifier (our)','ID3','ID3 (our)','KNN','K-MEANS']
    Algorithm_Combo = Combobox(FirstFrame,values=Algorithm_values, textvariable=Algorithm,font=('times', 20), width=24,state="readonly")
    Algorithm_Combo.place(x=600,y=360)

    Algorithm_Combo.current(0)
    Algorithm_Combo.bind("<<ComboboxSelected>>", Neighbours_Clusters)


    NumOfNeighbors_label = Label(FirstFrame, text="Number of neighbors :",bg="#D79771", font=('times', 20))
    NumOfNeighbors_label.place(x=135,y=430)

    NumOfNeighbors_entry= Entry(FirstFrame, font=('times', 20), textvariable=NumOfNeighbors, width=25,state='disabled')
    NumOfNeighbors_entry.place(x=600,y=430)
    result_label = Label(FirstFrame, text="", font=('arial', 20),bg="#D79771",fg="red")
    result_label.place(x=135,y=520)

    result_button = Button(FirstFrame, bg="#D79771",text="Run The Algorithm", font=('times', 25),command=Check_Input, width=25)

    result_button.place(x=400,y=600)


def Neighbours_Clusters(event):
    '''
    This functions decides whether to take clusters or neighbours as input, depends on the algorithm.
    :return:nothing
    '''
    if Algorithm.get() == 'KNN':
        NumOfNeighbors_entry.configure(state="normal")
        NumOfNeighbors_label['text']='Number of neighbors :'
    else:
        if Algorithm.get() == 'K-MEANS':
            NumOfNeighbors_entry.configure(state="normal")
            NumOfNeighbors_label['text'] = 'Number of clusters :'
        else:
            NumOfNeighbors.set("")
            NumOfNeighbors_entry.configure(state="disabled")


def Check_Input():
    '''
    This function check if the input is correct.
    :return:nothing
    '''

    if Algorithm.get() in ['KNN','K-MEANS']:
        if NumOfNeighbors.get() == '':
            NumOfNeighbors.set('2')
        else:
            try:
                num_neg = int(NumOfNeighbors.get())
                if num_neg <= 0:
                    result_label.configure(text="Number of neighbors field accept positive numbers")
                    return ''
            except ValueError:
                result_label.configure(text="Number of neighbors field accept just numbers")
                return ''

    if Path.get()=='':
        result_label.configure(text="Path field is empty")
    else:
        if os.path.exists(Path.get())==False:
            result_label.configure(text="The given path is not exist")
        else:
            if NumOFBins.get()=='':
                result_label.configure(text="Number of bins field is empty")
            else:
                try:
                    num_bins=int(NumOFBins.get())
                    if num_bins <= 0:
                        result_label.configure(text="Number of bins field accept positive numbers")
                    else:
                        result_label.configure(text="")
                        FirstFrame.destroy()
                        Update_Frame_Results()
                except ValueError:
                    result_label.configure(text="Number of bins field accept just numbers")
        FirstFrame.destroy()
        Update_Frame_Results()


def Back_To_MainFrame():
    '''
    This function takes us back to the main frame again after we see the results.
    :return:nothing
    '''
    Path.set("")
    NumOFBins.set("")
    Result_Frame.destroy()
    MainFrame()


def Update_Frame_Results():
    '''
    This function is responsible for showing the results.
    :return:nothing
    '''
    global Result_Frame,label
    Result_Frame = Frame(window)
    Result_Frame['bg'] = "#D79771"
    Result_Frame.place(x=0, y=0, width=width, height=height)

    bins=int(NumOFBins.get())


    try:
        Text=Algorithm.get()+' , '+Discretization.get()
        results=Apply_Algorithm(Path.get(),Algorithm.get(),Discretization.get(),bins,2 if NumOfNeighbors.get()=='' else int(NumOfNeighbors.get()))
        filename=Algorithm.get()+','+Discretization.get()+'_results'
        pickle.dump(results, open(Path.get()+'/'+filename, 'wb'))
        train_matrix=results['train']['Confusion Matrix']
        test_matrix=results['test']['Confusion Matrix']

        label0 = Label(Result_Frame, text=Text,bg='#D79771',font=('times',20, 'bold'))
        label0.place(x=50,y=50)
        label1 = Label(Result_Frame, text="Confusion Matrix (Train)",bg='#D79771',font=('times',20, 'bold'))
        label1.place(x=400,y=100)

        lst = [('TP = '+str(train_matrix[0][0]),'FP = '+str(train_matrix[0][1])),('FN = '+str(train_matrix[1][0]),'TN = '+str(train_matrix[1][1]))]

        for i in range(2):
            for j in range(2):
                e = Entry(Result_Frame, width=20,font=('times', 18),fg='black')
                e.place(x=300+j*350,y=150+i*50)
                e.insert(END,lst[i][j] )
                e.configure(state='disabled')


        label4 = Label(Result_Frame, text="Confusion Matrix (Test)",font=('times',20,'bold'),bg='#D79771')
        label4.place(x=400,y=250)


        lst = [('TP = '+str(test_matrix[0][0]),'FP = '+str(test_matrix[0][1])),('FN = '+str(test_matrix[1][0]),'TN = '+str(test_matrix[1][1]))]
        for i in range(2):
            for j in range(2):
                e2 = Entry(Result_Frame, width=20,font=('times', 18),fg='black')
                e2.place(x=300+j*350,y=300+i*50)
                e2.insert(END, lst[i][j])
                e2.configure(state='disabled')


        label7 = Label(Result_Frame, text="Results",font=('times',20, 'bold'),bg='#D79771')
        label7.place(x=500,y=400)

        lst = [(' ','Accuracy','Precision','Recall','F-measure')]
        for i in ['train','test']:
            Accuracy="{0:.2f} %".format(results[i]['Accuracy'] *100)
            Precision="{0:.2f} %".format(results[i]['Precision'] *100)
            Recall="{0:.2f} %".format(results[i]['Recall'] *100)
            Measure="{0:.2f} %".format(results[i]['F-measure'] *100)
            lst.append((i,Accuracy,Precision,Recall,Measure))

        for i in range(3):
            for j in range(5):
                e2 = Entry(Result_Frame, width=15, font=('times', 18),fg='black')
                e2.place(x=50+j*250,y=450+i*50)
                e2.insert(END, lst[i][j])
                e2.configure(state='disabled')

    except Exception as e:
        label = Label(Result_Frame, text=e.args, fg='Red',bg='#D79771',font=('times', 20, 'bold'))
        label.place(x=35,y=600)

    Return_button = Button(Result_Frame, text="Return for the First Page", font=('times', 20),command=Back_To_MainFrame, width=35,bg='#D79771')
    Return_button.place(x=300,y=650)

def Apply_Algorithm(Path,Algorithm,Discretization_type,NumOfBins,NumOfNeg):
    '''
    This function runs the algorithm based on the user inputs, after the data is cleaned.
    :return:nothing
    '''
    pre = Pre()

    test = pd.read_csv(Path+'/test.csv')
    train = pd.read_csv(Path+'/train.csv')
    struct = pre.read_structure(Path+'/Structure.txt')

    pre.Clean_Data(train, struct,Discretization_type,NumOfBins)
    pre.Delete_Nan_Class_Row(test)
    pre.Fill_Nan_Values(test, struct)

    pre.Save_Data(train,Path, 'train')
    pre.Save_Data(test,Path, 'test')

    if Algorithm not in ['naive bayes classifier (our)','ID3 (our)']:
        runner = BuildAlgorithm()
        train, test = runner.Convert_Strings_To_Numbers(Path)
        return runner.Run(Algorithm, train, test, Path,NumOfNeg)
    else:
        process=Process()
        model=process.Build_Model(Path,Algorithm,train)
        process.Save_Model(Path,model)
        train = pd.read_csv(Path+'/train.csv')
        pre.Delete_Nan_Class_Row(train)
        pre.Fill_Nan_Values(train,struct)
        return process.Running_Algorithm(Path,Algorithm,train,test)


MainFrame()
window.mainloop()
