import os
import tkinter as tk
import tkinter.ttk as ttk
import modules.list_repository
import modules.build_definition
import re
import time


class BuildDefinitionsFrame:
    build_frame = None
    list_frame_object = None
    operational_frame_object = None

    class OperationalFrameObject:
        # parent frame
        build_frame_object = None
        # self
        operational_frame = None

        # child frames
        console_frame = None
        control_frame = None

        # widgets
        console = None
        console_scrollbar=None
        build_button=None
        name_label=None

        def __init__(self, build_frame_object, build_frame):
            self.build_frame_object=build_frame_object
            self.operational_frame=tk.Frame(build_frame) 

        # Methods for console init
        def initConsoleFrame(self):
            self.console_frame=tk.Frame(self.operational_frame)
            
        def initConsole(self):
            self.console=tk.Text(self.console_frame, wrap=tk.WORD, state=tk.DISABLED)
            self.console_scrollbar=ttk.Scrollbar(master=self.console_frame, orient='vertical', command=self.console.yview)
            self.console.configure(yscrollcommand=self.console_scrollbar.set)


        # Methods for controls init
        def initControlsFrame(self):
            self.control_frame = tk.Frame(self.operational_frame)

        def initControls(self):
            self.name_label = tk.Label(self.control_frame, text='   OVAL Repository Management   ')
            self.build_button = tk.Button(self.control_frame, text='Build chosen definitions')
            self.build_button.bind('<1>',self.onBuildButtonClick)

        def onBuildButtonClick(self, args):
            button = self.build_button
            text = self.console

            # tree from another frame
            tree = self.build_frame_object.list_frame_object.tree
            #print(tree)

            if button['state']==tk.DISABLED:
                return

            button['state']=tk.DISABLED

            text['state']=tk.NORMAL
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
            if build_query:
                # cut off the last comma
                build_query = re.search('(.*)(, $)', build_query).group(1)
                # and go to build

                class BuildArguments:
                    options = None
                    def __init__(self, o):
                        self.options=o

                query = f'--definition_id {build_query} -o out.xml'
                print(query)
                args = BuildArguments(o=query)

                thread = Thread(target=modules.build_definition.build_definition, args=(args, ))
                thread.start()

                text.insert(tk.END, 'Building done. File out.xml')
                text.configure(state=tk.DISABLED)

            button['state']=tk.NORMAL
            text['state']=tk.DISABLED



    class ListFrameObject:
        # parent frame
        build_frame_object = None

        # self
        list_frame = None

        # widgets
        tree = None
        scrollbar=None
        
        def __init__(self, build_frame_object, build_frame):
            # Pointer to outer frame and itself
            self.build_frame_object=build_frame_object
            self.list_frame=tk.Frame(build_frame)

            # init tree and scrollbar
            self.tree = ttk.Treeview(self.list_frame)
            self.scrollbar = ttk.Scrollbar(self.list_frame, orient='vertical', command=self.tree.yview)
            self.tree.configure(yscrollcommand=self.scrollbar.set)

            # create columns
            self.tree['columns']=('Title', 'Path')
            self.tree.heading('#0', text='OVAL Class', anchor=tk.W)
            self.tree.heading('#1', text = 'Title', anchor=tk.W)
            self.tree.heading('#2', text = 'Path to file', anchor=tk.W)

            self.tree.column('#0', minwidth=85)
            self.tree.column('#1', minwidth=2)
            self.tree.column('#2', minwidth=85)

            self.tree.bind('<1>', self.onTreeClick)

        def getRepoContent(self):
            repo = modules.list_repository.get_repository_dir(os.path.relpath('./ScriptsEnvironment/repository/'))
            for oval_type in repo:
                ent_folder = self.tree.insert('',tk.END, text=oval_type, values=())
                if oval_type=='definitions':
                    for title in repo[oval_type]:
                        self.tree.insert(ent_folder,tk.END, text=oval_type, values=(title, repo[oval_type][title]))
                else: 
                    for entity in repo[oval_type]:
                        self.tree.insert(ent_folder,tk.END, text=oval_type, values=(entity.replace('\\','\\\\')))
        
        def onTreeClick(self, args):
            item = self.tree.selection()[0]
            print(self.tree.item(item))

    def initListFrame(self):
        self.list_frame_object = self.ListFrameObject(self, self.build_frame)
        self.list_frame_object.getRepoContent()
    
    def initOperationalFrame(self):
        self.operational_frame_object=self.OperationalFrameObject(self, self.build_frame)
        self.operational_frame_object.initConsoleFrame()
        self.operational_frame_object.initConsole()
        self.operational_frame_object.initControlsFrame()
        self.operational_frame_object.initControls()
        
    def packBuildFrame(self):
        # packing oval list
        self.list_frame_object.list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.list_frame_object.tree.pack(side=tk.LEFT,fill=tk.BOTH, expand=True)
        self.list_frame_object.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # packing cotrol frame
        self.operational_frame_object.operational_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        # and it's childs
        self.operational_frame_object.control_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.operational_frame_object.name_label.pack(side=tk.TOP)
        self.operational_frame_object.build_button.pack(side=tk.TOP)

        self.operational_frame_object.console_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.operational_frame_object.console.pack(side=tk.LEFT,fill=tk.BOTH, expand=True)
        self.operational_frame_object.console_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def runBuildFrame(self):
        self.build_frame.mainloop()

    def __init__(self, root):
        self.build_frame = root
        


def main():
    root = tk.Tk()
    root.geometry('1280x480')
    root.title('OVAL Repository Management')
    build_frame = BuildDefinitionsFrame(root)
    build_frame.initListFrame()
    build_frame.initOperationalFrame()
    build_frame.packBuildFrame()
    build_frame.runBuildFrame()


if __name__ == '__main__':
    main()

