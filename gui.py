import os
import tkinter as tk
import tkinter.ttk as ttk
import modules.list_repository
import modules.build_definition
import re
import time
from threading import Thread

class ListArguments:
    f = None,
    m = None
    def __init__(self, m, f):
        self.m=m
        self.f=f

def main():
    root = tk.Tk()
    root.geometry('1280x480')
    root.title('OVAL Repository Management')

   
    control_frame = tk.Frame(root)
    option_frame = tk.Frame(control_frame)

    label = tk.Label(option_frame, text='   OVAL Repository Management   ')
    button = tk.Button(option_frame, text='Build chosen definitions')
    #button.configure(state=tk.DISABLED)

    console_frame = tk.Frame(control_frame)
    text = tk.Text(console_frame, wrap=tk.WORD, state=tk.DISABLED)
    scroll_console = ttk.Scrollbar(master=console_frame, orient='vertical', command=text.yview)
    text.configure(yscrollcommand=scroll_console.set)

    args = ListArguments('d',None)
    repo= modules.list_repository.get_repository_dir(os.path.relpath('./ScriptsEnvironment/repository/'))


    tree_frame = tk.Frame(root)
    tree = ttk.Treeview(tree_frame)
    scrollbar = ttk.Scrollbar(master=tree_frame, orient='vertical', command=tree.yview)
    
    # without this the size of scrollbar's bar will be fixed
    tree.configure(yscrollcommand=scrollbar.set)

    tree['columns']=('Title', 'Path')
    tree.heading('#0', text='OVAL Class', anchor=tk.W)
    tree.heading('#1', text = 'Title', anchor=tk.W)
    tree.heading('#2', text = 'Path to file', anchor=tk.W)
    

    tree.column('#0', minwidth=85)
    tree.column('#1', minwidth=2)
    tree.column('#2', minwidth=85)


    for oval_type in repo:
        ent_folder = tree.insert('',tk.END, text=oval_type, values=())
        if oval_type=='definitions':
            for title in repo[oval_type]:
                tree.insert(ent_folder,tk.END, text=oval_type, values=(title, repo[oval_type][title]))
        else: 
            for entity in repo[oval_type]:
                tree.insert(ent_folder,tk.END, text=oval_type, values=(entity.replace('\\','\\\\')))
        

    def onButtonBuildClick(args):
        if button['state']==tk.DISABLED:
            return

        text.configure(state=tk.NORMAL)
        text.delete(1.0,tk.END)
        text.insert(1.0,'Building definitions:\n')
        
        items = tree.selection()
        build_query=''
        for i in items:
            it = tree.item(i)
            if it['text']=='definitions':
                try:
                    name = it['values'][0]
                    query = it['values'][1]
                    def_id = query.split('\\')[-1]
                    build_query+=def_id+', '
                    text.insert(2.0, name+'\n')
                except IndexError as e:
                    print(e)

        # cut off the last comma
        build_query = re.search('(.*)(, $)', build_query).group(1)
        # and go to build
        class BuildArguments:
            o = None
            def __init__(self, o):
                self.o=o

        query = f'--definition_id {build_query} -o out.xml'
        print(query)
        args = BuildArguments(o=query)

        
        modules.build_definition.build_definition(args)
        text.insert(3.0, 'Building done. File out.xml')
        text.configure(state=tk.DISABLED)


    def onTreeClick(args):
        item = tree.selection()[0]
        print(tree.item(item))

    tree.bind('<Double-1>', onTreeClick)
    button.bind('<1>',onButtonBuildClick)

    tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    tree.pack(side=tk.LEFT,fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)



    control_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

    option_frame.pack(side=tk.TOP, fill=tk.BOTH)
    label.pack(side=tk.TOP)
    button.pack(side=tk.TOP)

    console_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)
    text.pack(side=tk.LEFT,fill=tk.BOTH, expand=True)
    scroll_console.pack(side=tk.RIGHT, fill=tk.Y)
    
    
    
    



    root.mainloop()



if __name__ == '__main__':
    main()
