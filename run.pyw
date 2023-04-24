if __name__ =="__main__":
    from files.install_packages import check_new_packages
    try:
        with open('.\\files\\data.json','r') as file:
            pass   
    except: 
        check_new_packages()

    from files.functions import update
    from files.windowQT import main

    #update()
    main()  
 
