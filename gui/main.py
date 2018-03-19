from Tkinter import *;
import tkFileDialog;
import ttk;
from scripts import tx;

INITIAL_FOLDER="/home/henri/Github/tx-gtfs/gtfs";
STEP_LIST=[
    "Sort stop_times by stop_id",
    "Sort stops by stop_id",
    "Sort trips by route_id",
    "Remove stops which are too far",
    "Remove stop_times not related to relevant stops",
    "Remove routes regarding to the transport type",
    "Sort resulted routes by route_id",
    "Remove trips not linked to resulted routes",
    "Sort stoptimes by trip_id",
    "Sort trips by trip_id",
    "Remove stoptimes not related to resulted trips",
    "Generate successors by trips",
    "Sort resulted successor list by stop_id",
    "Aggregate by stop_id",
    "Sort stops in time order for each trip"
];

def launch():
    global folder_path_entry;
    global treeView;
    currdir = folder_path_entry.get();
    tx.start(currdir, treeView, 1);

def get_gtfs_path():
    global folder_path_entry;
    currdir = folder_path_entry.get()
    folder = tkFileDialog.askdirectory(initialdir=currdir);
    if folder != '':
        folder_path_entry.delete(0, END);
        folder_path_entry.insert(0, folder);

window = Tk();
window.geometry("500x400");
window.title("TX - GTFS")

Label(window, text="TX / GTFS extraction", font=25).pack();

select_folder_frame = Frame(window)

folder_path_entry = Entry(select_folder_frame);
folder_path_entry.insert(0, INITIAL_FOLDER);
folder_path_entry.pack(side=LEFT, expand=TRUE, fill=BOTH);

Button(select_folder_frame, text="Select folder", command=get_gtfs_path).pack(side=RIGHT);

select_folder_frame.pack(side=TOP, fill=BOTH)

treeView = ttk.Treeview(window, columns=('description', 'status'));
treeView.column("#0", minwidth=0, width=40, stretch=NO);
treeView.column("#2", minwidth=0, width=40, stretch=NO);
i = len(STEP_LIST) - 1;
while (i>=0):
    treeView.insert("", 0, text=str(i+1), values=(STEP_LIST[i], ""));
    i = i - 1;
treeView.pack(expand=1, fill=BOTH);

Button(window, text="Launch", command=launch).pack(side=LEFT, expand=TRUE, fill=BOTH);
Button(window, text="Quit", command=window.destroy).pack(side=RIGHT);

window.mainloop();
