from mainWindow import MainWindow

def main():
        app = MainWindow()

        def call_update():
                global update, update_after
                update_test()

        def update_test():
                global update, update_after
                app.draw_graphic()
                update_after = app.after(100, update_test)

        call_update()
        app.mainloop()

if __name__ == '__main__': 
        main()
