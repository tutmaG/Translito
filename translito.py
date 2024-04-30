#!/bin/python3.12
import sys
import os
import commands
import core
import install
import time
import filter
from pyfiglet import Figlet
from rich import print
from rich.console import Console
from rich.table import Table
from rich.style import Style



def intro():
    f = Figlet(font='slant')
    console = Console()
    print (f'[red1]{f.renderText("Translito")}[/red1]')
    console.print("\n[purple]Welcome to Translito, this is beta version[/purple] [black]0.0.1[/black]", style="bold")
    console.print("if you have some issues pleas report: [red1]tarieltsintskaladze@gmail.com[/red1]\n", style="bold red")

def fast_fixer(info=None):
    exit_=0
    print("CLI ---> Fast-fix mode\ntrying to fix all bugs!")
    while True:
        if info==None:
            error_msg="fix"
        else:
            error_msg=input("[FIX]Use 'info' or 'fix': ")
        if error_msg=="info":
                print(info)
        if error_msg=="fix":    
            inst_check=install.main()
            if inst_check["msg"]=="Success":
                core_check=core.core()
                if core_check["msg"]=="Success":
                    print("All bugs is fixed \t\t\t")
                    return main_func(intro_=0)
                else:
                    print("core.core() error!")
                    exit_=1
            else:
                print("install.main() error!")
                exit_=1
        if exit_==1:
            print("Fast-fix dont work! try 'python3 auto-fix.py'")
            exit()

def main_func(intro_=1):
    main_config_data:dict=core.core()
    if main_config_data["msg"]=="ERROR":
        print("App can`t start...")
        fast_fixer(main_config_data["info"])
        exit()

    db_name, tables_name = next(iter(main_config_data["data"]["db"].items()))
    if main_config_data["msg"]=="Success":
        if intro_==1:
            intro()
        error:int=1
        try:
            while True:
                print("[purple4][CLI][/purple4][green]Command[/green]: ",end="")
                comm_:str=input()
    #------------------Commands-------------------------- 
                if comm_=="exit" or comm_=="E":
                    print("\nBay-Bay\n")
                    exit()
                if comm_=="help" or comm_=="H":
                    commands.Commands.help()
                    error = 0
                if comm_=="avalible commands" or comm_=="AC":
                    ac_=commands.Commands.avalible_commands()
                    print(f"\nCommands: {ac_['Commands']}")
                    print(f"Modes:    {ac_['Modes']}\n")
                    error = 0
                if comm_=="show word" or comm_=="SW":
                    error = 0
                    rows = commands.Commands(db_name).show_write_db(tables_name[1])
                    if rows == "ERROR":
                        fast_fixer()
                    else:
                        header_style = Style(color="green", bold=True)
                        row_style = Style(color="magenta")
                        border_style = "blue"
                        table = Table(title="Only english words")
                        table.add_column("ID",style=header_style)
                        table.add_column("Word",style=header_style)
                        for column in table.columns:
                            column.header_style = header_style
                        for row in rows:
                            table.add_row(str(row[0]), row[1] ,style=row_style)
                        table.border_style = border_style
                        print(table)

    #------------------MODES-------------------------- 
    #================write==============================================================
                if comm_=="write" or comm_=="W":
                    error = 0
                    print("[purple4]Command Line Interface[/purple4] ---> [red]Mode[/red]:[red]write[/red]")
                    while True:
                        print("[red][M[/red]:[red]Write][/red][green]Word:[/green] ",end="")
                        word_:str=input()
                        if word_=="help" or word_=="H":
                            help_=commands.Mode("").write("","",flag="help")
                            print(help_)
                        elif word_=="back" or word_=="B":
                            print("exaiting...\nMode:write ---> Command Interface\n")
                            break
                        else:
                            filter_=filter.filter_input(word_)
                            if filter_=="ERROR":
                                print("[red1][*]Invalide input!!![/red1]")
                            else:
                                ret_word=commands.Mode(db_name).write(tables_name[1],word_)
                                if ret_word=="ERROR":
                                    print("[bright_yellow][!]Some bug is detacted![/bright_yellow]")
                                    time.sleep(1)
                                    fast_fixer()
                                if ret_word=="Entry already exists":
                                    print(f"word:[purple4]{word_}[/purple4]  [red1]already exists[/red1]")
                                else:
                                    print(f"[green]New Word added --->[/green] [purple4]{word_}[/purple4]")
    #=====================================================================================
    #---------------------------------------------------------------------  
                if error == 1:
                    print("\n[red1]Invalid command!!![/red1]\nUse 'help' or 'H' for help menu and 'avalible commands' or 'AC' to see avalible commands\n")
                error=1
        except KeyboardInterrupt:
            print("\n[yellow][!]Keyboard interrupt detected, terminating.[/yellow]")      


if __name__=="__main__":
    main_func()