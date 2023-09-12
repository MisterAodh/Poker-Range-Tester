import tkinter as tk
import random
import pandas as pd
import os

def get_ranks():
    ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    return ranks

def get_hand():
    ranks = get_ranks()
    suits = ['s', 'o']
    rank1, rank2 = random.sample(ranks, 2)
    suit = random.choice(suits)
    if ranks.index(rank1) < ranks.index(rank2):
        hand = rank1 + rank2 + suit
    else:
        hand = rank2 + rank1 + suit
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-page Example")
        self.geometry("800x600")
        self.frame = None
        self.show_frame(StartPage)


    def show_frame(self, frame_class, *args):
        if self.frame:
            self.frame.destroy()
        self.frame = frame_class(self, *args)
        self.frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Start Page").pack()

        tk.Button(self, text="Create_Range", command=lambda: master.show_frame(CreationPokerPage)).pack()
        dir_path = 'Range_sets'

        for folder in os.listdir(dir_path):
            if os.path.isdir(os.path.join(dir_path, folder)):
                button_text = f"Test Ranges {folder}"

                tk.Button(self, text=button_text,
                          command=lambda folder=folder: master.show_frame(TestingPokerPage, folder)).pack()
        for filename in os.listdir('attempts'):
            file_path = os.path.join('attempts', filename)
            if os.path.isfile(file_path):
                os.remove(file_path)



class TestingPokerPage(tk.Frame):
    def __init__(self, master, folder_name):
        self.folder_name = folder_name
        self.location = 'Range_sets/' + folder_name
        tk.Frame.__init__(self, master)
        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X)
        btn_frame = tk.Frame(self)
        btn_frame.pack(side=tk.TOP, fill=tk.X)
        grid_frame = tk.Frame(self)
        grid_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        tk.Button(top_frame, text="Back", command=lambda: master.show_frame(StartPage)).pack(side=tk.LEFT)
        self.positions = [folder[:-4] for folder in os.listdir(self.location)]
        self.current_position = tk.StringVar()
        self.current_position.set(self.positions[0])
        tk.Label(top_frame, text="Please select your hand range for the position").pack(side=tk.LEFT)
        tk.Label(top_frame, textvariable=self.current_position).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Previous Position", command=self.prev_position).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Next Position", command=self.next_position).pack(side=tk.LEFT)
        self.grid_buttons = {}
        self.ranks = get_ranks()
        for i, rank1 in enumerate(self.ranks):
            for j, rank2 in enumerate(self.ranks):
                hand = ""
                if i > j:
                    hand = rank2 + rank1 + 'o'
                elif i < j:
                    hand = rank1 + rank2 + 's'
                else:
                    hand = rank1 + rank2
                self.create_label_button(hand, i, j, grid_frame)

        mark_button_frame = tk.Frame(self)
        mark_button_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Button(mark_button_frame, text="Mark", command=self.mark_dataframe, height=2, width=10).pack(side=tk.LEFT)
        self.accuracy_label = tk.Label(mark_button_frame, text="Accuracy: ")
        self.accuracy_label.pack(side=tk.LEFT)
        tk.Button(mark_button_frame, text="Correct Range", command=lambda: self.show_csv_on_grid(
            self.location + '/' + self.current_position.get() + '.csv')).pack(side=tk.LEFT)
        tk.Button(mark_button_frame, text="My Answer", command=lambda: self.show_csv_on_grid(
            'attempts/' + self.current_position.get() + '_attempt.csv')).pack(side=tk.LEFT)

    def read_original_csv(self, csv_path):
        df = pd.read_csv(csv_path)
        return {row['hands']: row['toggle'] for index, row in df.iterrows()}

    def show_csv_on_grid(self, csv_path):
        data = self.read_original_csv(csv_path)
        for hand, toggle_value in data.items():
            lbl = self.grid_buttons[hand]
            if toggle_value == 2:
                color = 'red'
            elif toggle_value == 1:
                color = 'orange'
            elif toggle_value == 0.5:
                color = 'yellow'
            else:
                color = 'SystemButtonFace'
            lbl.config(bg=color)

    def create_label_button(self, hand, row, col, frame):
        lbl = tk.Label(frame, text=hand, width=4, height=2, bg="SystemButtonFace", borderwidth=1, relief="solid")
        lbl.grid(row=row, column=col, in_=frame)
        lbl.bind("<Button-1>", lambda e, hand=hand: self.toggle_highlight(hand, row, col))
        self.grid_buttons[hand] = lbl

    def toggle_highlight(self, hand, row, col):
        lbl = self.grid_buttons[hand]
        if lbl.cget('bg') == 'SystemButtonFace':
            new_color = 'red'
        elif lbl.cget('bg') == 'red':
            new_color = 'orange'
        elif lbl.cget('bg') == 'orange':
            new_color = 'yellow'
        else:
            new_color = 'SystemButtonFace'
        lbl.config(bg=new_color)

    def next_position(self):
        current_index = self.positions.index(self.current_position.get())
        if current_index < len(self.positions) - 1:
            self.current_position.set(self.positions[current_index + 1])

    def prev_position(self):
        current_index = self.positions.index(self.current_position.get())
        if current_index > 0:
            self.current_position.set(self.positions[current_index - 1])


    def mark_dataframe(self):
        data = []
        for hand, lbl in self.grid_buttons.items():
            color = lbl.cget('bg')
            toggle_value = 0
            if color == 'red':
                toggle_value = 2
            elif color == 'orange':
                toggle_value = 1
            elif color == 'yellow':
                toggle_value = 0.5
            data.append([hand, toggle_value])

        for lbl in self.grid_buttons.values():
            lbl.config(bg='SystemButtonFace')

        df = pd.DataFrame(data, columns=['hands', 'toggle'])
        file_name = f"attempts/{self.current_position.get()}_attempt.csv"
        df.to_csv(file_name, index=False)

        original_data = self.read_original_csv(
            self.location + '/' + self.current_position.get() + '.csv')

        correct_count = 0
        for hand, toggle_value in data:
            if original_data.get(hand) == toggle_value:
                correct_count += 1

        accuracy = (correct_count / len(data)) * 100
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.2f}%")


class CreationPokerPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        name_frame = tk.Frame(self)
        self.current_directory = ""
        name_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(name_frame, text="Name this range set: ").pack(side=tk.LEFT)
        self.range_name = tk.Entry(name_frame)
        self.range_name.pack(side=tk.LEFT)
        tk.Button(name_frame, text="Submit", command=self.create_directory).pack(side=tk.LEFT)
        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X)
        btn_frame = tk.Frame(self)
        btn_frame.pack(side=tk.TOP, fill=tk.X)
        grid_frame = tk.Frame(self)
        grid_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        tk.Button(top_frame, text="Back", command=lambda: master.show_frame(StartPage)).pack(side=tk.LEFT)
        self.grid_buttons = {}
        self.ranks = get_ranks()
        for i, rank1 in enumerate(self.ranks):
            for j, rank2 in enumerate(self.ranks):
                hand = ""
                if i > j:
                    hand = rank2 + rank1 + 'o'
                elif i < j:
                    hand = rank1 + rank2 + 's'
                else:
                    hand = rank1 + rank2
                self.create_label_button(hand, i, j, grid_frame)

        mark_button_frame = tk.Frame(self)
        mark_button_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(mark_button_frame, text="Name this position: ").pack(side=tk.LEFT)
        self.position_name = tk.Entry(mark_button_frame)
        self.position_name.pack(side=tk.LEFT)

        tk.Button(mark_button_frame, text="ADD", command=self.mark_dataframe, height=2, width=10).pack(side=tk.LEFT)

    def create_label_button(self, hand, row, col, frame):
        lbl = tk.Label(frame, text=hand, width=4, height=2, bg="SystemButtonFace", borderwidth=1, relief="solid")
        lbl.grid(row=row, column=col, in_=frame)
        lbl.bind("<Button-1>", lambda e, hand=hand: self.toggle_highlight(hand, row, col))
        self.grid_buttons[hand] = lbl

    def toggle_highlight(self, hand, row, col):
        lbl = self.grid_buttons[hand]
        if lbl.cget('bg') == 'SystemButtonFace':
            new_color = 'red'
        elif lbl.cget('bg') == 'red':
            new_color = 'orange'
        elif lbl.cget('bg') == 'orange':
            new_color = 'yellow'
        else:
            new_color = 'SystemButtonFace'
        lbl.config(bg=new_color)

    def create_directory(self):
        dir_name = self.range_name.get()
        dir_path = os.path.join('Range_sets', dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            self.current_directory = dir_path
            print(f"Directory {dir_name} created.")
        else:
            print(f"Directory {dir_name} already exists.")
    def next_position(self):
        current_index = self.positions.index(self.current_position.get())
        if current_index < len(self.positions) - 1:
            self.current_position.set(self.positions[current_index + 1])

    def prev_position(self):
        current_index = self.positions.index(self.current_position.get())
        if current_index > 0:
            self.current_position.set(self.positions[current_index - 1])

    def mark_dataframe(self):
        data = []
        for hand, lbl in self.grid_buttons.items():
            color = lbl.cget('bg')
            toggle_value = 0
            if color == 'red':
                toggle_value = 2
            elif color == 'orange':
                toggle_value = 1
            elif color == 'yellow':
                toggle_value = 0.5
            data.append([hand, toggle_value])

        for lbl in self.grid_buttons.values():
            lbl.config(bg='SystemButtonFace')

        df = pd.DataFrame(data, columns=['hands', 'toggle'])
        file_name = f"{self.position_name.get()}.csv"

        if self.current_directory:
            file_path = os.path.join(self.current_directory, file_name)
            df.to_csv(file_path, index=False)
            print(f"CSV {file_name} saved to {self.current_directory}.")
        else:
            print("No directory selected.")


if __name__ == "__main__":
    app = App()
    app.mainloop()

