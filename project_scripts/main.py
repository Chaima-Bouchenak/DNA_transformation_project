# coding ~utf-8
"""
Main script for project testing
"""


from GUI import UserInterface


if __name__ == '__main__':

    main_object = UserInterface()
    main_object.tk_main_window()
    main_object.main_windoow_buttons()
    main_object.main_loop()

